import type { RefreshScope } from "../Types/gasFlowTypes";

interface DashboardControlsProps {
  startDate: string;
  endDate: string;
  activeRefresh: RefreshScope | null;
  onStartDateChange: (value: string) => void;
  onEndDateChange: (value: string) => void;
  onApplyRange: () => void;
  onRefresh: (scope: RefreshScope) => void;
}

const refreshOptions: Array<{ scope: RefreshScope; label: string }> = [
  { scope: "all", label: "All" },
  { scope: "supply", label: "Supply" },
  { scope: "demand", label: "Demand" },
  { scope: "production", label: "Production" },
  { scope: "lng", label: "LNG" },
  { scope: "storage", label: "Storage" },
  { scope: "cross_border_flows", label: "Cross-border" }
];

export default function DashboardControls({
  startDate,
  endDate,
  activeRefresh,
  onStartDateChange,
  onEndDateChange,
  onApplyRange,
  onRefresh
}: DashboardControlsProps) {
  return (
    <section className="control-panel" aria-label="Dashboard controls">
      <div className="date-controls">
        <label>
          <span>Start</span>
          <input
            type="date"
            value={startDate}
            onChange={(event) => onStartDateChange(event.target.value)}
          />
        </label>
        <label>
          <span>End</span>
          <input
            type="date"
            value={endDate}
            onChange={(event) => onEndDateChange(event.target.value)}
          />
        </label>
        <button
          className="primary-button"
          type="button"
          onClick={onApplyRange}
          disabled={activeRefresh !== null}
        >
          Query stored range
        </button>
      </div>

      <div className="refresh-controls" aria-label="Run ETL">
        {refreshOptions.map((option) => (
          <button
            key={option.scope}
            type="button"
            onClick={() => onRefresh(option.scope)}
            disabled={activeRefresh !== null}
          >
            {activeRefresh === option.scope ? "Running..." : `Run ${option.label}`}
          </button>
        ))}
      </div>
    </section>
  );
}
