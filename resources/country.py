from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.country import CountryModel 
from schemas import CountrySchema
from db import db

blp = Blueprint("country", __name__, description="Operations on countries")


@blp.route("/country/<int:country_id>")
class Country(MethodView):
    @blp.response(200, CountrySchema)
    def get(self, country_id):
        country = CountryModel.query.get_or_404(country_id)
        return country

    def delete(self, country_id):
        country = CountryModel.query.get_or_404(country_id)
        try:
            db.session.delete(country)
            db.session.commit()
        except IntegrityError:
            abort(400, message="The country cannot be deleted because it has cities associated to it.")
        return {"message": "Country deleted"}


@blp.route("/country")
class CountryList(MethodView):

    @blp.response(200, CountrySchema(many=True))
    def get(self):
        return CountryModel.query.all()
    

    @blp.arguments(CountrySchema)
    @blp.response(201, CountrySchema)
    def post(self, country_data):
        print(country_data)
        country = CountryModel(**country_data)
        try:
            db.session.add(country)
            db.session.commit()
        except IntegrityError:
            abort(400,
                  message="A country with that description already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return country
