from db import db


class CountryModel(db.Model):
    __tablename__ = "tb_countries"

    cod_country = db.Column(db.Integer, primary_key=True)
    desc_country = db.Column(db.String(80), unique=True, nullable=False)

    cities = db.relationship("CityModel", back_populates="country", lazy="dynamic")

    