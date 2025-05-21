import uuid
from flask import Flask, jsonify, request, abort
import os

app = Flask(__name__)
DIR = './files'

#verificam daca exita directorul
os.makedirs(DIR, exist_ok=True)

#GET: listarea continutului directorului
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(DIR)
    return jsonify({'files': files})
        

#GET: listarea continutului unui fisier text, specificat prin nume
@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    file_path = os.path.join(DIR, filename)
    
    with open(file_path, 'r') as f:
        content = f.read()
    return jsonify({'filename': filename, 'content': content})

#PUT: crearea unui fisier specificat prin nume si continut
@app.route('/files/<filename>', methods=['PUT'])
def create_file_with_name_and_content(filename):
    file_path = os.path.join(DIR, filename)
    data = request.json
    content = data.get('content', '')

    with open(file_path, 'w') as f:
        f.write(content)
    return jsonify({'message': 'File created', 'filename': filename})

#POST: crearea unui fisier specificat prin continut
@app.route('/files', methods=['POST'])
def create_file_with_content():
    data = request.json

    #genereaza un nume de fisier
    filename = f"{uuid.uuid4().hex}.txt"
    content = data.get('content', '')
    
    file_path = os.path.join(DIR, filename)
    with open(file_path, 'w') as f:
        f.write(content)
    return jsonify({'message': 'File created', 'filename': filename})

#DELETE: stergerea unui fisier specificat prin nume
@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(DIR, filename)
    
    os.remove(file_path)
    return jsonify({'message': 'File deleted', 'filename': filename})

#PUT: modificarea continutului unui fisier specificat prin nume
@app.route('/files/<filename>/content', methods=['PUT'])
def update_file(filename):
    data = request.json
    new_content = data.get('content', '')
    file_path = os.path.join(DIR, filename)
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    return jsonify({'message': 'File updated', 'filename': filename})

if __name__ == '__main__':
    app.run(debug=True)
