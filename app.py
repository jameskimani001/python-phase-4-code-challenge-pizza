#!/usr/bin/env python3
# app.py
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Restaurant, RestaurantPizza, Pizza  # Import models here
import os

# Set up database URI and application configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False  # Format JSON output nicely

# Initialize migration object and DB
migrate = Migrate(app, db)
db.init_app(app)

# -------------------- CRUD for Restaurants --------------------

# Route for GET /restaurants
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200

# Route for GET /restaurants/<int:id>
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    # Include restaurant_pizzas in the response
    restaurant_data = restaurant.to_dict()
    restaurant_data["restaurant_pizzas"] = [
        restaurant_pizza.to_dict() for restaurant_pizza in restaurant.restaurant_pizzas
    ]
    
    return jsonify(restaurant_data), 200

# Route for POST /restaurants
@app.route("/restaurants", methods=["POST"])
def create_restaurant():
    data = request.get_json()
    
    name = data.get("name")
    address = data.get("address")
    
    if not name or not address:
        return jsonify({"error": "Name and address are required"}), 400
    
    try:
        new_restaurant = Restaurant(name=name, address=address)
        db.session.add(new_restaurant)
        db.session.commit()
        
        return jsonify(new_restaurant.to_dict()), 201  # Return created restaurant
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal error

# Route for PUT /restaurants/<int:id>
@app.route("/restaurants/<int:id>", methods=["PUT"])
def update_restaurant(id):
    data = request.get_json()
    
    restaurant = Restaurant.query.get(id)
    
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    name = data.get("name")
    address = data.get("address")
    
    if name:
        restaurant.name = name
    if address:
        restaurant.address = address
    
    try:
        db.session.commit()
        return jsonify(restaurant.to_dict()), 200  # Return updated restaurant
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal error

# Route for DELETE /restaurants/<int:id>
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    db.session.delete(restaurant)
    db.session.commit()
    
    return '', 204  # Empty response body with 204 status code

# -------------------- CRUD for Pizzas --------------------

# Route for GET /pizzas
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas]), 200

# Route for GET /pizzas/<int:id>
@app.route("/pizzas/<int:id>", methods=["GET"])
def get_pizza(id):
    pizza = Pizza.query.get(id)
    
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404
    
    return jsonify(pizza.to_dict()), 200

# Route for POST /pizzas
@app.route("/pizzas", methods=["POST"])
def create_pizza():
    data = request.get_json()
    
    name = data.get("name")
    ingredients = data.get("ingredients")
    
    if not name or not ingredients:
        return jsonify({"error": "Name and ingredients are required"}), 400
    
    try:
        new_pizza = Pizza(name=name, ingredients=ingredients)
        db.session.add(new_pizza)
        db.session.commit()
        
        return jsonify(new_pizza.to_dict()), 201  # Return created pizza
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal error

# Route for PUT /pizzas/<int:id>
@app.route("/pizzas/<int:id>", methods=["PUT"])
def update_pizza(id):
    data = request.get_json()
    
    pizza = Pizza.query.get(id)
    
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404
    
    name = data.get("name")
    ingredients = data.get("ingredients")
    
    if name:
        pizza.name = name
    if ingredients:
        pizza.ingredients = ingredients
    
    try:
        db.session.commit()
        return jsonify(pizza.to_dict()), 200  # Return updated pizza
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal error

# Route for DELETE /pizzas/<int:id>
@app.route("/pizzas/<int:id>", methods=["DELETE"])
def delete_pizza(id):
    pizza = Pizza.query.get(id)
    
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404
    
    db.session.delete(pizza)
    db.session.commit()
    
    return '', 204  # Empty response body with 204 status code

# -------------------- CRUD for RestaurantPizza --------------------

# Route for POST /restaurant_pizzas
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")
    price = data.get("price")

    try:
        # Validate price (should be between 1 and 30)
        if not (1 <= price <= 30):
            return jsonify({"errors": ["Price must be between 1 and 30."]}), 400

        # Create the new RestaurantPizza object
        new_restaurant_pizza = RestaurantPizza(
            pizza_id=pizza_id,
            restaurant_id=restaurant_id,
            price=price
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        # Return the newly created RestaurantPizza as JSON
        return jsonify(new_restaurant_pizza.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": ["An error occurred."]}), 500  # General error handling

# Route for DELETE /restaurant_pizzas/<int:id>
@app.route("/restaurant_pizzas/<int:id>", methods=["DELETE"])
def delete_restaurant_pizza(id):
    restaurant_pizza = RestaurantPizza.query.get(id)
    
    if not restaurant_pizza:
        return jsonify({"error": "RestaurantPizza not found"}), 404
    
    db.session.delete(restaurant_pizza)
    db.session.commit()
    
    return '', 204  # Empty response body with 204 status code

if __name__ == "__main__":
    app.run(port=5555, debug=True)
