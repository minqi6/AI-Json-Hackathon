import asyncio
from aijson import Flow
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Get user input for health and recipe system
    dietary_preferences = input("Enter your dietary preferences (e.g., vegetarian, vegan, gluten-free): ")
    health_goals = input("Enter your health goals (e.g., weight loss, muscle gain, improved digestion): ")

    meals = {}
    while True:
        meal_name = input("Enter meal name (or 'done' to finish): ")
        if meal_name.lower() == 'done':
            break
        meal_details = input(f"Enter details for {meal_name} (e.g., ingredients, preparation method): ")
        meals[meal_name] = meal_details

    # Create and run the flow
    flow = Flow.from_file('flow.ai.yaml')
    flow = flow.set_vars(
        dietary_preferences=dietary_preferences,
        health_goals=health_goals,
        meals=meals
    )
    
    results = await flow.run()
    
    # Print results
    print("\nHealth and Recipe Report:")
    print(results)


if __name__ == "__main__":
    asyncio.run(main())