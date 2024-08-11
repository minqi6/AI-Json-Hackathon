from aijson import Flow
import asyncio
import sys

async def main(food: str):
    # load the flow
    flow = Flow.from_file('project_Gradio_interface/ingredient_breakdown.ai.yaml')

    # set any variables
    flow = flow.set_vars(food=food)

    # run it
    result = await flow.run()
    print(result)

if __name__ == '__main__':
    food = sys.argv[1]
    asyncio.run(main(food))