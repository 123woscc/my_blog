from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    name = Column(String(24))
    email = Column(String(64))
    content = Column(Text)

    # 添加评论, post和comment一对多关系
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship('Post', backref='comments', uselist=False)

    def __repr__(self):
        return '<Comment:{}>'.format(self.id)

    def to_dict(self):
        return {'name': self.name, 'email': self.email, 'content':self.content}
