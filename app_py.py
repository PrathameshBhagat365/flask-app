# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jK2AhceNQewEzWB7jPpkmqqYLpOOLl55
"""

# Step 1: Install Required Libraries
!pip install flask pandas --quiet

# Step 2: Import Libraries
from flask import Flask, request, jsonify
import pandas as pd

# Step 3: Create Flask App
app = Flask(__name__)

# Load the CSV file (Upload your CSV to /content first)
file_path = "/content/mht data.csv"  # Ensure the file is uploaded
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Step 4: Define the /predict route to get user input and predict colleges
@app.route('/predict', methods=['GET'])
def predict_colleges():
    try:
        # Get user inputs from the URL
        percentile = request.args.get('percentile')
        branch = request.args.get('branch')
        seat_type = request.args.get('seat_type')

        # Validate inputs
        if not percentile or not branch or not seat_type:
            return jsonify({"error": "Missing required parameters"}), 400

        percentile = float(percentile)

        # Filter the data based on the user's input
        filtered_colleges = df[
            (df["Merit Percentile"] >= percentile - 5) &
            (df["Merit Percentile"] <= percentile + 5) &
            (df["branch"].str.lower() == branch.lower()) &
            (df["seat_type"].str.lower() == seat_type.lower())
        ]

        # Select top 10 colleges
        top_colleges = filtered_colleges[["college_name", "branch", "seat_type", "Merit Percentile"]].head(10)

        # Convert the result to JSON
        if not top_colleges.empty:
            return jsonify(top_colleges.to_dict(orient="records"))
        else:
            return jsonify({"message": "No colleges found for the given criteria"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Step 5: Run Flask App
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Use reloader=False to avoid issues in Colab