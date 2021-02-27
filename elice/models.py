from elice import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# 유저 DB


class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
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
    isbn = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    description = db.Column(db.Text())
    link = db.Column(db.String(256))
    img_url = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)


class Rental(db.Model):
    __table_name__ = 'rental'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('rent_set'))
    user = db.relationship('User', backref=db.backref('rent_set'))
    rent_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    return_date = db.Column(db.DateTime, nullable=True, default=None)


class Comment(db.Model):
    __table_name__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(100), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete="CASCADE"), nullable=False)
    book = db.relationship('Book', backref=db.backref('comment_set'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
