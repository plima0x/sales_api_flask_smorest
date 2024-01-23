from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.sale import SaleModel
from schemas import SaleSchema, SaleUpdateSchema
from db import db


blp = Blueprint("sales", __name__, description="Operations on sales")


@blp.route("/sale/<int:sale_id>")
class Sale(MethodView):
    @blp.response(200, SaleSchema)
    def get(self, sale_id):
        sale = SaleModel.query.get_or_404(sale_id)
        return sale
    
    @blp.arguments(SaleUpdateSchema)
    @blp.response(200, SaleSchema)
    def put(self, sale_data, sale_id):
        sale =  SaleModel.query.get_or_404(sale_id)
        sale.qtd_web_purchases = sale_data.get("qtd_web_purchases")
        sale.qtd_refunds = sale_data.get("qtd_refunds")
        db.session.add(sale)
        db.session.commit()
        return sale

    def delete(self, sale_id):
        sale = SaleModel.query.get_or_404(sale_id)
        try:
            db.session.delete(sale)
            db.session.commit()
        except IntegrityError:
            abort(400, message="The sale cannot be deleted because it has cities associated to it.")
        return {"message": "sale deleted."}


@blp.route("/sale")
class SaleList(MethodView):
    @blp.response(200, SaleSchema(many=True))
    def get(self):
        return SaleModel.query.all()

    @blp.arguments(SaleSchema)
    @blp.response(201, SaleSchema)
    def post(self, sale_data):
        new_sale = SaleModel(**sale_data)
        try:
            db.session.add(new_sale)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Enter a cod_city and a cod_product that is not associated "
                               "with a existing sale")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the sale.")
        return new_sale
