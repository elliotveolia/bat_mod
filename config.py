
SUPPLY_DELIVERY_RATE_PER_KWH = 0.055180

class BatteryConfig:
    # Physical Properties
    capacity_mw: float = 5
    cycle_time_hr: int = 4
    min_soc: float = 0.1
    rte: float = 0.9
    aux_load_kwhr: float = 100
    degrade: float = 0.1

class ProgamConfig:
    # Program Payouts
    cs_payment_per_kw: float = 200
    cs_min_events: int = 30
    cs_max_events: int = 60
    cpec_price: float = 64.0
    cpec_peak_multiplier: float = 4.0
    cpec_offpeak_multiplier: float = 1.0
    transmission_multiplier: float = 25.0
    fcm_payment_per_kw_month: float = 3.60
    monthly_service_fee: float = 5000.0
    iso_revenue_fee_fraction: float = 0.10