from datetime import date
import logging
import sys

from flask import Flask
from flask import request

import api_handler
from cache.connection import RedisInstance as Redis
import config
from query_utils import QueryParams

app = Flask(__name__)


@app.route('/')
def home_page():
    return ""


@app.route('/healthcheck')
def health_check():
    return "Success!", 200


@app.route('/website', methods=['GET'])
def get_metadata():
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

    logger = app.logger

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


def start(log_dir="logs", cache=False):
    """
        Start app with gunicorn

        Params:
        log_directory -- the directory where logs are, default log directory is logs
        cache -- whether to cache data to redis instance, default to False

        start gunicorn server with command:
            gunicorn -b 127.0.0.1:8000 'client.api:start("logs",False)'
    """
    if cache:
        Redis.init_redis_instance()
    init_logger(log_dir)
    logger = app.logger
    logger.info('Starting Server')
    return app


if __name__ == '__main__':
    """
        init app only for running a development server

        start development server with command:
            python client/api.py
    """
    if config.CACHE_DATA:
        Redis.init_redis_instance()
    default_log_dir = "logs"
    init_logger(default_log_dir)
    logger = app.logger
    logger.info('Starting Server')
    app.run(debug=config.IS_DEV)
    logger.info('Stopping Server')
