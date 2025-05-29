
import random 
from flask import Flask, jsonify, request, abort  
from flask_jwt_extended import JWTManager, create_access_token   
  
app = Flask(__name__)  
app.config['JWT_SECRET_KEY'] = 'secret-key'    
jwt = JWTManager(app)  
  

users = {  
    "user1": {"password": "parola1", "role": "admin"},  
    "user2": {"password": "parola2", "role": "owner"},  
    "user3": {"password": "parolaX", "role": "owner"},  
}  
 
active_tokens = {}  

#aflam rolul utilizatorului
def get_user_role():
    auth_header = request.headers.get("Authorization", "").replace("Bearer ", "")
  
    token = auth_header.split(" ")[1]
    if token not in active_tokens:
        return "guest"
    
    return active_tokens[token]["role"]

#POST: login
@app.route('/auth', methods=['POST'])  
def login():   
    data = request.json  
  
    username = data.get("username")  
    password = data.get("password")  
    if not username or not password:  
        abort(400, "Error: username or password is missing")  
  
    user = users.get(username)  
    if not user or user["password"] != password:  
        abort(401, "Error: username or password is invalid")  
  
    #generam un token  
    token = create_access_token(identity=username)    
    active_tokens[token] = {"username": username, "role": user["role"]}  
  
    return jsonify({"token": token}), 200  
  
 
#GET: verifica valabilitatea unui token
@app.route('/auth/jwtStore', methods=['GET'])  
def verify_token():  
    auth_header = request.headers.get("Authorization", "").replace("Bearer ", "")
  
    token = auth_header.split(" ")[1]   
    if token not in active_tokens:  
        return jsonify({"error": "Token not found"}), 404  
    
    role = active_tokens[token]["role"]  
    return jsonify({"message": "Token valid", "role": role}), 200  
  
   
#DELETE: logout prin invalidarea token-ului 
@app.route('/auth/jwtStore', methods=['DELETE'])  
def logout():  
    auth_header = request.headers.get("Authorization", "").replace("Bearer ", "")
  
    token = auth_header.split(" ")[1]  
    if token not in active_tokens:  
        return jsonify({"error": "Token not found"}), 404  

    del active_tokens[token]  
    return jsonify({"message": "Logout successful"}), 200  
  
#GET: citire senzor
@app.route('/sensors/data', methods=['GET'])
def read_sensor():
    role = get_user_role()
    if role not in ['owner', 'admin']:
        return abort(403, "Access denied: guests cannot read sensor")
    
    sensor_value = random.randint(0, 100)  
    return jsonify({'value senzorului': sensor_value})
     
if __name__ == '__main__':   
    app.run(debug=True)  
