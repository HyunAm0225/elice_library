from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import *
import config

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
bcrypt = Bcrypt()
api = Api()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SECRET_KEY'] = 'bee11777d0d22065bdb8fc7edafb0557'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ORM
    db.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, account, book, comment
    app.register_blueprint(main_views.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(book.bp)
    app.register_blueprint(comment.bp)

    return app
