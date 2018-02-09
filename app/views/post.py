from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required

from ..models import Post, Topic, Comment
from ..forms import PostForm, CommentForm


post = Blueprint('post', __name__, url_prefix='/post')


@post.route('/<int:id>', methods=['GET', 'POST'])
def post_view(id):
    form = CommentForm()
    if form.validate_on_submit():
        form.create_comment(id)
        return redirect(url_for('.post_view', id=id))
    post = Post.query.get(id)
    # 暂时返回10条评论
    comments = Comment.query.order_by(Comment.created_at.desc()).limit(10)
    return render_template('post_view.html', post=post, form=form, comments=comments)


@post.route('/new', methods=['GET', 'POST'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        form.create_post()
        return redirect(url_for('.new_post'))
    return render_template('post_new.html', form=form)


@post.route('/search')
def post_search():
    print(request.form)
    kw = request.args.get('kw', None)
    page = request.args.get('page', 1, type=int)
    if kw:
        pagination = Post.query.filter(Post.title.like('%{}%'.format(kw))).order_by(Post.created_at.desc()).paginate(
            page, per_page=10, error_out=False)
        posts = pagination.items
        total = pagination.total
        return render_template('post_search.html', posts=posts, pagination=pagination, total=total)
    else:
        return redirect(url_for('main.index'))
