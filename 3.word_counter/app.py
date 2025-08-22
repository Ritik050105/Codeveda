from flask import Flask, render_template, request
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    word_count = None
    filename = None

    if request.method == 'POST':
        file = request.files['text_file']
        if file and file.filename.endswith('.txt'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                word_count = len(re.findall(r'\b\w+\b', content))  # More accurate word count
                filename = file.filename
        else:
            word_count = 'Invalid file. Please upload a .txt file.'

    return render_template('index.html', word_count=word_count, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
