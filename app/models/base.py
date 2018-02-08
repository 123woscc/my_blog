import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime


db = SQLAlchemy()


# 默认添加创建时间和更新时间
class Base(db.Model):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)
