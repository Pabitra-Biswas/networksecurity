
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus

# Encode username and password to prevent special character issues
username = quote_plus("ppabitrabiswas02")
# password = quote_plus("Admin123")  # If '@', '!', '#', etc. exist, this will handle them

# Correct MongoDB URI with encoded credentials
uri = "mongodb+srv://ppabitrabiswas02:Admin123@cluster0.yrltz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("✅ Pinged your deployment. Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ Connection error: {e}")
