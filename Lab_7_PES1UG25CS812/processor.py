"""Input processors for the Car Rental Rate Lab 7 fuzz-testing exercise."""


def sanitize_license_plate(plate):
    """Remove supported separators and normalize a license plate.

    The original starter implementation intentionally has minimal validation;
    fuzz tests exercise both expected strings and unexpected input types.
    """
    plate = plate.strip()
    for ch in ["-", " ", "_", "#"]:
        plate = plate.replace(ch, "")
    return plate.upper()


def parse_trip_mileage(mileage_csv):
    """Parse comma-separated mileage values into floating-point numbers."""
    parts = mileage_csv.split(",")
    return [float(mileage) for mileage in parts]


def format_rental_invoice(record):
    """Format a rental record in Driver:Days:Category form."""
    parts = record.split(":")
    driver = parts[0].strip()
    days = int(parts[1])
    category = parts[2].strip()
    daily_rate = 50.0 if category.lower() == "suv" else 30.0
    total = days * daily_rate
    return f"Driver {driver} booked {category} for {days} days: Total ${total:.2f}"


def main():
    print("==== Running sanitize_license_plate ====")
    raw_plate = input("Enter license plate with delimiters (-, _, #): ")
    print("Sanitized Plate:", sanitize_license_plate(raw_plate))

    print("\n==== Running parse_trip_mileage ====")
    csv_input = input("Enter CSV of mileages (e.g. 100.5, 45.2, 80.0): ")
    print("Parsed Mileage List:", parse_trip_mileage(csv_input))

    print("\n==== Running format_rental_invoice ====")
    record_input = input("Enter rental record (Driver:Days:Category): ")
    print("Rental Invoice:", format_rental_invoice(record_input))


if __name__ == "__main__":
    main()
