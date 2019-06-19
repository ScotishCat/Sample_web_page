from flask import Flask, render_template, url_for, send_from_directory, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
import sqlite3
import os
from wtforms import StringField, SubmitField, validators, PasswordField


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.debug = True
log = app.logger
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

DATABASE_PATH = 'blog.db'
STATIC_PATH = os.path.join(app.root_path, 'static')


class LoginForm(Form):
    login = StringField(
        'Login',
        validators=[
            validators.input_required(),
            validators.email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            validators.input_required(),
            validators.length(min=4, max=8)
        ]
    )
    submit = SubmitField('Submit')


def create_users_table():
    with sqlite3.connect(DATABASE_PATH) as db:
        cursor = db.cursor()

        users_table = ('''CREATE TABLE IF NOT EXISTS user(
            id 	         INTEGER NOT NULL PRIMARY KEY,
            first_name   CHAR(50),
            last_name    CHAR(50),
            email        CHAR(50) NOT NULL,
            phone        CHAR(20),
            password     CHAR(20)
        );''')
        cursor.execute(users_table)


@app.route('/')
def hello():
    print(request.method)
    return render_template(
        'index.html',
        profile_url=url_for('static', filename='profile.png')
    )


@app.route('/profile/<profile_id>')
def profile(profile_id):
    return render_template(
        'profile.html',
        profile_id=profile_id
    )


@app.route('/form', methods=['GET', 'POST'])
def form():
    blog_form = LoginForm()

    create_users_table()

    if blog_form.validate_on_submit():
        mail = blog_form.login.data
        password = blog_form.password.data
        log.info(mail, password)

        with sqlite3.connect(DATABASE_PATH) as db:
            cursor = db.cursor()
            existing_user = cursor.execute(
                "SELECT * from user WHERE email = ?", (mail, )
            ).fetchall()
            if not existing_user:
                new_user = ('INSERT INTO user (id, email, password) '
                            'VALUES(NULL,?,?);')
                cursor.execute(new_user, (mail, password))

        return render_template(
            'index.html',
            profile_url=url_for('static', filename='profile.png'))

    return render_template('form.html', blog_form=blog_form)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH, 'favicon.ico')


@app.route('/profile.png')
def profile_image():
    return send_from_directory(STATIC_PATH, 'profile.png')


if __name__ == '__main__':
    app.run()
