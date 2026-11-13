"""Hypothesis tests for input validation in the Lab 7 car-rental processor."""
import math
import pytest
from hypothesis import given, settings, strategies as st

from processor import (
    format_rental_invoice,
    parse_trip_mileage,
    sanitize_license_plate,
)

FUZZ = settings(max_examples=150, deadline=None)


@FUZZ
@given(st.one_of(st.text(), st.none(), st.integers()))
def test_sanitize_license_plate_validates_generated_inputs(value):
    if not isinstance(value, str):
        with pytest.raises(TypeError):
            sanitize_license_plate(value)
        return
    normalized = value.strip().replace("-", "").replace(" ", "").replace("_", "").replace("#", "")
    if not normalized or not normalized.isalnum():
        with pytest.raises(ValueError):
            sanitize_license_plate(value)
    else:
        result = sanitize_license_plate(value)
        assert result == normalized.upper()
        assert result.isalnum()


@FUZZ
@given(st.one_of(st.text(), st.none(), st.integers()))
def test_parse_trip_mileage_validates_generated_inputs(value):
    if not isinstance(value, str):
        with pytest.raises(TypeError):
            parse_trip_mileage(value)
        return
    tokens = [part.strip() for part in value.split(",")]
    try:
        expected = [float(token) for token in tokens]
        valid = bool(value.strip()) and all(
            token != "" and math.isfinite(number) and number >= 0
            for token, number in zip(tokens, expected)
        )
    except ValueError:
        valid = False
    if not valid:
        with pytest.raises(ValueError):
            parse_trip_mileage(value)
    else:
        result = parse_trip_mileage(value)
        assert result == expected
        assert all(math.isfinite(number) and number >= 0 for number in result)


@FUZZ
@given(st.one_of(st.text(), st.none(), st.integers()))
def test_format_rental_invoice_validates_generated_inputs(value):
    if not isinstance(value, str):
        with pytest.raises(TypeError):
            format_rental_invoice(value)
        return
    parts = value.split(":")
    valid = len(parts) == 3 and bool(parts[0].strip()) and bool(parts[2].strip())
    try:
        days = int(parts[1].strip()) if len(parts) == 3 else 0
        valid = valid and days > 0
    except ValueError:
        valid = False
    if not valid:
        with pytest.raises(ValueError):
            format_rental_invoice(value)
    else:
        result = format_rental_invoice(value)
        assert result.startswith("Driver ")
        assert f" for {days} days: Total $" in result


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


@pytest.mark.parametrize("value", ["", "   ", "AB-!12"])
def test_invalid_license_plate_is_rejected(value):
    with pytest.raises(ValueError):
        sanitize_license_plate(value)


@pytest.mark.parametrize("value", ["", "1,,2", "nan,2", "-1,3", "1,inf"])
def test_invalid_mileage_is_rejected(value):
    with pytest.raises(ValueError):
        parse_trip_mileage(value)


@pytest.mark.parametrize(
    "value",
    ["", "Driver:0:SUV", "Driver:-2:SUV", "Driver:x:SUV", "Driver:2"],
)
def test_invalid_invoice_is_rejected(value):
    with pytest.raises(ValueError):
        format_rental_invoice(value)
