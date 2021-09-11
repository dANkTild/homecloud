from flask import Flask, redirect, render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from models import db_session
from models.users import User
from models.users_forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db = db_session.create_session()

        user = db.query(User).filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.passwd.data):
            login_user(user, remember=True)
            return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db = db_session.create_session()

        # TODO: Добавить проверки
        user = User(name=form.name.data,
                    email=form.email.data)
        user.set_password(form.passwd.data)

        login_user(user, remember=True)

        db.add(user)
        db.commit()

    return render_template("registration.html", form=form)


if __name__=='__main__':
    db_session.global_init("database/data.db")
    db = db_session.create_session()

    app.run(debug=True)
