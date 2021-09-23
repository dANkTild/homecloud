import os
from flask import Flask, redirect, render_template, request, session, send_from_directory
from flask_socketio import SocketIO
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from models import db_session
from models.users import User
from models.files import File, Folder
from models.users_forms import LoginForm, RegisterForm
from models.creating_forms import UploadForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, async_mode="eventlet")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return redirect("/login")

    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        f = upload_form.files.data
        f.save(os.path.join("files", f.filename))

    return render_template("files.html", upload_form=upload_form)


@app.route("/files", defaults={"folder_id": None}, methods=["GET", "POST"])
@app.route("/files/", defaults={"folder_id": None}, methods=["GET", "POST"])
@app.route("/files/<int:folder_id>", methods=["GET", "POST"])
def files(folder_id=0):
    if not current_user.is_authenticated:
        return redirect("/login")

    db = db_session.create_session()

    session["folder_id"] = folder_id
    if folder_id is None:
        cur_folder = db.query(Folder).filter_by(name="/",
                                                owner_id=current_user.id).one()
    else:
        cur_folder = db.query(Folder).filter_by(id=folder_id,
                                                owner_id=current_user.id).one()

    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        for file_data in upload_form.files.data:
            file = File(name=file_data.filename, owner_id=current_user.id,
                        parent=cur_folder)
            db.add(file)
            db.commit()
            db.refresh(file)

            file_name = "{}.{}".format(file.id, file.name.split('.')[-1])
            file_data.save(os.path.join("files", file_name))

    return render_template("files.html", folders=cur_folder.folders,
                           files=cur_folder.files,
                           upload_form=upload_form)


@app.route('/view/<int:file_id>')
def view(file_id):
    db = db_session.create_session()
    file = db.query(File).get(file_id)
    filename = "{}.{}".format(file.id, file.name.split('.')[-1])
    return send_from_directory("files", filename)


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

        db.add(user)
        db.commit()
        db.refresh(user)

        login_user(user, remember=True)

        root_folder = Folder(name="/", owner=user)

        db.add(root_folder)
        db.commit()

    return render_template("registration.html", form=form)


@socketio.on("create")
def create_file(params):
    db = db_session.create_session()

    folder_id = session.get("folder_id")

    if folder_id is None:
        cur_folder = db.query(Folder).filter_by(name="/",
                                                owner_id=current_user.id).one()
    else:
        cur_folder = db.query(Folder).filter_by(id=folder_id,
                                                owner_id=current_user.id).one()

    if params["type"] == "folder":
        new = Folder(name=params["name"], owner_id=current_user.id, parent=cur_folder)
    elif params["type"] == "file":
        new = File(name=params["name"], owner_id=current_user.id, parent=cur_folder)

    db.add(new)
    db.commit()
    db.refresh(new)

    if params["type"] == "file":
        name = "{}.{}".format(new.id, new.name.split(".")[-1])
        open("files/{}".format(name), "w").close()


if __name__ == '__main__':
    db_session.global_init("database/data.db")
    db = db_session.create_session()

    socketio.run(app, host='0.0.0.0', debug=True)
