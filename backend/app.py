from flask import Flask, request, jsonify
from handler import get_meal_recommendations

app = Flask(__name__)


@app.route("/recommend", methods=["POST"])
def recommend_meals():
    """Handle meal recommendations, ensuring robust input validation."""
    data = request.json

    # ✅ Edge Case 1: No data sent
    if not data:
        return jsonify({"error": "Invalid request. JSON data is required."}), 400

    # ✅ Edge Case 2: No 'ingredients' field or incorrect type
    if "ingredients" not in data or not isinstance(data["ingredients"], list):
        return jsonify({"error": "Invalid request. Please provide a list of ingredients."}), 400

    # ✅ Edge Case 3: Empty ingredients list
    if len(data["ingredients"]) == 0:
        return jsonify({"error": "Ingredient list cannot be empty."}), 400

    ingredients = data["ingredients"]
    meal_type = data.get("meal_type", "any")

    # ✅ Edge Case 4: Empty or invalid meal type (optional)
    if not isinstance(meal_type, str) or meal_type.strip() == "":
        meal_type = "any"  # Default to 'any' if invalid

    # Call GPT function
    response = get_meal_recommendations(ingredients, meal_type)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
