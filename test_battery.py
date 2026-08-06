import math
import unittest

from battery import Battery


class TestBattery(unittest.TestCase):
    def setUp(self):
        """Create a new independent battery before every test."""
        self.battery = Battery()
        self.charge_efficiency = math.sqrt(
            self.battery.config.round_trip_efficiency
        )
        self.discharge_efficiency = math.sqrt(
            self.battery.config.round_trip_efficiency
        )

    def test_initial_state(self):
        """Battery starts at the configured SOC."""
        expected_soc = (
            self.battery.config.initial_soc_fraction
            * self.battery.config.capacity_kwh
        )

        self.assertAlmostEqual(
            self.battery.soc_kwh,
            expected_soc,
            places=6,
        )
        self.assertGreaterEqual(
            self.battery.soc_kwh,
            self.battery.min_soc_kwh,
        )
        self.assertLessEqual(
            self.battery.soc_kwh,
            self.battery.max_soc_kwh,
        )

    def test_charge_power_limit(self):
        """Cannot charge above the maximum power in one hour."""
        self.battery.soc_kwh = self.battery.min_soc_kwh

        requested_charge_kwh = self.battery.max_power_kw * 2
        accepted_charge_kwh = self.battery.charge(
            requested_charge_kwh,
            interval_hours=1.0,
        )

        self.assertAlmostEqual(
            accepted_charge_kwh,
            self.battery.max_power_kw,
            places=6,
        )

    def test_discharge_power_limit(self):
        """Cannot discharge above the maximum power in one hour."""
        self.battery.soc_kwh = self.battery.max_soc_kwh

        requested_discharge_kwh = self.battery.max_power_kw * 2
        delivered_kwh = self.battery.discharge(
            requested_discharge_kwh,
            interval_hours=1.0,
        )

        self.assertAlmostEqual(
            delivered_kwh,
            self.battery.max_power_kw,
            places=6,
        )

    def test_charge_does_not_exceed_max_soc(self):
        """Battery cannot charge above configured maximum SOC."""
        self.battery.soc_kwh = self.battery.max_soc_kwh - 100

        accepted_charge_kwh = self.battery.charge(10_000)

        expected_grid_input = 100 / self.charge_efficiency

        self.assertAlmostEqual(
            accepted_charge_kwh,
            expected_grid_input,
            places=6,
        )
        self.assertAlmostEqual(
            self.battery.soc_kwh,
            self.battery.max_soc_kwh,
            places=6,
        )

    def test_discharge_does_not_go_below_min_soc(self):
        """Battery cannot discharge below configured minimum SOC."""
        self.battery.soc_kwh = self.battery.min_soc_kwh + 100

        delivered_kwh = self.battery.discharge(10_000)

        expected_delivered = 100 * self.discharge_efficiency

        self.assertAlmostEqual(
            delivered_kwh,
            expected_delivered,
            places=6,
        )
        self.assertAlmostEqual(
            self.battery.soc_kwh,
            self.battery.min_soc_kwh,
            places=6,
        )

    def test_no_charge_when_full(self):
        """A full battery must accept no further energy."""
        self.battery.soc_kwh = self.battery.max_soc_kwh

        self.assertEqual(
            self.battery.charge_available_for_input_kwh(),
            0.0,
        )
        self.assertEqual(self.battery.charge(1_000), 0.0)
        self.assertEqual(
            self.battery.soc_kwh,
            self.battery.max_soc_kwh,
        )

    def test_no_discharge_at_minimum_soc(self):
        """Battery at minimum SOC must deliver no energy."""
        self.battery.soc_kwh = self.battery.min_soc_kwh

        self.assertEqual(
            self.battery.discharge_available_for_output_kwh(),
            0.0,
        )
        self.assertEqual(self.battery.discharge(1_000), 0.0)
        self.assertEqual(
            self.battery.soc_kwh,
            self.battery.min_soc_kwh,
        )

    def test_round_trip_efficiency(self):
        """A charge followed by full discharge must equal configured RTE."""
        self.battery.soc_kwh = self.battery.min_soc_kwh

        grid_energy_charged_kwh = self.battery.charge(
            self.battery.max_power_kw,
            interval_hours=1.0,
        )

        delivered_energy_kwh = self.battery.discharge(
            self.battery.discharge_available_for_output_kwh(),
            interval_hours=1.0,
        )

        measured_rte = (
            delivered_energy_kwh / grid_energy_charged_kwh
        )

        self.assertAlmostEqual(
            measured_rte,
            self.battery.config.round_trip_efficiency,
            places=6,
        )
        self.assertAlmostEqual(
            self.battery.soc_kwh,
            self.battery.min_soc_kwh,
            places=6,
        )

    def test_half_hour_power_limit(self):
        """Power limit correctly scales with interval length."""
        self.battery.soc_kwh = self.battery.min_soc_kwh

        accepted_charge_kwh = self.battery.charge(
            10_000,
            interval_hours=0.5,
        )

        expected_charge_kwh = self.battery.max_power_kw * 0.5

        self.assertAlmostEqual(
            accepted_charge_kwh,
            expected_charge_kwh,
            places=6,
        )

    def test_negative_charge_raises_error(self):
        """Negative charging requests are invalid."""
        with self.assertRaises(ValueError):
            self.battery.charge(-1)

    def test_negative_discharge_raises_error(self):
        """Negative discharge requests are invalid."""
        with self.assertRaises(ValueError):
            self.battery.discharge(-1)

    def test_reset(self):
        """Reset returns the battery to initial configured SOC."""
        self.battery.charge(1_000)
        self.battery.reset()

        expected_soc = (
            self.battery.config.initial_soc_fraction
            * self.battery.config.capacity_kwh
        )

        self.assertAlmostEqual(
            self.battery.soc_kwh,
            expected_soc,
            places=6,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
