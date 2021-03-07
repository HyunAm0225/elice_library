from flask import Blueprint, render_template, url_for, redirect
from elice.decorator import login_required

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
@login_required
def index():
    return redirect(url_for('book.index'))
