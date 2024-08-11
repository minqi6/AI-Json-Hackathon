from flask import Flask, render_template, request
import asyncio
from aijson import Flow
from dotenv import load_dotenv
from werkzeug.urls import quote  # or other relevant function


load_dotenv()

app = Flask(__name__)

async def run_flow(dietary_preferences, health_goals, meals):
    flow = Flow.from_file('flow.ai.yaml')
    flow = flow.set_vars(
        dietary_preferences=dietary_preferences,
        health_goals=health_goals,
        meals=meals
    )
    
    results = await flow.run()
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dietary_preferences = request.form['dietary_preferences']
        health_goals = request.form['health_goals']
        meals = {}
        for i in range(1, 4):  # Assuming 3 meals
            meal_name = request.form.get(f'meal_name_{i}')
            meal_details = request.form.get(f'meal_details_{i}')
            if meal_name and meal_details:
                meals[meal_name] = meal_details
        
        results = asyncio.run(run_flow(dietary_preferences, health_goals, meals))
        return render_template('results.html', results=results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)