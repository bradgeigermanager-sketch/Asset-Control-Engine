import json, hashlib, time, os
from typing import Any

class AuditStore:
    def __init__(self, path: str = "data/audit_store.jsonl"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def append(self, actor: str, action: str, resourceId: str, payload: Any):
        entry = {
            "timestamp": time.time(),
            "actorId": actor,
            "actionType": action,
            "resourceId": resourceId,
            "payloadHash": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        }
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
