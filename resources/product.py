from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.product import ProductModel
from schemas import PlainProductSchema
from db import db

blp = Blueprint("products", __name__, description="Operations on products")


@blp.route("/product/<int:product_id>")
class Product(MethodView):
    @blp.response(200, PlainProductSchema)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product

    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        try:
            db.session.delete(product)
            db.session.commit()
        except IntegrityError:
            abort(400, message="The product cannot be deleted because it has sales associated to it.")
        return {"message": "Product deleted."}


@blp.route("/product")
class ProductList(MethodView):
    @blp.response(200, PlainProductSchema(many=True))
    def get(self):
        return ProductModel.query.all()

    @blp.arguments(PlainProductSchema)
    @blp.response(201, PlainProductSchema)
    def post(self, product_data):
        try:
            new_product = ProductModel(**product_data)
            db.session.add(new_product)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A product with the data informed already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the product.")
        return new_product
