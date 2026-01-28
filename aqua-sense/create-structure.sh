#!/bin/bash

# Create auth-service structure
mkdir -p services/auth-service/src/main/{java/com/aquasense/auth/{controller,service,repository,model,config,security,dto},resources}
mkdir -p services/auth-service/src/test/java/com/aquasense/auth

# Create sensor-service structure
mkdir -p services/sensor-service/src/main/{java/com/aquasense/sensor/{controller,service,repository,model,config,kafka,dto},resources/db}
mkdir -p services/sensor-service/src/test/java/com/aquasense/sensor

# Create alert-service structure
mkdir -p services/alert-service/src/main/{java/com/aquasense/alert/{controller,service,repository,model,config,kafka,dto},resources}
mkdir -p services/alert-service/src/test/java/com/aquasense/alert

# Create analytics-service structure
mkdir -p services/analytics-service/src/main/{java/com/aquasense/analytics/{controller,service,repository,model,config,dto},resources}
mkdir -p services/analytics-service/src/test/java/com/aquasense/analytics

# Create tenant-service structure
mkdir -p services/tenant-service/src/main/{java/com/aquasense/tenant/{controller,service,repository,model,config,dto},resources}
mkdir -p services/tenant-service/src/test/java/com/aquasense/tenant

# Create ml-service structure
mkdir -p services/ml-service/{app,models,tests}

# Create frontend structure
mkdir -p frontend/{public,src/{components,pages,services,redux,utils,types,assets}}

# Create infra structure
mkdir -p infra/{terraform/{modules/{vpc,eks,rds,s3},environments/{dev,staging,prod}},kubernetes/{namespaces,deployments,services,configmaps,secrets,ingress},helm/aquasense/{templates,charts}}

# Create CI/CD structure
mkdir -p ci-cd/{jenkins,github-actions}

# Create observability structure
mkdir -p observability/{prometheus,grafana/{dashboards,datasources},elk}

# Create docs structure
mkdir -p docs/{api,architecture,deployment,user-guide}

echo "Directory structure created successfully"
