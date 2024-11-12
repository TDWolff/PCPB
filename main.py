from flask import render_template, requests
from init import app

@app.route('/')
def index():
    return render_template('index.html')

# this runs the flask application on the development server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8873")