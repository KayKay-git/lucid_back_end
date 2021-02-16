# class User(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     id_token = db.Column(db.String)
#     username = db.Column(db.String, unique=True, nullable=False)
#     first_name = db.Column(db.String)
#     last_name = db.Column(db.String)
#     email = db.Column(db.String)
#     image_url = db.Column(db.String)
    

                                                
#     # Constructor
#     def __init__(self, id_token, username, first_name, last_name, email, image_url):
#         self.id_token = id_token
#         self.username = username
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.image_url = image_url

# @app.route("/users", methods=["GET", "POST", "DELETE"])
# def users():
#     method = request.method
#     if (method.lower() == "get"): # READ
#         user = User.query.all()
#         return jsonify([{"id": i.id, 
#                         "id_token": i.id_token, 
#                         "username": i.username, 
#                         "first_name": i.first_name,
#                         "last_name": i.last_name, 
#                         "email" : i.email, 
#                         "image_url": i.image_url} for i in user]) # Get all values from db
#     elif (method.lower() == "post"): # CREATE
#         try:
#             id_token = request.json["id_token"]
#             username = request.json["username"]
#             first_name = request.json["first_name"]
#             last_name = request.json["last_name"]
#             email = request.json["email"]
#             image_url = request.json["image_url"]
#             if (id_token and username and first_name and last_name and email and image_url ): 
#                 try:
#                     user = User(id_token, username, first_name, last_name, email, image_url) # Creates a new record
#                     db.session.add(user) # Adds the record for committing
#                     db.session.commit() # Saves our changes
#                     return jsonify({"success": True})
#                 except Exception as e:
#                     return ({"error": e})
#             else:
#                 return jsonify({"error": "Invalid form"}) # jsonify converts python vars to json
#         except Exception as e:
#             return jsonify({"error": e})
#     elif (method.lower() == "delete"): # DESTROY
#         try:
#             user_id = request.json["id"]  #i_id - user id
#             if (user_id):
#                 try:
#                     user = User.query.get(user_id) # Gets user with id = user_id (because id is primary key)
#                     db.session.delete(user) # Delete the user
#                     db.session.commit() # Save
#                     return jsonify({"success": True})
#                 except Exception as e:
#                     return jsonify({"error": e})
#             else:
#                 return jsonify({"error": "Invalid form"})
#         except:
#             return jsonify({"error": "m"})

# # view single user 
# @app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
# def get_user(id):
#     if not id.isnumeric(): 
#         user = User.query.filter_by(email = id).first()
        
#         if user is None:
#             abort(404)
            
#         response = {
#                     "id": user.id,
#                     "id_token": user.id_token, 
#                     "username": user.username, 
#                     "first_name": user.first_name,
#                     "last_name": user.last_name, 
#                     "email" : user.email, 
#                     "image_url": user.image_url
#             }
#         return {"user": response}
#     # print(type(id))
#     user = User.query.get_or_404(id)

#     if request.method == 'GET':
#         response = {"id": user.id,
#                     "id_token": user.id_token, 
#                     "username": user.username, 
#                     "first_name": user.first_name,
#                     "last_name": user.last_name, 
#                     "email" : user.email, 
#                     "image_url": user.image_url
#                     }
#         return {"user": response}

#     elif request.method == 'PUT':
#         data = request.get_json()
#         username = data["username"]
#         id_token = data["id_token"]
#         first_name = data["first_name"]
#         last_name = data["last_name"]
#         email = data["email"]
#         image_url = data["image_url"]

#         db.session.add(user)
#         db.session.commit()
#         return {"message": f"User: {user.username} successfully updated"}
    