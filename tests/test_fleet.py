"""Unit tests for FleetEngine."""

from fleet.engine import FleetEngine, Vehicle, FuelLog


def test_fuel_mileage_normal_and_anomaly():
    engine = FleetEngine()
    vehicle = Vehicle(
        license_plate="MH-04-AB-1234",
        vehicle_type="Truck",
        fuel_type="Diesel",
        expected_mileage_kmpl=6.0,
        current_odometer=50000.0,
    )
    engine.vehicles[vehicle.license_plate] = vehicle

    # Test normal fuel filling (Travelled 300 km on 50 liters -> 6.0 Km/L)
    log1 = FuelLog(
        log_id="FL-01",
        license_plate="MH-04-AB-1234",
        odometer_reading=50300.0,
        liters_filled=50.0,
        total_cost=4500.0,
        date="2026-11-05",
    )
    res1 = engine.log_fuel_filling(log1)
    assert res1["actual_mileage_kmpl"] == 6.0
    assert res1["anomaly_detected"] is False

    # Test anomaly: Fuel theft / leakage (Travelled 150 km on 50 liters -> 3.0 Km/L -> 50% drop)
    log2 = FuelLog(
        log_id="FL-02",
        license_plate="MH-04-AB-1234",
        odometer_reading=50450.0,
        liters_filled=50.0,
        total_cost=4500.0,
        date="2026-11-10",
    )
    res2 = engine.log_fuel_filling(log2)
    assert res2["actual_mileage_kmpl"] == 3.0
    assert res2["anomaly_detected"] is True
