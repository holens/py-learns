from aiohttp import web
from bson.json_util import dumps
import motor.motor_asyncio


app = web.Application()


async def start_background_tasks(app):
    app.client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://47.96.106.101:27017")
    app.db = app.client['test']


app.on_startup.append(start_background_tasks)


async def handle(request):
    rst = await request.app.db.runoob.find_one({}, {"phone":1})
    return web.Response(text=dumps(rst))


app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8888)

