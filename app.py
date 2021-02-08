from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship, backref
Base = declarative_base()

from flask_cors import CORS

# from flask.ext.cors import CORS
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)
cors = CORS(app)
# migrate = Migrate(app, db) 
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

#association table 
# product_ingredient = Table('product_ingredient',Base.metadata,
#     db.Column('product_id', 
#                 db.Integer, 
#                 db.ForeignKey('product.id')
#                 ),
#     db.Column('ingredient_id', 
#                 db.Integer, 
#                 db.ForeignKey('ingredient.id'
#                 )))


class Product(db.Model):
    # __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    image_url = db.Column(db.String)
    ingredients = db.Column(db.Text)
    # ingredient_relationship = db.relationship('ingredient', 
    #                                             secondary=product_ingredient, 
    #                                             lazy='subquery',
    #                                             backref=db.backref('products', lazy='dynamic'))
                                                
    # Constructor
    def __init__(self, name, description, image_url, ingredients):
        self.name = name
        self.description = description
        self.image_url = image_url
        self.ingredients = ingredients


@app.route("/products", methods=["GET", "POST", "DELETE"])
def products():
    method = request.method
    if (method.lower() == "get"): # READ
        products = Product.query.all()
        return jsonify([{"id": i.id, 
                        "name": i.name, 
                        "description": i.description,
                        "image_url": i.image_url, 
                        "ingredients": i.ingredients} for i in products]) # Get all values from db
    elif (method.lower() == "post"): # CREATE
        try:
            name = request.json["name"]
            description = request.json["description"]
            image_url = request.json["image_url"]
            ingredients = request.json["ingredients"]
            if (name and description and image_url and ingredients): # Checks if name, desc, image_url, ingred are empty
                try:
                    product = Product(name, description, image_url, ingredients) # Creates a new record
                    db.session.add(product) # Adds the record for committing
                    db.session.commit() # Saves our changes
                    return jsonify({"success": True})
                except Exception as e:
                    return ({"error": e})
            else:
                return jsonify({"error": "Invalid form"}) # jsonify converts python vars to json
        except Exception as e:
            return jsonify({"error": e})
    elif (method.lower() == "delete"): # DESTROY
        try:
            pid = request.json["id"]  #pid - product id
            if (pid):
                try:
                    product = Product.query.get(pid) # Gets product with id = pid (because id is primary key)
                    db.session.delete(product) # Delete the product
                    db.session.commit() # Save
                    return jsonify({"success": True})
                except Exception as e:
                    return jsonify({"error": e})
            else:
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "m"})

# view single item 
@app.route('/products/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'GET':
        response = {"id": product.id, 
                    "name": product.name, 
                    "description": product.description,
                    "image_url": product.image_url, 
                    "ingredients": product.ingredients
                    }
        return {"product": response}

    elif request.method == 'PUT':
        data = request.get_json()
        product.name = data['name']
        product.description = data['description']
        product.image_url = data['image_url']
        product.ingredients = data['ingredients']
        db.session.add(product)
        db.session.commit()
        return {"message": f"Product: {product.name} successfully updated"}

    # elif request.method == 'DELETE':
    #     db.session.delete(product)
    #     db.session.commit()
    #     return {"message": f"Product {product.name} successfully deleted."}



# INGREDIENTS DB 
class Ingredient(db.Model):
    # __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    alt_names = db.Column(db.String)
    description = db.Column(db.String)
    purpose = db.Column(db.String)
    safety = db.Column(db.String)
    image_url = db.Column(db.String)
    quick_facts = db.Column(db.String)

    # Constructor
    def __init__(self, name, alt_names, description, purpose, safety, image_url, quick_facts):
        self.name = name
        self.alt_names = alt_names
        self.description = description
        self.purpose = purpose
        self.safety = safety
        self.image_url = image_url
        self.quick_facts = quick_facts


@app.route("/ingredients", methods=["GET", "POST", "DELETE"])
def ingredient():
    method = request.method
    if (method.lower() == "get"): # READ
        ingredient = Ingredient.query.all()
        return jsonify([{"id": i.id, 
                        "name": i.name, 
                        "description": i.description, 
                        "purpose" : i.purpose, 
                        "safety": i.safety,
                        "image_url": i.image_url, 
                        "quick_facts": i.quick_facts} for i in ingredient]) # Get all values from db
    elif (method.lower() == "post"): # CREATE
        try:
            name = request.json["name"]
            alt_names = request.json["alt_names"]
            description = request.json["description"]
            purpose = request.json["purpose"]
            safety = request.json["safety"]
            image_url = request.json["image_url"]
            quick_facts = request.json["quick_facts"]
            if (name and alt_names and description and purpose and safety and image_url and quick_facts): # Checks if name, desc, image_url, ingred are empty
                try:
                    ingredient = Ingredient(name, alt_names, description, purpose, safety, image_url, quick_facts) # Creates a new record
                    db.session.add(ingredient) # Adds the record for committing
                    db.session.commit() # Saves our changes
                    return jsonify({"success": True})
                except Exception as e:
                    return ({"error": e})
            else:
                return jsonify({"error": "Invalid form"}) # jsonify converts python vars to json
        except Exception as e:
            return jsonify({"error": e})
    elif (method.lower() == "delete"): # DESTROY
        try:
            i_id = request.json["id"]  #i_id - ingredient id
            if (i_id):
                try:
                    ingredient = Ingredient.query.get(i_id) # Gets product with id = i_id (because id is primary key)
                    db.session.delete(product) # Delete the product
                    db.session.commit() # Save
                    return jsonify({"success": True})
                except Exception as e:
                    return jsonify({"error": e})
            else:
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "m"})

# view single item 
@app.route('/ingredients/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)

    if request.method == 'GET':
        response = {"id": ingredient.id, 
                    "name": ingredient.name, 
                    "description": ingredient.description, 
                    "purpose" : ingredient.purpose, 
                    "safety": ingredient.safety,
                    "image_url": ingredient.image_url, 
                    "quick_facts": ingredient.quick_facts
                    }
        return {"ingredient": response}

    elif request.method == 'PUT':
        data = request.get_json()
        name = data["name"]
        alt_names = data["alt_names"]
        description = data["description"]
        purpose = data["purpose"]
        safety = data["safety"]
        image_url = data["image_url"]
        quick_facts = data["quick_facts"]

        db.session.add(ingredient)
        db.session.commit()
        return {"message": f"Ingredient: {ingredient.name} successfully updated"}

if __name__ == "__main__":
    app.run(debug=True) # debug=True restarts the server everytime we make a change in our code