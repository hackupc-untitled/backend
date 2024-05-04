from flask import Flask, request, Response, jsonify
from clients import *
#from mi_app.users.views import users_bp
#from mi_app.posts.views import posts_bp

app = Flask(__name__)
client = ''

@app.route('/save', methods=['POST'])
def save():
    json_data = request.get_json()
    client = getInfluxClient()
    client.write_points(json_data)


#Each app.route represents an endpoint
@app.route('/countGalileos', methods=['GET'])
def countGalileos(mac_address):
    query = 'SELECT * FROM raw WHERE mac_address = \'' + mac_address + '\' LIMIT 10'
    result = client.query(query)
    return Response(status=200)




@app.route('/test', methods=['POST'])
def test():
    print(request.get_json())
    return Response(status=200)
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)  # Change port number if needed
