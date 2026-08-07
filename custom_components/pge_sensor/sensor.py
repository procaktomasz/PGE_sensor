"""Sensor platform for the PGE Sensor integration."""
                return summary.get("leftEnergyAmountSum")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        attrs = {}
        storage = self.coordinator.data.energy_storage
        if storage:
            zones = storage.get("zones", {})
            strefa_1 = zones.get("Strefa 1") or zones.get("Strefa 1 w sumie") or next(iter(zones.values()), {})
            summary = strefa_1.get("dataWarehouseSummary", {})
            
            if "settledEnergyAmountSumWithFactor" in summary:
                attrs["settled_energy_sum_with_factor"] = summary.get("settledEnergyAmountSumWithFactor")
            if "settledEnergyAmountSum" in summary:
                attrs["settled_energy_sum"] = summary.get("settledEnergyAmountSum")
            if "factor" in summary:
                attrs["factor"] = summary.get("factor")
                
            history = strefa_1.get("dataWarehousePpm")
            if history:
                attrs["history"] = history

        return attrs

    @property
    def available(self) -> bool:
        if not super().available:
            return False
        return self.coordinator.data.energy_storage is not None
