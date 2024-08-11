from aijson import Flow
import asyncio
import sys

async def main(age, weight, active_level):


    flow = Flow.from_file('project_Gradio_interface/health_assistant.ai.yaml')

        
    flow = flow.set_vars(age=age, weight=weight, active_level=active_level)

        
    result = await flow.run()
    print(result)


if __name__ == '__main__':
    age = sys.argv[1]
    weight = sys.argv[2]
    active_level = sys.argv[3]

    asyncio.run(main(age, weight, active_level))