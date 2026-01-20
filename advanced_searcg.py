from shared_functions import *

def main():
    """Main function for advanced search demonstrations"""
    try:
        print("🔬 Advanced Food Search System")
        print("=" * 50)
        print("Loading food database with advanced filtering capabilities...")

        food_items = load_food_data('./FoodDataSet.json')
        print(f"✅ Loaded {len(food_items)} food items successfully")

        # Create collection specifically for advanced search operations
        collection = create_similarity_search_collection(
            "advanced_food_search",
            {'description': 'A collection for advanced search demos'}
        )
        populate_similarity_collection(collection, food_items)

        interactive_advanced_search(collection)
        
    except Exception as error:
        print(f"❌ Error initializing advanced search system: {error}")

def interactive_advanced_search(collection):
    pass