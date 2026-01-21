from huggingface_hub import login
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM
from llama_index.llms.huggingface import HuggingFaceLLM
from shared_functions import *

import os
import config

load_dotenv()

def hf_login():
    token = os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not token:
        raise RuntimeError("HUGGINGFACE_HUB_TOKEN not set")
    login(token=token)

def create_hf_LLM(
    temperature: float = config.TEMPERATURE,
    max_new_tokens: int = config.MAX_NEW_TOKENS,
    decoding_method: str = "sample",
):
    model = AutoModelForCausalLM.from_pretrained(
        config.LLM_MODEL_ID,
        device_map='auto',
        dtype='auto'
    )
    try:
        llm = HuggingFaceLLM(
            model_name=config.LLM_MODEL_ID,
            tokenizer_name=config.LLM_MODEL_ID,
            max_new_tokens=max_new_tokens,
            model=model,
            messages_to_prompt=None,
            completion_to_prompt=None,
            generate_kwargs={
                "temperature": temperature,
                "top_k": config.TOP_K,
                "top_p": config.TOP_P,
                "do_sample": decoding_method == "sample",
            }
        )

        print(f"Created HuggingFace LLM model: {config.LLM_MODEL_ID}")
        return llm
    except Exception as e:
        print(f"Failed to create HuggingFace LLM: {e}")
        return None
    
def main():
    """Main function for enhanced RAG chatbot system"""
    try:
        print("🤖 Enhanced RAG-Powered Food Recommendation Chatbot")
        print("   Powered by IBM Granite & ChromaDB")
        print("=" * 55)
        
        # Load food data
        global food_items
        food_items = load_food_data('./FoodDataSet.json')
        print(f"✅ Loaded {len(food_items)} food items")
        
        # Create collection for RAG system
        collection = create_similarity_search_collection(
            "enhanced_rag_food_chatbot",
            {'description': 'Enhanced RAG chatbot with IBM watsonx.ai integration'}
        )
        populate_similarity_collection(collection, food_items)
        print("✅ Vector database ready")
        
        hf_login()
        model = create_hf_LLM()
        # Test LLM connection
        print("🔗 Testing LLM connection...")

        test_response = model.complete("Hello")

        if test_response:
            print("✅ LLM connection established")
        else:
            print("❌ LLM connection failed")
            return
        
        enhanced_rag_food_chatbot(collection)

    except Exception as error:
        print(f"❌ Error: {error}")

def enhanced_rag_food_chatbot(collection):
    pass