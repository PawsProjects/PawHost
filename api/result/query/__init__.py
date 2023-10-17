import aiosqlite
import os
from sanic import Blueprint
import json
from sanic.response import json as sanic_json
from .lists import lists

query = Blueprint.group(lists, url_prefix='/query')