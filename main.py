"""Summarize device telemetry from CSV into JSON and a terminal table."""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

INPUT_FILE = Path("device_telemetry.csv")
OUTPUT_FILE = Path("summary.json")
REQUIRED_COLUMNS = {"device_id", "status", "temperature"}


def summarize_csv(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    """Aggregate telemetry by device and export devices with mean temperature <= 80."""
    input_file = Path(input_file)
    output_file = Path(output_file)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file '{input_file}' was not found. Put it in the project folder."
        )

    grouped = defaultdict(lambda: {"temperatures": [], "records": 0, "error_count": 0})

    with input_file.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no header row.")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError("CSV is missing required column(s): " + ", ".join(sorted(missing)))

        for line_number, row in enumerate(reader, start=2):
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            raw_temperature = (row.get("temperature") or "").strip()

            if not device_id:
                print(f"Warning: skipping row {line_number}: empty device_id.", file=sys.stderr)
                continue
            try:
                temperature = float(raw_temperature)
            except (TypeError, ValueError):
                print(f"Warning: skipping row {line_number}: invalid temperature.", file=sys.stderr)
                continue

            if not (temperature == temperature and abs(temperature) != float("inf")):
                print(f"Warning: skipping row {line_number}: temperature is not finite.", file=sys.stderr)
                continue

            grouped[device_id]["records"] += 1
            grouped[device_id]["temperatures"].append(temperature)
            if status == "ERROR":
                grouped[device_id]["error_count"] += 1

    results = []
    for device_id in sorted(grouped):
        values = grouped[device_id]["temperatures"]
        if not values:
            continue
        average = sum(values) / len(values)
        if average > 80.0:
            continue
        results.append({
            "device_id": device_id,
            "total_records": grouped[device_id]["records"],
            "average_temperature": round(average, 2),
            "error_count": grouped[device_id]["error_count"],
        })

    with output_file.open("w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=2)

    print_summary(results)
    print(f"\nSaved {len(results)} device summary record(s) to {output_file}.")
    return results


def print_summary(results):
    """Print a simple aligned table without third-party dependencies."""
    headers = ("Device ID", "Records", "Average Temp", "ERROR Count")
    rows = [
        (r["device_id"], str(r["total_records"]),
         f'{r["average_temperature"]:.2f}', str(r["error_count"]))
        for r in results
    ]
    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]

    def format_row(row):
        return " | ".join(value.ljust(widths[i]) for i, value in enumerate(row))

    print(format_row(headers))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(format_row(row))


if __name__ == "__main__":
    try:
        summarize_csv()
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
