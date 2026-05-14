import type { GasFlowRecord, NullableNumber } from "../Types/gasFlowTypes";

interface FlowMatrixProps {
  records: GasFlowRecord[];
  unit: string;
}

interface FlowRow {
  id: string;
  section: string;
  label: string;
  emphasis?: "total" | "balance";
  getValue: (record: GasFlowRecord) => NullableNumber;
}

function formatNumber(value: NullableNumber): string {
  if (value === null || Number.isNaN(value)) {
    return "—";
  }
  return value.toFixed(1);
}

const flowRows: FlowRow[] = [
  {
    id: "balance",
    section: "System",
    label: "Balance",
    emphasis: "balance",
    getValue: (record) => record.balance
  },
  {
    id: "supply_total",
    section: "System",
    label: "Supply total",
    emphasis: "total",
    getValue: (record) => record.supply.total
  },
  {
    id: "demand_total",
    section: "System",
    label: "Demand total",
    emphasis: "total",
    getValue: (record) => record.demand.total
  },
  { id: "ldz", section: "Demand", label: "LDZ", getValue: (record) => record.demand.ldz },
  {
    id: "gas_for_power",
    section: "Demand",
    label: "Gas for Power",
    getValue: (record) => record.demand.gas_for_power
  },
  {
    id: "industry",
    section: "Demand",
    label: "Industry",
    getValue: (record) => record.demand.industry
  },
  {
    id: "ncs_total",
    section: "NCS",
    label: "NCS total",
    emphasis: "total",
    getValue: (record) => record.supply.ncs.total
  },
  {
    id: "easington_langeled",
    section: "NCS",
    label: "Easington Langeled",
    getValue: (record) => record.supply.ncs.easington_langeled
  },
  {
    id: "st_fergus_nsmp",
    section: "NCS",
    label: "St Fergus NSMP",
    getValue: (record) => record.supply.ncs.st_fergus_nsmp
  },
  {
    id: "st_fergus_shell_ncs",
    section: "NCS",
    label: "St Fergus Shell",
    getValue: (record) => record.supply.ncs.st_fergus_shell
  },
  {
    id: "ukcs_total",
    section: "UKCS",
    label: "UKCS total",
    emphasis: "total",
    getValue: (record) => record.supply.ukcs.total
  },
  {
    id: "teesside",
    section: "UKCS",
    label: "Teesside",
    getValue: (record) => record.supply.ukcs.teesside
  },
  {
    id: "theddlethorpe",
    section: "UKCS",
    label: "Theddlethorpe",
    getValue: (record) => record.supply.ukcs.theddlethorpe
  },
  {
    id: "st_fergus_mobil",
    section: "UKCS",
    label: "St Fergus Mobil",
    getValue: (record) => record.supply.ukcs.st_fergus_mobil
  },
  {
    id: "easington_dimlington",
    section: "UKCS",
    label: "Easington Dimlington",
    getValue: (record) => record.supply.ukcs.easington_dimlington
  },
  {
    id: "bacton_perenco",
    section: "UKCS",
    label: "Bacton Perenco",
    getValue: (record) => record.supply.ukcs.bacton_perenco
  },
  {
    id: "bacton_seal",
    section: "UKCS",
    label: "Bacton SEAL",
    getValue: (record) => record.supply.ukcs.bacton_seal
  },
  {
    id: "bacton_shell",
    section: "UKCS",
    label: "Bacton Shell",
    getValue: (record) => record.supply.ukcs.bacton_shell
  },
  {
    id: "lng_total",
    section: "LNG",
    label: "LNG total",
    emphasis: "total",
    getValue: (record) => record.supply.lng.total
  },
  { id: "dragon", section: "LNG", label: "Dragon", getValue: (record) => record.supply.lng.dragon },
  {
    id: "isle_of_grain",
    section: "LNG",
    label: "Isle of Grain",
    getValue: (record) => record.supply.lng.isle_of_grain
  },
  {
    id: "south_hook",
    section: "LNG",
    label: "South Hook",
    getValue: (record) => record.supply.lng.south_hook
  },
  {
    id: "cross_border_total",
    section: "Cross-border",
    label: "Cross-border total",
    emphasis: "total",
    getValue: (record) => record.supply.cross_border_flows.total
  },
  {
    id: "interconnector",
    section: "Cross-border",
    label: "Interconnector",
    getValue: (record) => record.supply.cross_border_flows.interconnector
  },
  {
    id: "bbl",
    section: "Cross-border",
    label: "BBL",
    getValue: (record) => record.supply.cross_border_flows.bbl
  },
  {
    id: "moffat",
    section: "Cross-border",
    label: "Moffat",
    getValue: (record) => record.supply.cross_border_flows.moffat
  },
  {
    id: "storage_total",
    section: "Storage",
    label: "Storage total",
    emphasis: "total",
    getValue: (record) => record.supply.storage.total
  },
  {
    id: "aldbrough",
    section: "Storage",
    label: "Aldbrough",
    getValue: (record) => record.supply.storage.aldbrough
  },
  {
    id: "avonmouth",
    section: "Storage",
    label: "Avonmouth",
    getValue: (record) => record.supply.storage.avonmouth
  },
  {
    id: "hatfield_moor",
    section: "Storage",
    label: "Hatfield Moor",
    getValue: (record) => record.supply.storage.hatfield_moor
  },
  {
    id: "hill_top_farm",
    section: "Storage",
    label: "Hill Top Farm",
    getValue: (record) => record.supply.storage.hill_top_farm
  },
  {
    id: "holehouse_farm",
    section: "Storage",
    label: "Hole House Farm",
    getValue: (record) => record.supply.storage.holehouse_farm
  },
  {
    id: "holford",
    section: "Storage",
    label: "Holford",
    getValue: (record) => record.supply.storage.holford
  },
  {
    id: "hornsea",
    section: "Storage",
    label: "Hornsea",
    getValue: (record) => record.supply.storage.hornsea
  },
  {
    id: "humbly_grove",
    section: "Storage",
    label: "Humbly Grove",
    getValue: (record) => record.supply.storage.humbly_grove
  },
  { id: "rough", section: "Storage", label: "Rough", getValue: (record) => record.supply.storage.rough },
  {
    id: "stublach",
    section: "Storage",
    label: "Stublach",
    getValue: (record) => record.supply.storage.stublach
  }
];

export default function FlowMatrix({ records, unit }: FlowMatrixProps) {
  return (
    <section className="panel flow-panel">
      <div className="section-heading">
        <div>
          <h2>Flow matrix</h2>
          <p>Rows are assets or totals; columns are gas days.</p>
        </div>
        <span>{unit}</span>
      </div>

      <div className="matrix-wrap">
        <table className="flow-matrix">
          <thead>
            <tr>
              <th scope="col">Section</th>
              <th scope="col">Flow</th>
              {records.map((record) => (
                <th scope="col" key={record.gas_day}>
                  {record.gas_day.slice(5)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {flowRows.map((row) => (
              <tr className={row.emphasis ? `is-${row.emphasis}` : undefined} key={row.id}>
                <th scope="row" className="section-cell">
                  {row.section}
                </th>
                <th scope="row" className="flow-cell">
                  {row.label}
                </th>
                {records.map((record) => (
                  <td key={`${row.id}-${record.gas_day}`}>{formatNumber(row.getValue(record))}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
