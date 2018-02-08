from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import db, Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    content = Column(Text)
    # user和post一对多关系
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # 通过关系获取 user，这样获取默认返回的是一个列表，设置 uselist=false
    # 让它直接返回 user 对象
    user = relationship('User', backref='posts', uselist=False)
    # topic和post一对多关系
    topic_id = Column(Integer, ForeignKey('topic.id'), nullable=False)
    topic = relationship('Topic', backref='posts', uselist=False)

    def __repr__(self):
        return '<Post:{}>'.format(self.title)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'user': self.user.to_dict(),
            'topic': self.topic.to_dict()
        }
