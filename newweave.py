import weaviate

import os
import json


from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings

import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore


from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

client = weaviate.connect_to_local(host="localhost", port=8080)

if not client.is_ready():
    print(f"initial connection failed...")
    exit()

ingest = []
with open('./navy_data.json', 'r') as fin:
    ingest = json.load(fin)

print(f"len: {len(ingest)}")

client.close()
