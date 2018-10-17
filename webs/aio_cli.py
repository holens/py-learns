#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/14
@desc: 
"""
import  aiohttp
import asyncio

async def func():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://httpbin.org/get") as resp:
            print(resp.status)
            print(await resp.text())

loop = asyncio.get_event_loop()
tasks = [func()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()



# from aiohttp import web
# from aiopg.sa import create_engine
# import sqlalchemy as sa
# from sqlalchemy import sql
#
#
# # 表的SQLAlchemy视图
# metadata = sa.MetaData()
# todos_tbl = sa.Table(
#     'todos', metadata,
#     sa.Column('id', sa.Integer, primary_key=True),
#     sa.Column('name', sa.String(255), unique=True, nullable=False),
#     sa.Column('finished', sa.Boolean(), default=False, nullable=False)
# )
#
#
# # -----------------------------------路由处理器----------------------------------
# # 使用 async with request.app['db'].acquire() as conn 连接数据库
# async def get_all_todos(request):
#     '''
#     获取所有代办事项
#     '''
#     async with request.app['db'].acquire() as conn:
#         todos = []
#         async for row in conn.execute(
#             todos_tbl.select().order_by(todos_tbl.c.id)
#         ):
#             todos.append(
#                 dict(row.items()))
#         return web.json_response(todos)
#
#
# async def get_one_todo(request):
#     '''
#     根据路由中的id参数获取指定代办事项
#     '''
#     id = int(request.match_info['id'])
#     async with request.app['db'].acquire() as conn:
#         result = await conn.execute(
#             todos_tbl.select().where(todos_tbl.c.id == id))
#         row = await result.fetchone()
#
#     if not row:
#         return web.json_response({'error': 'Todo not found'}, status=404)
#
#     return web.json_response(dict(row.items()))
#
#
# async def create_todo(request):
#     '''
#     创建一个新的代办事项
#     '''
#     data = await request.json()
#
#     if 'name' not in data:
#         return web.json_response({'error': '"name" is a required field'})
#
#     name = data['name']
#
#     if not name or not isinstance(name, str):
#         return web.json_response(
#             {'error': '"name" must be a string with at least one character'})
#
#     todo = {'name': name, 'finished': bool(data.get('finished', False))}
#
#     async with request.app['db'].acquire() as conn:
#         async with conn.begin():
#             await conn.execute(todos_tbl.insert().values(todo))
#             result = await conn.execute(
#                 sql.select([sql.func.max(todos_tbl.c.id).label('id')])
#             )
#             new_id = await result.fetchone()
#
#     return web.Response(
#         status=303,
#         headers={
#             'Location': str(
#                 request.app.router['one_todo'].url_for(id=new_id.id))
#         }
#     )
#
#
# async def remove_todo(request):
#     '''
#     清除指定代办事项
#     '''
#     id = int(request.match_info['id'])
#
#     async with request.app['db'].acquire() as conn:
#         result = await conn.execute(
#             todos_tbl.delete().where(todos_tbl.c.id == id))
#
#     if not result.rowcount:
#         return web.json_response({'error': 'Todo not found'}, status=404)
#
#     return web.Response(status=204)
#
#
# async def update_todo(request):
#     '''
#     更新某一条待办事项
#     '''
#     id = int(request.match_info['id'])
#     data = await request.json()
#
#     if 'finished' not in data:
#         return web.json_response(
#             {'error': '"finished" is a required key'}, status=400)
#
#     async with request.app['db'].acquire() as conn:
#         result = await conn.execute(
#             todos_tbl.update().where(todos_tbl.c.id == id).values({
#                 'finished': bool(data['finished'])
#             })
#         )
#
#     if result.rowcount == 0:
#         return web.json_response({'error': 'Todo not found'}, status=404)
#
#     return web.Response(status=204)
#
#
# # -----------------------------数据库连接初始化相关操作-----------------------------
# async def attach_db(app):
#     '''
#     连接数据库并附加到app
#     '''
#     app['db'] = await create_engine(
#         ' '.join([
#             # 或改为你的数据库配置
#             'host=localhost',
#             'port=5432',
#             'dbname=aiotodo',
#             'user=aiotodo',
#             'password=12345'
#         ])
#     )
#
#
# async def teardown_db(app):
#     '''
#     关闭与数据库的连接
#     '''
#     app['db'].close()
#     await app['db'].wait_closed()
#     app['db'] = None
#
#
# async def create_table(engine):
#     '''
#     在数据库中创建新表
#     '''
#     async with engine.acquire() as conn:
#         await conn.execute('DROP TABLE IF EXISTS todos')
#         await conn.execute('''CREATE TABLE todos (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255) NOT NULL UNIQUE,
#             finished BOOLEAN NOT NULL DEFAULT FALSE
#         )''')
#
#
# async def populate_initial_values(engine):
#     '''
#     初始化数据库的内容
#     '''
#     async with engine.acquire() as conn:
#         await conn.execute(todos_tbl.insert().values(
#             {'name': 'Start this tutorial', 'finished': True}))
#         await conn.execute(todos_tbl.insert().values(
#             {'name': 'Finish this tutorial', 'finished': False}))
#
#
# async def setup_todo_table(app):
#     '''
#     创建表并初始化内容，只需执行一次
#     '''
#     await create_table(app['db'])
#     await populate_initial_values(app['db'])
#
#
# # -----------------------------app工厂 - 设置信号与路由处理器----------------------------
# def app_factory(args=()):
#     app = web.Application()
#
#     app.on_startup.append(attach_db)
#     app.on_shutdown.append(teardown_db)
#
#     if '--make-table' in args:
#         app.on_startup.append(setup_todo_table)
#
#     app.router.add_get('/todos/', get_all_todos, name='all_todos')
#     app.router.add_post('/todos/', create_todo, name='create_todo',
#                         expect_handler=web.Request.json)
#     app.router.add_get('/todos/{id:\d+}', get_one_todo, name='one_todo')
#     app.router.add_patch('/todos/{id:\d+}', update_todo, name='update_todo')
#     app.router.add_delete('/todos/{id:\d+}', remove_todo, name='remove_todo')
#     return app