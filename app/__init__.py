import os
import json

from flask import Flask, jsonify

from .config import configs
from .models import db
from .ext import bootstrap, login_manager, babel, pagedown
from .admin import admin


APP_DIR = os.path.dirname(__file__)


# 注册拓展
def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    babel.init_app(app)
    pagedown.init_app(app)


# 注册蓝图
def register_bluprints(app):
    from .views import main
    from .views import auth
    from .views import post

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(post)


# 注册错误控制
def register_error_hanlers(app):
    @app.errorhandler(404)
    def not_fount(error):
        return jsonify('Not Found'), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify('Server Error'), 500


def register_context_processors(app):
    @app.context_processor
    def topics():
        from .models import Topic
        topics = Topic.query.all()
        return dict(topics=topics)



# 工厂模式
def create_app(config):
    app = Flask(__name__)
    if isinstance(config, dict):
        app.config.update(config)
    else:
        app.config.from_object(configs.get(config, None))

    register_extensions(app)
    register_bluprints(app)
    register_error_hanlers(app)
    register_context_processors(app)

    return app
