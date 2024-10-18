import os
import json


def get_settings_data():
    kb_vector_index = os.getenv('KB_VECTOR_INDEX', 'retail_kb')

    sample_questions_map = {
        'retail_kb': ["What is the Return Policy?", "How long does shipping take?", "What are the shipping options?"],
        'transport_kb': ["When is the next scheduled maintenance for truck LOG-TRK-8399?", "What is the status of the delivery for order QR-0812-54321?", "What is the current route for truck LOG-TRK-2321?"],
        'itsystems_kb': ["How can I reset my corporate email password?", "How do I set up a virtual meeting room?", "How do I map a network drive?"]
    }

    sample_3_questions = sample_questions_map.get(kb_vector_index, sample_questions_map['retail_kb'])

    model_details_json = os.getenv('MODEL_DETAILS', '[]')
    model_details = json.loads(model_details_json)
    model_names = [{"name": model['model_name'], "link": model['link']} for model in model_details]

    return {
        "temperature": 0.7,
        "max_tokens": 100,
        "vector_dbs": [
            {
                "name": "MILVUS",
                "link": "https://milvus.io/"
            },
        {
                "name": "PINECONE",
                "link": "https://www.pinecone.io/"
            },
            {
                "name": "CHROMA",
                "link": "https://www.trychroma.com/"
            },
            {
                "name": "FAISS",
                "link": "https://github.com/facebookresearch/faiss"
            },
            {
                "name": "PGVECTOR",
                "link": "https://github.com/pgvector/pgvector"
            }
        ],
        "user_id": "genius",
        "chatbot_name": "RetailGenius AI",
        "chatbot_desc": "ACME's Intelligent Shopping Assistant!",
        "models": model_names,
        "sample_3_questions": sample_3_questions,
        "kb_name": kb_vector_index
    }
