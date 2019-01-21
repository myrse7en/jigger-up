from flask import render_template, flash, redirect, url_for, request, session
import requests
import json
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProfileEditorForm, RecipeSearch
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime
import random # help importing

@app.route('/')
@app.route('/index')
# @login_required
def index():
    # API - Random
    response_random = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    random_drink = response_random.json()

    response_category = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail')
    category_drink = response_category.json()
    print(category_drink)

    # data=data['drinks']
    # category_drink=category_drink['drinks'])
    
    return render_template('index.html', title="Home", random_drink=random_drink['drinks'], category_drink=category_drink['drinks'])

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
    return render_template('login.html', title='Sign In', form=form)

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
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts, title="Profile")

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
    return render_template('profile_editor.html', title='Edit Profile', form=form)

@app.route('/search/', methods=['GET', 'POST'])
@app.route('/search/<type>/<ing>', methods=['GET', 'POST'])
def search(type='i', ing=''):
    form = RecipeSearch()

    if form.validate_on_submit():
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?{}={}'.format(type, form.ingredient.data))
        data = response.json()

        if type == 'i':
            return render_template('search.html', data=data['drinks'], form=form)

    return render_template('search.html', form=form, title="Search", data='')
