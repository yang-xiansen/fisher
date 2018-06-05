from math import floor

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import db, Base
from flask_login import UserMixin
from app import login_manager
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, Base):
    # __tablename__ = 'user1' 改变表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)   #赠送的书籍数目
    receive_counter = Column(Integer, default=0) #索要的书籍数目
    wx_open_id = Column(String(50)) #微信
    wx_name = Column(String(32)) #微信
    _password = Column('password', String(128), nullable=False)

    @property #属性读取
    def password(self):
        return self._password

    @password.setter  #属性写入
    def password(self, raw): #raw原始密码
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # def get_id(self):
    #     return self.id
    #继承了UserMixin该方法不用写了


    #此方法是判断用户能否赠送书籍
    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) !='isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        #不允许一个用户同时赠送多本相同的图书
        #一个用户不能同时成为一本书的赠送者和索要者

        #既不在赠送清单，也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600): #expiration过期时间
        s = Serializer(current_app.config['SECRET_KEY'], expiration) #相当于序列化器
        return s.dumps({'id':self.id}).decode('utf-8') #写入用户中

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))  #提取用户
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    #是否可以发送鱼鳔
    def can_send_drift(self):
        if self.beans < 1:
            return False

        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count() #送出多少本书
        sucess_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()  #成功索要几本书

        return True if \
            floor(sucess_receive_count/2) <= floor(success_gifts_count) \
            else False


    #赠送交易页面显示的用户信息
    @property
    def summary(self):
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.send_counter) + '/' + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))