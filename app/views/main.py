from flask import Blueprint, request, render_template

from ..models import Post


main = Blueprint('main', __name__)


@main.route('/')
def index():
    # posts = Post.query.all()`
    page = request.args.get('page', 1, type=int)
    topic_id = request.args.get('topic_id', 0, type=int)
    if topic_id:
        pagination = Post.query.order_by(
            Post.created_at.desc()).filter_by(topic_id=topic_id).paginate(
                page, per_page=10, error_out=False)
    else:
        pagination = Post.query.order_by(Post.created_at.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination, topic_id=topic_id)


@main.route('/about')
def about_me():
    return render_template('about.html')
