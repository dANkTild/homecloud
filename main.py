from flask import Flask, redirect, render_template
from flask_login import LoginManager

from models import db_session
from models.users import User

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
    return "asdasdasdasd"


if __name__=='__main__':
    db_session.global_init("database/data.db")
    db = db_session.create_session()

    app.run()
