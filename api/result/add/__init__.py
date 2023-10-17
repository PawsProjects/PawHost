from sanic import Blueprint
from .ports import ports
add = Blueprint.group(ports, url_prefix='/add')