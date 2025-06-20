from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB Atlas connection (replace <username>, <password>, and <cluster-url>)
client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/test?retryWrites=true&w=majority")
db = client["mydatabase"]
collection = db["mycollection"]

# API Route: Return JSON data from backend file
@app.route('/api')
def api():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Show the form
@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']

        if not name or not email:
            return render_template('form.html', error="All fields are required")

        collection.insert_one({"name": name, "email": email})
        return redirect(url_for('success'))

    except Exception as e:
        return render_template('form.html', error=str(e))

# Success page
@app.route('/success')
def success():
    return render_template('success.html')