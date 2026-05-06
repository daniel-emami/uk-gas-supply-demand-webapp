import { useEffect, useState } from "react";
import { fetchGasFlows } from "./Api/gasFlowApi";
import BalanceChart from "./Components/BalanceChart";
import ErrorState from "./Components/ErrorState";
import GasFlowsTable from "./Components/GasFlowsTable";
import LoadingState from "./Components/LoadingState";
import type { GasFlowsResponse } from "./Types/gasFlowTypes";

export default function App() {
  const [data, setData] = useState<GasFlowsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchGasFlows()
      .then((payload) => {
        setData(payload);
        setError(null);
      })
      .catch((unknownError: unknown) => {
        setError(unknownError instanceof Error ? unknownError.message : "Unknown error");
      })
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <main className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Gas Model UK</p>
          <h1>UK natural gas supply and demand dashboard</h1>
          <p className="hero-copy">
            Excel-backed FastAPI data served into a React + TypeScript dashboard shell.
          </p>
        </div>
      </header>

      {data?.is_demo_data && (
        <div className="demo-banner">Demo data is fake and for development only.</div>
      )}

      {isLoading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {data && !isLoading && !error && (
        <>
          <BalanceChart records={data.records} unit={data.unit} />
          <GasFlowsTable records={data.records} unit={data.unit} />
        </>
      )}
    </main>
  );
}
