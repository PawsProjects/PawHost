from sanic import Sanic
from api import api
from home import home
import aiosqlite
import json
import os


def get_dir():
    with open("config.json", 'r') as f:
        config = json.loads(f.read())
    return config['data_dir']


app = Sanic("Furry-Paw")


async def main():
    app.ctx.db = await aiosqlite.connect(os.path.join(get_dir(), 'ports.db'))


main()
app.blueprint(api)
app.blueprint(home)
app.static('/home', './home/static')
app.static('/home/', './home/static/index.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001)
