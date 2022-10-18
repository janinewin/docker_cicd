
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify("let's deploy to our containers!")
