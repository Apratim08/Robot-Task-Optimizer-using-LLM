from task_decomposer import Decomposer
from action_chain import ActionChain
from frontend import Analysis
from optimizer import Optimizer
from backend import filter

class MultiTasksManagement:
    def __init__(self) -> None:
        self.decomposer = Decomposer()
        self.chain = ActionChain()
        self.analysis = Analysis()

    async def merge(self,envs,robot_info,query,old_query,old_cmd,index):
        sub_tasks_info = self.decomposer.process(envs, query)
        sub_tasks = sub_tasks_info["possible_subtasks"]
        sub_tasks_objects = sub_tasks_info["objects"]
        sub_tasks_dependence = {}
        # we only treat two sub-tasks deal with the same object as dependence relationship
        for depend, base in sub_tasks_info["dependence"].items():
            depend_index = sub_tasks.index(depend)
            base_index = sub_tasks.index(base)
            if sub_tasks_objects[depend_index] == sub_tasks_objects[base_index]:
                sub_tasks_dependence[depend_index] = base_index

        sub_task_without_done = [
            x
            for x in sub_tasks_dependence.values()
            if x not in list(sub_tasks_dependence.keys())
        ]

        sub_task_actions = []
        for i, sub_task in enumerate(sub_tasks):
            actions = self.chain.execute(
                sub_task, envs, robot_info, i, sub_task_without_done
            )
            sub_task_actions.append(actions)
        # print(sub_task_actions)
        sub_task_actions.insert(0,old_cmd)
        sub_tasks.insert(0,old_query)

        sub_task_actions_analysis = []
        for i, sub_action in enumerate(sub_task_actions):
            input = {
                "Task": sub_tasks[i],
                "envs": envs,
                "robot info": robot_info,
                "actions": sub_action,
            }
            output = self.analysis.execute(input, i)
            sub_task_actions_analysis.append(output)

        sub_task_actions_analysis[0] = sub_task_actions_analysis[0][index:]
        # print(sub_task_actions_analysis)
        # print(len(sub_task_actions_analysis))
        # merge need to start from the original solution
        final_actions = Optimizer(sub_task_actions_analysis, sub_tasks_dependence,merge=True)
        final_actions  = filter(final_actions)
        return final_actions

    def arrangement(self, envs, robot_info, query):
        sub_tasks_info = self.decomposer.process(envs, query)
        sub_tasks = sub_tasks_info["possible_subtasks"]
        sub_tasks_objects = sub_tasks_info["objects"]
        sub_tasks_dependence = {}
        # we only treat two sub-tasks deal with the same object as dependence relationship
        for depend,base in sub_tasks_info["dependence"].items():
            depend_index = sub_tasks.index(depend)
            if type(base)== list:
                for sub_base in base:
                    base_index = sub_tasks.index(sub_base)
                    if sub_tasks_objects[depend_index] == sub_tasks_objects[base_index]:
                        sub_tasks_dependence[depend_index] = base_index
            else:
                base_index = sub_tasks.index(base)
                if sub_tasks_objects[depend_index] == sub_tasks_objects[base_index]:
                    sub_tasks_dependence[depend_index] = base_index

        # sub_tasks_dependence = [
        #     sub_tasks.index(x) for x in sub_tasks_info["dependence"]
        # ]
        # print(sub_tasks)
        sub_task_without_done = [
            x
            for x in sub_tasks_dependence.values()
            if x not in list(sub_tasks_dependence.keys())
        ]
        sub_task_actions = []
        for i, sub_task in enumerate(sub_tasks):
            actions = self.chain.execute(
                sub_task, envs, robot_info, i, sub_task_without_done
            )
            sub_task_actions.append(actions)
        # print(sub_task_actions)
        sub_task_actions_analysis = []
        for i, sub_action in enumerate(sub_task_actions):
            input = {
                "Task": sub_tasks[i],
                "envs": envs,
                "robot info": robot_info,
                "actions": sub_action,
            }
            output = self.analysis.execute(input, i)
            sub_task_actions_analysis.append(output)
        # print(sub_task_actions_analysis)
        # print(len(sub_task_actions_analysis))
        final_actions = Optimizer(sub_task_actions_analysis, sub_tasks_dependence)
        final_actions  = filter(final_actions)
        return final_actions


if __name__=="__main__":
    mtm = MultiTasksManagement()
    envs = "There's a red box on table3, a coffee and tea at table 1,  a green and a blue box at table2"
    query = "bring green box to table4, take coffee to table3, bring red box to table2 and bring blue box to table1,tea to table2"
    robot_info = ""
    res = mtm.arrangement(envs, robot_info, query)
    print(res)
    # envs = "There's a red box on table1, tea at table 2"
    # query = "bring the red box to table2, then bring all the items in table2 to table3"
    # robot_info = ""
    # mtm.arrangement(envs, robot_info, query)
    # query = "Bring all the items on table1 to table2, and bring pencil to table1"
    # envs = "there are one box, one rubber on the table1. on the far back of the robot, there are another table call table2, there’s a pencil on the table2"
    # robot_info = "robot stands in front of table1"
    # mtm.arrangement(envs, robot_info, query)
