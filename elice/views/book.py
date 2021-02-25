from flask import Blueprint
from flask import request, render_template, session, url_for, redirect, jsonify
from elice.models import Book

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/')
def index(methods=["GET"]):
    if request.method == "GET":
        books = Book.query.all()
        return render_template("book/index.html", books=books)


@bp.route('/detail/<int:book_id>')
def detail(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return render_template('book/detail.html', book=book)
