from pymongo import MongoClient


uri = "mongodb+srv://sampleR:sampleR@cluster0.ljwn3ub.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client["quiz"]

stulogin = db["stulogin"]
tealogin = db["tealogin"]


print(db.list_collection_names())