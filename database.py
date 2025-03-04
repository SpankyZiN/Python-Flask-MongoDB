from http import client
from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://alecolman0410:<db_password>@cluster0.bwuig.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]
    except ConnectionError:
        print("Error de conexion con la base de datos")
    return db