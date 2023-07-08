from flask import Flask,request,jsonify
from db import database,add_reading,get_reading,Reading
from datetime import datetime,timezone
from utils import get_validated_data


app = Flask(__name__)


@app.post("/data")
def post_data():
    text_data = request.get_data(as_text=True).split("\n")
    reading_data = get_validated_data(text_data)
    success = bool(reading_data)
    
    if success:
        database.update(reading_data)
    
    return {"success": success}


@app.route("/data", methods=["GET"])
def get_data():
    # Get the 'from' and 'to' date parameters from the request
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    # Convert 'from_date' to Unix timestamp or set it to negative infinity if not provided
    if from_date:
        from_timestamp = int(datetime.fromisoformat(from_date).timestamp())
    else:
        from_timestamp = float("-inf")
        
    # Convert 'to_date' to Unix timestamp or set it to positive infinity if not provided
    if to_date:
        to_timestamp = int(
            datetime.fromisoformat(to_date)
            .replace(hour=23, minute=59, second=59, microsecond=0, tzinfo=timezone.utc)
            .timestamp()
        )
    else:
        to_timestamp = float("inf")

    # Filter the keys based on the date range
    filtered_keys = [
        key for key in database.keys() if from_timestamp <= key <= to_timestamp
    ]

    # Retrieve the filtered data based on the filtered keys
    filtered_data = [value for key in filtered_keys for value in database[key]]

    # Return the filtered data as JSON response
    return jsonify(filtered_data)


if __name__ == "__main__":
    app.run()
