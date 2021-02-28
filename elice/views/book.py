from flask import Blueprint, flash
from flask import request, render_template, session, url_for, redirect, jsonify
from elice.models import Book, Rental
from elice import db
from datetime import datetime
from elice.decorator import login_required


bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/')
@login_required
def index(methods=["GET"]):
    if request.method == "GET":
        books = Book.query.all()
        return render_template("book/index.html", books=books)


@bp.route('/detail/<int:book_id>')
@login_required
def detail(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return render_template('book/detail.html', book=book)


@bp.route('/rent/<int:book_id>', methods=["POST"])
@login_required
def rent(book_id):
    # book_id = request.form.get("book_id")
    user_id = session['user_id']
    book = Book.query.filter_by(id=book_id).first()
    if book.stock < 0:
        error = "책의 재고가 부족합니다."
        flash(error)
    rent_book = Rental(book_id=book_id, user_id=user_id)
    book.stock -= 1
    db.session.add(rent_book)
    db.session.commit()
    return redirect(url_for('book.index'))


@bp.route('/rent_list', methods=["GET"])
@login_required
def rent_list():
    user_id = session['user_id']
    book_rentals = Rental.query.filter_by(user_id=user_id).all()
    return render_template('book/rent_list.html', book_rentals=book_rentals)


@bp.route('/return_list', methods=['GET', 'POST'])
@login_required
def return_list():
    user_id = session['user_id']
    if request.method == "POST":
        book_id = request.form.get("book_id")
        book = Book.query.filter_by(id=book_id).first()
        book.stock += 1
        book_rental = Rental.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
        book_rental.return_date = datetime.now()
        db.session.commit()
        return redirect(url_for('book.return_list'))

    book_rentals = Rental.query.filter_by(user_id=user_id).all()
    not_return_book_list = []
    for book_rental in book_rentals:
        if book_rental.return_date is None:
            not_return_book_list.append(book_rental)
    return render_template('book/return_list.html', return_book_list=not_return_book_list)
