from flask import render_template
import requests
from init import app
from api.amazonpricing import update_prices
import threading

from api.priceapi import price_api

app.register_blueprint(price_api)

# Configuration
API_KEY = "673147a734a4318291dc90e1"
FILE_PATH = "/Users/torinwolff/Documents/GitHub/PCPB/volume/data.csv"

@app.route('/')
def index():
    return render_template('index.html')

def run_price_monitor():
    update_prices(FILE_PATH, API_KEY)

if __name__ == "__main__":
    # price_monitor = threading.Thread(target=run_price_monitor, daemon=True)
    # price_monitor.start()
    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port="8873")