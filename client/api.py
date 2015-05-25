from flask import Flask, request, jsonify
import spider_work
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/website', methods=['GET'])
def websiteToScrape():
    return spider_work.start_spider(request.args.get('src'))

if __name__ == '__main__':
    app.run()