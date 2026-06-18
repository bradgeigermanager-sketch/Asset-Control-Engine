package asset.authority

default allow_update = false

# Authority mapping: attribute -> allowed sources or roles
authority_map = {
  "serialNumber": ["ITAM"],
  "assetTag": ["ITAM"],
  "macAddresses": ["NetworkInventory"],
  "hostname": ["AD","MDM"],
  "owner": ["IdentityService","Asset-Admin"],
  "purchaseDate": ["Procurement"]
}

# Check if source is authorized for attribute
source_authorized(attr) {
  allowed := authority_map[attr]
  allowed[_] == input.source
}

# Check if role is authorized for attribute (fallback)
role_authorized(attr) {
  allowed := authority_map[attr]
  # treat role names as allowed entries too
  some i
  allowed[i] == input.token.roles[_]
}

allow_update {
  some attr
  attr == input.attribute
  (source_authorized(attr) or role_authorized(attr))
}
