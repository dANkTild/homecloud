from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class UploadForm(FlaskForm):
    files = FileField("Выберите файлы", validators=[FileRequired()])
