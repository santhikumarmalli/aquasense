#!/usr/bin/env python3
"""
AquaSense File Generator
Generates all necessary files for the complete enterprise SaaS platform
"""

import os
from pathlib import Path

BASE_DIR = Path("/home/claude/aqua-sense")

# File contents dictionary
FILES = {
    # Auth Service Files
    "services/auth-service/Dockerfile": '''FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
''',

    "services/auth-service/src/main/java/com/aquasense/auth/model/Permission.java": '''package com.aquasense.auth.model;

import jakarta.persistence.*;
import lombok.*;
import java.util.*;

@Entity
@Table(name = "permissions")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Permission {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @Column(nullable = false, unique = true)
    private String name;
    
    private String description;
    
    @ManyToMany(mappedBy = "permissions")
    private Set<Role> roles = new HashSet<>();
}
''',

    "services/auth-service/src/main/java/com/aquasense/auth/controller/AuthController.java": '''package com.aquasense.auth.controller;

import com.aquasense.auth.dto.*;
import com.aquasense.auth.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/v1")
@RequiredArgsConstructor
@Tag(name = "Authentication", description = "Authentication and authorization endpoints")
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    @Operation(summary = "Register new user")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody RegisterRequest request) {
        return ResponseEntity.ok(authService.register(request));
    }

    @PostMapping("/login")
    @Operation(summary = "User login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @PostMapping("/refresh")
    @Operation(summary = "Refresh access token")
    public ResponseEntity<AuthResponse> refresh(@Valid @RequestBody RefreshTokenRequest request) {
        return ResponseEntity.ok(authService.refreshToken(request));
    }

    @PostMapping("/logout")
    @Operation(summary = "User logout")
    public ResponseEntity<Void> logout(@RequestHeader("Authorization") String token) {
        authService.logout(token);
        return ResponseEntity.ok().build();
    }
}
''',

    # Sensor Service Files
    "services/sensor-service/pom.xml": '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>com.aquasense</groupId>
        <artifactId>aquasense-parent</artifactId>
        <version>1.0.0</version>
    </parent>
    
    <artifactId>sensor-service</artifactId>
    <name>Sensor Service</name>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.kafka</groupId>
            <artifactId>spring-kafka</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-websocket</artifactId>
        </dependency>
    </dependencies>
</project>
''',

    "services/sensor-service/Dockerfile": '''FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8082
ENTRYPOINT ["java", "-jar", "app.jar"]
''',

    "services/sensor-service/src/main/java/com/aquasense/sensor/SensorServiceApplication.java": '''package com.aquasense.sensor;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableKafka
@EnableScheduling
public class SensorServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(SensorServiceApplication.class, args);
    }
}
''',

    "services/sensor-service/src/main/resources/application.yml": '''server:
  port: 8082
  servlet:
    context-path: /api/sensors

spring:
  application:
    name: sensor-service
  datasource:
    url: ${SPRING_DATASOURCE_URL:jdbc:postgresql://localhost:5432/aquasense}
    username: ${SPRING_DATASOURCE_USERNAME:aquasense}
    password: ${SPRING_DATASOURCE_PASSWORD:aquasense123}
  kafka:
    bootstrap-servers: ${SPRING_KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
    consumer:
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      group-id: sensor-service-group
      auto-offset-reset: earliest

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
''',

    # Frontend Files
    "frontend/package.json": '''{
  "name": "aquasense-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@reduxjs/toolkit": "^2.0.1",
    "react-redux": "^9.0.4",
    "@mui/material": "^5.15.0",
    "@mui/icons-material": "^5.15.0",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "axios": "^1.6.2",
    "recharts": "^2.10.3",
    "mapbox-gl": "^3.0.1",
    "date-fns": "^3.0.6"
  },
  "devDependencies": {
    "@types/react": "^18.2.45",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "typescript": "^5.3.3"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest"
  }
}
''',

    "frontend/Dockerfile": '''FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
''',

    "frontend/vite.config.ts": '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true
  }
})
''',

    "frontend/src/App.tsx": '''import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    secondary: { main: '#dc004e' },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
''',

    # Infrastructure Files
    "infra/terraform/main.tf": '''terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "aquasense-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"
  
  environment = var.environment
  vpc_cidr    = var.vpc_cidr
}

module "eks" {
  source = "./modules/eks"
  
  environment        = var.environment
  vpc_id            = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
}

module "rds" {
  source = "./modules/rds"
  
  environment        = var.environment
  vpc_id            = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  db_name           = "aquasense"
}
''',

    "infra/terraform/variables.tf": '''variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}
''',

    # Kubernetes manifests
    "infra/kubernetes/namespaces/aquasense.yaml": '''apiVersion: v1
kind: Namespace
metadata:
  name: aquasense
  labels:
    name: aquasense
    environment: production
''',

    "infra/kubernetes/deployments/auth-service.yaml": '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: aquasense
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
    spec:
      containers:
      - name: auth-service
        image: aquasense/auth-service:latest
        ports:
        - containerPort: 8081
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /actuator/health
            port: 8081
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health
            port: 8081
          initialDelaySeconds: 10
          periodSeconds: 5
''',

    # CI/CD Files
    "ci-cd/jenkins/Jenkinsfile": '''pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.azurecr.io'
        AWS_REGION = 'us-east-1'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Services') {
            parallel {
                stage('Auth Service') {
                    steps {
                        dir('services/auth-service') {
                            sh 'mvn clean package -DskipTests'
                        }
                    }
                }
                stage('Sensor Service') {
                    steps {
                        dir('services/sensor-service') {
                            sh 'mvn clean package -DskipTests'
                        }
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'mvn test'
            }
        }
        
        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }
        
        stage('Push to Registry') {
            steps {
                sh 'docker-compose push'
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f infra/kubernetes/'
            }
        }
    }
    
    post {
        always {
            junit '**/target/surefire-reports/*.xml'
            cleanWs()
        }
    }
}
''',

    "ci-cd/github-actions/deploy.yml": '''name: Deploy AquaSense

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
    
    - name: Build with Maven
      run: cd services && mvn clean install
    
    - name: Run tests
      run: cd services && mvn test
    
    - name: Build Docker images
      run: docker-compose build
    
    - name: Push to ECR
      run: |
        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
        docker-compose push
    
    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --region us-east-1 --name aquasense-cluster
        kubectl apply -f infra/kubernetes/
''',

    # Observability
    "observability/prometheus/prometheus.yml": '''global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'auth-service'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['auth-service:8081']
  
  - job_name: 'sensor-service'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['sensor-service:8082']
  
  - job_name: 'alert-service'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['alert-service:8083']
''',

    "observability/grafana/dashboards/overview.json": '''{
  "dashboard": {
    "title": "AquaSense Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_server_requests_seconds_count[5m])"
          }
        ]
      }
    ]
  }
}
''',

    # Documentation
    "docs/api/README.md": '''# AquaSense API Documentation

## Authentication API

### Register User
```
POST /api/auth/v1/register
```

### Login
```
POST /api/auth/v1/login
```

## Sensor API

### Get Sensor Data
```
GET /api/sensors/v1/data
```

### Submit Reading
```
POST /api/sensors/v1/readings
```

For complete API documentation, visit: http://localhost:8080/swagger-ui.html
''',

    "docs/architecture/README.md": '''# AquaSense Architecture

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
''',

    "LICENSE": '''MIT License

Copyright (c) 2026 AquaSense

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
}

def generate_files():
    """Generate all files in the dictionary"""
    created_count = 0
    for file_path, content in FILES.items():
        full_path = BASE_DIR / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        created_count += 1
        if created_count % 10 == 0:
            print(f"Created {created_count} files...")
    
    print(f"\\n✓ Successfully created {created_count} files")
    return created_count

if __name__ == "__main__":
    print("Generating AquaSense application files...")
    count = generate_files()
    print(f"\\nGeneration complete! Created {count} files.")
