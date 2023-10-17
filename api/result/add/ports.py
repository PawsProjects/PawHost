import threading

from sanic.request import Request
from sanic import Blueprint
from sanic.response import json as sanic_json
import json
import os
import re
import time
import aiosqlite
import socket
import asyncio
import threading

ports = Blueprint('port', url_prefix='/ports')


def get_dir():
    with open("config.json", 'r') as f:
        config = json.loads(f.read())
    return config['data_dir']


async def get_banner(ip, port):
    asm = asyncio.Semaphore(200)
    async with asm:
        try:
            tmp = await asyncio.open_connection(ip, port)
            reader, writer = await asyncio.open_connection(ip, port)
            banner = await asyncio.wait_for(reader.read(8192), timeout=2.5)
            assert banner != b''
            assert banner.decode('utf-8').replace(" ", "").replace("\n", "").replace("\r", "") != ""
            return banner.decode('utf-8')
        except Exception as e:
            print(e)
            try:
                tmp = await asyncio.open_connection(ip, port)
                reader, writer = await asyncio.open_connection(ip, port)
                writer.write(b'GET / HTTP/1.1\r\n\r\n')
                banner = await asyncio.wait_for(reader.read(8192), timeout=2.5)
                return banner.decode('utf-8')
            except Exception as e:
                print(e)
                return None


async def write_result(ip, port, banner, status, t, note=None):
    if banner is None:
        return -1
    note = str(note)
    asm = asyncio.Semaphore(200)
    async with asm:
        await aiosqlite.connect(os.path.join(get_dir(), 'ports.db'))
        async with aiosqlite.connect(os.path.join(get_dir(), 'ports.db')) as db:
            await db.execute('insert into results(ip, port, banner, status, time, note) values(?, ?, ?, ?, ?, ?)',
                             (ip, port, banner, status, t, note))
            await db.commit()
            result = await db.execute('select id from results where ip = ? and port = ? and time = ?',
                                      (ip, port, t))
            result = await result.fetchone()
            print(result)
            return result[0]

@ports.post('/custom')
async def add_ip(request: Request):
    data = request.json
    t = time.time()
    print(data)
    try:
        ip = data['ip']
        print("ip")
        # 判断ip是否合法
        assert re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip)
        port = int(data['port'])
        print(port)
        # 判断port是否合法
        assert 0 < port < 65536
        # 判断banner是否存在
        assert data.get('banner', -111111111) != -111111111
        # 判断状态是否合法
        assert data['status'] in ['open', 'closed', 'filtered']
        banner = data['banner']
        status = data['status']
        if status == "open":
            status = 1
        elif status == "closed":
            status = -1
        else:
            status = 0
    except:
        return sanic_json({'status': 'error', 'message': 'invalid data'}, status=400)
    note = data.get("note")
    if banner == "":
        print("get banner")
        banner = await get_banner(ip, port)
        print(banner)
    # 保存数据
    ids = await write_result(ip, port, banner, status, t, note)
    return sanic_json({'status': 'ok', 'id': ids})


@ports.get('/scan_ip')
async def scan_ip(request: Request):
    response = await request.respond(content_type='text/html')
    for port in range(0, 65525):
        banner = ""
        flag = False
        flagT = False
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((request.args.get('ip'), port))
            s.send(b'GET / HTTP/1.1\r\n\r\n')
            banner = s.recv(8192)
            flag = True
            if not "Content-Type" in banner.decode('utf-8'):
                assert False
            banner = banner.decode('utf-8')
        except Exception as e:
            try:
                if flagT:
                    assert False
                s = socket.socket()
                s.settimeout(2)
                s.connect((request.args.get('ip'), port))
                bannerT = s.recv(8192)
                flag = True
                if bannerT != b'':
                    banner = bannerT
                banner = banner.decode('utf-8')
            except Exception as e:
                flagT = True
                pass
        if banner != "" or flag:
            status = 1
            await write_result(request.args.get('ip'), port, banner, status, time.time())
            status = "open"
        else:
            status = "closed"
        await response.send(f"{request.args.get('ip')} {port} {status} {banner} <br>")
    await response.write_eof()
