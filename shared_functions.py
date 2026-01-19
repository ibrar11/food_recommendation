import chromadb
from chromadb.utils import embedding_functions
import json
import re
import numpy as np
from typing import List, Dict, Any, Optional

client = chromadb.Client()

def load_food_data(file_path: str) -> List[Dict]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            food_data = json.load(file)
        
        for i, item in enumerate(food_data):
            if "food_id" not in item:
                item['food_id'] = str(i + 1)
            else:
                item['food_id'] = str(item['food_id'])
            
            if 'food_ingredients' not in item:
                item['food_ingredients'] = []
            if 'food_description' not in item:
                item['food_description'] = ''
            if 'cuisine_type' not in item:
                item['cuisine_type'] = 'Unknown'
            if 'food_calories_per_serving' not in item:
                item['food_calories_per_serving'] = 0

            if "food_features" in item and isinstance(item["food_features"], dict):
                taste_features= []
                for key, value in item['food_features'].items():
                    if value:
                        taste_features.append(str[value])
                item['taste_profile'] = ', '.join(taste_features)
            else :
                item['taste_profile'] = ''
        
        print(f"Successfully loaded {len(food_data)} food items from {file_path}")
        return food_data
    except Exception as e:
        print(f"Error loading food data: {e}")
        return []

def create_similarity_search_collection(collection_name: str, collection_metadata: dict = None):
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    return client.create_collection(
        name= collection_name,
        metadata= collection_metadata,
        configuration={
            "hnsw": {"space": "cosine"},
            "embedding_function": sentence_transformer_ef
        }
    )
