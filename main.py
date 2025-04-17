from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'chFCBROZyDJS5O8Z3UcrjfM0EsoLQNpCLDKsm'
SHEET_ID = '3874576032288644'

@app.route('/', methods=['GET'])
def home():
    return "✅ Smartsheet Intake API is running!"

@app.route('/submit-intake', methods=['POST'])
def submit_intake():
    data = request.json

    print("Received POST /submit-intake request")
    print(data)

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    intake_data = {
        "Project Title": data.get("project_title", ""),
        "Requestor Name": data.get("requestor_name", ""),
        "Department": data.get("department", ""),
        "Problem Statement": data.get("problem_statement", ""),
        "Expected Outcome": data.get("expected_outcome", ""),
        "Data Source Type": data.get("data_source_type", ""),
        "Output Format": data.get("output_format", ""),
        "Integration Level": data.get("integration_level", ""),
        "Timeline Estimate": data.get("timeline_estimate", ""),
        "GxP Impact": data.get("gxp_impact", ""),
        "Cross-Functional Support": data.get("cross_functional_support", ""),
        "Comments": data.get("comments", "")
    }

    sheet = requests.get(
        f'https://api.smartsheet.com/2.0/sheets/{SHEET_ID}',
        headers=headers
    ).json()

    column_map = {col['title']: col['id'] for col in sheet['columns']}

    cells = []
    for key, value in intake_data.items():
        if key in column_map:
            cells.append({
                "columnId": column_map[key],
                "value": value
            })

    row_payload = {
        "toBottom": True,
        "rows": [
            {
                "cells": cells
            }
        ]
    }

    response = requests.post(
        f'https://api.smartsheet.com/2.0/sheets/{SHEET_ID}/rows',
        headers=headers,
        json=row_payload
    )

    return jsonify({
        "status": response.status_code,
        "response": response.json()
    }), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
