from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash,check_password_hash
from .base import Base
from flask_login import UserMixin
from ..ext import login_manager


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    _password = Column('password', String(255))


    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return 'Password is not readable!'

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'username': self.username}


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
