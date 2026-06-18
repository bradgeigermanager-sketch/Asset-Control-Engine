# opa/policies/reconciliation.rego
package asset.reconcile

default allow = false

# deny if user lacks required scope
has_scope(sc) {
  sc == input.token.scopes[_]
}

# separation of duties: cannot approve own asset
deny_approve_if_owner {
  input.action == "approve_redeploy"
  input.resource.owner_id == input.token.sub
}

# require MFA for create from discovery
require_mfa {
  input.action == "create_asset_from_discovery"
  input.token.acr != "urn:mfa:required"
}

allow {
  has_scope("discovery:manage")
  not deny_approve_if_owner
  not require_mfa
}
