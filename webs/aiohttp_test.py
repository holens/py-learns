#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/15
@desc: 
"""
import aiohttp
from sqlalchemy import sql

import sqlalchemy as sa
from aiomysql.sa import create_engine

# 表的SQLAlchemy视图
from schema import Schema, SchemaError

metadata = sa.MetaData()

users = sa.Table(
    'users', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(32), unique=True, nullable=False),
    sa.Column('password', sa.String(64), default=False, nullable=False),
    sa.Column('phone', sa.String(32), unique=True, nullable=False)
)

def validate_schema(schema: Schema, data: dict, remove_blank=False):
    """schema验证,验证成功返回数据，验证失败返回错误信息
    Parameters
    ----------
    schema:Schema: 验证规则
    data: 验证数据
    remove_blank : 是否去除空白字段

    Returns (data,errors)
    -------

    """
    data = {k: v for k, v in data.items()}
    d = {}
    if remove_blank:
        for k, v in data.items():
            if v != "":
                d[k] = v
    else:
        d = data
    try:
        validate_data = schema.validate(d)
        return validate_data, []
    except SchemaError as e:
        return {}, str(e.autos)
    else:
        return validate_data, []

async def attach_db(app):
    app['db'] = await create_engine(user='root', db='test_sql', host='47.96.106.101', password='HelinS1029')

async def teardown_db(app):
    app['db'].close()
    await app['db'].wait_closed()
    app['db'] = None

async def create_table(engine):
    """
    在数据库中创建新表
    """
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS users')
        await conn.execute('''CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(32) NOT NULL UNIQUE,
            password VARCHAR(64) NOT NULL,
            phone  VARCHAR(32) NOT NULL UNIQUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8''')


async def setup_create_table(app):
    await create_table(app['db'])

async def get_datas(request):
    id = int(request.match_info['id'])
    row = None
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(users.select().where(users.c.id == id))
        row = await result.fetchone()

    if not row:
        return aiohttp.web.json_response({'error': 'get_datas not found'}, status=404)
    return aiohttp.web.json_response(dict(row.items()))


async def post_datas(request):
    '''
    创建一个新的代办事项
    '''
    data = await request.json()
    schema = Schema({
        "username": str,
        "password":str,
        "phone":str,
    })
    req, errors = validate_schema(schema, data)
    if errors:
        return aiohttp.web.json_response({'error': '%s'%errors}, status=400)

    async with request.app['db'].acquire() as conn:
        async with conn.begin():
            await conn.execute(users.insert().values(req))
            result = await conn.execute(sql.select([sql.func.max(users.c.id).label('id')]))
            new_id = await result.fetchone()

    return aiohttp.web.Response(
        status=303,
        headers={ 'Location': str(request.app.router['get_data'].url_for(id=str(new_id.id)))}
    )


async def app_factory(*args):
    app = aiohttp.web.Application()
    app.on_startup.append(attach_db)
    app.on_shutdown.append(teardown_db)
    if "--make-table" in args:
        app.on_startup.append(setup_create_table)

    app.router.add_get('/get_data/{id:\d+}', get_datas, name='get_data')
    app.router.add_post('/post_data', post_datas, name='post_data', expect_handler=aiohttp.web.Request.json)
    return app


# if __name__ == '__main__':
#     app = app_factory("--make-table")
#     aiohttp.web.run_app(app, host='0.0.0.0', port=8888)

# gunicorn projects_test:app_factory --bind 0.0.0.0:8888 --worker-class aiohttp.GunicornUVLoopWebWorker

