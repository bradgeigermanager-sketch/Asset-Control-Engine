package asset.reconcile

default allow = false

# Helper: check scope presence
has_scope(s) {
  s == input.token.scopes[_]
}

# Helper: check role presence
has_role(r) {
  r == input.token.roles[_]
}

# Deny if user is owner and trying to approve their own asset
deny_self_approval {
  input.action == "approve_redeploy"
  input.resource.owner_id == input.token.sub
}

# Require MFA for create from discovery or high risk actions
require_mfa {
  input.action == "create_asset_from_discovery"
  not input.token.acr == "urn:mfa:required"
}

# Deny if user lacks required scope
deny_no_scope {
  not has_scope("discovery:manage")
}

# Main allow rule
allow {
  not deny_no_scope
  not deny_self_approval
  not require_mfa
  # additional role checks for specific actions
  (input.action == "link" -> has_scope("discovery:manage"))
  (input.action == "create" -> has_role("Asset-Admin"))
  (input.action == "approve_redeploy" -> has_role("Compliance-Lead"))
}
package asset.reconcile

default allow = false

# Helper: check scope presence
has_scope(s) {
  s == input.token.scopes[_]
}

# Helper: check role presence
has_role(r) {
  r == input.token.roles[_]
}

# Deny if user is owner and trying to approve their own asset
deny_self_approval {
  input.action == "approve_redeploy"
  input.resource.owner_id == input.token.sub
}

# Require MFA for create from discovery or high risk actions
require_mfa {
  input.action == "create_asset_from_discovery"
  not input.token.acr == "urn:mfa:required"
}

# Deny if user lacks required scope
deny_no_scope {
  not has_scope("discovery:manage")
}

# Main allow rule
allow {
  not deny_no_scope
  not deny_self_approval
  not require_mfa
  # additional role checks for specific actions
  (input.action == "link" -> has_scope("discovery:manage"))
  (input.action == "create" -> has_role("Asset-Admin"))
  (input.action == "approve_redeploy" -> has_role("Compliance-Lead"))
}
