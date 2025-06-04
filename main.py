from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load your CSV file
df = pd.read_csv("colleges.csv")

@app.route('/recommend')
def recommend():
    percentile = float(request.args.get("percentile"))
    branch = request.args.get("branch")
    seat_type = request.args.get("seat_type")

    # Filter the DataFrame based on inputs
    filtered = df[
        (df['branch'].str.lower() == branch.lower()) &
        (df['seat_type'].str.lower() == seat_type.lower())
    ]

    # Find 10 closest cutoffs to the user's percentile
    filtered['diff'] = abs(filtered['cutoff'] - percentile)
    result = filtered.sort_values(by='diff').head(10)

    # Select columns to return
    output = result[['college_name', 'branch', 'seat_type', 'cutoff']].to_dict(orient='records')
    return jsonify(output)

# Run the app on Replit
app.run(host='0.0.0.0', port=81)
