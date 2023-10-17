from sanic import Blueprint
from sanic.response import json as sanic_json, JSONResponse
import json
import os
import aiosqlite
from sanic.response import text

lists = Blueprint("list", url_prefix='/list')


def get_dir():
    with open("config.json", 'r') as f:
        config = json.loads(f.read())
    return config['data_dir']


@lists.middleware('request')
async def check_db(request):
    print(request.args)
    if request.args.get('limits') is None:
        request.args['limits'] = [20]
    else:
        request.args['limits'] = [int(request.args.get('limits'))]
    if request.args.get('page') is None:
        request.args['page'] = [1]
    else:
        request.args['page'] = [int(request.args.get('page'))]
    print(request.args)
    try:
        request.ctx.db
    except AttributeError:
        request.ctx.db = await aiosqlite.connect(os.path.join(get_dir(), 'ports.db'))

@lists.middleware('response')
async def response(request, response: JSONResponse):
    print(response.raw_body)
    if request.args.get("plain") is not None:
        p = []
        for i in response.raw_body:
            p.append("{}:{}\n".format(i[2], i[3]))
        return text("".join(p))
@lists.get('/ip')
async def lists_ip(request):
    limits = request.args.get('limits')
    page = request.args.get('page')
    data = []
    async with request.ctx.db.execute('select * from results limit ? offset ?',
                                      (limits, (page - 1) * limits)) as cursor:
        async for row in cursor:
            data.append(row)
    return sanic_json(data)


@lists.get('/ip/<ip>')
async def list_ip(request, ip):
    limits = request.args.get('limits')
    page = request.args.get('page')
    data = []
    async with request.ctx.db.execute('select * from results where ip = ? limit ? offset ?',
                                      (ip, limits, (page - 1) * limits)) as cursor:
        async for row in cursor:
            data.append(row)
    return sanic_json(data)


@lists.get('/port/<port>')
async def list_port(request, port):
    limits = request.args.get('limits')
    page = request.args.get('page')
    data = []
    async with request.ctx.db.execute('select * from results where port = ? limit ? offset ?',
                                      (port, limits, (page - 1) * limits)) as cursor:
        async for row in cursor:
            data.append(row)
    return sanic_json(data)


@lists.get('/banner/<banner>')
async def list_banner(request, banner):
    limits = request.args.get('limits')
    page = request.args.get('page')
    data = []
    async with request.ctx.db.execute('select * from results where banner like ? limit ? offset ?',
                                      ('%' + banner + '%', limits, (page - 1) * limits)) as cursor:
        async for row in cursor:
            data.append(row)
    return sanic_json(data)


@lists.get('/note/<note>')
async def list_note(request, note):
    limits = request.args.get('limits')
    page = request.args.get('page')
    data = []
    async with request.ctx.db.execute('select * from results where note like ? limit ? offset ?',
                                      ('%' + note + '%', limits, (page - 1) * limits)) as cursor:
        async for row in cursor:
            data.append(row)
    return sanic_json(data)
