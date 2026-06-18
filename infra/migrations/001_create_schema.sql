-- 001_create_schema.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- assets table
CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  asset_tag TEXT UNIQUE,
  serial_number TEXT,
  type TEXT,
  manufacturer TEXT,
  model TEXT,
  hostname TEXT,
  mac_addresses JSONB,
  ip_addresses JSONB,
  owner_id TEXT,
  owner_name TEXT,
  cost_center TEXT,
  location TEXT,
  purchase_date DATE,
  warranty_end DATE,
  lifecycle_state TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- discovery records
CREATE TABLE discovery_records (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  discovery_source TEXT NOT NULL,
  raw_payload JSONB,
  serial_number TEXT,
  hostname TEXT,
  mac_addresses JSONB,
  ip_addresses JSONB,
  os JSONB,
  last_seen TIMESTAMPTZ,
  reconciliation_status TEXT DEFAULT 'unmatched',
  linked_asset_id UUID REFERENCES assets(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- audit entries (append-only)
CREATE TABLE audit_entries (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  timestamp TIMESTAMPTZ DEFAULT now(),
  actor_id TEXT,
  action_type TEXT,
  resource_id TEXT,
  payload_hash TEXT,
  payload JSONB
);

-- custody records
CREATE TABLE custody_records (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  asset_id UUID REFERENCES assets(id),
  signer_id TEXT,
  signer_name TEXT,
  evidence_links JSONB,
  geo JSONB,
  timestamp TIMESTAMPTZ DEFAULT now()
);

-- indexes for performance
CREATE INDEX idx_assets_serial ON assets(serial_number);
CREATE INDEX idx_assets_asset_tag ON assets(asset_tag);
CREATE INDEX idx_assets_type ON assets(type);
CREATE INDEX idx_discovery_serial ON discovery_records(serial_number);
CREATE INDEX idx_discovery_status ON discovery_records(reconciliation_status);
CREATE INDEX idx_audit_timestamp ON audit_entries(timestamp);

-- GIN index for JSONB mac_addresses and metadata
CREATE INDEX gin_assets_mac ON assets USING gin ((mac_addresses)) ;
CREATE INDEX gin_discovery_mac ON discovery_records USING gin ((mac_addresses)) ;
CREATE INDEX gin_assets_metadata ON assets USING gin (metadata);
