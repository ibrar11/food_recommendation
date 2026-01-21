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

def prepare_context_for_llm(query: str, search_results: List[Dict]) -> str:
    """Prepare structured context from search results for LLM"""
    if not search_results:
        return "No relevant food items found in the database."
    
    context_parts = []
    context_parts.append("Based on your query, here are the most relevant food options from our database:")
    context_parts.append("")
    
    for i, result in enumerate(search_results[:3], 1):
        food_context = []
        food_context.append(f"Option {i}: {result['food_name']}")
        food_context.append(f"  - Description: {result['food_description']}")
        food_context.append(f"  - Cuisine: {result['cuisine_type']}")
        food_context.append(f"  - Calories: {result['food_calories_per_serving']} per serving")
        
        if result.get('food_ingredients'):
            ingredients = result['food_ingredients']
            if isinstance(ingredients, list):
                food_context.append(f"  - Key ingredients: {', '.join(ingredients[:5])}")
            else:
                food_context.append(f"  - Key ingredients: {ingredients}")
        
        if result.get('food_health_benefits'):
            food_context.append(f"  - Health benefits: {result['food_health_benefits']}")
        
        if result.get('cooking_method'):
            food_context.append(f"  - Cooking method: {result['cooking_method']}")
        
        if result.get('taste_profile'):
            food_context.append(f"  - Taste profile: {result['taste_profile']}")
        
        food_context.append(f"  - Similarity score: {result['similarity_score']*100:.1f}%")
        food_context.append("")
        
        context_parts.extend(food_context)
    
    return "\n".join(context_parts)

def generate_llm_rag_response(query: str, search_results: List[Dict]) -> str:
    """Generate response using IBM Granite with retrieved context"""
    try:
        # Prepare context from search results
        context = prepare_context_for_llm(query, search_results)
        
        # Build the prompt for the LLM
        prompt = config.USER_QUESTION_TEMPLATE.format(
            query=query,
            context=context
        )

        model = create_hf_LLM()

        response = model.complete(prompt)


        if response:            
            # Clean up the response if needed
            response_text = response.text.strip()
            
            # If response is too short, provide a fallback
            if len(response_text) < 50:
                return generate_fallback_response(query, search_results)
            
            return response_text
        else:
            return generate_fallback_response(query, search_results)

    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return

def generate_fallback_response(query: str, search_results: List[Dict]) -> str:
    """Generate fallback response when LLM fails"""
    if not search_results:
        return "I couldn't find any food items matching your request. Try describing what you're in the mood for with different words!"
    
    top_result = search_results[0]
    response_parts = []
    
    response_parts.append(f"Based on your request for '{query}', I'd recommend {top_result['food_name']}.")
    response_parts.append(f"It's a {top_result['cuisine_type']} dish with {top_result['food_calories_per_serving']} calories per serving.")
    
    if len(search_results) > 1:
        second_choice = search_results[1]
        response_parts.append(f"Another great option would be {second_choice['food_name']}.")
    
    return " ".join(response_parts)