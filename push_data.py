import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo
from urllib.parse import quote_plus
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

# Load environment variables
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
# Debugging: Print the encoded URI
print("MongoDB Connection URI:", MONGO_DB_URL)

ca = certifi.where()  # Ensure valid SSL certificate

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Establish MongoDB connection
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "PABITRA07"
    Collection = "NetworkData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)

    print(f"Extracted {len(records)} records.")
    
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(f"Inserted {no_of_records} records into MongoDB.")




4