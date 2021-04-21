import os
from dotenv import load_dotenv

import pymongo

# Credentials
load_dotenv('.env')
MONGODB_TOKEN = os.getenv('MONGODB_TOKEN')

def connect():
    client = pymongo.MongoClient(MONGODB_TOKEN)
    db = client.NiverBot
    users = db.USERS

    return client,db,users

def user_exists(users,data):
    
    query = {'telegram_id':data['telegram_id']}
    print(query)

    results = list(users.find(query))
    
    if len(results)>0:
        return True
    
    return False

def update_users_list(users,data):
    print(data['friends'][0])

    query = {'telegram_id': data['telegram_id']}
    insert = {'$push': {'friends': data['friends'][0]}}

    users.update(query,insert,upsert=True)

def insert_birthday(data):
    client,db,users = connect()

    if user_exists(users,data):
        update_users_list(users,data)
    else:
        users.insert_one(data)

    client.close()