from marshmallow import Schema, fields


class PlainCountrySchema(Schema):
    cod_country = fields.Int(dump_only=True)
    desc_country = fields.Str(required=True)


class PlainCitySchema(Schema):
    cod_city = fields.Int(dump_only=True)
    desc_city = fields.Str(required=True)
    qtd_population = fields.Int(required=True)


class PlainProductSchema(Schema):
    cod_product = fields.Int(dump_only=True)
    desc_product = fields.Str(required=True)


class PlainSaleSchema(Schema):
    cod_sale = fields.Int(dump_only=True)
    qtd_web_purchases = fields.Int(required=True)
    qtd_refunds = fields.Int(required=True)


class CityUpdateSchema(Schema):
    qtd_population = fields.Int()


class SaleUpdateSchema(Schema):
    qtd_web_purchases = fields.Int()
    qtd_refunds = fields.Int()


class CountrySchema(PlainCountrySchema):
    cities = fields.List(fields.Nested(PlainCitySchema()), dump_only=True)


class CitySchema(PlainCitySchema):
    cod_country = fields.Int(required=True, load_only=True)
    country = fields.Nested(PlainCountrySchema(), dump_only=True)
    sale = fields.Nested(PlainSaleSchema(), dump_only=True)

class SaleSchema(PlainSaleSchema):
    cod_city = fields.Int(required=True, load_only=True)
    cod_product = fields.Int(required=True, load_only=True)

    city = fields.Nested(PlainCitySchema(), dump_only=True)
    product = fields.Nested(PlainProductSchema(), dump_only=True)
