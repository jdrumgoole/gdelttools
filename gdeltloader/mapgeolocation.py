import argparse

import pymongo

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", default="mongodb://localhost:27017",
                        help="MongoDB URI [%(default)s]")

    parser.add_argument("--database", default="GDELT",
                        help="Default database for loading [%(default)s]")

    parser.add_argument("-i", "--inputcollection", default="events_csv",
                        help="Default collection for input [%(default)s]")
    parser.add_argument("-o", "--outputcollection", default="events",
                        help="Default collection for output [%(default)s]")

    args = parser.parse_args()

    client = pymongo.MongoClient(host=args.host)
    db = client[args.database]
    input_collection = db[args.inputcollection]
    output_collection = db[args.outputcollection]

    matcher = {"$match": {"ActionGeo_Lat": {"$type": "double"},
                          "ActionGeo_Long": {"$type": "double"},
                          "Actor1Geo_Lat": {"$type": "double"},
                          "Actor1Geo_Long": {"$type": "double"},
                          "Actor2Geo_Lat": {"$type": "double"},
                          "Actor2Geo_Long": {"$type": "double"}}}

    adder = {"$addFields": {"Actor1Geo": {"type": "Point", "coordinates": ["$Actor1Geo_Long", "$Actor1Geo_Lat"]},
                            "Actor2Geo": {"type": "Point", "coordinates": ["$Actor2Geo_Long", "$Actor2Geo_Lat"]},
                            "ActionGeo": {"type": "Point", "coordinates": ["$ActionGeo_Long", "$ActionGeo_Lat"]}}}

    deleter = {"$unset": ["ActionGeo_Lat", "ActionGeo_Long", "Actor1Geo_Lat",
                          "Actor1Geo_Long", "Actor2Geo_Lat", "Actor2Geo_Long"]}

    merger = {"$merge": {"into": args.outputcollection,
                         "on": "_id",
                         "whenMatched": "replace",
                         "whenNotMatched": "insert"}}
    input_collection.aggregate([matcher, adder, deleter, merger])
    output_collection = db[args.outputcollection]
    print(f"Processed documents total : {output_collection.count_documents({})}")
