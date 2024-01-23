import os
from flask import Flask
from flask_smorest import Api
from db import db
from resources.country import blp as CountryBlueprint
from resources.city import blp as CityBlueprint
from resources.product import blp as ProductBlueprint
from resources.sale import blp as SaleBlueprint


def create_app():
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Sales by City"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] =  "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)
    api.register_blueprint(CountryBlueprint)
    api.register_blueprint(CityBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(SaleBlueprint)

    return app
