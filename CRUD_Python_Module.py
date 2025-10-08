# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired  to use the aac 
        # database, the animals collection, and the aac user. 
        #
        # Changed username and password to variables instead of being hard-wired
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = username # created username variable
        PASS = password # created password variable
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)]
        print ("Connection is Successful")
            
    # Complete this create method to implement the C in CRUD.
    
    def create(self, data):
        if data is not None: 
            self.collection.animals.insert_one(data)# data should be dictionary
            return "Successfully Added" # prints if successful
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 

    # Create method to implement the R in CRUD.
    def read(self, data):
        if data is not None:
            return list(self.collection.find(data)) # check for correct collection usage
        else:
            raise Exception("Nothing to read, because data parameter is empty")
            
    # Create method to implement the U in CRUD
    def update(self, data, newData):
        if data is not None and newData is not None:
            result = self.collection.animals.update_one(data, {"$set": newData})
            return result.modified_count;
        else:
            raise Exception("Nothing to update, because data parameter is empty")
    
    # Create method to implement the D in CRUD
    
    def delete(self, data):
        if data is not None:
            result = self.collection.animals.delete_one(data)
            return result.deleted_count #correct attribute 
        else:
            raise Exception("Nothing to Delete, because data parameter is empty")
