# AquaSense Architecture

## System Overview

AquaSense uses a microservices architecture deployed on Kubernetes.

### Services
- Auth Service: Authentication and authorization
- Sensor Service: Sensor data ingestion and processing
- Alert Service: Real-time alerting
- Analytics Service: Data analytics and reporting
- Tenant Service: Multi-tenancy management
- ML Service: Machine learning model serving

### Data Flow
1. Sensors send data via HTTPS to Sensor Service
2. Data is validated and published to Kafka
3. Multiple consumers process data for different purposes
4. Processed data is stored in TimescaleDB
5. Real-time updates pushed via WebSocket

## Technology Stack
- Backend: Java 17, Spring Boot 3.2
- Message Broker: Apache Kafka
- Database: PostgreSQL 15 + TimescaleDB
- Cache: Redis
- Container Orchestration: Kubernetes (EKS)
- Monitoring: Prometheus + Grafana
