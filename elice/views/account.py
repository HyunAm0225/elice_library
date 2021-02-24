# account.py
from flask import Blueprint
from flask import request, render_template, session, url_for, redirect, jsonify
from flask_jwt_extended import *
from datetime import timedelta, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from elice import db, bcrypt
from elice.models import User

bp = Blueprint("account", __name__, template_folder="templates", url_prefix='/account')

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@bp.route('/')
def account_main():
    return "account main test"


@bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify(message="user가 없거나 비밀번호가 틀립니다.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        identity=email, expires_delta=access_token_expires)
    return jsonify(access_token=access_token)


@bp.route('/signup', methods=["POST"])
def signup():
    email = request.form['email']
    fullname = request.form['fullname']
    password1 = request.form['password1']
    password2 = request.form['password2']
    user = User.query.filter_by(email=email).first()
    if password1 != password2:
        return jsonify(message="비밀번호를 다시 확인해 주세요.")
    if user:
        return jsonify(message="이미 같은 아이디가 존재합니다.")

    new_user = User(email=email, fullname=fullname, password=bcrypt.generate_password_hash(password1).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="회원가입 성공!")
