from db import db


class ProductModel(db.Model):

    __tablename__ = "tb_products"
    
    cod_product = db.Column(db.Integer, primary_key=True)
    desc_product = db.Column(db.String(80), unique=True, nullable=False)