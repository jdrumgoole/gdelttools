import argparse
import pymongo
import pprint

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--host",
                        default="http://localhost:27017",
                        help="MongoDB URI")

    parser.add_argument("--sample", type=int, default=10,
                        help = "The sample size : default to 10")

    args = parser.parse_args()

    client = pymongo.MongoClient(args.host)

    db = client["GDELT2"]
    source = db["eventscsv"]
    sink = db["events"]

    sample_cursor = source.aggregate([{"$sample" : {"size": 10}}])

    for d in sample_cursor:
        pprint.pprint(d)


