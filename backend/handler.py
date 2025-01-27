import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_meal_recommendations(ingredients, meal_type):
    prompt = f"""
    Given these ingredients: {', '.join(ingredients)}, suggest 7 {meal_type} dishes.
    Format the response as a numbered list, with each dish name on a new line.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response["choices"][0]["message"]["content"]
    return parse_gpt_response(output)

def parse_gpt_response(response_text):
    meals = response_text.strip().split("\n")
    return [meal.strip() for meal in meals if meal]
