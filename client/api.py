from flask import Flask, request
from scraper import general_metadata, wikipedia_metadata
from constants import UrlTypes

import url_utils

app = Flask(__name__)

# set debug to False on non prod env
is_dev = True


@app.route('/website', methods=['GET'])
def get_metadata():
    url = request.args.get('src')
    response = url_utils.get_url_data(url)
    scraper = get_scraper(response)
    return scraper.parse_content(response.content)


def get_scraper(response):
    scraper = None
    if response.type is UrlTypes.WIKI:
        scraper = wikipedia_metadata.WikipediaMetadata()
    else:
        scraper = general_metadata.GeneralMetadata()
    return scraper

if __name__ == '__main__':
    app.run(debug=is_dev)
