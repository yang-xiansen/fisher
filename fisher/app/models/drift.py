#鱼书交易的模型（鱼鳔）
from sqlalchemy import String, Column, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):

    id = Column(Integer, primary_key=True)
    #邮递信息
    recipient_name = Column(String(20), nullable=False) #收件人姓名
    address = Column(String(100), nullable=False)
    mobile = Column(String(20), nullable=False)
    message = Column(String(200))

    #书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_image = Column(String(50))

    #请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    #赠送人的信息
    gifter_id = Column(Integer) #赠送人id
    gift_id = Column(Integer) #书籍id
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)  #交易的状态，如拒绝，同意，撤销。。。


    @property
    def pending(self):
        return PendingStatus(self._pending)    #增加了pending属性， 转换为枚举类型   #返回的不在是数字，而是枚举

    @pending.setter
    def pending(self, status):
        self._pending = status.value   #将枚举转换成数字

    #没有选择模型关联，而是选择了重复用户信息的方法
    # #没有选择模型关联，而是选择了重复用户信息的方法
    # #没有选择模型关联，而是选择了重复用户信息的方法



    # requester = relationship('User')
    # requester_id = Column(Integer, ForeignKey('requester.id'))
    # gift = relationship('Gift')
    # gift_id = Column(Integer, ForeignKey('gift.id'))