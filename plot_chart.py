"""Create a bar chart from summary.json."""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt


INPUT_FILE = Path("summary.json")
OUTPUT_FILE = Path("temperature_chart.png")


def create_chart(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    input_file = Path(input_file)
    output_file = Path(output_file)

    if not input_file.exists():
        raise FileNotFoundError(
            f"'{input_file}' not found. Run main.py first to create the JSON file."
        )

    with input_file.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    if not isinstance(data, list):
        raise ValueError("summary.json must contain a JSON list.")

    if not data:
        print("No devices passed the temperature filter; no chart was created.")
        return

    required = {"device_id", "average_temperature"}
    for index, item in enumerate(data):
        if not isinstance(item, dict) or not required.issubset(item):
            raise ValueError(f"Invalid summary entry at position {index}.")

    device_ids = [item["device_id"] for item in data]
    averages = [float(item["average_temperature"]) for item in data]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(device_ids, averages)
    ax.set_title("Average Temperature by Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.margins(y=0.15)
    fig.tight_layout()
    fig.savefig(output_file, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved to {output_file}.")


if __name__ == "__main__":
    try:
        create_chart()
    except (FileNotFoundError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
