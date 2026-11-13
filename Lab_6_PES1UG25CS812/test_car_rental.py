"""Unit tests targeting line and branch coverage of the rental module."""

import pytest

from car_rental_rate import check_fleet_telematics, process_rental_fleet


def test_single_economy_rental():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "economy",
        "driver_age": 30,
        "days": 2,
        "trip_segments": [100],
    }]
    assert process_rental_fleet(rentals, 10.0) == {
        "total_revenue": 110.0,
        "status": "STANDARD",
    }


@pytest.mark.parametrize(
    ("rentals", "fee"),
    [
        (None, 10.0),
        ([], -1.0),
    ],
)
def test_invalid_input_raises_value_error(rentals, fee):
    with pytest.raises(ValueError, match="Invalid rental list or admin fee"):
        process_rental_fleet(rentals, fee)


def test_unconfirmed_rental_is_skipped_and_returns_empty_batch():
    assert process_rental_fleet([{"is_confirmed": False}], 10.0) == {
        "total_revenue": 0.0,
        "status": "EMPTY_BATCH",
    }


def test_default_rental_fields_and_economy_pricing():
    assert process_rental_fleet([{"is_confirmed": True}], 5.0) == {
        "total_revenue": 45.0,
        "status": "STANDARD",
    }


def test_non_positive_days_are_flagged_and_skipped():
    assert process_rental_fleet(
        [{"is_confirmed": True, "days": 0}], 10.0
    ) == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


@pytest.mark.parametrize(
    ("vehicle_type", "expected_base"),
    [("luxury", 250.0), ("suv", 150.0), ("van", 90.0)],
)
def test_vehicle_rate_selection(vehicle_type, expected_base):
    rental = {
        "is_confirmed": True,
        "vehicle_type": vehicle_type,
        "driver_age": 30,
        "days": 2,
    }
    assert process_rental_fleet([rental], 10.0)["total_revenue"] == expected_base


def test_short_mileage_segment_and_young_driver_surcharge():
    rental = {
        "is_confirmed": True,
        "vehicle_type": "economy",
        "driver_age": 24,
        "days": 2,
        "trip_segments": [0, 100, 300],
    }
    # 80 base + (0 + 20 + 60) mileage + 40 young-driver surcharge.
    assert process_rental_fleet([rental], 0.0)["total_revenue"] == 200.0


def test_long_mileage_segment_for_adult_driver():
    rental = {
        "is_confirmed": True,
        "driver_age": 25,
        "days": 1,
        "trip_segments": [301],
    }
    assert process_rental_fleet([rental], 0.0)["total_revenue"] == 160.4


def test_underage_driver_long_trip_uses_fixed_risk_surcharge_and_breaks():
    rental = {
        "is_confirmed": True,
        "driver_age": 20,
        "days": 1,
        "trip_segments": [301, 50],
    }
    # The second segment is not processed after the underage long-trip break.
    assert process_rental_fleet([rental], 0.0)["total_revenue"] == 310.0


def test_underage_luxury_driver_uses_luxury_young_driver_surcharge():
    rental = {
        "is_confirmed": True,
        "vehicle_type": "luxury",
        "driver_age": 24,
        "days": 1,
        "trip_segments": [],
    }
    assert process_rental_fleet([rental], 0.0)["total_revenue"] == 170.0


def test_negative_mileage_is_flagged_but_processing_continues():
    rental = {
        "is_confirmed": True,
        "driver_age": 30,
        "days": 1,
        "trip_segments": [-5, 50],
    }
    assert process_rental_fleet([rental], 0.0) == {
        "total_revenue": 50.0,
        "status": "STANDARD",
    }


def test_more_than_four_risk_flags_triggers_audit():
    rentals = [
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
    ]
    assert process_rental_fleet(rentals, 0.0) == {
        "total_revenue": 0.0,
        "status": "HIGH_RISK_AUDIT",
    }


def test_exactly_four_risk_flags_do_not_trigger_audit():
    rentals = [{"is_confirmed": True, "days": 0} for _ in range(4)]
    assert process_rental_fleet(rentals, 0.0)["status"] == "EMPTY_BATCH"


def test_no_telematics_data():
    assert check_fleet_telematics([]) == "NO_DATA"
    assert check_fleet_telematics(None) == "NO_DATA"


def test_telematics_safe_for_single_speeding_reading():
    assert check_fleet_telematics([[110, 90, 120]]) == "SAFE"


def test_telematics_safe_when_speeding_streak_is_broken():
    assert check_fleet_telematics([[110, 101, 80, 120]]) == "SAFE"


def test_telematics_grounds_vehicle_after_two_consecutive_speeding_readings():
    assert check_fleet_telematics([[80, 101, 105, 70]]) == "GROUND_VEHICLE"


def test_telematics_checks_multiple_vehicles():
    assert check_fleet_telematics([[120, 80], [90, 101, 102]]) == "GROUND_VEHICLE"
