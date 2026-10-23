# Device Log Summarizer CLI

A Python command-line tool that reads device telemetry from a CSV file, calculates per-device statistics, exports a JSON summary, and generates a chart of average temperatures.

## Requirements

- Python 3.10 or newer recommended
- pip

## Setup

Open a terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
```

## Run

1. Make sure `device_telemetry.csv` is in the project folder.
2. Generate the device summary:

```bash
python main.py
```

This prints a summary table and creates `summary.json`. Devices with an average temperature above 80.0 are excluded.

3. Generate the temperature chart:

```bash
python plot_chart.py
```

This creates `temperature_chart.png`.

4. Run the sensor-reading cleaning function and its basic examples:

```bash
python data_cleaning.py
```

## Data Cleaning

The `clean_sensor_readings` function converts valid readings to floats, skips values that cannot be converted and negative values, and caps readings above 500.0 at 500.0. It also handles empty and all-invalid inputs.

## CSV Format

The CSV must contain these columns:

- `device_id`
- `status`
- `temperature`

The program skips invalid temperature values and rows without a device ID, with warnings where applicable.

## Sample Data

The included `device_telemetry.csv` contains sample data created for testing because no assessment CSV was provided. Replace it with the actual assessment data if the recruiter supplies a CSV.

## Submission Checklist

- [ ] Run `python data_cleaning.py`
- [ ] Run `python main.py`
- [ ] Run `python plot_chart.py`
- [ ] Inspect `summary.json` and `temperature_chart.png`
- [ ] Review `PROMPT_LOG.md` to ensure it accurately records the AI assistance used
- [ ] Submit the project as a ZIP file or GitHub repository