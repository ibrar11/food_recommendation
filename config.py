LLM_MODEL_ID = "ibm-granite/granite-3.2-2b-instruct"

SIMILARITY_TOP_K = 5
TEMPERATURE = 0.1
MAX_NEW_TOKENS = 500
MIN_NEW_TOKENS = 1
TOP_K = 50
TOP_P = 1

CHUNK_SIZE = 500

USER_QUESTION_TEMPLATE = '''You are a helpful food recommendation assistant. A user is asking for food recommendations, and I've retrieved relevant options from a food database.
User Query: "{query}"
Retrieved Food Information:
{context}
Please provide a helpful, short response that:
1. Acknowledges the user's request
2. Recommends 2-3 specific food items from the retrieved options
3. Explains why these recommendations match their request
4. Includes relevant details like cuisine type, calories, or health benefits
5. Uses a friendly, conversational tone
6. Keeps the response concise but informative
Response:'''