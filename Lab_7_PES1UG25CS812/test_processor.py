"""Hypothesis fuzz tests for the Lab 7 Car Rental Rate processors."""

import pytest
from hypothesis import given, settings, strategies as st

from processor import (
    format_rental_invoice,
    parse_trip_mileage,
    sanitize_license_plate,
)


# Keep examples deterministic in CI while still exploring a broad input space.
FUZZ_SETTINGS = settings(max_examples=200, deadline=None)


@FUZZ_SETTINGS
@given(st.one_of(st.text(), st.none()))
def test_sanitize_license_plate_no_crash(value):
    """String inputs should normalize; unsupported types should fail cleanly."""
    if value is None:
        with pytest.raises(AttributeError):
            sanitize_license_plate(value)
        return

    result = sanitize_license_plate(value)
    assert isinstance(result, str)
    assert result == result.upper()
    assert all(separator not in result for separator in ("-", " ", "_", "#"))


@FUZZ_SETTINGS
@given(st.one_of(st.text(), st.none()))
def test_parse_trip_mileage_safe(value):
    """Valid CSV numbers parse; malformed values raise a documented error."""
    if value is None:
        with pytest.raises(AttributeError):
            parse_trip_mileage(value)
        return

    try:
        result = parse_trip_mileage(value)
    except ValueError:
        # Empty fields and non-numeric tokens are invalid float values.
        return

    assert isinstance(result, list)
    assert all(isinstance(mileage, float) for mileage in result)


@FUZZ_SETTINGS
@given(st.one_of(st.text(), st.none()))
def test_format_rental_invoice_safe(value):
    """Valid rental records produce invoices; malformed records fail safely."""
    if value is None:
        with pytest.raises(AttributeError):
            format_rental_invoice(value)
        return

    try:
        result = format_rental_invoice(value)
    except (IndexError, ValueError):
        # Missing fields or a non-integer day count are invalid records.
        return

    assert result.startswith("Driver ")
    assert " booked " in result
    assert " for " in result
    assert " days: Total $" in result


def test_sanitize_license_plate_removes_supported_delimiters():
    assert sanitize_license_plate(" ka-01_ab#1234 ") == "KA01AB1234"


def test_parse_trip_mileage_returns_float_values():
    assert parse_trip_mileage("100.5,45.2,80") == [100.5, 45.2, 80.0]


def test_format_rental_invoice_uses_suv_rate():
    assert format_rental_invoice("Dhanush:2:SUV") == (
        "Driver Dhanush booked SUV for 2 days: Total $100.00"
    )


def test_format_rental_invoice_uses_standard_rate_for_other_categories():
    assert format_rental_invoice("Dhanush:3:Sedan") == (
        "Driver Dhanush booked Sedan for 3 days: Total $90.00"
    )
