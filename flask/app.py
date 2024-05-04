from flask import Flask, request, Response, jsonify
from clients import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

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

# Route for registration
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        return jsonify({'message': 'User already exists'}), 400
    hashed_password = generate_password_hash(password)
    user = User(1, username, hashed_password)
    
    

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                   (user.username, user.password))
    conn.commit()
    conn.close()
    
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
    print(user[2])
    print(password)
    if user and check_password_hash(user[2], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Protected route example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    
    user_list = []
    for user in users:
        print(user)

        user_list.append({'password': user[2], 'username': user[1]})
    
    return jsonify(users=user_list), 200



@app.route('/save', methods=['POST'])
def save():
    json_data = request.get_json()
    client = getInfluxClient()
    client.write_points(json_data)


#Each app.route represents an endpoint
@app.route('/countGalileos', methods=['GET'])
def countGalileos(mac_address):
    flux_query = '''
        from(bucket: "your_bucket")
        |> range(start: -1h)  // Adjust the time range as needed
        |> filter(fn: (r) => r["_measurement"] == "raw" and r["mac_address"] == "your_mac_address" and r["constellation"] == "your_constellation")
        |> count()
        '''
    result = client.query_api().query_data_frame(flux_query)
    count = result.iloc[0]['_value']


@app.route('/test', methods=['POST'])
def test():
    print(request.get_json())
    return Response(status=200)

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)
