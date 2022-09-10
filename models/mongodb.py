import pymongo

MONGO_URI = "mongodb+srv://heetae185:sksms0824@cluster0.l0auavr.mongodb.net/?retryWrites=true&w=majority"
MONGO_CONN = pymongo.MongoClient(MONGO_URI)

def conn_mongodb():
    db = MONGO_CONN.online_store
    return db