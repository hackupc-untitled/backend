from influxdb import InfluxDBClient

INFLUXDBUSER = "A5205-32"
DATABASEINFLUX = "A5205-32"
DATABASETEST = "gnss_testdata"
INFLUXPSWD = "28a93c29db780ed1"
INFLUXIP = "84.247.188.251"
INFLUXPORT = 8086

def getInfluxClient():
    try:
        client = InfluxDBClient(host=INFLUXIP, port=INFLUXPORT, username=INFLUXDBUSER, password=INFLUXPSWD)
        client.switch_database(DATABASEINFLUX)
        client.ping
        return client

    except Exception as e:
        print("Error connecting to InfluxDB:", e)
        return None

def getInfluxTestClient():
    try:
        client = InfluxDBClient(host=INFLUXIP, port=INFLUXPORT, username=INFLUXDBUSER, password=INFLUXPSWD)
        client.switch_database(DATABASETEST)
        client.ping
        return client

    except Exception as e:
        print("Error connecting to InfluxDB:", e)
        return None

def printAllTest():
        
    client = getInfluxClient()

    query = 'SELECT * FROM Fix LIMIT 1'

    result = client.query(query)
    
    print("-----------------FIX ------------------\n")
    print(result)

    query = 'SELECT * FROM Nav LIMIT 1'

    result = client.query(query)
    
    print("-----------------Nav ------------------\n")
    print(result)

    query = 'SELECT * FROM Raw LIMIT 1'

    result = client.query(query)
    
    print("-----------------Raw ------------------\n")
    print(result)

    query = 'SELECT * FROM fix LIMIT 10'

    result = client.query(query)
    
    print("-----------------Status ------------------\n")
    print(result)
    client.close()
#printAllTest()
