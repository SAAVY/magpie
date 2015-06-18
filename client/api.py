from flask import Flask, request
from scraper import general_metadata, wikipedia_metadata
import requests
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/website', methods=['GET'])
def get_metadata():
    src_url = request.args.get('src')
    connection = requests.get(src_url)
    if "wikipedia" in src_url:
        scraper = wikipedia_metadata.WikipediaMetadata()
        return scraper.parse_content(connection.content)
    else:
        scraper = general_metadata.GeneralMetadata()
        return scraper.parse_content(connection.content)

if __name__ == '__main__':
    app.run(debug=True)
