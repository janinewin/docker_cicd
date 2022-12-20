# wsgi.py
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return 'Wow! If you see this it means your are doing a great job!'
