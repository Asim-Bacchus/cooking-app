import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_meal_recommendations(ingredients, meal_type):
    """Fetch meal recommendations from ChatGPT based on ingredients."""
    
    prompt = f"""
    Given these ingredients: {', '.join(ingredients)}, suggest 7 {meal_type} dishes.
    Format the response as a numbered list, with each dish name on a new line.
    """

    # Use latest OpenAI API format
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful chef assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    # Extract response correctly
    output = response.choices[0].message.content.strip()
    
    # Parse response into a list
    return parse_gpt_response(output)

def parse_gpt_response(response_text):
    """Convert GPT response into a list of meal recommendations."""
    meals = response_text.split("\n")
    return [meal.strip() for meal in meals if meal]
