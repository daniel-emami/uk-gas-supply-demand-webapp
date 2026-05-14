import { useCallback, useEffect, useMemo, useState } from "react";
import { fetchGasFlows, runEtl } from "./Api/gasFlowApi";
import BalanceChart from "./Components/BalanceChart";
import DashboardControls from "./Components/DashboardControls";
import ErrorState from "./Components/ErrorState";
import FlowMatrix from "./Components/FlowMatrix";
import LoadingState from "./Components/LoadingState";
import SummaryStrip from "./Components/SummaryStrip";
import type { DateRangeFilters, GasFlowsResponse, RefreshScope } from "./Types/gasFlowTypes";

function getLoadedRange(payload: GasFlowsResponse): DateRangeFilters {
  const firstRecord = payload.records[0];
  const lastRecord = payload.records[payload.records.length - 1];
  return {
    startDate: firstRecord?.gas_day,
    endDate: lastRecord?.gas_day
  };
}

function formatRefreshTime(): string {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function App() {
  const [data, setData] = useState<GasFlowsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeRefresh, setActiveRefresh] = useState<RefreshScope | null>(null);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const filters = useMemo<DateRangeFilters>(
    () => ({
      startDate: startDate || undefined,
      endDate: endDate || undefined
    }),
    [endDate, startDate]
  );

  const loadStoredData = useCallback(
    async (requestedFilters: DateRangeFilters = filters, shouldSeedInputs = false) => {
      try {
        const payload = await fetchGasFlows(requestedFilters);
        setData(payload);
        setError(null);
        setLastUpdated(formatRefreshTime());

        if (shouldSeedInputs) {
          const loadedRange = getLoadedRange(payload);
          setStartDate(loadedRange.startDate ?? "");
          setEndDate(loadedRange.endDate ?? "");
        }
      } catch (unknownError: unknown) {
        setError(unknownError instanceof Error ? unknownError.message : "Unknown error");
      } finally {
        setIsInitialLoading(false);
      }
    },
    [filters]
  );

  useEffect(() => {
    void loadStoredData({}, true);
  }, []);

  const handleLoadRange = async () => {
    await loadStoredData(filters);
  };

  const handleRunEtl = async (scope: RefreshScope) => {
    if (!startDate || !endDate) {
      setError("Choose both a start date and an end date before running ETL.");
      return;
    }

    const requestedFilters = { startDate, endDate };
    setActiveRefresh(scope);
    try {
      await runEtl(scope, requestedFilters);
      await loadStoredData(requestedFilters);
    } catch (unknownError: unknown) {
      setError(unknownError instanceof Error ? unknownError.message : "Unknown error");
    } finally {
      setActiveRefresh(null);
    }
  };

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Gas Model UK</p>
          <h1>Supply and demand control room</h1>
          <p className="header-copy">
            Query stored gas-flow data by date range, or run ETL for a selected scope to update
            the workbook.
          </p>
        </div>
        {lastUpdated && <span className="last-updated">View loaded {lastUpdated}</span>}
      </header>

      <DashboardControls
        startDate={startDate}
        endDate={endDate}
        activeRefresh={activeRefresh}
        onStartDateChange={setStartDate}
        onEndDateChange={setEndDate}
        onApplyRange={() => void handleLoadRange()}
        onRefresh={(scope) => void handleRunEtl(scope)}
      />

      {isInitialLoading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {data && !isInitialLoading && (
        <>
          <SummaryStrip records={data.records} unit={data.unit} />
          <BalanceChart records={data.records} unit={data.unit} />
          <FlowMatrix records={data.records} unit={data.unit} />
        </>
      )}
    </main>
  );
}
