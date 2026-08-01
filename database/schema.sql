-- Canonical PostgreSQL schema. SQLAlchemy creates this model automatically on first application startup.
CREATE TABLE users (
  id VARCHAR(36) PRIMARY KEY,
  email VARCHAR(320) UNIQUE NOT NULL,
  full_name VARCHAR(120) NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  role VARCHAR(40) NOT NULL DEFAULT 'operator',
  is_verified BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE machines (
  id VARCHAR(36) PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(150) NOT NULL,
  location VARCHAR(120) NOT NULL,
  status VARCHAR(30) NOT NULL,
  health_score DOUBLE PRECISION NOT NULL,
  utilization DOUBLE PRECISION NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sensor_readings (
  id VARCHAR(36) PRIMARY KEY,
  machine_id VARCHAR(36) NOT NULL REFERENCES machines(id),
  metric VARCHAR(50) NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  unit VARCHAR(20) NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX sensor_readings_machine_recorded_idx ON sensor_readings(machine_id, recorded_at DESC);

CREATE TABLE maintenance_records (
  id VARCHAR(36) PRIMARY KEY,
  machine_id VARCHAR(36) NOT NULL REFERENCES machines(id),
  title VARCHAR(180) NOT NULL,
  maintenance_type VARCHAR(30) NOT NULL,
  priority VARCHAR(20) NOT NULL,
  status VARCHAR(30) NOT NULL,
  due_at TIMESTAMPTZ NOT NULL,
  notes TEXT
);

CREATE TABLE alerts (
  id VARCHAR(36) PRIMARY KEY,
  machine_id VARCHAR(36) REFERENCES machines(id),
  title VARCHAR(180) NOT NULL,
  severity VARCHAR(20) NOT NULL,
  message TEXT NOT NULL,
  acknowledged BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE production_orders (
  id VARCHAR(36) PRIMARY KEY,
  order_number VARCHAR(60) UNIQUE NOT NULL,
  product_name VARCHAR(150) NOT NULL,
  target_quantity INTEGER NOT NULL,
  actual_quantity INTEGER NOT NULL DEFAULT 0,
  status VARCHAR(30) NOT NULL,
  due_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE products (
  id VARCHAR(36) PRIMARY KEY,
  sku VARCHAR(60) UNIQUE NOT NULL,
  name VARCHAR(150) NOT NULL,
  category VARCHAR(50) NOT NULL,
  unit VARCHAR(20) NOT NULL DEFAULT 'pcs'
);

CREATE TABLE inventory_items (
  id VARCHAR(36) PRIMARY KEY,
  sku VARCHAR(60) UNIQUE NOT NULL,
  name VARCHAR(150) NOT NULL,
  category VARCHAR(50) NOT NULL,
  quantity DOUBLE PRECISION NOT NULL,
  reorder_point DOUBLE PRECISION NOT NULL,
  unit VARCHAR(20) NOT NULL,
  location VARCHAR(120) NOT NULL
);

CREATE TABLE energy_readings (
  id VARCHAR(36) PRIMARY KEY,
  machine_id VARCHAR(36) REFERENCES machines(id),
  source VARCHAR(40) NOT NULL,
  consumption_kwh DOUBLE PRECISION NOT NULL,
  carbon_kg DOUBLE PRECISION NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE defect_inspections (
  id VARCHAR(36) PRIMARY KEY,
  product_code VARCHAR(60) NOT NULL,
  image_url VARCHAR(500),
  result VARCHAR(30) NOT NULL,
  defect_type VARCHAR(80),
  confidence DOUBLE PRECISION NOT NULL,
  bounding_boxes JSONB NOT NULL DEFAULT '[]',
  inspected_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE documents (
  id VARCHAR(36) PRIMARY KEY,
  title VARCHAR(180) NOT NULL,
  content TEXT NOT NULL,
  document_type VARCHAR(50) NOT NULL,
  source_uri VARCHAR(500),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE chat_messages (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL REFERENCES users(id),
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  sources JSONB NOT NULL DEFAULT '[]',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE reports (
  id VARCHAR(36) PRIMARY KEY,
  title VARCHAR(180) NOT NULL,
  report_type VARCHAR(50) NOT NULL,
  generated_by VARCHAR(36) NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_logs (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) REFERENCES users(id),
  action VARCHAR(100) NOT NULL,
  entity_type VARCHAR(80) NOT NULL,
  entity_id VARCHAR(36),
  details JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
