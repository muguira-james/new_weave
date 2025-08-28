from weaviate.classes.query import MetadataQuery

import weaviate
import argparse

import os
import json


from langchain_core.documents import Document


import weaviate

from langchain_huggingface import HuggingFaceEmbeddings


parser = argparse.ArgumentParser()

parser.add_argument('-q', "--query", required=True)
parser.add_argument('-l', "--limit", required=True)

args = parser.parse_args()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/msmarco-roberta-base-v3")

try:
    client = weaviate.connect_to_local(host="localhost", port=8080)

    if not client.is_ready():
        print(f"initial connection failed...")
        exit()

    print(f"args {args}: {args.query}")


    query_text = args.query
    limit = int(args.limit)

    if limit == 0:
        limit=100

    query = embeddings.embed_query(query_text)

    jeopardy = client.collections.get("Unreal")
    response = jeopardy.query.near_vector(
        near_vector=query,
        limit=limit,
        return_metadata=MetadataQuery(distance=True)
    )

    for j, o in enumerate(response.objects):
        print(f"{j}: {o.metadata.distance}: {o.properties['text']}\n{o.properties['url']}\n{o.properties['capabilities']}\n\n")


    client.close()
    
except weaviate.exceptions.WeaviateConnectionError as err:
    print(f"{err}")