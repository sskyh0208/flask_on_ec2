from wtforms import Form, ValidationError
from wtforms.fields import StringField, PasswordField, SubmitField, FileField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo
from flask import flash
from flask_login import current_user

from flaskr.models import User, ProjectType


class LoginForm(Form):
    email = StringField('メールアドレス', validators=[DataRequired(), Email('メールアドレスに誤りがあります')])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class RegisterForm(Form):
    email = StringField('メール', validators=[DataRequired(), Email('メールアドレスに誤りがあります')])
    username = StringField('名前', validators=[DataRequired()])
    submit = SubmitField('登録')

    def validate_email(self, field):
        if User.select_user_by_email(field.data):
            raise ValidationError('そのメールアドレスは既に登録されています')

class PasswordResetForm(Form):
    password = PasswordField('パスワード', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')])
    confirm_password = PasswordField('パスワード確認', validators=[DataRequired()])
    submit = SubmitField('更新')

    def validate_password(self, field):
        if len(field.data) < 8:
            return ValidationError('パスワードは8文字以上です')

class UserForm(Form):
    email = StringField('メールアドレス', validators=[DataRequired(), Email('メールアドレスが誤っています')])
    username = StringField('名前', validators=[DataRequired()])
    picture_path = FileField('画像アップロード')
    submit = SubmitField('更新')

    def validate(self):
        if not super(Form, self).validate():
            return False
        user = User.select_user_by_email(self.email.data)
        if user:
            if user.id != int(current_user.get_id()):
                flash('そのメールアドレスは既に登録されています')
                return False
        return True

class ProjectForm(Form):
    name = StringField('プロジェクト名', validators=[DataRequired()])
    type = SelectField('種別', coerce=int)
    price = FloatField('費用', validators=[DataRequired()])
    time = FloatField('工数', validators=[DataRequired()])
    submit = SubmitField('登録')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_project_types()
        
    def _set_project_types(self):
        project_types = ProjectType.query.all()
        self.type.choices = [(project_type.id, project_type.name) for project_type in project_types]