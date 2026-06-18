from fastapi import FastAPI, HTTPException, Body
import json, uuid, datetime
from .matcher import Matcher
from .audit import AuditStore
from .db import ASSETS, DISCOVERIES

app = FastAPI(title="Asset Control Engine API")

with open("api/config.json") as f:
    CONFIG = json.load(f)

matcher = Matcher(CONFIG)
audit = AuditStore("data/audit_store.jsonl")

@app.get("/api/health")
def health():
    return {"status": "ok", "version": CONFIG.get("version", "0.0.0")}

@app.post("/api/discovery", status_code=201)
def post_discovery(payload: dict = Body(...)):
    did = payload.get("id") or f"d-{uuid.uuid4()}"
    payload["id"] = did
    payload["reconciliationStatus"] = "unmatched"
    DISCOVERIES[did] = payload
    audit.append(actor="system", action="discovery.ingest", resourceId=did, payload=payload)
    return {"id": did}

@app.post("/api/reconciliation/suggest")
def suggest(discoveryId: str = Body(..., embed=True)):
    rec = DISCOVERIES.get(discoveryId)
    if not rec:
        raise HTTPException(status_code=404, detail="Discovery not found")
    suggestions = matcher.suggest(rec, list(ASSETS.values()))
    audit.append(actor="system", action="reconciliation.suggest", resourceId=discoveryId, payload={"suggestions": suggestions})
    return {"suggestions": suggestions}

@app.post("/api/discovery/reconcile")
def reconcile(discoveryId: str = Body(...), action: str = Body(...), assetId: str = Body(None), actor: str = Body("operator")):
    rec = DISCOVERIES.get(discoveryId)
    if not rec:
        raise HTTPException(status_code=404, detail="Discovery not found")
    if action == "link":
        if not assetId or assetId not in ASSETS:
            raise HTTPException(status_code=400, detail="assetId required")
        rec["reconciliationStatus"] = "matched"
        rec["linkedAssetId"] = assetId
        audit.append(actor=actor, action="reconciliation.link", resourceId=discoveryId, payload={"assetId": assetId})
        return {"success": True, "assetId": assetId}
    if action == "create":
        new_id = f"a-{uuid.uuid4()}"
        asset = {
            "id": new_id,
            "assetTag": f"AT-{str(uuid.uuid4())[:8]}",
            "serialNumber": rec.get("serialNumber"),
            "hostname": rec.get("hostname"),
            "macAddresses": rec.get("macAddresses"),
            "lifecycleState": "active",
            "createdAt": datetime.datetime.utcnow().isoformat() + "Z"
        }
        ASSETS[new_id] = asset
        rec["reconciliationStatus"] = "matched"
        rec["linkedAssetId"] = new_id
        audit.append(actor=actor, action="reconciliation.create", resourceId=discoveryId, payload={"assetId": new_id})
        return {"success": True, "assetId": new_id}
    if action == "ignore":
        rec["reconciliationStatus"] = "ignored"
        audit.append(actor=actor, action="reconciliation.ignore", resourceId=discoveryId, payload={})
        return {"success": True}
    raise HTTPException(status_code=400, detail="unknown action")
