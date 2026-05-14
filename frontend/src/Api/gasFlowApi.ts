import type {
  DateRangeFilters,
  GasFlowsResponse,
  RefreshScope
} from "../Types/gasFlowTypes";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "";

function buildUrl(
  path: string,
  filters: DateRangeFilters = {},
  extraParams: Record<string, string> = {}
): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(extraParams)) {
    params.set(key, value);
  }
  if (filters.startDate) {
    params.set("start_date", filters.startDate);
  }
  if (filters.endDate) {
    params.set("end_date", filters.endDate);
  }
  const query = params.toString();
  return `${apiBaseUrl}${path}${query ? `?${query}` : ""}`;
}

async function fetchJson<TPayload>(url: string, init?: RequestInit): Promise<TPayload> {
  const response = await fetch(url, init);
  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }
  return response.json() as Promise<TPayload>;
}

export async function fetchGasFlows(
  filters: DateRangeFilters = {}
): Promise<GasFlowsResponse> {
  return fetchJson<GasFlowsResponse>(buildUrl("/api/gas-flows", filters));
}

export async function runEtl(
  scope: RefreshScope,
  filters: Required<DateRangeFilters>
): Promise<void> {
  await fetchJson(buildUrl("/api/etl/run", filters, { scope }), { method: "POST" });
}
