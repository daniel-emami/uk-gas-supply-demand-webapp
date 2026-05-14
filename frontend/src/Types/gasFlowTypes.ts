export type NullableNumber = number | null;

export interface DemandRecord {
  ldz: NullableNumber;
  gas_for_power: NullableNumber;
  industry: NullableNumber;
  total: NullableNumber;
}

export interface StorageRecord {
  aldbrough: NullableNumber;
  avonmouth: NullableNumber;
  hatfield_moor: NullableNumber;
  hill_top_farm: NullableNumber;
  holehouse_farm: NullableNumber;
  holford: NullableNumber;
  hornsea: NullableNumber;
  humbly_grove: NullableNumber;
  rough: NullableNumber;
  stublach: NullableNumber;
  total: NullableNumber;
}

export interface LngRecord {
  dragon: NullableNumber;
  isle_of_grain: NullableNumber;
  south_hook: NullableNumber;
  total: NullableNumber;
}

export interface NcsRecord {
  easington_langeled: NullableNumber;
  st_fergus_nsmp: NullableNumber;
  st_fergus_shell: NullableNumber;
  total: NullableNumber;
}

export interface UkcsRecord {
  teesside: NullableNumber;
  theddlethorpe: NullableNumber;
  st_fergus_mobil: NullableNumber;
  easington_dimlington: NullableNumber;
  bacton_perenco: NullableNumber;
  bacton_seal: NullableNumber;
  bacton_shell: NullableNumber;
  total: NullableNumber;
}

export interface CrossBorderFlowsRecord {
  interconnector: NullableNumber;
  bbl: NullableNumber;
  moffat: NullableNumber;
  total: NullableNumber;
}

export interface SupplyRecord {
  ncs: NcsRecord;
  ukcs: UkcsRecord;
  lng: LngRecord;
  cross_border_flows: CrossBorderFlowsRecord;
  storage: StorageRecord;
  total: NullableNumber;
}

export interface GasFlowRecord {
  gas_day: string;
  demand: DemandRecord;
  supply: SupplyRecord;
  balance: NullableNumber;
}

export interface GasFlowsResponse {
  unit: string;
  records: GasFlowRecord[];
}

export type RefreshScope =
  | "all"
  | "supply"
  | "demand"
  | "production"
  | "lng"
  | "storage"
  | "cross_border_flows";

export interface DateRangeFilters {
  startDate?: string;
  endDate?: string;
}

export interface SectionRecordMap {
  demand: DemandRecord;
  production: {
    ncs: NcsRecord;
    ukcs: UkcsRecord;
    total: NullableNumber;
  };
  lng: LngRecord;
  storage: StorageRecord;
  cross_border_flows: CrossBorderFlowsRecord;
}

export type SectionResponse<TScope extends Exclude<RefreshScope, "all" | "supply">> = {
  unit: string;
  section: TScope;
  records: Array<{ gas_day: string } & Pick<SectionRecordMap, TScope>>;
};
