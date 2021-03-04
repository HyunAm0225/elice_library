from flask import Blueprint, flash
from flask import request, render_template, session, url_for, redirect, jsonify
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
    if comment == None or stars == None:
        flash("모든 항목을 채워주세요")
    new_comment = Comment(comment=comment, stars=stars, user_id=user_id, book_id=book_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('book.detail', book_id=book_id))
