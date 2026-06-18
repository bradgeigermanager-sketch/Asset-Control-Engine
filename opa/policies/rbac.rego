package asset.rbac

default allow = false

# Map endpoints to required scopes and roles
endpoint_policy = {
  "/api/assets:get": {"scopes": ["assets:read"], "roles": []},
  "/api/assets:post": {"scopes": ["assets:write"], "roles": ["Asset-Admin"]},
  "/api/discovery/reconcile:post": {"scopes": ["discovery:manage"], "roles": []}
}

get_policy(endpoint) = p {
  p := endpoint_policy[endpoint]
}

has_all_scopes(required) {
  all_required := [s | s := required[_]]
  all_required == [s | s := required[_]; s == input.token.scopes[_]]
}

allow {
  p := get_policy(input.endpoint)
  # require at least one required scope present
  some s
  p.scopes[_] == s
  s == input.token.scopes[_]
  # if roles required, ensure token has one
  (count(p.roles) == 0) or (some r; r == input.token.roles[_]; r == p.roles[_])
}
