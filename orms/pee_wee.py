#!usr/bin/env python
# coding=utf-8
"""
@time: 2018/10/17
@desc: 
"""
from datetime import date

from peewee import MySQLDatabase, Model, CharField, DateField, IntegerField

mysql_db = MySQLDatabase('test_sql', user='root', password='HelinS1029', host='47.96.106.101', port=3306) # 创建连接

class Person(Model):
    name = CharField(max_length=64, help_text="用户名字", unique=True)
    birthday = DateField(default="2018-10-17")
    is_women = IntegerField()

    class Meta:
        database = mysql_db
        table_name = 'persons'

# 创建表
Person.create_table()
# 添加一条数据
p = Person(name='liuchungui', birthday=date(1990, 12, 20), is_women=True)
p.save()

# 删除姓名为perter的数据
p = Person.delete().where(Person.name == 'perter')
p.execute()

# 已经实例化的数据, 使用delete_instance
p = Person(name='liuchungui', birthday=date(1990, 12, 20), is_women=False)
p.id = 1
p.save()
p.delete_instance()


# 已经实例化的数据,指定了id这个primary key,则此时保存就是更新数据
p = Person(name='liuchungui', birthday=date(1990, 12, 20), is_women=False)
p.id = 1
p.save()

# 更新birthday数据
q = Person.update({Person.birthday: date(1983, 12, 21)}).where(Person.name == 'liuchungui')
q.execute()


# 查询单条数据
p = Person.get(Person.name == 'liuchungui')
print(p.name, p.birthday, p.is_women)

# 使用where().get()查询
p = Person.select().where(Person.name == 'liuchungui').get()
print(p.name, p.birthday, p.is_women)

# 查询多条数据
persons = Person.select().where(Person.is_women == True)
for p in persons:
    print(p.name, p.birthday, p.is_women)


