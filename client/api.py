import logging
import sys

from datetime import date

from flask import Flask
from flask import request
from flask.ext.cors import CORS

import api_handler
from cache.connection import RedisInstance as Redis
import config

app = Flask(__name__)
CORS(app)


@app.route('/')
def home_page():
    return ""


@app.route('/healthcheck')
def health_check():
    return "Success!", 200


@app.route('/website', methods=['GET'])
def get_metadata():
    local_request = request
    url = request.args.get('src').strip()
    response_type = local_request.args.get('format')
    logger = app.logger
    try:
        if response_type:
            return api_handler.get_metadata(url, response_type)
        return api_handler.get_metadata(url)
    except Exception:
        logger.exception("Unexpected error: %s", sys.exc_info()[0])
    return "Something went wrong", 400


def get_file_log_handler():
    today = date.today()
    timestamp = "%d-%d-%d" % (today.year, today.month, today.day)
    file_level = logging.DEBUG
    if config.IS_DEV:
        fh = logging.FileHandler("logs/%s.debug.magpie.log" % timestamp)
    else:
        fh = logging.FileHandler("logs/%s.magpie.log" % timestamp)
        file_level = logging.INFO
    fh.setLevel(file_level)
    fh_format = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)-8s - %(message)s')
    fh.setFormatter(fh_format)
    return fh


def get_file_warn_log_handler():
    today = date.today()
    timestamp = "%d-%d-%d" % (today.year, today.month, today.day)
    fh_warn = logging.FileHandler(filename="logs/%s.errors.magpie.log" % timestamp)
    fh_warn.setLevel(logging.WARNING)
    fh_format = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)-8s - %(message)s')
    fh_warn.setFormatter(fh_format)
    return fh_warn


def get_stream_log_handler(console_level=logging.DEBUG):
    ch = logging.StreamHandler()  # StreamHandler logs to console
    ch.setLevel(console_level)
    ch_format = logging.Formatter('%(name)s:%(lineno)d - %(message)s')
    ch.setFormatter(ch_format)
    return ch


def init_logger():
    if config.IS_DEV:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)
    app.logger.addHandler(get_file_log_handler())
    app.logger.addHandler(get_file_warn_log_handler())

if __name__ == '__main__':
    if config.CACHE_DATA:
        Redis.init_redis_instance()
    init_logger()
    logger = app.logger
    logger.info('Starting Server')
    app.run(debug=config.IS_DEV)
    logger.info('Stopping Server')
