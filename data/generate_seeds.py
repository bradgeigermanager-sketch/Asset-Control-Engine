import csv, uuid, random
from datetime import datetime, timedelta

OUT_ASSETS = "data/assets_seed.csv"
OUT_DISC = "data/discoveries_seed.csv"
OUT_ANOM = "data/anomalies_seed.csv"

def rand_mac(i):
    base = 0x001122334400 + i
    return ":".join(f"{(base >> (8*j)) & 0xff:02x}" for j in reversed(range(6)))

def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def gen_assets(n=500):
    types = ["laptop","desktop","server","switch","printer","iot","vm"]
    rows = []
    now = datetime.utcnow()
    for i in range(1, n+1):
        aid = str(uuid.uuid4())
        tag = f"AT-{i:04d}"
        sn = f"SN-ABC-{1000 + i}"
        t = random.choice(types)
        hostname = f"user-{i}-host"
        mac = rand_mac(i)
        ip = f"10.0.{i%250}.{10 + (i%200)}"
        ownerId = f"u-{1000 + (i%200)}"
        ownerName = f"User {i}"
        costCenter = f"CC-{100 + (i%50)}"
        purchase = (now - timedelta(days=random.randint(100,1500))).date().isoformat()
        warranty = (now + timedelta(days=random.randint(90,900))).date().isoformat()
        created = iso(now - timedelta(days=random.randint(1,30)))
        updated = iso(now - timedelta(days=random.randint(0,5)))
        rows.append({
            "id":aid,"assetTag":tag,"serialNumber":sn,"type":t,
            "manufacturer":"Vendor","model":"ModelX","hostname":hostname,
            "macAddresses":mac,"ipAddresses":ip,"ownerId":ownerId,"ownerName":ownerName,
            "costCenter":costCenter,"location":"HQ","purchaseDate":purchase,
            "warrantyEnd":warranty,"lifecycleState":"active","metadata":"{}",
            "createdAt":created,"updatedAt":updated
        })
    return rows

def gen_discoveries(assets, n_match=100, n_conflict=30, n_orphan=20):
    rows = []
    now = datetime.utcnow()
    for i in range(n_match):
        a = assets[i]
        rows.append({
            "id":f"d-{i+1:04d}",
            "discoverySource": random.choice(["agent","mdm","network","cloud"]),
            "rawPayload":"{}",
            "serialNumber": a["serialNumber"],
            "hostname": a["hostname"],
            "macAddresses": a["macAddresses"],
            "ipAddresses": a["ipAddresses"],
            "lastSeen": iso(now - timedelta(minutes=random.randint(1,120))),
            "reconciliationStatus":"unmatched"
        })
    for i in range(n_conflict):
        a = assets[n_match + i]
        parts = a["macAddresses"].split(":")
        last = int(parts[-1],16) ^ 0x01
        parts[-1] = f"{last:02x}"
        rows.append({
            "id":f"d-{n_match + i +1:04d}",
            "discoverySource": random.choice(["network","agent"]),
            "rawPayload":"{}",
            "serialNumber": "" if random.random() < 0.6 else a["serialNumber"],
            "hostname": a["hostname"] + ("-CLONE" if random.random() < 0.5 else ""),
            "macAddresses": ":".join(parts),
            "ipAddresses": a["ipAddresses"],
            "lastSeen": iso(now - timedelta(minutes=random.randint(10,500))),
            "reconciliationStatus":"unmatched"
        })
    for i in range(n_orphan):
        idx = n_match + n_conflict + i
        rows.append({
            "id":f"d-{idx+1:04d}",
            "discoverySource": random.choice(["network","cloud"]),
            "rawPayload":"{}",
            "serialNumber": "",
            "hostname": f"unknown-{i+1}",
            "macAddresses": rand_mac(10000 + i),
            "ipAddresses": f"10.1.{i%250}.{20 + i%200}",
            "lastSeen": iso(now - timedelta(minutes=random.randint(5,1000))),
            "reconciliationStatus":"unmatched"
        })
    return rows

def write_csv(path, rows, headers):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(r)

if __name__ == "__main__":
    assets = gen_assets(500)
    discoveries = gen_discoveries(assets, n_match=100, n_conflict=30, n_orphan=20)
    anomalies = [
        {"id":"an-0001","type":"duplicate_mac","description":"Two canonical assets share same MAC","discoveryId":"","notes":"seeded conflict"},
        {"id":"an-0002","type":"missing_serial","description":"Discovery payload missing serial and hostname","discoveryId":"d-0003","notes":"orphan"}
    ]
    asset_headers = ["id","assetTag","serialNumber","type","manufacturer","model","hostname","macAddresses","ipAddresses","ownerId","ownerName","costCenter","location","purchaseDate","warrantyEnd","lifecycleState","metadata","createdAt","updatedAt"]
    disc_headers = ["id","discoverySource","rawPayload","serialNumber","hostname","macAddresses","ipAddresses","lastSeen","reconciliationStatus"]
    an_headers = ["id","type","description","discoveryId","notes"]
    write_csv(OUT_ASSETS, assets, asset_headers)
    write_csv(OUT_DISC, discoveries, disc_headers)
    write_csv(OUT_ANOM, anomalies, an_headers)
    print("Generated seed CSVs")
