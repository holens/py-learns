#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/12
@desc: 
"""

from wsgiref.simple_server import make_server

# application
def application(environ, start_response):
    """
        :param environ: 一个包含所有HTTP请求信息的dict对象
        :param start_response: 一个发送HTTP响应的函数
        :return:
    """
    status = '200 OK'
    from io import StringIO
    stdout = StringIO()
    for k, v in environ.items():
        print(f"{k}, {v}", file=stdout)
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)  # #start_response接收两参数：HTTP响应码，HTTP Header(key,value)用tuple表示
    return [stdout.getvalue().encode("utf-8")]


print('Serving HTTP on port 8000...')
# create server, IP address, port number, application
httpd = make_server('0.0.0.0', 8000, application)

#开始监听HTTP请求
httpd.serve_forever()