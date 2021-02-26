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
    comment = db.relationship('Comment', backref=db.backref('user'))
    rent = db.relationship('Rent', backref=db.backref('user'))

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
    isbn = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    description = db.Column(db.Text())
    link = db.Column(db.String(256))
    img_url = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    comment = db.relationship('Comment', backref=db.backref('book'))
    rent = db.relationship('Rent', backref=db.backref('book'))


class Rent(db.Model):
    __table_name__ = 'rent'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.String(50), db.ForeignKey('book.book_name', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('user.email', ondelete="CASCADE"), nullable=False)
    rent_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)


class Comment(db.Model):
    __table_name__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(100), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    book_name = db.Column(db.String(50), db.ForeignKey('book.book_name', ondelete="CASCADE"), nullable=False)
    create_user = db.Column(db.String(100), db.ForeignKey('user.email', ondelete="CASCADE"), nullable=False)
