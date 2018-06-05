from contextlib import contextmanager

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger


#重写filter_by方法
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys(): #status逻辑删除
           kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

db = SQLAlchemy(query_class=Query)   #替换query


class Base(db.Model):
    __abstract__ = True #设置成基类表，没有主键
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)   #逻辑删除

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):  #判断form表中的字段是否有模型表中的字段(python动态语言的特性)
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    #时间转换
    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
