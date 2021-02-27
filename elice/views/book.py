from flask import Blueprint
from flask import request, render_template, session, url_for, redirect, jsonify
from elice.models import Book, Rental
from elice import db

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


@bp.route('/rent/<int:book_id>', methods=["POST"])
def rent(book_id):
    # book_id = request.form.get("book_id")
    user_id = session['user_id']
    book = Book.query.filter_by(id=book_id).first()
    if book.stock > 0:
        rent_book = Rental(book_id=book_id, user_id=user_id)
        book.stock -= 1
        db.session.add(rent_book)
        db.session.commit()
        return redirect(url_for('book.index'))
    else:
        return "책의 재고가 부족합니다."
