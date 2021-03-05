from flask import Blueprint, flash
from flask import request, render_template, session, url_for, redirect, jsonify, g
from elice.models import Book, Rental, Comment
from elice import db
from datetime import datetime
from elice.decorator import login_required
import math


bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/<int:book_id>', methods=["POST"])
def comment(book_id):
    user_id = session['user_id']
    stars = request.form.get("rating")
    comment = request.form.get("comment")
    book = Book.query.filter_by(id=book_id).first()
    comment_user = None
    if Comment.query.filter_by(user_id=user_id).first():
        comment_user = Comment.query.filter_by(user_id=user_id).first().user_id
    if user_id == comment_user:
        flash(f"이미 댓글을 작성하셨습니다.")
        return redirect(url_for('book.detail', book_id=book_id))
    if comment == None or stars == None:
        flash("모든 항목을 채워주세요")
        return redirect(url_for('book.detail', book_id=book_id))
    new_comment = Comment(comment=comment, stars=stars, user_id=user_id, book_id=book_id)
    db.session.add(new_comment)
    db.session.commit()
    book.update_rating_stars(book.comment_set)
    db.session.commit()
    return redirect(url_for('book.detail', book_id=book_id))
