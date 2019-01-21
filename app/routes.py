from flask import render_template, flash, redirect, url_for, request, session
import requests
import json
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProfileEditorForm, RecipeSearch, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime

import random # help importing

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    # API - Random
    response_random = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    random_drink = response_random.json()

    response_category = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail')
    category_drink = response_category.json()
    # print(category_drink)

    # data=data['drinks']
    # category_drink=category_drink['drinks'])

    form=PostForm()
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None


    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('explore'))

    return render_template('index.html', title="Home", active_page="home", posts=posts.items, form=form, next_url=next_url, prev_url=prev_url, random_drink=random_drink['drinks'], category_drink=category_drink['drinks'])

@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    # API - Random
    response_random = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    random_drink = response_random.json()

    response_category = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail')
    category_drink = response_category.json()

    form=PostForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('explore'))

    return render_template("index.html", title='Explore', active_page="explore", posts=posts.items, form=form, next_url=next_url, prev_url=prev_url, random_drink=random_drink['drinks'], category_drink=category_drink['drinks'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # DELETE: log successful form submission
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', active_page="signin", form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Signed out successfully!')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you have signed up successfully! Let\'s get mixing!!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', active_page="signup", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = current_user.followed_posts().all()

    return render_template('user.html', title="Profile", active_page="profile", user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/profile_editor', methods=['GET', 'POST'])
@login_required
def profile_editor():
    form = ProfileEditorForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.headline = form.headline.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile_editor'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.headline.data = current_user.headline
        form.bio.data = current_user.bio

    return render_template('profile_editor.html', title='Edit Profile', active_page="profile_editor", form=form)

@app.route('/search/', methods=['GET', 'POST'])
@app.route('/search/<type>/<ing>', methods=['GET', 'POST'])
def search(type='i', ing=''):
    form = RecipeSearch()

    if form.validate_on_submit():
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?{}={}'.format(type, form.ingredient.data))
        data = response.json()

        if type == 'i':
            return render_template('search.html', data=data['drinks'], form=form)

    return render_template('search.html', title="Search", active_page="search", form=form, data='')


@app.route('/recipe', methods=['GET', 'POST'])
@app.route('/recipe/<recipeid>', methods=['GET', 'POST'])
@login_required
def recipe():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('recipe'))
    posts = current_user.followed_posts().all()

    return render_template("recipe.html", title='Recipe', active_page="recipe", form=form, posts=posts)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))

    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You unfollowed {}.'.format(username))

    return redirect(url_for('user', username=username))
