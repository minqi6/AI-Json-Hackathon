import gradio as gr
import json
import random
import subprocess

def ingredient_breakdown(food):
    result = subprocess.run(
            ['python', 'run_flow.py', food],
            text=True,          # Capture output as string
            capture_output=True # Capture both stdout and stderr
        )
    ingredients = result.stdout
    return json.dumps({"ingredient_list": ingredients})
# Simulated functions to mimic the behavior of the actual LLM calls


def recipe_recommendation(category, dietary_restrictions):
    recipe = f"Delicious {category} recipe"
    steps = [f"Step {i}: Do something delicious" for i in range(1, random.randint(4, 7))]
    return json.dumps({"recommended_recipe": recipe, "steps": steps})

def health_assistant(age, weight, activity_level):
    nutrients = [
        "Vitamin C",
        "Vitamin D",
        "Iron",
        "Calcium",
        "Protein",
        "Omega-3 fatty acids"
    ]
    return json.dumps({"essential_nutrients": random.sample(nutrients, k=random.randint(3, 6))})

# Updated Custom CSS for styling with a new color scheme
custom_css = """
body {
    background-color: #FFF8E1;
}
.container {
    max-width: 850px;
    margin: auto;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: #FFFAF0;
}
.input-container, .output-container {
    background-color: #FFF3E0;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 1px solid #FFE0B2;
}
.button-primary {
    background-color: #FF9800 !important;
    color: white !important;
}
.button-primary:hover {
    background-color: #F57C00 !important;
}
h1, h2, h3 {
    color: #5D4037;
}
.gr-input, .gr-box {
    border-color: #FFE0B2 !important;
    background-color: #FFF8E1 !important;
}
.gr-input:focus, .gr-box:focus {
    border-color: #FFB74D !important;
}
.gr-button {
    border: none !important;
}
.gr-form {
    background-color: transparent !important;
    border: none !important;
}
"""

def parse_json_output(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON output"}

def format_output(output_dict):
    if "error" in output_dict:
        return output_dict["error"]
    
    formatted = ""
    for key, value in output_dict.items():
        formatted += f"{key.replace('_', ' ').title()}:\n"
        if isinstance(value, list):
            formatted += "\n".join(f"- {item}" for item in value)
        else:
            formatted += str(value)
        formatted += "\n\n"
    return formatted.strip()

def gradio_recipe_health_assistant():
    with gr.Blocks(css=custom_css) as app:
        gr.Markdown("# 🍽️ Recipe and Health Assistant")
        
        with gr.Tab("🥕 Ingredient Breakdown"):
            with gr.Column(elem_classes="input-container"):
                food_input = gr.Textbox(label="Enter a food item", placeholder="e.g., Spaghetti Carbonara")
                breakdown_button = gr.Button("Get Ingredients", elem_classes="button-primary")
            with gr.Column(elem_classes="output-container"):
                breakdown_output = gr.Textbox(label="Ingredients", lines=5)
        
        with gr.Tab("👨‍🍳 Recipe Recommendation"):
            with gr.Column(elem_classes="input-container"):
                category_input = gr.Dropdown(["Appetizer", "Main Course", "Dessert", "Snack"], label="Food Category")
                dietary_input = gr.CheckboxGroup(
                    ["Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Nut-free"],
                    label="Dietary Restrictions"
                )
                recipe_button = gr.Button("Get Recipe", elem_classes="button-primary")
            with gr.Column(elem_classes="output-container"):
                recipe_output = gr.Textbox(label="Recommended Recipe", lines=8)
        
        with gr.Tab("🥗 Health Assistant"):
            with gr.Column(elem_classes="input-container"):
                age_input = gr.Slider(18, 100, step=1, label="Age")
                weight_input = gr.Slider(40, 200, step=1, label="Weight (kg)")
                activity_input = gr.Radio(["Low", "Medium", "High"], label="Activity Level")
                health_button = gr.Button("Get Nutrition Advice", elem_classes="button-primary")
            with gr.Column(elem_classes="output-container"):
                health_output = gr.Textbox(label="Nutritional Advice", lines=6)

        # Event handlers
        breakdown_button.click(
            lambda x: format_output(parse_json_output(ingredient_breakdown(x))),
            inputs=[food_input],
            outputs=[breakdown_output]
        )
        recipe_button.click(
            lambda x, y: format_output(parse_json_output(recipe_recommendation(x, y))),
            inputs=[category_input, dietary_input],
            outputs=[recipe_output]
        )
        health_button.click(
            lambda x, y, z: format_output(parse_json_output(health_assistant(x, y, z))),
            inputs=[age_input, weight_input, activity_input],
            outputs=[health_output]
        )

    return app

# Launch the app
if __name__ == "__main__":
    app = gradio_recipe_health_assistant()
    app.launch()
