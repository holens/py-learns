#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/14
@desc: Python 3.5 async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：
        把@asyncio.coroutine替换为async；
        把yield from替换为await
"""
# 异步函数（coroutine）
# async def async_function():
#     return 1

# 异步生成器(async_generator)
# async def async_generator():
#     yield 1
import asyncio


@asyncio.coroutine
def hello1():
    print("Hello world!")
    r = yield from asyncio.sleep(1)
    print("Hello again!")


async def hello2():
    print("Hello world!")
    r = await asyncio.sleep(1)
    print("Hello again!")

loop = asyncio.get_event_loop()
tasks = [hello1(), hello2()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()