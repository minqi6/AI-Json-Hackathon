from flask import Flask, render_template, request
import asyncio
from aijson import Flow
from dotenv import load_dotenv
import markdown
import traceback
import logging
import json

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

async def run_flow(dietary_preferences, health_goals, meals):
    try:
        flow = Flow.from_file('flow.ai.yaml')
        flow = flow.set_vars(
            dietary_preferences=dietary_preferences,
            health_goals=health_goals,
            meals=meals
        )
        
        results = await flow.run()
        logging.debug(f"Flow results: {results}")
        return results
    except Exception as e:
        logging.error(f"Error in run_flow: {str(e)}")
        logging.error(traceback.format_exc())
        return None

def format_results(results):
    if not results:
        return "No results available. Please try again."

    logging.debug(f"Results type: {type(results)}")
    logging.debug(f"Results content: {results}")

    try:
        if isinstance(results, str):
            # If results is already a string, try to parse it as JSON
            try:
                formatted_results = json.loads(results)
            except json.JSONDecodeError:
                # If it's not valid JSON, return it as is
                return markdown.markdown(results)
        elif isinstance(results, dict):
            # If results is a dictionary, get the 'compile_results' key
            compile_results = results.get('compile_results', '')
            if isinstance(compile_results, str):
                try:
                    formatted_results = json.loads(compile_results)
                except json.JSONDecodeError:
                    # If it's not valid JSON, return it as is
                    return markdown.markdown(compile_results)
            else:
                formatted_results = compile_results
        else:
            return "Unexpected result format. Please try again."

        markdown_results = f"""
# Health and Recipe Report

## Recipe Ideas
{formatted_results.get('Recipe Ideas', 'No recipe ideas available.')}

## Nutritional Evaluation
{formatted_results.get('Nutritional Evaluation', 'No nutritional evaluation available.')}
"""
        return markdown.markdown(markdown_results)
    except Exception as e:
        logging.error(f"Error in format_results: {str(e)}")
        logging.error(traceback.format_exc())
        return f"An error occurred while formatting the results: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            logging.debug(f"Received POST request: {request.form}")
            dietary_preferences = request.form['dietary_preferences']
            health_goals = request.form['health_goals']
            meals = {}
            for i in range(1, 4):  # Assuming 3 meals
                meal_name = request.form.get(f'meal_name_{i}')
                meal_details = request.form.get(f'meal_details_{i}')
                if meal_name and meal_details:
                    meals[meal_name] = meal_details
            
            logging.debug(f"Processed form data: dietary_preferences={dietary_preferences}, health_goals={health_goals}, meals={meals}")
            
            results = asyncio.run(run_flow(dietary_preferences, health_goals, meals))
            formatted_results = format_results(results)
            return render_template('results.html', results=formatted_results)
        except Exception as e:
            logging.error(f"Error in index route: {str(e)}")
            logging.error(traceback.format_exc())
            return render_template('results.html', results=f"An error occurred while processing your request: {str(e)}")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
