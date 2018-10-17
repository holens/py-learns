#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/17
@desc: 
"""
class MyObject(object):
    def __init__(self, *args, **kwargs):
        self.init()

    def init(self):
        pass


class SubObject(MyObject):
    def init(self):
        self.a = 100


obj = SubObject()
print(obj.a)