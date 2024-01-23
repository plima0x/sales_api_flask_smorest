from db import db


class SaleModel(db.Model):
    __tablename__ = "tb_sales"

    cod_sale = db.Column(db.Integer, primary_key=True)
    qtd_web_purchases = db.Column(db.Integer, unique=False, nullable=False)
    qtd_refunds = db.Column(db.Integer, unique=False, nullable=False)
    cod_city = db.Column(db.Integer, db.ForeignKey("tb_cities.cod_city"), unique=True, nullable=False)
    cod_product = db.Column(db.Integer, db.ForeignKey("tb_products.cod_product"), unique=False, nullable=False)

    city = db.relationship("CityModel", back_populates="sale")
