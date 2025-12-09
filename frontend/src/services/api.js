// frontend/src/services/api.js
// Simple, robust API client for TruEstate frontend.
// Uses VITE_API_BASE_URL env var (default falls back to empty string).

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

function buildUrl(path, params = {}) {
  const base = API_BASE || "";
  const url = new URL(base + path, window.location.origin);
  Object.entries(params).forEach(([k, v]) => {
    if (v === undefined || v === null) return;
    if (Array.isArray(v)) {
      v.forEach(val => url.searchParams.append(k, val));
    } else {
      url.searchParams.set(k, String(v));
    }
  });
  return url.toString();
}

export async function fetchSales({ page = 1, limit = 50, search = "", sort_field = "date", sort_order = "desc", filters = {} } = {}) {
  // filters expected as object: { region: ["North","South"], category: ["Clothing"] } -> we append as repeated params
  const params = { page, limit, sort_field, sort_order };
  if (search) params.search = search;

  // Flatten multi-select filters into URL params (e.g., tags=tag1&tags=tag2)
  // We prefix filter keys with "filter_" to keep them distinct on backend (or match your backend expected names)
  Object.entries(filters || {}).forEach(([k, v]) => {
    if (!v) return;
    params[k] = v;
  });

  const url = buildUrl("/api/sales/", params);
  const res = await fetch(url, { method: "GET", credentials: "same-origin" });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`fetchSales failed: ${res.status} ${text}`);
  }
  return await res.json();
}

export default { fetchSales };
