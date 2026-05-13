import { flexRender, getCoreRowModel, useReactTable, type ColumnDef } from "@tanstack/react-table";
import { useMemo } from "react";
import type { GasFlowRecord, NullableNumber } from "../Types/gasFlowTypes";

interface GasFlowsTableProps {
  records: GasFlowRecord[];
  unit: string;
}

function formatNumber(value: NullableNumber): string {
  if (value === null || Number.isNaN(value)) {
    return "—";
  }
  return value.toFixed(1);
}

export default function GasFlowsTable({ records, unit }: GasFlowsTableProps) {
  const columns = useMemo<ColumnDef<GasFlowRecord>[]>(() => [
    {
      header: "Gas day",
      accessorKey: "gas_day",
      cell: (info) => String(info.getValue())
    },
    {
      header: "Demand",
      columns: [
        { header: "LDZ", accessorFn: (row) => row.demand.ldz, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
        { header: "Gas for Power", accessorFn: (row) => row.demand.gas_for_power, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
        { header: "Industry", accessorFn: (row) => row.demand.industry, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
        { header: "Total Demand", accessorFn: (row) => row.demand.total, cell: (info) => formatNumber(info.getValue() as NullableNumber) }
      ]
    },
    {
      header: "Supply",
      columns: [
        {
          header: "NCS",
          columns: [
            { header: "Easington Langeled", accessorFn: (row) => row.supply.ncs.easington_langeled, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "St Fergus NSMP", accessorFn: (row) => row.supply.ncs.st_fergus_nsmp, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "St Fergus Shell", accessorFn: (row) => row.supply.ncs.st_fergus_shell, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Total NCS", accessorFn: (row) => row.supply.ncs.total, cell: (info) => formatNumber(info.getValue() as NullableNumber) }
          ]
        },
        {
          header: "UKCS",
          columns: [
            { header: "Teesside", accessorFn: (row) => row.supply.ukcs.teesside, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Theddlethorpe", accessorFn: (row) => row.supply.ukcs.theddlethorpe, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "St Fergus Mobil", accessorFn: (row) => row.supply.ukcs.st_fergus_mobil, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Easington Dimlington", accessorFn: (row) => row.supply.ukcs.easington_dimlington, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Bacton Perenco", accessorFn: (row) => row.supply.ukcs.bacton_perenco, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Bacton SEAL", accessorFn: (row) => row.supply.ukcs.bacton_seal, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Bacton Shell", accessorFn: (row) => row.supply.ukcs.bacton_shell, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Total UKCS", accessorFn: (row) => row.supply.ukcs.total, cell: (info) => formatNumber(info.getValue() as NullableNumber) }
          ]
        },
        {
          header: "LNG",
          columns: [
            { header: "Dragon", accessorFn: (row) => row.supply.lng.dragon, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Isle of Grain", accessorFn: (row) => row.supply.lng.isle_of_grain, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "South Hook", accessorFn: (row) => row.supply.lng.south_hook, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Total LNG", accessorFn: (row) => row.supply.lng.total, cell: (info) => formatNumber(info.getValue() as NullableNumber) }
          ]
        },
        {
          header: "Cross Border Flows",
          columns: [
            { header: "Interconnector", accessorFn: (row) => row.supply.cross_border_flows.interconnector, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "BBL", accessorFn: (row) => row.supply.cross_border_flows.bbl, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Moffat", accessorFn: (row) => row.supply.cross_border_flows.moffat, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Total Cross Border", accessorFn: (row) => row.supply.cross_border_flows.total, cell: (info) => formatNumber(info.getValue() as NullableNumber) }
          ]
        },
        {
          header: "Storage",
          columns: [
            { header: "Aldbrough", accessorFn: (row) => row.supply.storage.aldbrough, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Hatfield Moor", accessorFn: (row) => row.supply.storage.hatfield_moor, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Hill Top Farm", accessorFn: (row) => row.supply.storage.hill_top_farm, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Hole House Farm", accessorFn: (row) => row.supply.storage.holehouse_farm, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Holford", accessorFn: (row) => row.supply.storage.holford, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Hornsea", accessorFn: (row) => row.supply.storage.hornsea, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Humbly Grove", accessorFn: (row) => row.supply.storage.humbly_grove, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Rough", accessorFn: (row) => row.supply.storage.rough, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Stublach", accessorFn: (row) => row.supply.storage.stublach, cell: (info) => formatNumber(info.getValue() as NullableNumber) },
            { header: "Total Storage", accessorFn: (row) => row.supply.storage.total, cell: (info) => formatNumber(info.getValue() as NullableNumber) }
          ]
        },
        { header: "Total Supply", accessorFn: (row) => row.supply.total, cell: (info) => formatNumber(info.getValue() as NullableNumber) }
      ]
    },
    {
      header: "Balance",
      accessorFn: (row) => row.balance,
      cell: (info) => formatNumber(info.getValue() as NullableNumber)
    }
  ], []);

  const table = useReactTable({
    data: records,
    columns,
    getCoreRowModel: getCoreRowModel()
  });

  return (
    <section className="card">
      <div className="section-heading">
        <h2>Daily gas flows</h2>
        <span>{unit}</span>
      </div>
      <div className="table-wrap">
        <table className="gas-table">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id} colSpan={header.colSpan}>
                    {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
