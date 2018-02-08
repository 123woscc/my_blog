from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request


from ..models import db, User, Post, Topic


admin = Admin(name='后台管理系统')


class AdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username=='admin':
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


admin.add_view(AdminModelView(User, db.session, name='用户', category='数据库'))
admin.add_view(AdminModelView(Post, db.session, name='文章', category='数据库', endpoint='posts'))
admin.add_view(AdminModelView(Topic, db.session, name='话题', category='数据库'))
