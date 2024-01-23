from db import db


class CityModel(db.Model):

    __tablename__ = "tb_cities"

    cod_city = db.Column(db.Integer, primary_key=True)
    desc_city = db.Column(db.String(80), unique=True, nullable=False)
    qtd_population = db.Column(db.Integer, nullable=False)

    cod_country = db.Column(db.Integer, db.ForeignKey("tb_countries.cod_country"), unique=False, nullable=False)

    country = db.relationship("CountryModel", back_populates="cities")

    sale = db.relationship("SaleModel", back_populates="city", uselist=False)

    