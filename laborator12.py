
import uuid  
from flask import Flask, jsonify, request, abort  
import os  
import random  
  
app = Flask(__name__)  
DIR = './sensor'  

#verificam daca exita directorul
os.makedirs(DIR, exist_ok=True)  

#GET: citirea valorii simulate a unui senzor    
@app.route('/sensors/<sensor_id>', methods=['GET'])  
def get_value(sensor_id):   
    sensor_value = random.randint(0, 100)  
    return jsonify({'sensor_id': sensor_id, 'value': sensor_value})  
  
#POST: creeaza un fisier de configurare pentru un senzor
@app.route('/sensors/<sensor_id>', methods=['POST'])  
def create_config(sensor_id):  
    data = request.json if request.is_json else {}  
    scale = data.get('scale', 1.0)   
    filename = f"config_{sensor_id}.txt"  
    file_path = os.path.join(DIR, filename)  
  
    if os.path.exists(file_path):   
        return jsonify({'error': 'Config file already exists.'}), 409  
    
    content = f"scale={scale}"  
    with open(file_path, 'w') as f:  
        f.write(content)  
    return jsonify({'message': 'File created', 'sensor_id': sensor_id, 'config_file': filename, 'scale': scale})  

#PUT: modifica fisierul de configurare a unui senzor   
@app.route('/sensors/<sensor_id>/<filename>', methods=['PUT'])  
def update_config(sensor_id, filename):  
    file_path = os.path.join(DIR, filename)  
    if not os.path.exists(file_path):  
        return jsonify({'error': 'Config file does not exist'}), 409  
  
    data = request.json if request.is_json else {}   
    scale = data.get('scale', 1.0)  
    content = f"scale={scale}"  
    with open(file_path, 'w') as f:  
        f.write(content)  
    return jsonify({'message': 'File updated.', 'sensor_id': sensor_id, 'filename': filename, 'new_scale': scale})  
  
  
if __name__ == '__main__':  
    app.run(debug=True)