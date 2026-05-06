import type { GasFlowsResponse } from "../Types/gasFlowTypes";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "";

export async function fetchGasFlows(): Promise<GasFlowsResponse> {
  const response = await fetch(`${apiBaseUrl}/api/gas-flows`);
  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }
  return response.json() as Promise<GasFlowsResponse>;
}
