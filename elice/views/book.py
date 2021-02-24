from flask import Blueprint
from flask import request, render_template, session, url_for, redirect, jsonify

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/')
def index():
    return 'book page test'
