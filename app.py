from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship, backref
Base = declarative_base()

from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ma = Marshmallow(app)
cors = CORS(app)
migrate = Migrate(app, db) 
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# association table 
# product_ingredient = db.Table('product_ingredient',Base.metadata,
#     db.Column('product_id', 
#                 db.Integer, 
#                 db.ForeignKey('product.id')
#                 ),
#     db.Column('ingredient_id', 
#                 db.Integer, 
#                 db.ForeignKey('ingredient.id')
#                 )
#             )

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    image_url = db.Column(db.String)
    ingredients = db.Column(db.Text)
    # ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

                                                
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

    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return {"message": f"Product {product.name} successfully deleted."}

# def get_product(id):
#     if not id.isnumeric(): 
#         product = Product.query.filter_by(name = id).first()
        
#         if product is None:
#             abort(404)
            
#         response = {"id": product.id, 
#                     "name": product.name, 
#                     "description": product.description,
#                     "image_url": product.image_url, 
#                     "ingredients": product.ingredients
#                     }
#         return {"product": response}
#         product = Product.query.get_or_404(id)



# INGREDIENTS DB 
class Ingredient(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    alt_names = db.Column(db.String)
    description = db.Column(db.String)
    purpose = db.Column(db.String)
    safety = db.Column(db.String)
    image_url = db.Column(db.String)
    quick_facts = db.Column(db.String)

    # product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # products = db.relationship('Product', 
    #                             secondary=product_ingredient, 
    #                             backref=db.backref('ingredient',lazy = 'dynamic'),
    #                             lazy='dynamic')

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
                        "alt_names": i.alt_names,
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
                    ingredient = Ingredient.query.get(i_id) # Gets ingredient with id = i_id (because id is primary key)
                    db.session.delete(ingredient) # Delete the ingredient
                    db.session.commit() # Save
                    return jsonify({"success": True})
                except Exception as e:
                    return jsonify({"error": e})
            else:
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "m"})

# @app.route('/ingredients/<name>', methods=['GET'])
# def get_ingredient_by_name(name):
#     ingredient = Ingredient.query.filter_by(name = name).first()
#     response = {"id": ingredient.id, 
#                 "name": ingredient.name, 
#                 "description": ingredient.description, 
#                 "purpose" : ingredient.purpose, 
#                 "safety": ingredient.safety,
#                 "image_url": ingredient.image_url, 
#                 "quick_facts": ingredient.quick_facts
#                 }
#     return {"ingredient": response}

# view single item 
@app.route('/ingredients/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_ingredient(id):
    if not id.isnumeric(): 
        ingredient = Ingredient.query.filter_by(name = id).first()
        
        if ingredient is None:
            abort(404)
            
        response = {
            "id": ingredient.id, 
            "name": ingredient.name, 
            "description": ingredient.description, 
            "purpose" : ingredient.purpose, 
            "safety": ingredient.safety,
            "image_url": ingredient.image_url, 
            "quick_facts": ingredient.quick_facts
            }
        return {"ingredient": response}
    # print(type(id))
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
    
    # elif request.method == 'DELETE':
    #     db.session.delete(ingredient)
    #     db.session.commit()
    #     return {"message": f"Product {product.name} successfully deleted."}


# ----------------------------------------------- #
# USER 


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_token = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    image_url = db.Column(db.String)
    

                                                
    # Constructor
    def __init__(self, id_token, username, first_name, last_name, email, image_url):
        self.id_token = id_token
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.image_url = image_url

@app.route("/users", methods=["GET", "POST", "DELETE"])
def users():
    method = request.method
    if (method.lower() == "get"): # READ
        user = User.query.all()
        return jsonify([{"id": i.id, 
                        "id_token": i.id_token, 
                        "username": i.username, 
                        "first_name": i.first_name,
                        "last_name": i.last_name, 
                        "email" : i.email, 
                        "image_url": i.image_url} for i in user]) # Get all values from db
    elif (method.lower() == "post"): # CREATE
        try:
            id_token = request.json["id_token"]
            username = request.json["username"]
            first_name = request.json["first_name"]
            last_name = request.json["last_name"]
            email = request.json["email"]
            image_url = request.json["image_url"]
            if (id_token and username and first_name and last_name and email and image_url ): 
                try:
                    user = User(id_token, username, first_name, last_name, email, image_url) # Creates a new record
                    db.session.add(user) # Adds the record for committing
                    db.session.commit() # Saves our changes

            #     response = {
            #         "id": user.id,
            #         "id_token": user.id_token, 
            #         "username": user.username, 
            #         "first_name": user.first_name,
            #         "last_name": user.last_name, 
            #         "email": user.email, 
            #         "image_url": user.image_url
            #     }

            # return {"user": response}

                    return jsonify({
                                    "id": user.id, 
                                    "id_token": user.id_token, 
                                    "username": user.username, 
                                    "first_name": user.first_name,
                                    "last_name": user.last_name, 
                                    "email" : user.email, 
                                    "image_url": user.image_url
                                        }
                                    )
                except Exception as e:
                    return ({"error": e})
            else:
                return jsonify({"error": "Invalid form"}) # jsonify converts python vars to json
        except Exception as e:
            return jsonify({"error": e})
    elif (method.lower() == "delete"): # DESTROY
        try:
            user_id = request.json["id"]  #i_id - user id
            if (user_id):
                try:
                    user = User.query.get(user_id) # Gets user with id = user_id (because id is primary key)
                    db.session.delete(user) # Delete the user
                    db.session.commit() # Save
                    return jsonify({"success": True})
                except Exception as e:
                    return jsonify({"error": e})
            else:
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "m"})

# view single user 
@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(id):
    if not id.isnumeric(): 
        user = User.query.filter_by(email = id).first()
        
        if user is None:
            abort(404)
            
        response = {
                    "id": user.id,
                    "id_token": user.id_token, 
                    "username": user.username, 
                    "first_name": user.first_name,
                    "last_name": user.last_name, 
                    "email": user.email, 
                    "image_url": user.image_url
        }
        return {"user": response}
    # print(type(id))
    user = User.query.get_or_404(id)

    if request.method == 'GET':
        response = {"id": user.id,
                    "id_token": user.id_token, 
                    "username": user.username, 
                    "first_name": user.first_name,
                    "last_name": user.last_name, 
                    "email" : user.email, 
                    "image_url": user.image_url
                    }
        return {"user": response}

# needs to be fixed 
    elif request.method == 'PUT':
        data = request.get_json()
        username = data["username"]
        id_token = data["id_token"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        image_url = data["image_url"]

        db.session.add(user)
        db.session.commit()
        return {"message": f"User: {user.username} successfully updated"}
    

if __name__ == "__main__":
    # app.run(debug=True) # debug=True restarts the server everytime we make a change in our code
    manager.run()