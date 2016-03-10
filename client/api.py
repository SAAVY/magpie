from datetime import date
import logging
import sys

from flask import Flask
from flask import request
from flask.ext.cors import CORS

import api_handler
import blacklist
from cache.connection import RedisInstance as Redis
from config import config
from query_utils import QueryParams

app = Flask(__name__)
CORS(app)


@app.route('/')
def home_page():
    return "", 200


@app.route('/healthcheck')
def health_check():
    return "Success!", 200


@app.route('/website', methods=['GET'])
def get_metadata():
    logger = app.logger
    urls = request.args.getlist('src')
    query_params = QueryParams()
    local_request = request

    response_type = local_request.args.get('format')
    desc_length = local_request.args.get('desc_cap')

    query_params.query_urls = urls
    if desc_length is not None:
        query_params.desc_length = int(desc_length)
    if response_type is not None:
        query_params.response_type = response_type

    try:
        if len(urls) == 1:
            return api_handler.get_url_metadata(query_params)
        else:
            return api_handler.get_urls_metadata(query_params)
    except Exception:
        logger.exception("Unexpected error: %s", sys.exc_info()[0])
    return "Something went wrong", 400


def get_file_log_handler(log_directory):
    today = date.today()
    timestamp = "%d-%d-%d" % (today.year, today.month, today.day)
    file_level = logging.DEBUG
    if config.IS_DEV:
        fh = logging.FileHandler("%s/%s.debug.magpie.log" % (log_directory, timestamp))
    else:
        fh = logging.FileHandler("%s/%s.magpie.log" % (log_directory, timestamp))
        file_level = logging.INFO
    fh.setLevel(file_level)
    fh_format = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)-8s - %(message)s')
    fh.setFormatter(fh_format)
    return fh


def get_file_warn_log_handler(log_directory):
    today = date.today()
    timestamp = "%d-%d-%d" % (today.year, today.month, today.day)
    fh_warn = logging.FileHandler(filename="%s/%s.errors.magpie.log" % (log_directory, timestamp))
    fh_warn.setLevel(logging.WARNING)
    fh_format = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)-8s - %(message)s')
    fh_warn.setFormatter(fh_format)
    return fh_warn


def init_logger(log_directory):
    if config.IS_DEV:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)
    app.logger.addHandler(get_file_log_handler(log_directory))
    app.logger.addHandler(get_file_warn_log_handler(log_directory))


def start(log_dir="logs"):
    """
        Start app with gunicorn

        Params:
        log_directory -- the directory where logs are, default log directory is logs

        start gunicorn server with command:
            gunicorn -b 127.0.0.1:8000 'client.api:start("logs")'
    """
    if config.CACHE_DATA:
        Redis.init_redis_instance()
    init_logger(log_dir)
    logger = app.logger
    logger.info('Starting Server')
    blacklist.build_inc_request_blacklist(logger)
    blacklist.build_website_blacklist(logger)
    return app


if __name__ == '__main__':
    """
        init app only for running a development server

        start development server with command:
            python client/api.py
    """
    app = start()
    app.run(debug=config.IS_DEV)
