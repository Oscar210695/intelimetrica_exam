import os
import pandas as pd
from config import db
from models import Restaurant

#CSV to load into DB restaurant into table restaurant
RESTAURANT = pd.read_csv('https://recruiting-datasets.s3.us-east-2.amazonaws.com/restaurantes.csv', header=0)

#Delete DB if exists
if os.path.exists("restaurant.db"):
    os.remove("restaurant.db")

#Create restaurant
db.create_all()

#Iterate over the file and populate the database
for key,res in RESTAURANT.iterrows():
    r = Restaurant(id=res["id"], rating=res["rating"], name=res["name"], site=res["site"], email=res["email"],
                   phone=res["phone"], street=res["street"], city=res["city"], state=res["state"], lat=res["lat"],
                   lng=res["lng"])
    db.session.add(r)

db.session.commit()

