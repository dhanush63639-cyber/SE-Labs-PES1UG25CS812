"""Original buggy starter implementation, retained for before/after evidence."""

def sanitize_license_plate(plate):
    plate = plate.strip()
    for ch in ["-", " ", "_", "#"]:
        plate = plate.replace(ch, "")
    return plate.upper()


def parse_trip_mileage(mileage_csv):
    parts = mileage_csv.split(",")
    return [float(mileage) for mileage in parts]


def format_rental_invoice(record):
    parts = record.split(":")
    driver = parts[0].strip()
    days = int(parts[1])
    category = parts[2].strip()
    daily_rate = 50.0 if category.lower() == "suv" else 30.0
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
