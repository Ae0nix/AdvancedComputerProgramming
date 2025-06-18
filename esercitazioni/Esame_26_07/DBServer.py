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

    message = 









if __name__ == "__main__":
    app.run(debug=True, port=5001)