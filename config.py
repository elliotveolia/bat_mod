
SUPPLY_DELIVERY_RATE_PER_KWH = 0.055180


class BatteryConfig:
    # Nameplate battery power: 5 MW = 5,000 kW
    max_power_kw: float = 5000.0

    # Four-hour duration at the maximum discharge power.
    capacity_kwh: float = 20000.0
    duration_hours: float = 4.0

    # State of charge limits, expressed as fractions of capacity.
    min_soc_fraction: float = 0.10
    max_soc_fraction: float = 0.90
    initial_soc_fraction: float = 0.50

    # Round-trip efficiency.
    round_trip_efficiency: float = 0.90

    # This represents a constant 100 kW auxiliary load while operating.
    auxiliary_load_kw: float = 100.0

    # Placeholder only. Do not use until its meaning/unit is confirmed.
    annual_capacity_degradation_fraction: float = 0.10


class ProgramConfig:
    # Connected Solutions
    cs_payment_per_kw: float = 200.0
    cs_min_events: int = 30
    cs_max_events: int = 60

    # Clean Peak Energy Credits
    cpec_price: float = 64.0
    cpec_peak_multiplier: float = 4.0
    cpec_offpeak_multiplier: float = 1.0
    transmission_multiplier: float = 25.0

    # ISO-NE Forward Capacity Market
    fcm_payment_per_kw_month: float = 3.60

    # Service fees
    monthly_service_fee: float = 5_000.0
    iso_revenue_fee_fraction: float = 0.10
