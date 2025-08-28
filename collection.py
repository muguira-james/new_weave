import weaviate

import os
import json

try:
    client = weaviate.connect_to_local(host="localhost", port=8080)

    resp = client.collections.list_all(simple=False)
    import pprint

    for k in resp.keys():
        pprint.pprint(f"{type(resp[k])}\n\n{resp[k]}")


    client.close()

except weaviate.exceptions.WeaviateConnectionError as err:
    print(f"{err}")