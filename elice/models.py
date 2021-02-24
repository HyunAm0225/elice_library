from elice import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
# 유저 DB


class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = password

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        print(f"디비에 저장된 비밀번호 {self.password}")
        print(f"입력한 비밀번호 해쉬 {bcrypt.generate_password_hash(password).decode('utf-8')}")
        return bcrypt.check_password_hash(self.password, password)


class Book(db.Model):
    __table_name__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(50), unique=True, nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    description = db.Column(db.Text())
    link = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(50), nullable=False)
