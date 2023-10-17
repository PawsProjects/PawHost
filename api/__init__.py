from sanic import Blueprint
from .health import health
from .result import result
api = Blueprint.group(health, result, url_prefix='/api')

