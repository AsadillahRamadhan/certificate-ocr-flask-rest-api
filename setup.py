import json
from flask import Flask, jsonify, request

import process

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    result = process.predict(request.form['link'])
    return jsonify(result)

if __name__ == '__main__':
   app.run(port=5000)