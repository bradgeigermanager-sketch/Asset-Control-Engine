package asset.mfa

default allow = false

high_risk_actions = {"create_asset_from_discovery", "approve_redeploy", "vendor_master_change"}

evidence_required = {
  "approve_redeploy": ["mfaEvidenceHash", "approvalSignature"],
  "create_asset_from_discovery": ["mfaEvidenceHash"]
}

# Check MFA presence and verification flag
mfa_valid {
  input.token.acr == "urn:mfa:required"
  input.mfa.verified == true
}

evidence_present(action) {
  required := evidence_required[action]
  required == [r | r := required[_]; input.audit[r] != null]
}

allow {
  action := input.action
  not (action in high_risk_actions)  # non high-risk allowed if other policies permit
}

allow {
  action := input.action
  action in high_risk_actions
  mfa_valid
  evidence_present(action)
}
