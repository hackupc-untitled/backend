from flask import Flask, request, Response, jsonify
from clients import *
#from mi_app.users.views import users_bp
#from mi_app.posts.views import posts_bp

app = Flask(__name__)
client = ''

@app.route('/save', methods=['POST'])
def save():
    json_data = request.get_json()
    #print(json_data)
    client = getInfluxClient()
    json_data = {'measurement': 'status', 'tags': {'satelliteCount': 34, 'azimuthDegrees': '282.0', 'carrierFrequencyHz': '1575420032.0', 'cn0DbHz': '0.0', 'elevationDegrees': '42.0', 'svid': '19', 'hasAlmanacData': 'false', 'hasCarrierFrequencyHz': 'true', 'hasEphemerisData': 'false', 'usedInFix': 'false', 'mac-address': {'version': 'REL', 'board': 'k6853v1_64_6360_k419', 'bootloader': 'unknown', 'brand': 'OPPO', 'device': 'OP4F4DL1', 'display': 'CPH2211_11_F.51', 'fingerprint': 'OPPO/CPH2211EEA/OP4F4DL1:13/TP1A.220905.001/R.15a1d76-4bc5:user/release-keys', 'hardware': 'mt6853', 'host': 'dg02-pool06-kvm61', 'id': 'TP1A.220905.001', 'manufacturer': 'OPPO', 'model': 'CPH2211', 'product': 'CPH2211EEA'}, 'date': '04-05-2024 20:34:13'}, 'fields': {'constellationType': 1}}
    client.write_points(json_data)


#Each app.route represents an endpoint
@app.route('/countGalileos', methods=['GET'])
def countGalileos(mac_address):
    query = 'SELECT COUNT("constellation") FROM "raw" WHERE "constellation"=\'1\' GROUP BY "user_id"'
    result = client.query(query)
    count = result.iloc[0]['_value']


@app.route('/test', methods=['POST'])
def test():
    print(request.get_json())
    return Response(status=200)
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)  # Change port number if needed
