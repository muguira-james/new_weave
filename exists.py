import weaviate
import argparse
import os
import json
import pprint


import weaviate
import weaviate.exceptions
import weaviate.config 

parser = argparse.ArgumentParser()

parser.add_argument('-c', "--collectionName", required=True)

args = parser.parse_args()

try:
    client = weaviate.connect_to_local(host="localhost", port=8080)

    if not client.is_ready():
        print(f"initial connection failed...")
        exit()


    resp = client.collections.exists(args.collectionName)
    if resp == True:
        print(f"{args.collectionName} exists")
    else:
        print(f"{args.collectionName} does not exist")
    
    client.close()

except weaviate.exceptions.WeaviateConnectionError as err:
    print(f"{err}")
    
    