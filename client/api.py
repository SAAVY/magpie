from flask import Flask, request, jsonify
from scraper import scraper
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/website', methods=['GET'])
def websiteToScrape():
    local_scraper = scraper.Scraper(url=request.args.get('src'))
    return local_scraper.scrape_website()

if __name__ == '__main__':
    app.run(debug=True)
