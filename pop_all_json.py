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

filePath = './'
ingest = []
files = os.listdir('./')
for file in files:
    filename, file_extension = os.path.splitext(file)
    if file_extension == '.json':
        fl = os.path.join(filePath, file)
        print(f"opening: {file}")
        with open(fl, 'r') as fin:
            js = json.load(fin)
        for j in js:
            # a couple of the capabilities items are badly formed. check and fix
            if type(j['capabilities'][0]) == list:
                j['capabilities'] = [d for d in j['capabilities'][0]]
            ingest.append(j)

print(f"len: {len(ingest)}")
#
# debug code if needed
#
# for k in ingest:
#     print(f"{len(k)}: {k.keys()}")

index_sources = []
not_indexed_sources = []
for idx, el in enumerate(ingest):

    # c = json.dumps(el['capabilities'])
    c = [str(e) for e in el['capabilities']]
    # print(f"-> {type(c)}: {c}")
    m = {
        'text': el['description'],
        'product_name': el['product_name'],
        'url': el['url'],
        'capabilities': c,

    }
    z = {
        'sha': 'spiffy space',
        'sec_class': ['TS', 'S', 'COMP-A', 'COMP-b']
    }
    index_sources.append(m)
    not_indexed_sources.append(z)

print(f"len: {len(index_sources)}")

embeddings = model.encode(index_sources)

collection = client.collections.create(
        name="Unreal",
        properties=[
            wvc.config.Property(name="text", data_type=DataType.TEXT),
            wvc.config.Property(name="url", data_type=DataType.TEXT),
            wvc.config.Property(name="product_name", data_type=DataType.TEXT),
            wvc.config.Property(name="capabilities", data_type=DataType.TEXT_ARRAY),
            wvc.config.Property(
                name="credentials", 
                data_type=DataType.OBJECT, 
                nested_properties=[
                    wvc.config.Property(name="sha", data_type=DataType.TEXT),
                    wvc.config.Property(name="sec_class", data_type=DataType.TEXT_ARRAY)
                ],
                vectorize_property_name=False, skip_vectorization=True, index_searchable=False),
        ],
        vector_config=wvc.config.Configure.Vectors.self_provided(),
    )

final_sources = list(zip(index_sources, not_indexed_sources))
# for indx, el in enumerate(final_sources):
#     print(f"{len(el)}\n{el[0]}\n\n{el[1]}\n\n")
#     if indx > 3:
#         break

# client.close()

try:
    with client.batch.fixed_size(batch_size=100, concurrent_requests=4) as batch:  # or <collection>.batch.fixed_size()
        # Batch import objects/references - e.g.:
        for idx in range(len(final_sources)):
            element = final_sources[idx][0]    # these are the indexable fields
            batch.add_object(
                properties={
                    "text": element['text'],
                    "url": element['url'],
                    "product_name": element['product_name'],
                    "capabilities": element['capabilities'],
                    "sec_class": final_sources[idx][1]    # non indexable
                },
                collection="Unreal", 
                vector=embeddings[idx]),

finally:
    client.close()



