# AquaSense – Enterprise Water Intelligence Platform

![AquaSense Logo](docs/assets/logo.png)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![Version](https://img.shields.io/badge/version-1.0.0-orange)]()

## 🌊 Overview

AquaSense is a real-time, cloud-native SaaS platform that helps enterprises monitor, analyze, and respond to water quality risks across industrial facilities. Built with microservices architecture and designed for scale.

## 🎯 Core Capabilities

- **Multi-tenant Enterprise Architecture**: Secure data isolation and tenant management
- **Real-time Data Ingestion**: Apache Kafka for high-throughput sensor data
- **AI-Assisted Image Analysis**: Computer vision for water quality assessment
- **Compliance-Ready Audit Trails**: Complete audit logging for regulatory compliance
- **Geo-spatial Risk Visualization**: Interactive maps with real-time risk heatmaps

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (Kong)                       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌────────▼────────┐   ┌──────▼──────┐
│   Auth Service  │   │  Sensor Service │   │ Alert Service│
│   (Spring Boot) │   │  (Spring Boot)  │   │(Spring Boot) │
└────────┬────────┘   └────────┬────────┘   └──────┬───────┘
         │                     │                    │
         └─────────────────────┼────────────────────┘
                               │
                     ┌─────────▼──────────┐
                     │   Apache Kafka     │
                     └─────────┬──────────┘
                               │
                     ┌─────────▼──────────┐
                     │   PostgreSQL       │
                     │   TimescaleDB      │
                     └────────────────────┘
```

## 🚀 Tech Stack

### Backend
- **Language**: Java 17
- **Framework**: Spring Boot 3.2
- **Messaging**: Apache Kafka
- **Database**: PostgreSQL 15 + TimescaleDB
- **Cache**: Redis
- **API Gateway**: Kong

### Frontend
- **Framework**: React 18
- **State Management**: Redux Toolkit
- **UI Library**: Material-UI (MUI)
- **Charts**: Recharts, Mapbox GL
- **Build Tool**: Vite

### Infrastructure
- **Cloud**: AWS (EKS, RDS, S3, CloudWatch)
- **Container Orchestration**: Kubernetes (EKS)
- **IaC**: Terraform
- **Service Mesh**: Istio

### CI/CD & Observability
- **CI/CD**: Jenkins, GitHub Actions
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: Jaeger

## 📁 Repository Structure

```
aqua-sense/
├── services/              # Microservices
│   ├── auth-service/     # Authentication & Authorization
│   ├── sensor-service/   # Sensor data ingestion & processing
│   ├── alert-service/    # Real-time alerting
│   ├── analytics-service/# Data analytics & reporting
│   ├── tenant-service/   # Multi-tenancy management
│   └── ml-service/       # ML model serving (Python)
├── frontend/             # React web application
├── infra/               # Infrastructure as Code
│   ├── terraform/       # AWS infrastructure
│   ├── kubernetes/      # K8s manifests
│   └── helm/           # Helm charts
├── ci-cd/              # CI/CD pipelines
│   ├── jenkins/        # Jenkinsfiles
│   └── github-actions/ # GitHub Actions workflows
├── observability/      # Monitoring & logging configs
│   ├── prometheus/
│   ├── grafana/
│   └── elk/
├── docs/              # Documentation
├── docker-compose.yml # Local development setup
└── README.md
```

## 🛠️ Getting Started

### Prerequisites

- Docker Desktop 24+
- Docker Compose 2.20+
- Node.js 18+
- Java 17+
- Maven 3.9+
- kubectl 1.28+
- Terraform 1.5+
- AWS CLI 2.x

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/aqua-sense.git
   cd aqua-sense
   ```

2. **Start infrastructure services**
   ```bash
   docker-compose up -d postgres redis kafka zookeeper
   ```

3. **Initialize databases**
   ```bash
   ./scripts/init-databases.sh
   ```

4. **Start backend services**
   ```bash
   cd services
   ./mvnw spring-boot:run -pl auth-service
   ./mvnw spring-boot:run -pl sensor-service
   ./mvnw spring-boot:run -pl alert-service
   ```

5. **Start frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:8080
   - Grafana: http://localhost:3001
   - Kibana: http://localhost:5601

### Running with Docker Compose

```bash
docker-compose up -d
```

This starts all services in containers. Access at http://localhost:3000

## 🔐 Security

- **Authentication**: OAuth 2.0 / OpenID Connect
- **Authorization**: RBAC with fine-grained permissions
- **Data Encryption**: TLS 1.3 in transit, AES-256 at rest
- **Secrets Management**: AWS Secrets Manager / HashiCorp Vault
- **API Security**: Rate limiting, CORS, CSRF protection
- **Compliance**: GDPR, SOC 2, ISO 27001 ready

## 📊 Key Features

### Real-time Monitoring Dashboard
- Live sensor data visualization
- Historical trend analysis
- Anomaly detection with ML
- Customizable alerts

### Multi-tenant Management
- Tenant isolation at database level
- Per-tenant configuration
- Usage tracking and billing
- White-label support

### Compliance & Reporting
- Automated compliance reports
- Audit trail with immutable logs
- Export to PDF/Excel
- Regulatory alert notifications

### AI/ML Capabilities
- Water quality prediction models
- Image-based contamination detection
- Anomaly detection algorithms
- Predictive maintenance

## 🧪 Testing

```bash
# Unit tests
./mvnw test

# Integration tests
./mvnw verify -P integration-tests

# E2E tests
cd frontend && npm run test:e2e

# Load tests
k6 run tests/load/scenario.js
```

## 📈 Deployment

### AWS EKS Deployment

1. **Provision infrastructure**
   ```bash
   cd infra/terraform
   terraform init
   terraform plan
   terraform apply
   ```

2. **Deploy to Kubernetes**
   ```bash
   cd infra/kubernetes
   kubectl apply -f namespaces/
   kubectl apply -f configmaps/
   kubectl apply -f secrets/
   kubectl apply -f deployments/
   ```

3. **Deploy with Helm**
   ```bash
   helm install aquasense ./infra/helm/aquasense \
     --namespace production \
     --values infra/helm/values-prod.yaml
   ```

## 🔍 Monitoring & Observability

- **Metrics**: Prometheus collects metrics from all services
- **Logs**: Centralized logging with ELK stack
- **Traces**: Distributed tracing with Jaeger
- **Dashboards**: Pre-built Grafana dashboards
- **Alerts**: PagerDuty integration for critical alerts

## 📝 API Documentation

- **OpenAPI/Swagger**: http://localhost:8080/swagger-ui.html
- **API Docs**: See [docs/api/README.md](docs/api/README.md)
- **Postman Collection**: [docs/postman/](docs/postman/)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issue Tracker**: GitHub Issues
- **Email**: support@aquasense.io
- **Slack**: #aquasense-support

## 🗺️ Roadmap

- [ ] Q1 2026: Mobile app (iOS/Android)
- [ ] Q2 2026: Advanced ML models for predictive analytics
- [ ] Q3 2026: IoT device SDK
- [ ] Q4 2026: Blockchain-based audit trail

## 👥 Team

Built with ❤️ by the AquaSense Team

---

**Version**: 1.0.0  
**Last Updated**: January 2026
