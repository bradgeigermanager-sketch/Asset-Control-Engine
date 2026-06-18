# api/auth.py
from fastapi import Request, HTTPException
from jose import jwt, JWTError
import requests
import time

OIDC_CONFIG = {
  "issuer": "https://idp.example.com",
  "jwks_uri": "https://idp.example.com/.well-known/jwks.json",
  "audience": "asset-control-api"
}

JWKS = requests.get(OIDC_CONFIG["jwks_uri"]).json()

def verify_jwt(token: str):
    try:
        # Use jose or PyJWT with JWKS verification
        payload = jwt.decode(token, JWKS, algorithms=["RS256"], audience=OIDC_CONFIG["audience"])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_scope(payload, scope):
    scopes = payload.get("scope", "") or " ".join(payload.get("scp", []))
    if scope not in scopes.split():
        raise HTTPException(status_code=403, detail="Insufficient scope")

def validate_mfa(mfa_token: str, user_sub: str):
    # Option A: introspect MFA token at IdP
    resp = requests.post("https://idp.example.com/oauth2/introspect", data={"token": mfa_token})
    if resp.status_code != 200 or not resp.json().get("active"):
        raise HTTPException(status_code=403, detail="Invalid MFA token")
    # Ensure MFA token subject matches user
    if resp.json().get("sub") != user_sub:
        raise HTTPException(status_code=403, detail="MFA token mismatch")
