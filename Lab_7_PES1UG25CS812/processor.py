"""Hardened input processors for the Lab 7 car-rental fuzz-testing exercise."""
import math


def sanitize_license_plate(plate: str) -> str:
    """Normalize a plate; reject wrong types, empty values and invalid characters."""
    if not isinstance(plate, str):
        raise TypeError("license plate must be a string")
    normalized = plate.strip()
    for separator in ("-", " ", "_", "#"):
        normalized = normalized.replace(separator, "")
    if not normalized:
        raise ValueError("license plate cannot be empty")
    if not normalized.isalnum():
        raise ValueError("license plate may contain only letters, digits and supported separators")
    return normalized.upper()


def parse_trip_mileage(mileage_csv: str) -> list[float]:
    """Parse comma-separated, finite, non-negative mileage values."""
    if not isinstance(mileage_csv, str):
        raise TypeError("mileage input must be a comma-separated string")
    if not mileage_csv.strip():
        raise ValueError("mileage input cannot be empty")
    tokens = [token.strip() for token in mileage_csv.split(",")]
    if any(token == "" for token in tokens):
        raise ValueError("mileage list contains an empty value")
    try:
        values = [float(token) for token in tokens]
    except ValueError as exc:
        raise ValueError("mileage values must be numeric") from exc
    if any(not math.isfinite(value) or value < 0 for value in values):
        raise ValueError("mileage values must be finite and non-negative")
    return values


def format_rental_invoice(record: str) -> str:
    """Format Driver:Days:Category records with validated fields."""
    if not isinstance(record, str):
        raise TypeError("rental record must be a string")
    parts = record.split(":")
    if len(parts) != 3:
        raise ValueError("rental record must contain exactly Driver:Days:Category")
    driver, raw_days, category = (part.strip() for part in parts)
    if not driver:
        raise ValueError("driver name cannot be empty")
    if not category:
        raise ValueError("vehicle category cannot be empty")
    try:
        days = int(raw_days)
    except ValueError as exc:
        raise ValueError("rental days must be a positive integer") from exc
    if days <= 0:
        raise ValueError("rental days must be greater than zero")
    daily_rate = 50.0 if category.casefold() == "suv" else 30.0
    total = days * daily_rate
    return f"Driver {driver} booked {category} for {days} days: Total ${total:.2f}"


def main():
    print("==== Running sanitize_license_plate ====")
    print("Sanitized Plate:", sanitize_license_plate(" ka-01_ab#1234 "))
    print("\n==== Running parse_trip_mileage ====")
    print("Parsed Mileage List:", parse_trip_mileage("100.5, 45.2, 80.0"))
    print("\n==== Running format_rental_invoice ====")
    print("Rental Invoice:", format_rental_invoice("Dhanush:2:SUV"))


if __name__ == "__main__":
    main()
