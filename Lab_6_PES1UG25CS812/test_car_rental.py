"""Basic functional test for the supplied car rental example."""

from car_rental_rate import process_rental_fleet


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
