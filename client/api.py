from flask import Flask, request
from scraper import general_metadata, wikipedia_metadata
import json
import requests

from response import Response
import url_utils

app = Flask(__name__)

# set debug to False on non prod env
is_dev = True

@app.route('/website', methods=['GET'])
def get_metadata():
    url = request.args.get('src')
    response =  url_utils.get_url_data(url)
    # TODO(Meenu): Scraper must take in a response object and not a url
    connection = requests.get(response.url)
    if "wikipedia" in response.url:
        scraper = wikipedia_metadata.WikipediaMetadata()
        return scraper.parse_content(connection.content)
    else:
        scraper = general_metadata.GeneralMetadata()
        return scraper.parse_content(connection.content)

    return json_return

if __name__ == '__main__':
    app.run(debug=is_dev)
