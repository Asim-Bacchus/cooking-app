from flask import Flask, request, jsonify
from handler import get_meal_recommendations

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend_meals():
    data = request.json
    ingredients = data.get("ingredients", [])
    meal_type = data.get("meal_type", "any")

    response = get_meal_recommendations(ingredients, meal_type)
    return jsonify({"meals": response})

if __name__ == "__main__":
    app.run(debug=True)
