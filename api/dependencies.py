from fastapi import Depends

def auth_dependency(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401)
    token = auth.split()[1]
    payload = verify_jwt(token)
    request.state.user = payload
    return payload

@app.post("/api/discovery/reconcile")
def reconcile(..., payload=Depends(auth_dependency)):
    # enforce scope
    require_scope(payload, "discovery:manage")
    # if endpoint is high-risk, require MFA header
    if endpoint_is_high_risk():
        mfa_token = request.headers.get("X-MFA-Token")
        if not mfa_token:
            raise HTTPException(status_code=403, detail="MFA required")
        validate_mfa(mfa_token, payload["sub"])
    # call OPA for policy decision
