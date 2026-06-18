# scripts/import_csv.py
import csv
import json
import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/assetdb")
engine = create_engine(DB_URL, future=True)

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def upsert_asset(conn, row):
    macs = [row['macAddresses']] if row.get('macAddresses') else []
    ips = [row['ipAddresses']] if row.get('ipAddresses') else []
    stmt = text("""
    INSERT INTO assets (id, asset_tag, serial_number, type, manufacturer, model, hostname, mac_addresses, ip_addresses, owner_id, owner_name, cost_center, location, purchase_date, warranty_end, lifecycle_state, metadata, created_at, updated_at)
    VALUES (:id, :asset_tag, :serial_number, :type, :manufacturer, :model, :hostname, :mac_addresses::jsonb, :ip_addresses::jsonb, :owner_id, :owner_name, :cost_center, :location, :purchase_date, :warranty_end, :lifecycle_state, :metadata::jsonb, :created_at, :updated_at)
    ON CONFLICT (id) DO UPDATE SET
      asset_tag = EXCLUDED.asset_tag,
      serial_number = EXCLUDED.serial_number,
      hostname = EXCLUDED.hostname,
      mac_addresses = EXCLUDED.mac_addresses,
      ip_addresses = EXCLUDED.ip_addresses,
      updated_at = EXCLUDED.updated_at
    """)
    conn.execute(stmt, {
        "id": row.get("id"),
        "asset_tag": row.get("assetTag"),
        "serial_number": row.get("serialNumber"),
        "type": row.get("type"),
        "manufacturer": row.get("manufacturer"),
        "model": row.get("model"),
        "hostname": row.get("hostname"),
        "mac_addresses": json.dumps(macs),
        "ip_addresses": json.dumps(ips),
        "owner_id": row.get("ownerId"),
        "owner_name": row.get("ownerName"),
        "cost_center": row.get("costCenter"),
        "location": row.get("location"),
        "purchase_date": row.get("purchaseDate") or None,
        "warranty_end": row.get("warrantyEnd") or None,
        "lifecycle_state": row.get("lifecycleState") or "active",
        "metadata": row.get("metadata") or "{}",
        "created_at": row.get("createdAt") or datetime.utcnow().isoformat(),
        "updated_at": row.get("updatedAt") or datetime.utcnow().isoformat()
    })

def import_assets(csv_path):
    rows = load_csv(csv_path)
    with engine.begin() as conn:
        for r in rows:
            upsert_asset(conn, r)
    print(f"Imported {len(rows)} assets")

def import_discoveries(csv_path):
    rows = load_csv(csv_path)
    with engine.begin() as conn:
        for r in rows:
            macs = [r['macAddresses']] if r.get('macAddresses') else []
            ips = [r['ipAddresses']] if r.get('ipAddresses') else []
            stmt = text("""
            INSERT INTO discovery_records (id, discovery_source, raw_payload, serial_number, hostname, mac_addresses, ip_addresses, last_seen, reconciliation_status, created_at)
            VALUES (:id, :discovery_source, :raw_payload::jsonb, :serial_number, :hostname, :mac_addresses::jsonb, :ip_addresses::jsonb, :last_seen, :reconciliation_status, :created_at)
            ON CONFLICT (id) DO NOTHING
            """)
            conn.execute(stmt, {
                "id": r.get("id"),
                "discovery_source": r.get("discoverySource"),
                "raw_payload": json.dumps({}),
                "serial_number": r.get("serialNumber") or None,
                "hostname": r.get("hostname") or None,
                "mac_addresses": json.dumps(macs),
                "ip_addresses": json.dumps(ips),
                "last_seen": r.get("lastSeen") or None,
                "reconciliation_status": r.get("reconciliationStatus") or "unmatched",
                "created_at": datetime.utcnow().isoformat()
            })
    print(f"Imported {len(rows)} discoveries")

if __name__ == "__main__":
    import_assets("data/assets_seed.csv")
    import_discoveries("data/discoveries_seed.csv")
