from flask import Blueprint, flash
from flask import request, render_template, session, url_for, redirect, jsonify
from elice.models import Book, Rental, Comment
from elice import db
from datetime import datetime
from elice.decorator import login_required


bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/')
@login_required
def index():
    page = request.args.get('page', type=int, default=1)
    books = Book.query
    books = books.paginate(page, per_page=8)
    return render_template("book/index.html", books=books)


@bp.route('/detail/<int:book_id>')
@login_required
def detail(book_id):
    book = Book.query.filter_by(id=book_id).first()
    comments = Comment.query.filter_by(book_id=book_id).all()
    # 여기서 처리하는지?.
    return render_template('book/detail.html', book=book, comments=comments)


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

    book_rentals = Rental.query.filter_by(user_id=user_id, return_date=None).all()
    return render_template('book/return_list.html', return_book_list=book_rentals)


@bp.route('/comment/<int:book_id>', methods=["POST"])
def comment(book_id):
    user_id = session['user_id']
    stars = request.form.get("rating")
    comment = request.form.get("comment")
    if comment == None or stars == None:
        flash("모든 항목을 채워주세요")
    new_comment = Comment(comment=comment, stars=stars, user_id=user_id, book_id=book_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('book.detail', book_id=book_id))
