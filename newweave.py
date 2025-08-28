
"""

example using langchain - do not follow this. query.py, list_all.py, and the oter codes are better

"""

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

sources = []
for idx, el in enumerate(ingest):

    # c = json.dumps(el['capabilities'])
    c = [str(e) for e in el['capabilities']]
    # print(f"-> {type(c)}: {c}")
    m = {
        'product_name': el['product_name'],
        'url': el['url'],
        'capabilities':  c

    }
    sources.append( Document(page_content=el['description'], metadata=m) )

print(f"len: {len(sources)}")


db = WeaviateVectorStore.from_documents(sources, embeddings, client=client, index_name="Unreal")

resp = client.collections.list_all(simple=True)
print(f"all collections: {resp.keys()}")

# client.collections.delete('Unreal')



client.close()
