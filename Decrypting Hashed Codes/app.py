from flask import Flask, render_template, request
import hashlib  # Example of a module for hashing

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Ensure your HTML file is named index.html

@app.route('/hash', methods=['POST'])
def hash_code():
    if request.method == 'POST':
        input_data = request.form['input_data']
        # Example hashing function (SHA-256)
        hashed_code = hashlib.sha256(input_data.encode()).hexdigest()
        return render_template('index.html', hashed_code=hashed_code)

if __name__ == '__main__':
    app.run(debug=True)
