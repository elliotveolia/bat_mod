import math

from config import BatteryConfig

class Battery:
    "One hour step model of the battery"

    def __init__(self, config = BatteryConfig):
        self.config = config

        self.capacity_kwh = config.capacity_kwh
        self.max_power_kw = config.max_power_kw
        self.min_soc_kwh = (config.min_soc_fraction * config.capacity_kwh)
        self.max_soc_kwh = (config.max_soc_fraction * config.capacity_kwh)
        self.soc_kwh = (config.initial_soc_fraction * config.capacity_kwh)

        # Round trip efficiency is split between charging and discharging to give the overall efficiency
        self.charge_efficiency = math.sqrt(config.round_trip_efficiency)
        self.discharge_efficiency = math.sqrt(config.round_trip_efficiency)

    def charge_available_for_input_kwh(self, interval_hours = 1.0):
        "The maximum energy that can be taken from the grid for charging"

        power_limited_input = self.max_power_kw * interval_hours
        storage_limited_input = ((self.max_soc_kwh - self.soc_kwh) / self.charge_efficiency)

        return max(0.0, min(power_limited_input, storage_limited_input),)

    def discharge_available_for_output_kwh(self, interval_hours = 1.0):
        "The maximum energy that the battery can deliver to the grid"

        power_limited_output = self.max_power_kw * interval_hours
        energy_limited_output = ((self.soc_kwh - self.min_soc_kwh) * self.discharge_efficiency)

        return max(0.0, min(power_limited_output, energy_limited_output),)

    def charge(self, grid_energy_kwh, interval_hours = 1.0):
        "Charge the battery from the grid, returns the accepted grid energy"

        if grid_energy_kwh < 0:
            raise ValueError("Error: Energy charged cannot be negative")

        accepted_kwh = min(grid_energy_kwh, self.charge_available_for_input_kwh(interval_hours),)
        self.soc_kwh = self.soc_kwh + accepted_kwh * self.charge_efficiency

        return accepted_kwh

    def discharge(self, requested_output_kwh, interval_hours = 1.0):
        "Discharge the battery to the grid, returns the delivered outputted energy"

        if requested_output_kwh < 0:
            raise ValueError("Error: Energy discharged cannot be negative")

        delivered_kwh = min(requested_output_kwh, self.discharge_available_for_output_kwh(interval_hours),)
        self.soc_kwh = self.soc_kwh - (delivered_kwh / self.discharge_efficiency)
        return delivered_kwh

    def reset(self):
        "Reset the battery to the initial state"

        self.soc_kwh = (self.config.initial_soc_fraction * self.capacity_kwh)

    def status(self):
        "Return the status of the battery"

        return {
            "soc_kwh": round(self.soc_kwh, 2),
            "soc_percent": round(
                self.soc_kwh / self.capacity_kwh * 100,
                2,
            ),
            "min_soc_kwh": round(self.min_soc_kwh, 2),
            "max_soc_kwh": round(self.max_soc_kwh, 2),
            "available_charge_input_kwh": round(
                self.charge_available_for_input_kwh(),
                2,
            ),
            "available_discharge_output_kwh": round(
                self.discharge_available_for_output_kwh(),
                2,
            ),
        }

