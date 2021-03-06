from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp


class UserCreateForm(FlaskForm):
    fullname = StringField('사용자이름', validators=[DataRequired(), Length(min=2, max=25, message="최소 2글자부터 최대 25글자까지 입력 가능합니다"), Regexp(r'[가-힣A-Za-z]', message='영문이나 한글만 입력 가능합니다')])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다'), Regexp(r'^[A-Z]+[a-z]+[0-9]+[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]+', message='소문자,대문자,특수문자,숫자를 모두 포함해야 합니다'), Length(min=8, max=25, message='8글자 이상 25글자 이하여야 합니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
