from aijson import Flow
import asyncio
import sys

async def main(age, weight, active_level):
    # load the flow
    flow = Flow.from_file('reciepe_n_health_assisstant/health_assistant.ai.yaml')

    # set any variables
    flow = flow.set_vars(age=age, weight=weight, active_level=active_level)
    # run it
    result = await flow.run()
    print(result)

if __name__ == '__main__':
    age = sys.argv[1]
    weight = sys.argv[2]
    active_level = sys.argv[3]
    asyncio.run(main(age, weight, active_level))