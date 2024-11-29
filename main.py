# main.py
from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from utils.cryption import Encryptor
from utils.utils import scan_recurse

app = Flask(__name__)
BASE_DIR = 'files'
encryptor = Encryptor(BASE_DIR)

@app.route('/')
def index():
    try:
        files = [item for item in scan_recurse(BASE_DIR) if item != "key.key"]
    except Exception as e:
        return (f"Exception: {e}")
    return render_template('index.html', files=files)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    password = request.json['password']
    encryptor.encrypt(password)
    return jsonify({"message": "Files encrypted successfully!"})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    key = request.json['password']
    encryptor.decrypt(key)
    return jsonify({"message": "Files decrypted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
