from fastapi import FastAPI

app = FastAPI()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


@app.get('/')
def home():
    print("this from home media")
    return {"message": "this from home media"}  # Added return statement

@app.post("/test/{id}")  # Missing curly braces {id}
def test(id: int):
    print(id, "this the id")
    return {"id": id, "message": "this the id"}  # Added return statement

'''
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ashenafidejene75:rItH4pBm3d0c2r3R@nahoocare.qgkx8.mongodb.net/?retryWrites=true&w=majority&appName=NahooCare"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    

'''