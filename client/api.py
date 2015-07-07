from flask import Flask
from flask import request

import api_handler
from client.constants import ResponseType


app = Flask(__name__)

# set debug to False on non prod env
is_dev = True


@app.route('/')
def home_page():
    return ""


@app.route('/website', methods=['GET'])
def get_metadata():
    local_request = request
    url = request.args.get('src')
    response_type = local_request.args.get('format')
    if response_type is None:
        response_type = ResponseType.JSON  # Default return format is json
    return api_handler.get_metadata(url, response_type)


if __name__ == '__main__':
    app.run(debug=is_dev)