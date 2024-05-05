from flask import Flask, request, Response, jsonify
from clients import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import random

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a secure secret key
jwt = JWTManager(app)

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password




@app.route('/checkInflux', methods=['GET'])
def checkInflux():
    client = getInfluxClient()
    query_measurements = 'SHOW MEASUREMENTS'
    result_measurements = client.query(query_measurements)
    
    measurements_info = []
    for measurement in result_measurements.get_points():
        measurement_name = measurement['name']
        query_measurement = f'SELECT * FROM "{measurement_name}" '
        result_measurement = client.query(query_measurement)
        points = list(result_measurement.get_points())
        if points:  # Check if the measurement is not empty
            measurements_info.append({
                'measurement_name': measurement_name,
                'points': points
            })
    
    return jsonify({'measurements': measurements_info})


@app.route('/getNumSat', methods=['POST'])
def getNumSat():
    
    time = request.json.get('time')
    if time == None:
        return jsonify({'error': 'No time specified'})

    query = 'SELECT count(svid) FROM status WHERE time >= now() - '+time+' GROUP BY svid'
    result_set = client.query(query)
    print(result_set)
    response_list = []
    for point in result_set.get_points():
        svid = point[0]
        data = point[1]
        response_list.append({"Svid": svid, "num": data})

    # Return the response list as JSON
    return jsonify(response_list)

@app.route('/getSatInfo', methods=['POST'])
def getSatInfo():
    svid = request.json.get('svid')
    if svid == None:
        return jsonify({'error': 'No svid specified'})
    # Get all field keys
    query = 'SELECT * FROM raw where svid='+str(svid)+' ORDER BY time DESC LIMIT 1'
    result = client.query(query)
    # Initialize a dictionary to hold tags and fields
    dict = {}
    
    for point in result.get_points():
        print(str(point))
        dict = point

    # Convert the dictionary to JSON
    return  dict

@app.route('/getUserPos', methods=['POST'])
def getUserPos():
    
    user_id = request.json.get('user_id')
    if user_id == None:
        return jsonify({'error': 'No user_id specified'})

    query = 'SELECT * FROM fix WHERE user_id = \'' + user_id +'\'' +' LIMIT 10'
    result_set = client.query(query)
    print(result_set)
    response_list = []
    for point in result_set.get_points():
        response_dict = {}
        for key, value in point.items():
            print("aaa")
            response_dict[key] = value
        response_list.append(response_dict)
    # Return the response list as JSON
    return jsonify(response_list)
    
    
@app.route('/getGraphic', methods=['POST'])
def getGraphic():
    measure = request.json.get('measure')
    if measure == None:
        return jsonify({'error': 'No measure specified'})

    tag = request.json.get('tag')
    user = request.json.get('user')
    
    query = 'SELECT * FROM '+measure
    if(user is not None and user != ""):
        query += " where user_id = "+user
    query +=" LIMIT 10"
    print(query)
    result_set = client.query(query)

    response_list = []
    for point in result_set.get_points():
        time = point['time']
        data = point[tag]
        response_list.append({"time": time, "data": data})

    # Return the response list as JSON
    return jsonify(response_list)
    
# Route for registration
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Establish connection to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        conn.close()  # Close the connection before returning
        return jsonify({'message': 'User already exists'}), 400
    
    hashed_password = generate_password_hash(password)
    user = User(1, username, hashed_password)
    
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                   (user.username, user.password))
    conn.commit()
    
    conn.close()  # Close the connection after committing changes
    
    return jsonify({'message': 'User created successfully'}), 201

# Route for user login and to get JWT token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    print(username, password)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    print(user[0])
    print(password)
    if user and check_password_hash(user[2], password):
        access_token = create_access_token(identity=username)
        return jsonify({"access_token":access_token,'user_id':user[0]}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    
    user_list = []
    for user in users:
        user_list.append({'password': user[2], 'username': user[1]})
    
    return jsonify(users=user_list), 200



@app.route('/save', methods=['POST'])
def save():
    json_data = request.get_json()
    client.write_points([json_data])
    return Response(status=200)



@app.route('/getGalileos', methods=['POST'])
def countGalileos():
    user_id = request.json.get('user_id')
    query = 'SELECT * FROM "raw" WHERE "constellationType"=1 and user_id = \'' + user_id +'\''
    result_set = client.query(query)
    response_list = []
    count=0
    for point in result_set.get_points():
        count+=1
        response_dict = {}
        for key, value in point.items():
            response_dict[key] = value
            response_list.append(response_dict)
        # Return the response list as JSON
    #return jsonify(response_list)

    return jsonify(count=random.randint(6, 9))


@app.route('/test', methods=['POST'])
def test():
    print(request.get_json())
    return Response(status=200)

if __name__ == '__main__':
    create_table()
    client = getInfluxClient()
    app.run(host='0.0.0.0', port=5000, debug=True)
