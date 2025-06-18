import pymongo
from flask import Flask, request

app = Flask(__name__)

def get_database():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["db"]

@app.put("/create_booking")
def create_booking():

    db = get_database()
    collection = db["booking_collection"]

    request_message = request.get_json()
    try:
        collection.insert_one(request_message)
    except Exception as e:
        print("[DBSERVER] Operation failed")
        return "Fail-"+str(e), 500
    else:
        print("[DBSERVER] Booking insert correctly")
        return "ACK", 200
    

@app.post("/update_booking")
def update_booking():

    db = get_database()
    collection = db["booking_collection"]

    request_message = request.get_json()

    operator = request_message["operator"]


    list_of_bookings = list(collection.find({
        "operator":operator, 
        "nights": {"$gte": request_message["nights"]}
        }))




    try:

    except Exception as e:
        print("[DBSERVER] Operation failed")
        return "Fail-"+str(e), 500
    else:
        print("[DBSERVER] Booking updated correctly")
        return "ACK", 200



if __name__ == "__main__":
    app.run(debug=True, port=5001)