"""
Module that supports all the CRUD operations and statistics endpoint
"""
import json
import pandas as pd
from flask import make_response, abort
from config import db
from models import Restaurant, RestaurantSchema
from math import radians
from geopy import distance

#Function that returns all the rows /api/restaurant GET
def read_all():
    #List of restaurant
    res = Restaurant.query.order_by(Restaurant.name).all()

    # Serialize the data
    restaurant_schema = RestaurantSchema(many=True)
    data = restaurant_schema.dump(res)
    return data

#Function that returns a especific row by ID /api/restaurant/{id]} GET
def read_one(id):
    #Get the row by id
    res = Restaurant.query.filter(Restaurant.id == id).one_or_none()

    #Condition if exists
    if res is not None:
        # Serialize the data for the response
        restaurant_schema = RestaurantSchema()
        data = restaurant_schema.dump(res)
        return data

    #If not catch an error
    else:
        abort(
            404,
            "Restaurant not found for Id: id".format(id=id),
        )

#Function tha allow insert a row /api/restaurant POST
def create(restaurant):

    #Setting the rows to insert
    id = restaurant.get("id")
    rating = restaurant.get("rating")
    name = restaurant.get("name")
    site = restaurant.get("site")
    email = restaurant.get("email")
    phone = restaurant.get("phone")
    street = restaurant.get("street")
    city = restaurant.get("city")
    state = restaurant.get("state")
    lat = restaurant.get("lat")
    lng = restaurant.get("lng")

    #Boolean if row already exists by ID
    existing_restaurant = (
        Restaurant.query.filter(Restaurant.id == id)
        .one_or_none()
    )

    #Condition if already exists
    if existing_restaurant is None:
        #Create a restaurant instance using the schema 
        schema = RestaurantSchema()
        new_restaurant = schema.load(restaurant, session=db.session)

        #Insert row to the DB
        db.session.add(new_restaurant)
        db.session.commit()

        #Serialize and return the newly created row
        data = schema.dump(new_restaurant)

        return data, 201

    #If not exists catch an error
    else:
        abort(
            409,
            "Restaurant {id} already exists".format(
                id=id
            ),
        )

#Function that update a row by ID /api/restaurant/{id} PUT
def update(id, restaurant):
    #Get the row requested from the db
    update_restaurant = Restaurant.query.filter(
        Restaurant.id == id
    ).one_or_none()

    #Setting the rows to update
    rating=restaurant.get("rating")
    name=restaurant.get("name")
    site=restaurant.get("site")
    email=restaurant.get("email")
    phone=restaurant.get("phone")
    street=restaurant.get("street")
    city=restaurant.get("city")
    state=restaurant.get("state")
    lat=restaurant.get("lat")
    lng=restaurant.get("lng")

    #Boolean if row already exists by ID
    existing_restaurant = (
        Restaurant.query.filter(Restaurant.id == id)
        .one_or_none()
    )

    #If not exists catch an error
    if existing_restaurant is None:
        abort(
            404,
            "Restaurant not found for Id: {id}".format(id=id),
        )

    #If exists and check if already exists in DB
    elif (
        existing_restaurant is not None and existing_restaurant.name == name
    ):
        abort(
            409,
            "Restaurant {name} exists already".format(
                name=name
            ),
        )

    #Otherwise update the row
    else:
        #Create a restaurant instance using the schema
        schema = RestaurantSchema()
        update = schema.load(restaurant, session=db.session)

        #Set the id to the row that we want to update
        update.id = update_restaurant.id

        #Merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        #Return updated row
        data = schema.dump(update_restaurant)

        return data, 200

#Function that delete a row by ID /api/restaurant/{id} DELETE
def delete(id):
    #Get the row requested
    res = Restaurant.query.filter(Restaurant.id == id).one_or_none()

    #Condition if row exists
    if res is not None:
        db.session.delete(res)
        db.session.commit()
        return make_response(
            "Restaurant {id} deleted".format(id=id), 200
        )

    #If not exists catch an error
    else:
        abort(
            404,
            "Restaurant not found for Id: {id}".format(id=id),
        )

#Function that calculate the rows in input coordenates returning Count, Average and Standard Deviation /api/restaurant/statistics PUT
def statistics(coordenates):
    #Intitialize variables
    dictFinal = {}
    final_data= []

    #Get all rows
    res = Restaurant.query.order_by(Restaurant.name).all()

    #Serialize the data for the response
    restaurant_schema = RestaurantSchema(many=True)
    data = restaurant_schema.dump(res)

    #Convert result into Dataframe
    datos = pd.DataFrame(data)

    #Setting variables 
    lat1 = float(coordenates["latitude"])
    lng1 = float(coordenates["longitude"])

    #Convert variables into radians
    lat1, lng1 = map(radians, [lat1, lng1])

    #Iterate over all rows
    for x,y in datos.iterrows():
        #Setting variables of corresponding row
        lat2 = radians(y['lat'])
        lng2 = radians(y['lng'])

        #Create tuples with values of the corresponding row
        center_point_tuple = tuple([lat1, lng1]) 
        test_point_tuple = tuple([lat2, lng2]) 
        
        #Check distance between center and coordenates of the previous row
        dis = distance.distance(center_point_tuple, test_point_tuple).meters

        #Validate if distance is less or equal from the radius
        if dis <= int(coordenates["radius"]):
            final_data.append(y)

    #Create dataframe with records that meet the condition
    df = pd.DataFrame(final_data)

    #Create a dictionary with the final values (Count, Average and Standard Deviation) to return
    dictFinal['count'] = str(df['name'].count())
    dictFinal['avg'] = str(df['rating'].mean())
    dictFinal['std'] = str(df['rating'].std())

    json_data = json.dumps(dictFinal)

    return json_data, 200
