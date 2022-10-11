from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin

# PDF Date Extractor processing functionality
from helpers.pdf import DateExtractor

# Create server and add cors support
app = Flask(__name__)
cors = CORS(app)


"""
Server Routes for PDF Extractor
"""


@app.route('/', methods=['GET'])
@cross_origin()
def index() -> str:
    """ 
    Route for testing only. Says hello.
    """
    return 'Hello Harbour!'


@ app.route('/api/upload', methods=['POST'])
@ cross_origin()
def upload() -> object:
    """ 
    Primary file upload route. Checks the request
    object for uploaded files, created DateExtractor object and 
    prepares response. Expects the files to be named 'source'.
    :return: JSON response with date matches.
    """
    if len(request.files) == 0:
        return make_response("No files provided.", 400)

    result = {}
    for file in request.files.getlist("source"):
        extractor = DateExtractor(file)
        result[file.filename] = extractor.get_results()
    return result


if __name__ == '__main__':
    """ For local testing. Use waitress-serve otherwise. """
    app.run(host='0.0.0.0', port=5000, debug=True)
