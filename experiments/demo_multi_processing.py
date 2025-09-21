# from test_envs.env3 import Env3
from multi_tasks_optimization import MultiTasksManagement
import asyncio
async def main(toml, exec_file):
    mtm = MultiTasksManagement()

    description = "'There's a red-box on table 3, a coffee and tea at table 1, a green-box and a blue-box at table 2'"
    task = 'take coffee to table 3 and come back to table 1'
    # actions = mtm.arrangement(description,"",task)
    print(f"Original tasks: {task}")
    actions = [('Goto', 'table 1'), ('Pick', 'coffee'), ('Goto', 'table 3'), ('Place', 'coffee'), ('Goto', 'table 1'), 'Done']
    print(actions)
    i = 0
    injected = True
    while i <len(actions):
        if i==2 and injected:
            new_tasks = 'carry red-box to table 1'
            print("At step 2 inject new tasks during its operation")
            print(f"new tasks: {new_tasks}")
            actions = await mtm.merge(description,"",new_tasks,task,actions,i)
            i = 0
            injected = False
            continue
        action = actions[i]
        print(action)
        i+=1

if __name__ == "__main__":
    toml = "./room3.toml"
    exec_file = "./ar-control-2023.01.13a"
    asyncio.run(main(toml, exec_file))
