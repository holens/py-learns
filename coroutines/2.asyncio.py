#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/14
@desc: Python 3.4版本引入的标准库
"""
import asyncio

@asyncio.coroutine
def smart_fab(n):
    dex, a, b = 0, 0, 1
    while dex < n:
        yield from asyncio.sleep(1)
        print("sleep 1")
        a, b = b, a+b
        dex += 1

@asyncio.coroutine
def stupid_fab(n):
    dex, a, b = 0, 0, 1
    while dex < n:
        yield from asyncio.sleep(5)
        print("sleep 5")
        a, b = b, a+b
        dex += 1

loop = asyncio.get_event_loop()
tasks = [smart_fab(10), stupid_fab(20)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()