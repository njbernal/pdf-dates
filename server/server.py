import os
import uuid
import json
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin

from helpers.pdf import parsePDF


app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return 'hello'


@app.route('/api/user', methods=['GET'])
@cross_origin()
def user():
    with open('./data/users.json', 'r') as userfile:
        users = json.load(userfile)

    unique_id = str(uuid.uuid4())
    while (unique_id in users['users']):
        unique_id = str(uuid.uuid4())

    users['users'].append(unique_id)
    os.mkdir(f'./data/{unique_id}')
    with open('./data/users.json', 'w') as userfile:
        json.dump(users, userfile)

    return str(unique_id)


@ app.route('/api/upload', methods=['POST'])
@ cross_origin()
def upload():
    uuid = request.form.get('user')
    if len(request.files) == 0:
        return make_response("Record not found", 400)
    if not uuid:
        return make_response("Invalid user ID", 404)

    result = {}
    for file in request.files.getlist("source"):
        file.save(f"./data/{uuid}/{file.filename}")
        result[file.filename] = parsePDF(file)
    return result


@ app.route('/api/files', methods=['POST'])
@ cross_origin()
def get_files():
    uuid = request.get_json()['user']
    if not uuid:
        return 'Error: Invalid user ID'

    result = {}
    for filename in os.listdir(f'./data/{uuid}'):
        with open(f"./data/{uuid}/{filename}", 'rb') as file:
            result[filename] = parsePDF(file)
    return result


if __name__ == '__main__':
    # For testing purposes only
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
