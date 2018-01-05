#!/usr/bin/env python
from __future__ import print_function
import argparse
import datetime
import sys
import pymongo
import uuid
import random
import traceback
from loremipsum import get_paragraph
from random import randint


def run(args):
    settings = {
        'host': args.host,
        'database': args.database,
        'username': args.username,
        'password': args.password,
        'port': args.port,
    }

    avenger = ""
    avengers = ["Black Widow", "Jarvis", "Iron Man", "Thor", "Hulk",
                "Captain America", "Hulk", "Nick Fury", "Pepper Potts", "Hawkeye",
                "Luke Cage", "Falcon", "Scarlet Witch"]

    try:
        uri = "mongodb://{username}:{password}@{host}:{port}/{database}".format(**settings) if \
            settings['username'] else "mongodb://{}:{}/{}".format(settings['host'], settings['port'], settings['database'])
        conn = pymongo.MongoClient(uri)
    except Exception as ex:
        print("Error: {}\ntraceback: {}".format(str(ex), traceback.format_exc()))
        exit('Failed to connect, terminating.')

    db = conn.random_data

    while True:
        if len(sys.argv) > 1:
            avenger = sys.argv[1]
            print("Using avenger: {}".format(avenger))
        else:
            avenger = random.choice(avengers)

        doc = {
            'timestamp': datetime.datetime.utcnow(),
            'review_id': str(uuid.uuid1()),
            'user_id': str(uuid.uuid1()),
            'product_name': avenger,
            'comment': get_paragraph(),
            'cost': randint(1, 10),
            'value': randint(1, 10),
            'product_quality': randint(1, 10),
            'up_votes': randint(1, 2000),
            'down_votes': randint(1, 1000),
        }

        mongo_collection = 'Hulk'

        print("{: <25}  {: >20}".format(mongo_collection, db[mongo_collection].insert(doc)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str,
                        help='Mongodb host to which to connect')
    parser.add_argument('database', type=str,
                        help='Mongodb database to use')
    parser.add_argument('--username', type=str, action='store', const=None,
                        help='Mongodb username')
    parser.add_argument('--password', type=str, action='store', const=None,
                        help='Mongodb password')
    parser.add_argument('--port', type=int, action='store', const=27017, default=27017, nargs='?',
                        help='Mongodb port')

    args = parser.parse_args()
    run(args)
