from datetime import datetime, timezone
from flask import abort

def get_validated_data(data):
    data_length = len(data)

    # Check if the number of lines is even
    if data_length % 2 != 0:
        return False

    readings_data = {}

    # Process data in pairs
    for i in range(data_length // 2):
        voltage_item = data[i]
        current_item = data[data_length // 2 + i]

        voltage_parts = voltage_item.split()
        current_parts = current_item.split()

        # Check if both voltage and current items have three parts
        if len(voltage_parts) != 3 or len(current_parts) != 3:
            return False

        # Extract the parts for voltage item
        voltage_time, voltage_name, voltage_value = voltage_parts

        # Extract the parts for current item
        current_time, current_name, current_value = current_parts

        # Check if the names and times match
        if voltage_name != "Voltage" or current_name != "Current" or voltage_time != current_time:
            return False

        try:
            # Convert the timestamp to Unix timestamp
            unix_timestamp = int(voltage_time)

            # Convert the Unix timestamp to ISO 8601 format
            date_time_str = datetime.fromtimestamp(unix_timestamp, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

            # Convert the values to float and calculate power
            voltage_value = float(voltage_value)
            current_value = float(current_value)
            power_value = format(voltage_value * current_value, ".2f")

            # Store the readings data for the Unix timestamp
            readings_data[unix_timestamp] = [
                {"time": date_time_str, "name": "Voltage", "value": voltage_value},
                {"time": date_time_str, "name": "Current", "value": current_value},
                {"time": date_time_str, "name": "Power", "value": power_value}
            ]
        except Exception as e:
            print(f"{e}")
            # Return False if there's an exception during conversion
            return False

    return readings_data
