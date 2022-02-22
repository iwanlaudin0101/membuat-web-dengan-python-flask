from flask import Blueprint, render_template, redirect, request, url_for, abort
from app import db
from app.controller.site import site_controller
from app.model.user import User
from app.model.blog import Blog

site = Blueprint('site', __name__)

@site.route('/')
@site.route('/home')
def home():
    title = 'Home'
    page = request.args.get('page', 1, type=int)
    posts = Blog.query.order_by(Blog.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home/home.html', menu='home', title=title, posts=posts)

@site.route('/user/<string:name>')
def user_posted(name):
    title = 'User Posted'
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(name=name).first_or_404()
    posts = Blog.query.filter_by(author=user)\
        .order_by(Blog.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('home/post_filter.html', title=title, posts=posts, user=user)

@site.route('/post/<string:post_slug>')
def post_detail(post_slug):
    post = Blog.query.filter_by(slug=post_slug).first_or_404()
    post.views+=1
    db.session.commit()
    return render_template('home/post_detail.html', menu='post-detail', title=post.title, post=post)