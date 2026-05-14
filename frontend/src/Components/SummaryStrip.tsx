import type { GasFlowRecord, NullableNumber } from "../Types/gasFlowTypes";

interface SummaryStripProps {
  records: GasFlowRecord[];
  unit: string;
}

function formatNumber(value: NullableNumber): string {
  if (value === null || Number.isNaN(value)) {
    return "—";
  }
  return value.toFixed(1);
}

function formatTrend(current: NullableNumber, previous: NullableNumber): string {
  if (current === null || previous === null) {
    return "No comparison";
  }
  const delta = current - previous;
  if (delta === 0) {
    return "Flat vs previous gas day";
  }
  return `${delta > 0 ? "+" : ""}${delta.toFixed(1)} vs previous gas day`;
}

export default function SummaryStrip({ records, unit }: SummaryStripProps) {
  const latest = records[records.length - 1];
  const previous = records[records.length - 2];

  if (!latest) {
    return null;
  }

  const cards = [
    {
      label: "Balance",
      value: latest.balance,
      trend: formatTrend(latest.balance, previous?.balance ?? null),
      tone:
        latest.balance === null
          ? "neutral"
          : latest.balance >= 0
            ? "positive"
            : "negative"
    },
    {
      label: "Supply",
      value: latest.supply.total,
      trend: formatTrend(latest.supply.total, previous?.supply.total ?? null),
      tone: "positive"
    },
    {
      label: "Demand",
      value: latest.demand.total,
      trend: formatTrend(latest.demand.total, previous?.demand.total ?? null),
      tone: "negative"
    },
    {
      label: "Gas day",
      value: null,
      displayValue: latest.gas_day,
      trend: `${records.length} record${records.length === 1 ? "" : "s"} loaded`,
      tone: "neutral"
    }
  ] as const;

  return (
    <section className="summary-strip" aria-label="Latest gas day summary">
      {cards.map((card) => (
        <article className={`summary-tile ${card.tone}`} key={card.label}>
          <span>{card.label}</span>
          <strong>
            {"displayValue" in card ? card.displayValue : `${formatNumber(card.value)} ${unit}`}
          </strong>
          <small>{card.trend}</small>
        </article>
      ))}
    </section>
  );
}
