from flask import Flask, request, render_template, send_from_directory
import os
from utils.cryption import Encryptor
from utils.utils import scan_recurse, make_response, handle_error

app = Flask(__name__)
BASE_DIR = 'files'
encryptor = Encryptor(BASE_DIR)

@app.route('/')
def index():
    try:
        files = [item for item in scan_recurse(BASE_DIR) if item != ".key.key"]

        files = [file for file in files]
    
    except Exception as e:
        return (f"Exception: {e}")
    return render_template('index.html', files=files)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        password = request.json['password']
        files, key = encryptor.encrypt(password)
        return make_response(True, {"key": str(key), "text": f"Encrypted {len(files)} files..."}, 200)
    except:
        return handle_error("An error occured while encrypting.")

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        key = request.json['password']
        files = encryptor.decrypt(key)
        files_length = len(files)
        if files_length == 0:
            return handle_error("An error occured while decrypting.")
        return make_response(True, { "text": f"Decrypted {files_length} files..."}, 200)
    except:
        return handle_error("An error occured while decrypting.")


@app.route('/files/<path:filename>')
def serve_file(filename):
    try:
        # Debugging: Print the file path
        file_path = os.path.join(BASE_DIR, filename)
        print(f"Serving file: {file_path}")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return handle_error("File not found", 404)
        return send_from_directory(BASE_DIR, filename)
    except Exception as e:
        return handle_error(f"An error occurred while serving the file: {e}")


if __name__ == '__main__':
    app.run(debug=True)
