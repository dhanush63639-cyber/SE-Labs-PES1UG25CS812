"""Statement/line coverage tests for the car rental module."""

from car_rental_rate import check_fleet_telematics, process_rental_fleet


def test_economy_suv_and_luxury_rates():
    assert process_rental_fleet([{"is_confirmed": True, "vehicle_type": "economy", "driver_age": 30, "days": 1}], 0)["total_revenue"] == 40
    assert process_rental_fleet([{"is_confirmed": True, "vehicle_type": "suv", "driver_age": 30, "days": 1}], 0)["total_revenue"] == 70
    assert process_rental_fleet([{"is_confirmed": True, "vehicle_type": "luxury", "driver_age": 30, "days": 1}], 0)["total_revenue"] == 120


def test_mileage_calculation_and_age_surcharge():
    rental = {"is_confirmed": True, "vehicle_type": "economy", "driver_age": 24, "days": 2, "trip_segments": [100, 300]}
    assert process_rental_fleet([rental], 0)["total_revenue"] == 200


def test_adult_long_trip():
    rental = {"is_confirmed": True, "driver_age": 30, "days": 1, "trip_segments": [301]}
    assert process_rental_fleet([rental], 0)["total_revenue"] == 160.4


def test_telematics_no_data_safe_and_grounded():
    assert check_fleet_telematics([]) == "NO_DATA"
    assert check_fleet_telematics([[110]]) == "SAFE"
    assert check_fleet_telematics([[101, 102]]) == "GROUND_VEHICLE"
