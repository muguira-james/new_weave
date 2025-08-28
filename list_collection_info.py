import weaviate
import argparse
import os
import json
import pprint

import weaviate
import weaviate.config 

parser = argparse.ArgumentParser()

parser.add_argument('-c', "--collectionName", required=True)

args = parser.parse_args()

try:
    client = weaviate.connect_to_local(host="localhost", port=8080)

    r = client.collections.exists(args.collectionName)
    if r == True:
        # found the collection
        resp = client.collections.list_all(simple=True)
        # give me a short list
        print(f"all collections: {resp.keys()}")
        # now, show schema info
        collectionName = args.collectionName
        collection = client.collections.get(collectionName)
        print("\n")
        pprint.pprint(collection.config.get(), width=1)
    else:
        print(f"no collection named: {args.collectionName}")

    client.close()
    
except weaviate.exceptions.WeaviateConnectionError as err:
    print(f"{err}")