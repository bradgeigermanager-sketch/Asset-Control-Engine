import os, requests, csv, json, time
API_BASE = os.getenv("API_BASE", "http://localhost:8000")
TOKEN = os.getenv("API_TOKEN", "testtoken")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def test_seed_and_reconcile():
    assets = load_csv("data/assets_seed.csv")
    discoveries = load_csv("data/discoveries_seed.csv")
    # seed assets via direct API create (if implemented) or via in-memory injection
    for a in assets[:50]:
        payload = {
            "id": a["id"],
            "assetTag": a["assetTag"],
            "serialNumber": a["serialNumber"],
            "type": a["type"],
            "hostname": a["hostname"],
            "macAddresses": [a["macAddresses"]],
            "ipAddresses": [a["ipAddresses"]],
            "owner": {"id": a["ownerId"], "name": a["ownerName"]},
            "lifecycleState": a["lifecycleState"]
        }
        r = requests.post(f"{API_BASE}/api/discovery", json={"id": f"seed-{a['id']}", "discoverySource":"manual", "rawPayload":{}, "serialNumber": a["serialNumber"], "hostname": a["hostname"], "macAddresses":[a["macAddresses"]], "ipAddresses":[a["ipAddresses"]], "lastSeen": a.get("createdAt")})
        assert r.status_code == 201
    # basic health check
    h = requests.get(f"{API_BASE}/api/health")
    assert h.status_code == 200
