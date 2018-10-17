#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/12
@desc: 
"""

# 通过g.send(None)或者next(g)启动生成器函数，执行到第一个yield语句结束的位置
# receive=yield value 实际程序只执行了两步，返回value值，并暂停(pause)，并没有执行第3步给receive赋值
# 通过g.send('hello')从上次暂停的位置继续执行赋值给receive
def gen():
    value = 0
    while True:
        receive = yield value
        if receive == "e":
            break
        value = "got:%s" % receive

g = gen()
print(next(g))  # 或者是g.send(None)
print(g.send("hello"))
print(g.send("123456"))
# g.send("e") #会得到StopIteration异常


# Python3.3的yield from语法
# yield from iterable等价于for item in iterable: yield item的缩写版,把生成器的操作委托给另一个生成器
def g1():
    yield range(5)

def g2():
    yield from range(5) #


it1 = g1()
it2 = g2()
for x in it1:
    print(x)

for x in it2:
    print(x)

