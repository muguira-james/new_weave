import weaviate
import argparse
import os
import json


from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings

import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore


from langchain_huggingface import HuggingFaceEmbeddings


parser = argparse.ArgumentParser()

parser.add_argument('-c', "--collectionName", required=True)

args = parser.parse_args()

try:
    client = weaviate.connect_to_local(host="localhost", port=8080)

    client.collections.delete(args.collectionName)

    client.close()
    
except weaviate.exceptions.WeaviateConnectionError as err:
    print(f"{err}")