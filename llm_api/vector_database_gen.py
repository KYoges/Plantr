
import pandas as pd 
import time
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

def get_embeddings(rawText):
	text = f"passage:{text}"
	embeddings = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[d["text"] for d in rawText],
    parameters={
        "input_type": "passage", 
        "truncate": "END"
    }
	)



pc = Pinecone(api_key="pcsk_3E9gYh_Lo3TAmA7yhKKRwzjWHtVrk9A1uzobwk4yLr4EHDSu8KWpJcg6NhEqsr8hb5r23o")




index_name = "plantr-index"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws", 
            region="us-east-1"
        ) 
#     ) 

# embeddings = pc.inference.embed(
#     model="multilingual-e5-large",
#     inputs=[d["text"] for d in data],
#     parameters={
#         "input_type": "passage", 
#         "truncate": "END"
#     }
# )

# # Create a serverless index



# index = pc.Index(index_name)




# records = []
# for d, e in zip(data, embeddings):
#     records.append({
#         "id": d["id"],
#         "values": e["values"],
#         "metadata": {
#             "source_text": d["text"],
#             "category": d["category"]
#         }
#     })

# # Upsert the records into the index
# index.upsert(
#     vectors=records,
#     namespace="plantr-namespace"
# )

# # Wait for the index to be ready
# while not pc.describe_index(index_name).status['ready']:
#     time.sleep(1)



# print(embeddings)