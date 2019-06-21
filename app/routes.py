from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from flask import render_template, flash, send_from_directory, request
from werkzeug.urls import url_parse


@app.route('/')
def index():
    print(request.method)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('index.html')

    blog_form = LoginForm()

    if blog_form.validate_on_submit():
        user = User.query.filter_by(username=blog_form.username.data).first()

        if user is None or not user.check_password(blog_form.password.data):
            flash('Invalid username or password.')
            return render_template('login.html', blog_form=blog_form)

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = 'index'
        return render_template(f'{next_page}.html')

    return render_template('login.html', blog_form=blog_form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('index.html')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, registration is completed!')
        return render_template('login.html')
    return render_template('register.html', title='Register', form=form)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.STATIC_PATH, 'favicon.ico')


@app.route('/profile.png')
def profile_image():
    return send_from_directory(app.STATIC_PATH, 'profile.png')
