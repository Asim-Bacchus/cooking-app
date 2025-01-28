import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_meal_recommendations(ingredients, meal_type):
    """Check if ChatGPT recognizes the ingredients before generating meals."""

    # Step 1: Ask ChatGPT if it recognizes all the ingredients
    validation_prompt = f"""
    Here is a list of ingredients: {', '.join(ingredients)}.
    Identify any ingredients that are not commonly used in cooking. 
    Respond only with a comma-separated list of unknown ingredients, 
    or respond with 'VALID' if all ingredients are recognized.
    """
    
    validation_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful chef assistant."},
                  {"role": "user", "content": validation_prompt}],
        temperature=0
    )

    validation_result = validation_response.choices[0].message.content.strip()

    # Step 2: If ChatGPT detects unknown ingredients, return them instead of meal recommendations
    if validation_result != "VALID":
        unknown_ingredients = validation_result.split(", ")
        return {"unknown_ingredients": unknown_ingredients}

    # Step 3: If all ingredients are recognized, generate meal recommendations with only titles
    prompt = f"""
    Given these ingredients: {', '.join(ingredients)}, suggest 7 {meal_type} dishes.
    Respond with ONLY the recipe titles, each on a new line, with no numbers, no extra formatting, and no additional explanation.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful chef assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )

    output = response.choices[0].message.content.strip()
    
    return {"meals": parse_gpt_response(output)}

def parse_gpt_response(response_text):
    """Convert GPT response into a clean list of meal titles."""
    meals = response_text.split("\n")
    return [meal.strip() for meal in meals if meal]
