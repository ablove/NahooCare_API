from pymongo import MongoClient

client = MongoClient("mongodb+srv://ashenafidejene75:rItH4pBm3d0c2r3R@nahoocare.qgkx8.mongodb.net/?retryWrites=true&w=majority&appName=NahooCare")

db = client.nahooCare

collection_name = db("nahooCare")
