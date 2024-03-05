from flask import render_template, redirect, url_for, flash, request, abort
from blog import app, db
from blog.forms import RegisterForm, LoginForm, UpdateProfileForm, PostForm
from blog.models import UserModel, PostModel
from blog import bcrypt
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def home():
    posts = PostModel.query.all()
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('you are already logged in', 'info')
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserModel(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('you registered successfully', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('you are already logged in', 'info')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('you logged in successfully', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            flash('Email or password is wrong', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you logged out successfully', 'success')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your profile updated', 'success')
        return redirect('profile')
    else:
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', form=form)


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = PostModel(title=form.title.data, content=form.content.data, auther_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('post created', 'info')
        return redirect(url_for('profile'))
    return render_template('create_post.html', form=form)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = PostModel.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


@app.route('/post/<int:post_id>/delete')
def post_delete(post_id):
    post = PostModel.query.get_or_404(post_id)
    if post.auther != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post deleted', 'info')
    return redirect(url_for('home'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def post_update(post_id):
    post = PostModel.query.get_or_404(post_id)
    if post.auther != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('post is updated', 'info')
        return redirect(url_for('post_detail', post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('post_update.html', form=form)
