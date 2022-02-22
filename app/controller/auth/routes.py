from flask import Blueprint, flash, render_template, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.model.user import User
from app.model.blog import Blog
from app.form_validate import ( RegisterValidate, LoginValidate, UpdateAccountValidate,
                                BlogsValidate, RequestResetForm, ResetPasswordForm )
from app.controller.auth import auth_controller

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/post/new', methods=['POST','GET'])
@login_required
def post_new():
    form = BlogsValidate()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = auth_controller.save_picture(form.picture.data, 'static/img_posted')
            post = Blog(title=form.title.data, slug=form.slug.data, content=form.content.data, author=current_user, image_file=image_file)
        else:
            post = Blog(title=form.title.data, slug=form.slug.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('site.home'))
    return render_template('blog/form.html', menu='post', title='New Post', form=form)

@auth.route('/post/<int:post_id>/update', methods=['POST','GET'])
@login_required
def post_update(post_id):
    title = 'Update Post'
    post = Blog.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    form = BlogsValidate()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = auth_controller.save_picture(form.picture.data, 'static/img_posted')
            post.image_file = image_file
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been update!', 'success')
        return redirect(url_for('site.post_detail', post_id=post.id))
    
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.slug.data = post.slug
    return render_template('blog/form.html', menu='post-detail', title=title, form=form)

@auth.route('/post/<int:post_id>/delete', methods=['GET'])
@login_required
def post_delete(post_id):
    post = Blog.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been delete!', 'success')
    return redirect(url_for('site.home'))

@auth.route('/account', methods=['POST','GET'])
@login_required
def account():
    title = 'Your Account'
    form = UpdateAccountValidate()

    if not form.password.data:
        form.password.data = current_user.password
        
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = auth_controller.save_picture(form.picture.data, 'static/img')
            current_user.image_file = picture_file
        
        if form.password.data:
            hashed_password = auth_controller.hashed_password(form.password.data)
            current_user.password = hashed_password
            
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/'+current_user.image_file)
    return render_template('auth/account.html',
                            image_file=image_file,
                            menu='account',
                            title=title,
                            form=form)

@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))

    title = 'Login'
    form = LoginValidate()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and auth_controller.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('site.home'))
        else:
            flash('Login unsuccesful. Please check email and password!', 'danger')
    return render_template('auth/login.html', form=form, menu='login', title=title)

@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))

    title = 'Registration Now'
    form = RegisterValidate()
    if form.validate_on_submit():
        hashed_password = auth_controller.hashed_password(form.password.data)
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=hashed_password
                    )
        db.session.add(user)
        db.session.commit()
        flash('Your acccount has been created!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form, menu='regis', title=title)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))

@auth.route('/reset-password', methods=['GET','POST'])
def reset_password():
    title = 'Reset Password'
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        auth_controller.sen_reset_email(user)
        flash('An email has been sent with instructions to rset your password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, title=title)

@auth.route('/reset-password/<token>', methods=['GET','POST'])
def reset_token():
    title = 'Set new Password'
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is a invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = auth_controller.hashed_password(form.password.data)
        user.password = hashed_password
        flash('Your password has been update!. You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/set_password_new.html', form=form, title=title)