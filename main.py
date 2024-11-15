from flask import render_template, jsonify
from init import app
import pandas as pd

from api.amazonpricing import update_prices
from api.priceapi import price_api

app.register_blueprint(price_api)

# Configuration
API_KEY = "673147a734a4318291dc90e1"
FILE_PATH = "/Users/torinwolff/Documents/GitHub/PCPB/volume/data.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/api/parts', methods=['GET'])
def get_parts():
    parts_df = pd.read_csv('volume/parts.csv')
    parts_dict = parts_df.groupby('type')['name'].apply(list).to_dict()
    return jsonify(parts_dict)

def run_price_monitor():
    update_prices(FILE_PATH, API_KEY)

if __name__ == "__main__":
    # price_monitor = threading.Thread(target=run_price_monitor, daemon=True)
    # price_monitor.start()
    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port="8873")