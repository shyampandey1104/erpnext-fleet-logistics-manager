"""Commercial Fleet & Fuel Logistics Management Engine for ERPNext."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class Vehicle(BaseModel):
    license_plate: str
    vehicle_type: str  # Truck, Van, Trailer, Car
    fuel_type: str  # Diesel, Petrol, Electric
    expected_mileage_kmpl: float
    current_odometer: float
    status: str = "Active"


class FuelLog(BaseModel):
    log_id: str
    license_plate: str
    odometer_reading: float
    liters_filled: float
    total_cost: float
    date: str


class FleetEngine:
    """Monitors fleet odometer progression, fuel efficiency, and anomaly detection."""

    def __init__(self):
        self.vehicles: Dict[str, Vehicle] = {}
        self.fuel_logs: Dict[str, List[FuelLog]] = {}

    def log_fuel_filling(self, log: FuelLog) -> Dict[str, Any]:
        if log.license_plate not in self.vehicles:
            raise ValueError(f"Vehicle {log.license_plate} not registered in fleet")

        veh = self.vehicles[log.license_plate]
        prev_odometer = veh.current_odometer
        distance_travelled = log.odometer_reading - prev_odometer

        if distance_travelled <= 0:
            raise ValueError("Odometer reading must be higher than vehicle's current odometer")

        actual_kmpl = distance_travelled / log.liters_filled
        veh.current_odometer = log.odometer_reading

        # Fuel Theft / Engine Health Anomaly Check
        expected = veh.expected_mileage_kmpl
        drop_pct = ((expected - actual_kmpl) / expected * 100.0) if expected > 0 else 0.0
        is_anomaly = drop_pct > 25.0  # More than 25% drop in mileage

        if log.license_plate not in self.fuel_logs:
            self.fuel_logs[log.license_plate] = []
        self.fuel_logs[log.license_plate].append(log)

        return {
            "vehicle": log.license_plate,
            "distance_travelled_km": distance_travelled,
            "liters_filled": log.liters_filled,
            "actual_mileage_kmpl": round(actual_kmpl, 2),
            "expected_mileage_kmpl": expected,
            "mileage_drop_percent": round(drop_pct, 1),
            "anomaly_detected": is_anomaly,
            "status": "Logged",
        }
