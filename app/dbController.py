import os
from dotenv import load_dotenv

import pymongo

import datetime

# Credentials
load_dotenv('.env')
MONGODB_TOKEN = os.getenv('MONGODB_TOKEN')


def connect():
    client = pymongo.MongoClient(MONGODB_TOKEN)
    db = client.NiverBot
    users = db.USERS

    return client, db, users


def user_exists(users, data):

    query = {'telegram_id': data['telegram_id']}

    results = list(users.find(query))

    if len(results) > 0:
        return True

    return False


def update_users_list(users, data):
    query = {'telegram_id': data['telegram_id']}
    insert = {'$push': {'friends': data['friends'][0]}}

    users.update(query, insert, upsert=True)


def insert_birthday(data):
    client, db, users = connect()

    if user_exists(users, data):
        update_users_list(users, data)
    else:
        users.insert_one(data)

    client.close()


# The functions above are made to remind the user their frieds birthdays
def get_all_today_birthdays():
    client, db, users = connect()

    current_day = datetime.datetime.today().day
    current_month = datetime.datetime.today().month

    search_query = [{
        "$match": {
            "friends.birthday.day": current_day,
            "friends.birthday.month": current_month
        }
    }, {
        "$unwind": "$friends"
    }, {
        "$match": {
            "friends.birthday.day": current_day,
            "friends.birthday.month": current_month
        }
    }]

    users = users.aggregate(search_query)

    client.close()

    return users