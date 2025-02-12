import { useState } from "react";

export default function CookingApp() {
  const [ingredients, setIngredients] = useState("");
  const [mealType, setMealType] = useState("any");
  const [loading, setLoading] = useState(false);
  const [meals, setMeals] = useState([]);
  const [unknownIngredients, setUnknownIngredients] = useState([]);
  const [error, setError] = useState(null);

  const handleRecommend = async () => {
    setLoading(true);
    setMeals([]);
    setUnknownIngredients([]);
    setError(null);

    // Convert input string into a cleaned-up list
    const ingredientList = ingredients
      .split(",")
      .map((ing) => ing.trim())
      .filter((ing) => ing !== "");

    if (ingredientList.length === 0) {
      setError("Please enter at least one valid ingredient.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: ingredientList, meal_type: mealType }),
      });

      const data = await response.json();

      if (data.unknown_ingredients) {
        setUnknownIngredients(data.unknown_ingredients);
      } else if (data.error) {
        setError(data.error);
      } else {
        setMeals(data.meals || []);
      }
    } catch (err) {
      setError("Failed to fetch recommendations. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-green-400 to-blue-500 p-6 text-white">
      <div className="w-full max-w-xl bg-white p-6 shadow-2xl rounded-3xl text-gray-900">
        <h1 className="text-3xl font-bold text-center mb-6">AI Cooking Assistant</h1>
        
        {/* Ingredient Input */}
        <input
          type="text"
          placeholder="Enter ingredients (comma-separated)"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-xl mb-4 text-gray-900"
        />

        {/* Meal Type Dropdown */}
        <select
          value={mealType}
          onChange={(e) => setMealType(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-xl mb-4 text-gray-900"
        >
          <option value="any">Any</option>
          <option value="breakfast">Breakfast</option>
          <option value="lunch">Lunch</option>
          <option value="dinner">Dinner</option>
        </select>

        {/* Submit Button */}
        <button
          onClick={handleRecommend}
          disabled={loading}
          className="w-full p-3 bg-gradient-to-r from-green-500 to-blue-600 text-white rounded-xl shadow-md hover:opacity-90"
        >
          {loading ? "Loading..." : "Get Meal Recommendations"}
        </button>

        {/* Error Message */}
        {error && <p className="text-red-600 mt-4 text-center font-semibold">{error}</p>}

        {/* Unknown Ingredients Warning */}
        {unknownIngredients.length > 0 && (
          <div className="mt-4 bg-yellow-200 text-yellow-900 p-3 rounded-lg text-center">
            <p className="font-semibold">Unknown ingredients:</p>
            <p>{unknownIngredients.join(", ")}</p>
          </div>
        )}
      </div>

      {/* Recommended Meals List */}
      {meals.length > 0 && (
        <div className="w-full max-w-xl mt-6 p-6 bg-white shadow-2xl rounded-3xl text-gray-900">
          <h2 className="text-xl font-semibold mb-4 text-center">Suggested Meals</h2>
          <ul className="list-disc pl-6 space-y-2">
            {meals.map((meal, index) => (
              <li key={index} className="text-gray-700 text-lg font-medium">{meal}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
