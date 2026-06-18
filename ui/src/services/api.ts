const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export async function fetchAssets(q?: string) {
  const url = new URL(`${API_BASE}/api/assets`);
  if (q) url.searchParams.set("q", q);
  const r = await fetch(url.toString(), { headers: { "Content-Type": "application/json" }});
  return r.json();
}

export async function postDiscovery(d: any) {
  const r = await fetch(`${API_BASE}/api/discovery`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(d)
  });
  return r.json();
}

export async function suggest(discoveryId: string) {
  const r = await fetch(`${API_BASE}/api/reconciliation/suggest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ discoveryId })
  });
  return r.json();
}
