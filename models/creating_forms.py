from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import MultipleFileField


class UploadForm(FlaskForm):
    files = MultipleFileField('File(s) Upload')
