from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Load the Excel data
data = pd.read_excel("VOTE.xlsx")

@app.route("/get-data", methods=["POST"])
def get_data():
    # Get data from the request
    user_input = request.json.get('query', '').strip()  # Single input for both Name or HRMS ID

    data['HRMS'] = data['HRMS'].astype(str)
    data['IPAS'] = data['IPAS'].astype(str)

    # Perform search based on the input (Name or HRMS ID)
    if user_input.isdigit():  # If input is a number, we assume it's HRMS ID
        result = data[data['HRMS_ID'].astype(str) == user_input]  # Convert HRMS_ID to string
    else:  # Otherwise, treat the input as Name
        result = data[data['IPAS'] == user_input]

    # Return results as JSON
    if result.empty:
        return jsonify({"message": "No data found"}), 200  # If no data found, return a message

    return jsonify(result.to_dict(orient='records')), 200  # If data found, return the data

if __name__ == "__main__":
    app.run(debug=True, port=5000)
