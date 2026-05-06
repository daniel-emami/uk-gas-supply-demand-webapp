from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from GasModelUk.Models.cross_border_gas_flow_record import CrossBorderGasFlowRecord
from GasModelUk.Models.demand_gas_flow_record import DemandGasFlowRecord
from GasModelUk.Models.lng_gas_flow_record import LngGasFlowRecord
from GasModelUk.Models.ncs_gas_flow_record import NcsGasFlowRecord
from GasModelUk.Models.storage_gas_flow_record import StorageGasFlowRecord
from GasModelUk.Models.ukcs_gas_flow_record import UkcsGasFlowRecord
from GasModelUk.Utilities.date_utils import format_gas_day
from GasModelUk.Utilities.number_utils import sum_optional_values


@dataclass(frozen=True)
class DailyGasFlowRecord:
    """Frontend-ready daily gas flow record with calculated totals and balance."""

    gas_day: date
    demand: DemandGasFlowRecord
    ncs: NcsGasFlowRecord
    ukcs: UkcsGasFlowRecord
    lng: LngGasFlowRecord
    cross_border_flows: CrossBorderGasFlowRecord
    storage: StorageGasFlowRecord

    @property
    def supply_total(self) -> float | None:
        """Return total supply excluding demand."""

        return sum_optional_values(
            [
                self.ncs.total,
                self.ukcs.total,
                self.lng.total,
                self.cross_border_flows.total,
                self.storage.total,
            ]
        )

    @property
    def balance(self) -> float | None:
        """Return net balance as supply plus signed demand.

        Demand values are stored as negative numbers, so the balance is:

            supply_total + demand_total
        """

        if self.supply_total is None or self.demand.total is None:
            return None
        return round(self.supply_total + self.demand.total, 3)

    def to_payload(self) -> dict[str, object]:
        """Return the nested API response payload for this gas day."""

        return {
            "gas_day": format_gas_day(self.gas_day),
            "demand": self.demand.to_payload(),
            "supply": {
                "ncs": self.ncs.to_payload(),
                "ukcs": self.ukcs.to_payload(),
                "lng": self.lng.to_payload(),
                "cross_border_flows": self.cross_border_flows.to_payload(),
                "storage": self.storage.to_payload(),
                "total": self.supply_total,
            },
            "balance": self.balance,
        }
