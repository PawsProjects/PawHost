from sanic.response import json
from sanic import Blueprint

health = Blueprint('health', url_prefix='/health')

@health.route('/')
async def health_check(request):
    return json({'status': 'ok'})