from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from cryptography.fernet import Fernet
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecret'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

KEY_FILE = 'secret.key'

# Load or generate encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return Fernet(key)

fernet = load_key()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files:
        flash('No file uploaded!')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file!')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    with open(input_path, 'rb') as f:
        original = f.read()
    encrypted = fernet.encrypt(original)

    output_filename = f"{filename}.encrypted"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    with open(output_path, 'wb') as f:
        f.write(encrypted)

    return send_file(output_path, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files:
        flash('No file uploaded!')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file!')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    with open(input_path, 'rb') as f:
        encrypted = f.read()

    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception as e:
        flash('Decryption failed! Invalid key or file.')
        return redirect(url_for('index'))

    output_filename = f"decrypted_{filename.replace('.encrypted', '')}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    with open(output_path, 'wb') as f:
        f.write(decrypted)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
