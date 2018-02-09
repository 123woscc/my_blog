from flask import request, session
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, TextField, SubmitField, SelectField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length, Email, Required, StopValidation, DataRequired
from flask_login import current_user

from app.models import db, User, Topic, Post, Comment


class LoginForm(FlaskForm):
    email = StringField(validators=[
        Required('请输入您的邮箱'),
        Email(message='请输入有效的邮箱地址'),
    ])
    password = PasswordField(validators=[Required('请输入您的密码')])
    submit = SubmitField('登录')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise StopValidation('该邮箱还未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and not user.verify_password(field.data):
            raise StopValidation('密码错误')


class PostForm(FlaskForm):
    def query_factory():
        return db.session.query(Topic).all()

    def get_pk(obj):
        return obj

    title = StringField('标题', validators=[Required()])
    topic = QuerySelectField(
        label=u'脚本名',
        validators=[Required()],
        query_factory=query_factory,
        get_pk=get_pk,
        get_label='name')
    content = TextAreaField(validators=[Required()])
    submit = SubmitField('发布')

    def create_post(self):
        post = Post(
            title=self.title.data,
            content=self.content.data,
            user_id=current_user.id,
            topic_id=self.topic.data.id)
        db.session.add(post)
        db.session.commit()
        return post


class CommentForm(FlaskForm):
    name = StringField('昵称', validators=[Length(1, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Length(4, 64), Email('邮箱格式错误')])
    content = TextAreaField(
        '评论', description='请提出宝贵的意见', validators=[DataRequired()])
    submit = SubmitField('提交')

    def create_comment(self, post_id):
        comment = Comment(
            name=self.name.data,
            email=self.email.data,
            content=self.content.data,
            post_id=post_id
        )
        db.session.add(comment)
        db.session.commit()
        return comment
