
def clean_sensor_readings(values):
    """Return cleaned sensor readings as floats."""
    cleaned = []

    for value in values:
        try:
            number = float(value)
        except (ValueError, TypeError):
            continue

        if number < 0:
            continue

        if number > 500:
            number = 500.0

        cleaned.append(number)

    return cleaned


if __name__ == "__main__":
    print(clean_sensor_readings([12, "20.5", None, -1, "bad", 700]))
    print(clean_sensor_readings([]))
    print(clean_sensor_readings([None, "bad", -5]))
