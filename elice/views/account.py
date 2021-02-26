# account.py
from flask import Blueprint, flash
from flask import request, render_template, session, url_for, redirect, jsonify, g
# from flask_jwt_extended import *
from datetime import timedelta, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from elice import db, bcrypt
from elice.models import User
from elice.forms import UserCreateForm, UserLoginForm

bp = Blueprint("account", __name__, template_folder="templates", url_prefix='/account')

# ACCESS_TOKEN_EXPIRE_MINUTES = 30


@bp.route('/')
def account_main():
    return "account main test"


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not user.check_password(form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('account/login.html', form=form)


@bp.route('/signup/', methods=["POST", "GET"])
def signup():
    form = UserCreateForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(fullname=form.fullname.data,
                        password=bcrypt.generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 이메일입니다.')
    return render_template('account/register.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
