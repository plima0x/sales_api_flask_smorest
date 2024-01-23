from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.city import CityModel
from schemas import CitySchema, CityUpdateSchema
from db import db

blp = Blueprint("cities", __name__, description="Operations on cities")


@blp.route("/city/<int:city_id>")
class City(MethodView):
    @blp.response(200, CitySchema)
    def get(self, city_id):
        city = CityModel.query.get_or_404(city_id)
        print(city.sale)
        return city
    
    @blp.arguments(CityUpdateSchema)
    @blp.response(200, CitySchema)
    def put(self, city_data, city_id):
        city = CityModel.query.get_or_404(city_id)
        city.qtd_population = city_data.get("qtd_population")
        db.session.add(city)
        db.session.commit()
     
        return city

    def delete(self, city_id):
        city = CityModel.query.get_or_404(city_id)
        try:
            db.session.delete(city)
            db.session.commit()
        except IntegrityError:
            return abort(400, message="The city cannot be deleted because it has sales associated to it.")
        return {"message": "City deleted."}


@blp.route("/city")
class CityList(MethodView):
    @blp.response(200, CitySchema(many=True))
    def get(self):
        return CityModel.query.all()

    @blp.arguments(CitySchema)
    @blp.response(201, CitySchema)
    def post(self, city_data):
        city = CityModel(**city_data)
        try:
            db.session.add(city)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A city with the data informed already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the city.")
        return city
    