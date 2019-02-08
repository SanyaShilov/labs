import json

import pymongo


def create_db():
    mongo_client = pymongo.MongoClient()
    db = mongo_client.networks
    return db


def reload_db(db):
    db.users.delete_many({})
    users = json.load(open('./users.json'))
    db.users.insert_many(users)

    db.maps.delete_many({})
    maps = json.load(open('./maps.json'))
    db.maps.insert_many(maps)


def main():
    db = create_db()
    reload_db(db)


if __name__ == '__main__':
    main()
