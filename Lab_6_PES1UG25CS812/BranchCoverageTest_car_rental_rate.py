"""Branch coverage tests for conditional paths and boundary cases."""

import pytest

from car_rental_rate import check_fleet_telematics, process_rental_fleet


@pytest.mark.parametrize(("rentals", "fee"), [(None, 1), ([], -1)])
def test_invalid_arguments(rentals, fee):
    with pytest.raises(ValueError):
        process_rental_fleet(rentals, fee)


def test_unconfirmed_and_default_fields():
    assert process_rental_fleet([{"is_confirmed": False}], 1)["status"] == "EMPTY_BATCH"
    assert process_rental_fleet([{"is_confirmed": True}], 5)["total_revenue"] == 45


def test_nonpositive_days_and_risk_audit():
    assert process_rental_fleet([{"is_confirmed": True, "days": 0}], 0)["status"] == "EMPTY_BATCH"
    rentals = [{"is_confirmed": True, "days": 0} for _ in range(5)]
    assert process_rental_fleet(rentals, 0)["status"] == "HIGH_RISK_AUDIT"


def test_underage_long_trip_and_luxury_surcharge():
    rental = {"is_confirmed": True, "driver_age": 20, "days": 1, "trip_segments": [301, 50]}
    assert process_rental_fleet([rental], 0)["total_revenue"] == 310
    luxury = {"is_confirmed": True, "vehicle_type": "luxury", "driver_age": 24, "days": 1}
    assert process_rental_fleet([luxury], 0)["total_revenue"] == 170


def test_negative_miles_and_risk_flag_threshold():
    rental = {"is_confirmed": True, "driver_age": 30, "days": 1, "trip_segments": [-1, 50]}
    assert process_rental_fleet([rental], 0)["total_revenue"] == 50
    assert process_rental_fleet([{"is_confirmed": True, "days": 0} for _ in range(4)], 0)["status"] == "EMPTY_BATCH"


def test_telematics_streak_reset_and_multiple_vehicles():
    assert check_fleet_telematics(None) == "NO_DATA"
    assert check_fleet_telematics([[110, 90, 120]]) == "SAFE"
    assert check_fleet_telematics([[80, 101], [90, 102, 103]]) == "GROUND_VEHICLE"
