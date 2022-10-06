"""
    Create initial bare server and ensure docker works.
    Deploy to GCP and test in the cloud.
"""

import os
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from helpers.pdf import parsePDF

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return 'hello'


@app.route('/api/upload', methods=['POST'])
@cross_origin()
def upload():
    print(request.files)
    if len(request.files) == 0:
        return make_response("Record not found", 400)

    result = {}
    for file in request.files.getlist("source"):
        result[file.filename] = parsePDF(file)

    return result


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
