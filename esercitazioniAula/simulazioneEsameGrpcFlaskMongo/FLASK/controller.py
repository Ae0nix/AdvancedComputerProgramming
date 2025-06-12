from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)


### Definire una funzione che prenda il riferimento a un MongoClient e ci restituisce un ref al database
def get_db():
    client = MongoClient("localhost", 27017)
    return client["sensors_data"]




@app.post("/sensor")
def add_sensor():
    body = request.get_json()
    print("[CONTROLLER] Ricevuto body", body)

    ### Prendi un ref al database
    db = get_db()
    sensor_collection = db["sensors"]

    try:
        sensor_collection.insert_one(body)
    except Exception as e:
        print("[CONTROLLER] Error DBMS side")
        return {"result": "failure - " +  str(e)}, 500
    else:
        print("[CONTROLLER] New sensor added...")
        return {"result": "success"}
    

@app.post("/data/<data_type>")
def store_data(data_type):
    try:
        body = request.get_json()
        id = body["sensor_id"]
        data = body["data"]

    except KeyError as e:
        return {"result": "failure - " +  str(e)}, 500

    db = get_db()
    if data_type in "temp":
        data_collection = db["temp_data"]
    elif data_type in "press":
        data_collection = db["press_data"]
    else:
        return {"result": "datatype non supportato" + data_type}, 500
    

    try:
        data_collection.insert_one(body)
    except Exception as e:
        print("[CONTROLLER] Error DBMS side")
        return {"result": "failure - " +  str(e)}, 500
    else:
        print("[CONTROLLER] New sensor added...")
        return {"result": "success"}



if __name__ == "__main__":
    app.run(debug=True) 