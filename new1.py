import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import Configure, Property, DataType

import os
import json

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('msmarco-roberta-base-v3')

client = weaviate.connect_to_local(host="localhost", port=8080)

if not client.is_ready():
    print(f"initial connection failed...")
    exit()

ingest = []
with open('./unreal_data2.json', 'r') as fin:
    ingest = json.load(fin)

sources = []
for idx, el in enumerate(ingest):

    # c = json.dumps(el['capabilities'])
    c = [str(e) for e in el['capabilities']]
    # print(f"-> {type(c)}: {c}")
    m = {
        'text': el['description'],
        'product_name': el['product_name'],
        'url': el['url'],

        'sha': 'eurviuebrviuaerivbekjieuriuerivueaiuvrbieubvri',
    }
    sources.append( m )

print(f"len: {len(sources)}")

embeddings = model.encode(sources)

collection = client.collections.create(
        name="Unreal",
        properties=[
            wvc.config.Property(name="text", data_type=DataType.TEXT),
            wvc.config.Property(name="url", data_type=DataType.TEXT),
            wvc.config.Property(name="product_name", data_type=DataType.TEXT),
            wvc.config.Property(name="capabilities", data_type=DataType.TEXT_ARRAY),
            wvc.config.Property(name="sha", data_type=DataType.TEXT, skip_vectorization=True),
        ],
        vector_config=wvc.config.Configure.Vectors.self_provided(),


    )

try:
    with client.batch.fixed_size(batch_size=100, concurrent_requests=4) as batch:  # or <collection>.batch.fixed_size()
        # Batch import objects/references - e.g.:
        for el in range(len(ingest)):
            batch.add_object(
                properties={
                    "text": ingest[el]['description'],
                    "url": ingest[el]['url'],
                    "product_name": ingest[el]['product_name'],
                    "capabilities": ingest[el]['capabilities'],
                },
                collection="Unreal", 
                vector=embeddings[el]),
          
          

finally:
    client.close()

# resp = client.collections.list_all(simple=True)
# print(f"all collections: {resp.keys()}")

# client.collections.delete('Unreal')



client.close()
