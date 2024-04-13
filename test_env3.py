from test_envs.env3 import Env3
from multi_tasks_optimization import MultiTasksManagement
import asyncio
import agility
import agility.messages as msgs
import aioconsole
async def main(toml,exec_file):
    mtm = MultiTasksManagement()
    env = Env3(toml,exec_file)
    task = 'bring green-box to table 4, take coffee to table 3, bring red-box to table 2 and bring blue-box to table 1, tea to table 2'
    # actions = mtm.arrangement(env.description,"",task)
    actions = [('Goto', 'table 1'), ('Pick', 'coffee'), ('Goto', 'table 3'), ('Place', 'coffee'), ('Pick', 'red-box'), ('Goto', 'table 2'), ('Place', 'red-box'), ('Pick', 'blue-box'), ('Goto', 'table 1'), ('Place', 'blue-box'), ('Pick', 'tea'), ('Goto', 'table 2'), ('Place', 'tea'), ('Pick', 'green-box'), ('Goto', 'table 4'), ('Place', 'green-box'), 'Done']
    # actions = [('Goto', 'table 1'), ('Pick', 'coffee'), ('Goto', 'table 3'), ('Place', 'coffee'), ('Pick', 'red-box')]
    # actions = [('Pick', 'coffee'), ('Goto', 'table 3'), ('Place', 'coffee'), ('Pick', 'red box'), ('Goto', 'table 2'), ('Place', 'red box'), ('Pick', 'blue box'), ('Goto', 'table 1'), ('Place', 'blue box'), ('Pick', 'tea'), ('Goto', 'table 2'), ('Place', 'tea'), ('Pick', 'green box'), ('Goto', 'table 4'), ('Place', 'green box'), 'Done']
    print(actions)
    async with agility.JsonApi() as api:
        await env.VirtualEnvSetup(api)
        await asyncio.sleep(2)
        for action in actions:
            print(action)
            await env.interact(api,action)

if __name__ == "__main__":
    toml = "./room3.toml"
    exec_file = "./ar-control-2023.01.13a"
    asyncio.run(main(toml,exec_file))