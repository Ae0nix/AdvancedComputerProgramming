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
    except:
        
    return "ACK", 200









if __name__ == "__main__":
    app.run(debug=True, port=5001)