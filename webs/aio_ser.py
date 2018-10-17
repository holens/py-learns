#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/15
@desc: 
"""

from aiohttp import web


async def index(request):
    return web.Response(text="Welcome home!")

async def my_web_app_gunicorn():
    app = web.Application()
    app.router.add_get('/', index)
    return app

def my_web_app():
    app = web.Application()
    app.router.add_get('/index', index)
    return app

if __name__ == '__main__':
    app = my_web_app()
    web.run_app(app, host='0.0.0.0', port=8888)