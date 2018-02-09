import random

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask import current_app
from faker import Faker

from app import create_app, db
from app.models import User, Post, Topic

app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app)


# 初始化数据库
@manager.command
def create_db():
    db.drop_all()
    db.create_all()
    print('创建数据库成功!')


# 初始化站点
@manager.command
def create_admin():
    admin = current_app.config['ADMIN']
    user = User(
        username=admin['username'],
        email=admin['email'],
        password=admin['password'])
    db.session.add(user)
    db.session.commit()
    print('创建管理员成功!')
    topic_list = current_app.config['TOPICS']
    for t in topic_list:
        topic = Topic(t, '')
        db.session.add(topic)
        db.session.commit()
    print('创建文章分类成功!')


# 测试使用
@manager.command
def create_test_data():
    # 初始化数据库
    db.drop_all()
    db.create_all()
    print('数据库初始化成功!')
    # 创建管理员
    admin = current_app.config['ADMIN']
    user = User(
        username=admin['username'],
        email=admin['email'],
        password=admin['password'])
    db.session.add(user)
    db.session.commit()
    print('创建管理员成功!')
    # 创建文章分类
    topic_list = ['随笔', 'Python', '其他']
    for t in topic_list:
        topic = Topic(t, '')
        db.session.add(topic)
        db.session.commit()
    print('创建文章分类成功!')
    # 选择作者,默认admin
    topics = Topic.query.all()
    # 创建假数据
    fake = Faker('zh_CN')
    for i in range(100):
        post = Post()
        post.title = fake.sentence(
            nb_words=6, variable_nb_words=True, ext_word_list=None)
        post.content = fake.text(max_nb_chars=200, ext_word_list=None)
        post.user = user
        post.topic = random.choice(topics)
        db.session.add(post)
        db.session.commit()
    print('创建测试数据成功!')


if __name__ == '__main__':
    manager.run()
