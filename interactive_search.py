from shared_functions import *

food_items = []
search_history = []

def main():
    try:
        print("🍽️  Interactive Food Recommendation System")
        print("=" * 50)
        print("Loading food database...")

        global food_items
        global search_history
        food_items = load_food_data('./FoodDataSet.json')
        print(f"✅ Loaded {len(food_items)} food items successfully")

        collection = create_similarity_search_collection(
            "interactive_food_search",
            {'description': 'A collection for interactive food search'}
        )
        populate_similarity_collection(collection, food_items)
        
        # Start interactive chatbot
        interactive_food_chatbot(collection)
    except Exception as e:
        print(f"❌ Error initializing system: {e}")

def interactive_food_chatbot(collection):
    print("\n" + "="*50)
    print("🤖 INTERACTIVE FOOD SEARCH CHATBOT")
    print("="*50)
    print("Commands:")
    print("  • Type any food name or description to search")
    print("  • 'help' - Show available commands")
    print("  • 'quit' or 'exit' - Exit the system")
    print("  • Ctrl+C - Emergency exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n🔍 Search for food: ").strip()

            if not user_input:
                print("   Please enter a search term or 'help' for commands")
                continue

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using the Food Recommendation System!")
                print("   Goodbye!")
                break

            elif user_input.lower() in ['help', 'h']:
                show_help_menu()

            elif user_input.lower() in ['history']:
                handle_history_command()

            else:
                handle_food_search(collection, user_input)
        
        except KeyboardInterrupt:
            print("\n\n👋 System interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error processing request: {e}")

def show_help_menu():
    """Display help information for users"""
    print("\n📖 HELP MENU")
    print("-" * 30)
    print("Search Examples:")
    print("  • 'chocolate dessert' - Find chocolate desserts")
    print("  • 'Italian food' - Find Italian cuisine")
    print("  • 'sweet treats' - Find sweet desserts")
    print("  • 'baked goods' - Find baked items")
    print("  • 'low calorie' - Find lower-calorie options")
    print("\nCommands:")
    print("  • 'help' - Show this help menu")
    print("  • 'quit' - Exit the system")

def handle_food_search(collection, query):
    
    search_history.append(query)
    print(f"\n🔍 Searching for '{query}'...")
    print("   Please wait...")

    results = perform_similarity_search(collection, query, 5)

    if not results:
        print("❌ No matching foods found.")
        print("💡 Try different keywords like:")
        print("   • Cuisine types: 'Italian', 'American'")
        print("   • Ingredients: 'chocolate', 'flour', 'cheese'")
        print("   • Descriptors: 'sweet', 'baked', 'dessert'")
        return
    
    print(f"\n✅ Found {len(results)} recommendations:")
    print("=" * 60)

    for i, result in enumerate(results, 1):
        # Calculate percentage score
        percentage_score = result['similarity_score'] * 100
        
        print(f"\n{i}. 🍽️  {result['food_name']}")
        print(f"   📊 Match Score: {percentage_score:.1f}%")
        print(f"   🏷️  Cuisine: {result['cuisine_type']}")
        print(f"   🔥 Calories: {result['food_calories_per_serving']} per serving")
        print(f"   📝 Description: {result['food_description']}")
        
        # Add visual separator
        if i < len(results):
            print("   " + "-" * 50)
    
    print("=" * 60)
    
    # Provide suggestions for further exploration
    suggest_related_searches(results)

def suggest_related_searches(results):
    
    if not results:
        return
    
    cuisines = list(set([r['cuisine_type'] for r in results]))

    for cuisine in cuisines[:3]:  # Limit to 3 suggestions
        print(f"   • Try '{cuisine} dishes' for more {cuisine} options")

    avg_calories = sum([r['food_calories_per_serving'] for r in results]) / len(results)
    if avg_calories > 350:
        print("   • Try 'low calorie' for lighter options")
    else:
        print("   • Try 'hearty meal' for more substantial dishes")

def handle_history_command():

    if not search_history:
        print("📝 No search history available")
        return
    
    print("\n📝 Your Search History:")
    print("-" * 30)

    for i, search in enumerate(search_history[-10:], 1):  # Show last 10
        print(f"{i}. {search}")

if __name__ == "__main__":
    main()