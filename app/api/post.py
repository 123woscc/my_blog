from flask import jsonify, request, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.datastructures import MultiDict

from . import api
from ..models import Post, Comment, db
from .auth import auth
from ..forms import PostForm


@api.route('/post')
def get_post():
    post_id = request.args.get('post_id', 0, type=int)
    if not post_id:
        return jsonify(msg='not data')
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    topic_id = request.args.get('topic_id', 0, type=int)
    if topic_id:
        pagination = Post.query.order_by(
            Post.created_at.desc()).filter_by(topic_id=topic_id).paginate(
                page, per_page=10, error_out=False)
    else:
        pagination = Post.query.order_by(Post.created_at.desc()).paginate(
            page, per_page=10, error_out=False)
    posts = pagination.items
    posts_dict = [p.to_dict() for p in posts]
    return jsonify(posts=posts_dict)


@api.route('/comments')
def get_comments():
    post_id = request.args.get('post_id', 0, type=int)
    if post_id:
        comments = Comment.query.filter_by(post_id=post_id).limit(10).all()
        comments_dict = [c.to_dict() for c in comments]
        return jsonify(comments=comments_dict)
    else:
        return jsonify(comments=[])


@api.route('/posts', methods=['POST'])
@auth.login_required
def create_post():
    # 这个接口需要用户先登录
    # print(request.form)
    formdata = request.form
    print(formdata)
    form = PostForm(formdata=formdata, obj=None, csrf_enabled=False)
    if not form.validate():
        return jsonify(form.errors), 422
    post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=g.current_user.id,
            topic_id=form.topic.data.id)
    db.session.add(post)
    db.session.commit()
    # print(form.topic.data.id)
    # print(g.current_user)
    return jsonify(post.to_dict()), 201
