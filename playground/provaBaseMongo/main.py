from pymongo import MongoClient
client = MongoClient("localhost", 27017)

db = client["test-database"]

collection = db["test-collection"]

post = [
    {
    "name": "Scott McFratm",
    "description": "Forza Napoli",
    "tags": ["Napoli", "Manchester United"],
    "goal": 15
    },
    {
    "name": "Pasquale Mazzocchi",
    "description": "Forza Napoli",
    "tags": ["Napoli"],
    "goal": 0
    },
]

collection.delete_many({"description": "Forza Napoli"})
collection.insert_many(post)

result = collection.find({"goal": {"$gt":1}})
for item in result:
    print("name: ", item["name"])

collection.update_many({"name": "Scott McFratm"}, {"$set": {"name": "Scott McTominay"}})
print("Database updated...")
result = collection.find({"goal": {"$gt":1}})
for item in result:
    print("name: ", item["name"])


client.drop_database("test-database")