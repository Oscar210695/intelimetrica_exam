from config import db, ma

#Create Restaurant Class
class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.TEXT, primary_key=True)
    rating = db.Column(db.INTEGER)
    name = db.Column(db.TEXT)
    site = db.Column(db.TEXT)
    email = db.Column(db.TEXT)
    phone = db.Column(db.TEXT)
    street = db.Column(db.TEXT)
    city = db.Column(db.TEXT)
    state = db.Column(db.TEXT)
    lat = db.Column(db.REAL) 
    lng = db.Column(db.REAL)

#Create Restaurant Schema
class RestaurantSchema(ma.ModelSchema):
    class Meta:
        model = Restaurant
        sqla_session = db.session