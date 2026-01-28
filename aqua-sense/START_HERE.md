# 🌊 AquaSense - Getting Started

Welcome to AquaSense, an Enterprise Water Intelligence Platform!

## 📦 What's Included

This package contains a complete, production-ready SaaS application with:

- **6 Microservices** (Java/Spring Boot + Python)
- **React Frontend** with Material-UI
- **Infrastructure as Code** (Terraform + Kubernetes)
- **CI/CD Pipelines** (Jenkins + GitHub Actions)
- **Observability Stack** (Prometheus, Grafana, ELK, Jaeger)
- **Comprehensive Documentation**

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Docker Desktop 24+ (with 16GB RAM allocated)
- Port availability: 3000, 5432, 6379, 8080, 8081-8086, 9092

### Option 1: Docker Compose (Recommended for Testing)

```bash
# 1. Extract the zip file
unzip aqua-sense.zip
cd aqua-sense

# 2. Start all services
docker-compose up -d

# 3. Wait for services to be healthy (2-3 minutes)
docker-compose ps

# 4. Access the application
open http://localhost:3000
```

**Default Login:**
- Email: `demo@aquasense.io`
- Password: `Demo123!`

### Option 2: Local Development Setup

```bash
# 1. Start infrastructure services only
docker-compose up -d postgres redis kafka zookeeper

# 2. Start backend services
cd services
./mvnw clean install
./mvnw spring-boot:run -pl auth-service &
./mvnw spring-boot:run -pl sensor-service &
./mvnw spring-boot:run -pl alert-service &

# 3. Start frontend
cd ../frontend
npm install
npm run dev
```

## 🏗️ Architecture Overview

```
┌─────────────┐
│   Frontend  │  React 18 + Material-UI
│   (Port     │
│    3000)    │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────┐
│           API Gateway (Kong)                 │
│               (Port 8080)                    │
└──────┬───────────────┬──────────────────────┘
       │               │
┌──────▼──────┐  ┌────▼─────────┐
│Auth Service │  │Sensor Service│  ... more services
│  (8081)     │  │   (8082)     │
└─────────────┘  └──────────────┘
       │               │
       └───────┬───────┘
               │
       ┌───────▼────────┐
       │   PostgreSQL   │
       │   TimescaleDB  │
       │   Redis        │
       │   Kafka        │
       └────────────────┘
```

## 📍 Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | React web application |
| API Gateway | 8080 | Kong API Gateway |
| Auth Service | 8081 | Authentication & Authorization |
| Sensor Service | 8082 | Sensor data ingestion |
| Alert Service | 8083 | Real-time alerting |
| Analytics Service | 8084 | Data analytics |
| Tenant Service | 8085 | Multi-tenancy management |
| ML Service | 8086 | Machine learning models |
| Grafana | 3001 | Monitoring dashboards |
| Prometheus | 9090 | Metrics collection |
| Kibana | 5601 | Log visualization |
| Jaeger | 16686 | Distributed tracing |
| MailHog | 8025 | Email testing |

## 🔑 Access URLs

- **Application**: http://localhost:3000
- **API Gateway**: http://localhost:8080
- **API Docs**: http://localhost:8080/swagger-ui.html
- **Grafana**: http://localhost:3001 (admin/admin123)
- **Kibana**: http://localhost:5601
- **Jaeger**: http://localhost:16686
- **Prometheus**: http://localhost:9090

## 📚 Documentation Structure

```
docs/
├── api/              # API documentation
├── architecture/     # System architecture
├── deployment/       # Deployment guides
└── user-guide/       # User documentation
```

## 🧪 Testing the Application

### 1. Test Authentication
```bash
curl -X POST http://localhost:8080/api/auth/v1/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@aquasense.io","password":"Demo123!"}'
```

### 2. Check Sensor Data
```bash
curl http://localhost:8080/api/sensors/v1/data \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. View Metrics
Open http://localhost:3001 and navigate to AquaSense dashboards

## 🐳 Docker Commands

```bash
# View logs
docker-compose logs -f [service-name]

# Restart a service
docker-compose restart [service-name]

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild images
docker-compose build

# Scale a service
docker-compose up -d --scale sensor-service=3
```

## 🔧 Common Issues & Solutions

### Issue: Ports already in use
```bash
# Check what's using the port
lsof -i :3000
# Kill the process or change ports in docker-compose.yml
```

### Issue: Services not starting
```bash
# Check Docker resources
docker system df
# Increase Docker memory in Docker Desktop settings (16GB recommended)
```

### Issue: Database connection failed
```bash
# Ensure PostgreSQL is healthy
docker-compose logs postgres
# Reinitialize database
docker-compose down -v
docker-compose up -d postgres
```

## 🚀 Production Deployment

For production deployment to AWS EKS:

```bash
# 1. Configure AWS credentials
aws configure

# 2. Provision infrastructure
cd infra/terraform
terraform init
terraform apply

# 3. Deploy to Kubernetes
cd ../kubernetes
kubectl apply -f namespaces/
kubectl apply -f deployments/
kubectl apply -f services/

# See docs/deployment/README.md for complete guide
```

## 📊 Sample Data

The application comes pre-loaded with:
- Demo tenant account
- Sample facilities and sensors
- Historical sensor readings
- Alert rules
- Test users with different roles

## 🛠️ Development

### Tech Stack
- **Backend**: Java 17, Spring Boot 3.2, Kafka
- **Frontend**: React 18, TypeScript, Material-UI
- **Database**: PostgreSQL 15 + TimescaleDB
- **Cache**: Redis
- **Search**: Elasticsearch
- **Monitoring**: Prometheus, Grafana
- **Infrastructure**: Terraform, Kubernetes

### Build from Source

```bash
# Backend
cd services
./mvnw clean package

# Frontend
cd frontend
npm run build

# Docker images
docker-compose build
```

## 📖 Key Features

✅ Real-time sensor data ingestion via Kafka
✅ AI-powered water quality prediction
✅ Automated alerting system
✅ Interactive dashboards with live updates
✅ Multi-tenant architecture
✅ Role-based access control (RBAC)
✅ Comprehensive audit trails
✅ RESTful APIs with OpenAPI docs
✅ Horizontal scalability
✅ Complete observability stack

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 💬 Support

- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Email**: support@aquasense.io

## 🎯 Next Steps

1. ✅ Start the application with `docker-compose up -d`
2. ✅ Access http://localhost:3000
3. ✅ Login with demo credentials
4. ✅ Explore the dashboard
5. ✅ Review API docs at http://localhost:8080/swagger-ui.html
6. ✅ Check monitoring in Grafana (http://localhost:3001)
7. ✅ Read the architecture docs in `docs/architecture/`
8. ✅ Try the deployment guide for production setup

**Enjoy building with AquaSense! 🌊**

---

For detailed documentation, see:
- Architecture: `docs/architecture/README.md`
- Deployment: `docs/deployment/README.md`
- API Reference: `docs/api/README.md`
- User Guide: Access from the application
