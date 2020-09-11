from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLALchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLALchemy(app)


class User(db.Model):
    id = db.column(db.integer, primary_key=True)
    username = db.column(db.string(20), unique=True, nullable=False)
    email = db.column(db.string(120), unique=True, nullable=False)
    image_file = db.column(db.string(20),  nullable=False, default='default.jpg')
    password = db.column(db.string(20),  nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"user('{self.username}', '{self.email}', '{self.image_file}')"


class post(db.Model):
    id = db.column(db.integer, primary_key=True)
    title = db.column(db.string(20), nullable=False)
    date_posted = db.column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.column(db.string(20), nullable=False)
    user_id = db.column(db.integer, db.foreignkey('user.id'), nullable=False)

    def __repr__(self):
        return f"user('{self.title}', '{self.date_posted}')"
        







posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
