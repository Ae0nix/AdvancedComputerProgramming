from pymongo import MongoClient
from flask import Flask, request

def get_database():
    client = MongoClient("mongodb://localhost:27017")

    return client["test_database"]


app = Flask(__name__)


@app.post("/sensor")
def add_sensor():

    body = request.get_json()

    db = get_database()

    sensor_collection = db["sensors"]

    if sensor_collection.find_one(body):
        print("[ADD SENSOR] Sensor already exists")
        return {"result": "failed - sensor already exists"}, 400

    try:
        sensor_collection.insert_one(body)
    except Exception as e:
        print("[ADD SENSOR] Operation failed")
        return {"result":f"failed - {str(e)}"}, 500
    
    else:
        print("[ADD SENSOR] Sensor added correctly")
        return {"result":"success"}
    

@app.post("/data/<data_type>")
def add_measure(data_type):

    body = request.get_json()

    db = get_database()

    if data_type == "press":
        collection = db["press_data"]
    elif data_type == "temp":
        collection = db["temp_data"]
    else:
        print("[ADD MEASURE] Data type not valid")
        return {"result": "Unsupported data type"}, 400
    

    try:
        collection.insert_one(body)
    except Exception as e:
        print("[ADD MEASURE] Error while inserting measure in database")
        return {"reault": f"failed - {str(e)}"}
    
    else:
        print(f"[ADD MEASURE measure for {data_type} saved on DB")
        return {"result": "success"}

if __name__ == "__main__":
    app.run(debug=True, port=5001)