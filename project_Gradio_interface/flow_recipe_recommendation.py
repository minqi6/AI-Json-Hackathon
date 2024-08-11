from aijson import Flow
import asyncio
import sys

async def main(category, dietary_restrictions):
    # load the flow
    flow = Flow.from_file('project_Gradio_interface/reciepe_recommendation.ai.yaml')

    # set any variables
    flow = flow.set_vars(category=category, dietary_restrictions=dietary_restrictions)

    # run it
    result = await flow.run()
    print(result)

if __name__ == '__main__':
    category = sys.argv[1]
    dietary_restrictions = sys.argv[2]
    asyncio.run(main(category, dietary_restrictions))