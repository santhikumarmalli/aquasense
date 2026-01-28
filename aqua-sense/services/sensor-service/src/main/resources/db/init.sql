-- AquaSense Database Initialization Script

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS sensor;
CREATE SCHEMA IF NOT EXISTS alert;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS tenant;

-- Auth Schema Tables

CREATE TABLE IF NOT EXISTS auth.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    tenant_id UUID NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    account_non_expired BOOLEAN DEFAULT TRUE,
    account_non_locked BOOLEAN DEFAULT TRUE,
    credentials_non_expired BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version BIGINT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS auth.roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auth.permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auth.user_roles (
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES auth.roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS auth.role_permissions (
    role_id UUID REFERENCES auth.roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES auth.permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

-- Sensor Schema Tables

CREATE TABLE IF NOT EXISTS sensor.facilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    address TEXT,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor.sensors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    facility_id UUID REFERENCES sensor.facilities(id),
    sensor_code VARCHAR(50) UNIQUE NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',
    metadata JSONB,
    installed_at TIMESTAMP,
    last_maintenance_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor.sensor_readings (
    id UUID DEFAULT uuid_generate_v4(),
    sensor_id UUID REFERENCES sensor.sensors(id),
    timestamp TIMESTAMP NOT NULL,
    ph DECIMAL(4, 2),
    temperature DECIMAL(5, 2),
    turbidity DECIMAL(8, 2),
    dissolved_oxygen DECIMAL(6, 2),
    conductivity DECIMAL(8, 2),
    orp DECIMAL(6, 2),
    tds DECIMAL(8, 2),
    metadata JSONB,
    PRIMARY KEY (sensor_id, timestamp)
);

-- Convert sensor_readings to hypertable (TimescaleDB)
SELECT create_hypertable('sensor.sensor_readings', 'timestamp', if_not_exists => TRUE);

-- Alert Schema Tables

CREATE TABLE IF NOT EXISTS alert.alert_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    metric VARCHAR(50) NOT NULL,
    condition VARCHAR(20) NOT NULL,
    threshold DECIMAL(10, 2) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alert.alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id UUID REFERENCES alert.alert_rules(id),
    sensor_id UUID REFERENCES sensor.sensors(id),
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'open',
    acknowledged_at TIMESTAMP,
    acknowledged_by UUID,
    resolved_at TIMESTAMP,
    resolved_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Tenant Schema Tables

CREATE TABLE IF NOT EXISTS tenant.tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE,
    status VARCHAR(20) DEFAULT 'active',
    plan VARCHAR(50) DEFAULT 'basic',
    max_facilities INTEGER DEFAULT 10,
    max_sensors INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tenant.tenant_settings (
    tenant_id UUID PRIMARY KEY REFERENCES tenant.tenants(id),
    settings JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes

CREATE INDEX idx_users_email ON auth.users(email);
CREATE INDEX idx_users_tenant_id ON auth.users(tenant_id);
CREATE INDEX idx_sensors_facility_id ON sensor.sensors(facility_id);
CREATE INDEX idx_sensors_status ON sensor.sensors(status);
CREATE INDEX idx_sensor_readings_sensor_id ON sensor.sensor_readings(sensor_id);
CREATE INDEX idx_sensor_readings_timestamp ON sensor.sensor_readings(timestamp DESC);
CREATE INDEX idx_alerts_sensor_id ON alert.alerts(sensor_id);
CREATE INDEX idx_alerts_status ON alert.alerts(status);
CREATE INDEX idx_alerts_created_at ON alert.alerts(created_at DESC);
CREATE INDEX idx_facilities_tenant_id ON sensor.facilities(tenant_id);

-- Insert default roles

INSERT INTO auth.roles (name, description) VALUES
    ('ROLE_SUPER_ADMIN', 'Super administrator with full system access'),
    ('ROLE_TENANT_ADMIN', 'Tenant administrator'),
    ('ROLE_FACILITY_MANAGER', 'Facility manager'),
    ('ROLE_OPERATOR', 'System operator'),
    ('ROLE_VIEWER', 'Read-only viewer'),
    ('ROLE_API_USER', 'API access user')
ON CONFLICT (name) DO NOTHING;

-- Insert default permissions

INSERT INTO auth.permissions (name, description) VALUES
    ('user:read', 'Read user information'),
    ('user:write', 'Create and update users'),
    ('user:delete', 'Delete users'),
    ('sensor:read', 'Read sensor data'),
    ('sensor:write', 'Configure sensors'),
    ('sensor:delete', 'Delete sensors'),
    ('alert:read', 'Read alerts'),
    ('alert:write', 'Create and update alerts'),
    ('alert:delete', 'Delete alerts'),
    ('facility:read', 'Read facility information'),
    ('facility:write', 'Create and update facilities'),
    ('facility:delete', 'Delete facilities'),
    ('tenant:read', 'Read tenant information'),
    ('tenant:write', 'Manage tenant settings'),
    ('analytics:read', 'View analytics'),
    ('report:generate', 'Generate reports')
ON CONFLICT (name) DO NOTHING;

-- Grant permissions to roles

DO $$
DECLARE
    super_admin_id UUID;
    tenant_admin_id UUID;
    facility_manager_id UUID;
    operator_id UUID;
    viewer_id UUID;
BEGIN
    SELECT id INTO super_admin_id FROM auth.roles WHERE name = 'ROLE_SUPER_ADMIN';
    SELECT id INTO tenant_admin_id FROM auth.roles WHERE name = 'ROLE_TENANT_ADMIN';
    SELECT id INTO facility_manager_id FROM auth.roles WHERE name = 'ROLE_FACILITY_MANAGER';
    SELECT id INTO operator_id FROM auth.roles WHERE name = 'ROLE_OPERATOR';
    SELECT id INTO viewer_id FROM auth.roles WHERE name = 'ROLE_VIEWER';
    
    -- Super admin gets all permissions
    INSERT INTO auth.role_permissions (role_id, permission_id)
    SELECT super_admin_id, id FROM auth.permissions
    ON CONFLICT DO NOTHING;
    
    -- Tenant admin gets most permissions except tenant:write
    INSERT INTO auth.role_permissions (role_id, permission_id)
    SELECT tenant_admin_id, id FROM auth.permissions 
    WHERE name != 'tenant:write'
    ON CONFLICT DO NOTHING;
    
    -- Facility manager gets facility and sensor permissions
    INSERT INTO auth.role_permissions (role_id, permission_id)
    SELECT facility_manager_id, id FROM auth.permissions 
    WHERE name IN ('facility:read', 'facility:write', 'sensor:read', 'sensor:write', 'alert:read', 'alert:write', 'analytics:read')
    ON CONFLICT DO NOTHING;
    
    -- Operator gets read/write for sensors and alerts
    INSERT INTO auth.role_permissions (role_id, permission_id)
    SELECT operator_id, id FROM auth.permissions 
    WHERE name IN ('sensor:read', 'sensor:write', 'alert:read', 'alert:write', 'facility:read')
    ON CONFLICT DO NOTHING;
    
    -- Viewer gets read-only permissions
    INSERT INTO auth.role_permissions (role_id, permission_id)
    SELECT viewer_id, id FROM auth.permissions 
    WHERE name LIKE '%:read'
    ON CONFLICT DO NOTHING;
END $$;

-- Create default demo tenant

INSERT INTO tenant.tenants (id, name, subdomain, plan, max_facilities, max_sensors)
VALUES 
    ('123e4567-e89b-12d3-a456-426614174000', 'Demo Corporation', 'demo', 'enterprise', 50, 500)
ON CONFLICT DO NOTHING;

-- Create demo facility

INSERT INTO sensor.facilities (id, tenant_id, name, location_lat, location_lng, type)
VALUES 
    ('223e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000', 'Central Treatment Plant', 40.7128, -74.0060, 'treatment_plant')
ON CONFLICT DO NOTHING;

-- Create sample sensors

INSERT INTO sensor.sensors (facility_id, sensor_code, sensor_type, location, installed_at)
VALUES 
    ('223e4567-e89b-12d3-a456-426614174000', 'S-001', 'pH', 'Inlet Basin 1', NOW() - INTERVAL '90 days'),
    ('223e4567-e89b-12d3-a456-426614174000', 'S-002', 'temperature', 'Inlet Basin 1', NOW() - INTERVAL '90 days'),
    ('223e4567-e89b-12d3-a456-426614174000', 'S-003', 'turbidity', 'Filtration Unit 1', NOW() - INTERVAL '90 days'),
    ('223e4567-e89b-12d3-a456-426614174000', 'S-004', 'dissolved_oxygen', 'Aeration Tank', NOW() - INTERVAL '90 days')
ON CONFLICT DO NOTHING;

-- Create sample alert rule

INSERT INTO alert.alert_rules (tenant_id, name, metric, condition, threshold, severity)
VALUES 
    ('123e4567-e89b-12d3-a456-426614174000', 'High Turbidity Alert', 'turbidity', 'greater_than', 10.0, 'high')
ON CONFLICT DO NOTHING;

-- Views for analytics

CREATE OR REPLACE VIEW analytics.sensor_summary AS
SELECT 
    s.id,
    s.sensor_code,
    s.sensor_type,
    f.name as facility_name,
    COUNT(sr.id) as reading_count,
    MAX(sr.timestamp) as last_reading,
    s.status
FROM sensor.sensors s
LEFT JOIN sensor.facilities f ON s.facility_id = f.id
LEFT JOIN sensor.sensor_readings sr ON s.id = sr.sensor_id
GROUP BY s.id, s.sensor_code, s.sensor_type, f.name, s.status;

CREATE OR REPLACE VIEW analytics.daily_water_quality AS
SELECT 
    date_trunc('day', timestamp) as date,
    sensor_id,
    AVG(ph) as avg_ph,
    AVG(temperature) as avg_temperature,
    AVG(turbidity) as avg_turbidity,
    AVG(dissolved_oxygen) as avg_do,
    AVG(conductivity) as avg_conductivity,
    MIN(ph) as min_ph,
    MAX(ph) as max_ph
FROM sensor.sensor_readings
GROUP BY date_trunc('day', timestamp), sensor_id;

COMMENT ON DATABASE aquasense IS 'AquaSense Enterprise Water Intelligence Platform Database';
