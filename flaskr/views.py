import os
import datetime

from flask import abort, Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

# from flaskr import db, login_manager, s3
from flaskr import db, login_manager
from flaskr.models import User, UserPasswordResetToken
from flaskr.forms import LoginForm, RegisterForm, PasswordResetForm, UserForm

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
@login_required
def home():
    user = User.select_user_by_id(current_user.id)
    return render_template('home.html', user=user)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_user_by_email(form.email.data)
        if user and user.is_active and user.validate_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('NEXT')
            if not next:
                next = url_for('app.home')
            return redirect(next)
        elif not user:
            flash('存在しないユーザです')
        elif not user.is_active:
            flash('無効なユーザです、パスワードを再設定してください')
        elif not user.validate_password(form.password.data):
            flash('パスワードが正しくありません')

    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            email=form.email.data
            )
        with db.session.begin(subtransactions=True):
            user.create_new_user()
        db.session.commit()
        token = ''
        with db.session.begin(subtransactions=True):
            token = UserPasswordResetToken.publish_token(user)
        db.session.commit()
        flash('パスワード設定用のURLをメールにてお送りしました。ご確認ください')
        print(f'パスワード設定用URL用token: /password_reset/{token}')
        # メール送信処理
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)

@bp.route('/password_reset/<uuid:token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm(request.form)
    reset_id = UserPasswordResetToken.get_user_id_by_token(token)
    if not reset_id:
        abort(500)
    if request.method == 'POST' and form.validate():
        new_password = form.password.data
        user = User.select_user_by_id(reset_id)
        with db.session.begin(subtransactions=True):
            user.save_new_password(new_password)
            UserPasswordResetToken.delete_token(token)
        db.session.commit()
        flash('パスワードを更新しました')
        # メール送信処理
        return redirect(url_for('app.login'))
    return render_template('password_reset.html', form=form)

@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = UserForm(request.form)
    user_id = current_user.get_id()
    user = User.select_user_by_id(user_id)
    if request.method == 'POST' and form.validate():
        with db.session.begin(subtransactions=True):
            user.username = form.username.data
            user.email = form.email.data
            file = request.files[form.picture_path.name].read()
            if file:
                file_name = user_id + '_' + str(int(datetime.datetime.now().timestamp())) + '.jpg'
                picture_path = 'flaskr/static/user_image/' + file_name
                open(picture_path, 'wb').write(file)
                # picture_path = 'https://sskyh-bucket.s3-ap-northeast-1.amazonaws.com/' + file_name
                # s3.put_object(Body=file, bucket='sskyh-bucket', Key=file_name)
                user.picture_path = 'user_image/' + file_name
        db.session.commit()
        flash('ユーザ情報を更新しました')
    return render_template('user.html', user=user, form=form)
