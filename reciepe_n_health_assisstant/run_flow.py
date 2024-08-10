from aijson import Flow
import asyncio
import sys
from new_actions import split_text

async def main(food: str):
    # load the flow
    flow = Flow.from_file('reciepe_n_health_assisstant/test1.ai.yaml')

    # set any variables
    flow = flow.set_vars(thing=food)

    # run it
    result = await flow.run()
    print(result)

if __name__ == '__main__':
    food = sys.argv[1]
    asyncio.run(main(food))