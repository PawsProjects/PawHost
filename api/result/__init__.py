import sanic
from sanic import Blueprint
from .add import add
from .query import query
import hashlib
import json
import os

result = Blueprint.group(add, query, url_prefix='/result')


def hash_string(string):
    return hashlib.md5(string.encode()).hexdigest()


def get_dir():
    with open("config.json", 'r') as f:
        config = json.loads(f.read())
    return config['data_dir']


@result.middleware('request')
async def print_on_request(request: sanic.Request):
    with open('config.json', 'r') as f:
        config = json.loads(f.read())
    if config['worker_pass'] is None:
        return sanic.response.text('Pass is not set', status=400)
    passW = config['worker_pass']
    if request.headers.get('FurPass') != hash_string(passW) and request.args.get("FurPass") != hash_string(passW):
        return sanic.response.text('404 NOT FOUND', status=404)
