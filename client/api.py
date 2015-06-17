from flask import Flask, request
from scraper import scraper, wikipedia_scraper
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/website', methods=['GET'])
def get_metadata():
    src_url = request.args.get('src')
    if "wikipedia" in src_url:
        wikipedia_scraper.scrape(url=src_url)
        return ""
    else:
        local_scraper = scraper.Scraper(url=request.args.get('src'))
        prop_map = local_scraper.scrape_website()
        json_return = json.dumps(prop_map)
        return json_return

if __name__ == '__main__':
    app.run(debug=True)
