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
    app.run(host='0.0.0.0', port=5000,debug=True)  # Change port number if needed
