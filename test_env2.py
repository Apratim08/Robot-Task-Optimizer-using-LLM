from test_envs.env2 import Env2
from multi_tasks_optimization_copy import MultiTasksManagement
import asyncio
import agility
import agility.messages as msgs
import aioconsole
async def main(toml,exec_file):
    env = Env2(toml,exec_file)
    mtm = MultiTasksManagement(env.description)
    task = "bring the red-box to table2, then bring all the items in table2 to table3"
    actions = mtm.arrangement(env.description,"",task)

    print(actions)
    async with agility.JsonApi() as api:
        await env.VirtualEnvSetup(api)
        await asyncio.sleep(2)
        for action in actions:
            print(action)
            await env.interact(api,action)

if __name__ == "__main__":
    toml = "./room2.toml"
    exec_file = "./ar-control-2023.01.13a"
    asyncio.run(main(toml,exec_file))