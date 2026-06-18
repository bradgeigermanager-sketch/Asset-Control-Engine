from pydantic import BaseModel
from typing import List, Optional, Dict

class UserRef(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None

class Asset(BaseModel):
    id: str
    assetTag: str
    serialNumber: Optional[str] = ""
    type: Optional[str] = ""
    hostname: Optional[str] = ""
    macAddresses: Optional[List[str]] = []
    ipAddresses: Optional[List[str]] = []
    owner: Optional[UserRef] = None
    lifecycleState: Optional[str] = "active"
    metadata: Optional[Dict] = {}
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

class DiscoveryRecord(BaseModel):
    id: str
    discoverySource: str
    rawPayload: dict
    serialNumber: Optional[str] = ""
    hostname: Optional[str] = ""
    macAddresses: Optional[List[str]] = []
    ipAddresses: Optional[List[str]] = []
    lastSeen: Optional[str] = None
    reconciliationStatus: Optional[str] = "unmatched"
