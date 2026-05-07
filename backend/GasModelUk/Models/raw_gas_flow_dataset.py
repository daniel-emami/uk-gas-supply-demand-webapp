from __future__ import annotations

from typing import TypeAlias

from GasModelUk.Models.raw_cross_border_gas_flow_dataset import RawCrossBorderGasFlowDataset
from GasModelUk.Models.raw_demand_gas_flow_dataset import RawDemandGasFlowDataset
from GasModelUk.Models.raw_lng_gas_flow_dataset import RawLngGasFlowDataset
from GasModelUk.Models.raw_production_gas_flow_dataset import RawProductionGasFlowDataset
from GasModelUk.Models.raw_storage_gas_flow_dataset import RawStorageGasFlowDataset

RawGasFlowDataset: TypeAlias = (
    RawDemandGasFlowDataset
    | RawStorageGasFlowDataset
    | RawLngGasFlowDataset
    | RawProductionGasFlowDataset
    | RawCrossBorderGasFlowDataset
)
