# AquaSense Deployment Guide

This guide covers deploying AquaSense to various environments.

## Table of Contents
1. [Local Development](#local-development)
2. [AWS EKS Production](#aws-eks-production)
3. [Monitoring Setup](#monitoring-setup)
4. [Troubleshooting](#troubleshooting)

## Local Development

### Prerequisites
- Docker Desktop 24+
- 16GB RAM minimum
- 50GB free disk space

### Quick Start

```bash
# Clone repository
git clone https://github.com/your-org/aqua-sense.git
cd aqua-sense

# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f auth-service

# Access applications
# Frontend: http://localhost:3000
# API Gateway: http://localhost:8080
# Grafana: http://localhost:3001 (admin/admin123)
# Kibana: http://localhost:5601
```

### Stopping Services
```bash
docker-compose down
# Or to remove volumes
docker-compose down -v
```

## AWS EKS Production

### Step 1: Prerequisites

```bash
# Install required tools
brew install awscli terraform kubectl helm

# Configure AWS credentials
aws configure
```

### Step 2: Provision Infrastructure

```bash
cd infra/terraform

# Initialize Terraform
terraform init

# Review plan
terraform plan -var-file=environments/prod/terraform.tfvars

# Apply infrastructure
terraform apply -var-file=environments/prod/terraform.tfvars
```

This creates:
- VPC with public/private subnets
- EKS cluster with node groups
- RDS PostgreSQL instance
- ElastiCache Redis cluster
- MSK (Managed Kafka)
- S3 buckets
- IAM roles and policies

### Step 3: Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig --region us-east-1 --name aquasense-cluster

# Verify connection
kubectl get nodes
```

### Step 4: Deploy Applications

#### Option A: Using Kubernetes Manifests

```bash
cd infra/kubernetes

# Create namespaces
kubectl apply -f namespaces/

# Create secrets (update values first!)
kubectl create secret generic db-credentials \
  --from-literal=username=aquasense \
  --from-literal=password=YOUR_SECURE_PASSWORD \
  -n aquasense

kubectl create secret generic jwt-secret \
  --from-literal=secret=YOUR_JWT_SECRET \
  -n aquasense

# Deploy services
kubectl apply -f configmaps/
kubectl apply -f deployments/
kubectl apply -f services/
kubectl apply -f ingress/

# Check deployment status
kubectl get pods -n aquasense
kubectl get svc -n aquasense
```

#### Option B: Using Helm

```bash
cd infra/helm

# Add required repos
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager for TLS
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true

# Install nginx ingress
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace

# Install AquaSense
helm install aquasense ./aquasense \
  --namespace aquasense \
  --create-namespace \
  --values aquasense/values-prod.yaml

# Check installation
helm status aquasense -n aquasense
```

### Step 5: Configure DNS

```bash
# Get load balancer address
kubectl get svc ingress-nginx-controller -n ingress-nginx

# Create DNS records (example for Route53)
aws route53 change-resource-record-sets \
  --hosted-zone-id YOUR_ZONE_ID \
  --change-batch file://dns-records.json
```

### Step 6: Set up SSL/TLS

```bash
# Apply cert-manager issuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@yourdomain.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Update ingress with TLS
kubectl apply -f infra/kubernetes/ingress/ingress-tls.yaml
```

## Monitoring Setup

### Prometheus & Grafana

```bash
# Add Prometheus helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Install Prometheus operator
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --values observability/prometheus/values.yaml

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Default credentials: admin / prom-operator
```

### ELK Stack

```bash
# Add Elastic helm repo
helm repo add elastic https://helm.elastic.co

# Install Elasticsearch
helm install elasticsearch elastic/elasticsearch \
  --namespace logging \
  --create-namespace \
  --values observability/elk/elasticsearch-values.yaml

# Install Kibana
helm install kibana elastic/kibana \
  --namespace logging \
  --values observability/elk/kibana-values.yaml

# Install Filebeat
helm install filebeat elastic/filebeat \
  --namespace logging \
  --values observability/elk/filebeat-values.yaml
```

## Database Migrations

```bash
# Run Flyway migrations
cd services
./mvnw flyway:migrate -Dflyway.url=jdbc:postgresql://your-rds-endpoint:5432/aquasense
```

## Scaling

### Horizontal Pod Autoscaling

```bash
# Apply HPA configurations
kubectl apply -f - <<EOF
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service-hpa
  namespace: aquasense
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
EOF
```

### Cluster Autoscaling

```bash
# Enable cluster autoscaler
kubectl apply -f infra/kubernetes/cluster-autoscaler.yaml
```

## Backup and Recovery

### Database Backup

```bash
# Automated backups (RDS)
aws rds modify-db-instance \
  --db-instance-identifier aquasense-db \
  --backup-retention-period 30 \
  --preferred-backup-window "03:00-04:00"

# Manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier aquasense-db \
  --db-snapshot-identifier aquasense-backup-$(date +%Y%m%d)
```

### Application State Backup

```bash
# Backup Kubernetes resources
kubectl get all --all-namespaces -o yaml > k8s-backup-$(date +%Y%m%d).yaml

# Using Velero
velero backup create aquasense-backup --include-namespaces aquasense
```

## Security Hardening

### Network Policies

```bash
kubectl apply -f infra/kubernetes/network-policies/
```

### Pod Security Policies

```bash
kubectl apply -f infra/kubernetes/security/pod-security-policy.yaml
```

### Secrets Management

```bash
# Using AWS Secrets Manager
aws secretsmanager create-secret \
  --name aquasense/prod/db-password \
  --secret-string "YOUR_SECURE_PASSWORD"

# Using External Secrets Operator
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace
```

## Troubleshooting

### Common Issues

#### Pods not starting

```bash
# Check pod events
kubectl describe pod POD_NAME -n aquasense

# Check logs
kubectl logs POD_NAME -n aquasense --previous

# Check resource constraints
kubectl top pods -n aquasense
kubectl top nodes
```

#### Database connection issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql -h RDS_ENDPOINT -U aquasense -d aquasense

# Check security groups
aws ec2 describe-security-groups --group-ids YOUR_SG_ID
```

#### High latency

```bash
# Check service mesh
kubectl get vs,dr -n aquasense

# Check ingress
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# Review metrics
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

### Health Checks

```bash
# Check all services
for service in auth sensor alert analytics tenant; do
  echo "Checking $service-service..."
  kubectl exec -n aquasense deploy/${service}-service -- \
    curl -f http://localhost:808X/actuator/health || echo "Failed"
done

# Check Kafka
kubectl run kafka-test --rm -it --restart=Never --image=confluentinc/cp-kafka -- \
  kafka-topics --bootstrap-server kafka:9092 --list
```

## Performance Tuning

### JVM Settings

Update deployment with optimized JVM settings:

```yaml
env:
  - name: JAVA_OPTS
    value: "-Xms512m -Xmx2g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
```

### Database Connection Pool

```yaml
env:
  - name: SPRING_DATASOURCE_HIKARI_MAXIMUM_POOL_SIZE
    value: "20"
  - name: SPRING_DATASOURCE_HIKARI_MINIMUM_IDLE
    value: "5"
```

## Rollback Procedures

```bash
# Rollback deployment
kubectl rollout undo deployment/auth-service -n aquasense

# Rollback to specific revision
kubectl rollout undo deployment/auth-service --to-revision=2 -n aquasense

# Check rollout history
kubectl rollout history deployment/auth-service -n aquasense
```

## Support

For additional help:
- Documentation: https://docs.aquasense.io
- Email: support@aquasense.io
- Slack: #aquasense-support
