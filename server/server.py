"""
    Create initial bare server and ensure docker works.
    Deploy to GCP and test in the cloud.
"""

import os
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
@cross_origin()
def index():
    return 'hello'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
