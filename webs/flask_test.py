#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/16
@desc: 
"""
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from schema import SchemaError, Schema, Use

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:HelinS1029@47.96.106.101/test_sql"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 30
app.config["SQLALCHEMY_POOL_SIZE"] = 10


api = Api(app)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, doc="id", primary_key=True)
    username = db.Column(db.String(32), doc="用户昵称", unique=True)
    password = db.Column(db.String(64), doc="手机号")
    phone = db.Column(db.String(32), doc="姓名", unique=True)


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

class GetData(Resource):
    def get(self):
        schema = Schema({
            "id": Use(int),
        })
        data, errors = validate_schema(schema, request.args)
        if errors:
            return "参数错误", 400
        user = User.query.filter_by(id=data["id"]).first()
        return {"phone":user.phone, "id":user.id, "password":user.password, "username":user.username}, 200


class PostData(Resource):
    def post(self):
        schema = Schema({
            "username": str,
            "password": str,
            "phone": str,
        })
        data, errors = validate_schema(schema, request.json)
        if errors:
            return "参数错误", 400
        user = User(
            username=data["username"],
            password=data["password"],
            phone=data["phone"]
        )
        db.session.add(user)
        db.session.commit()
        return "OK", 200





api.add_resource(GetData, "/get_data")  # 预加载
api.add_resource(PostData, "/post_data")  # 注册

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=9999)

# gunicorn -b 0.0.0.0:9999 flask_test:app -k gevent
