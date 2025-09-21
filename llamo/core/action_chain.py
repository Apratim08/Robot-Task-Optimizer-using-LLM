from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import json
from collections import OrderedDict

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


class ActionChain:
    def __init__(self) -> None:
        prompt_system = """
            You are a planner for a robot. Your output MUST be one of the following format:
            * Goto {somewhere}
            * Pick {something}
            * Place {something}
            * Done
            
            Here are some examples:
            
            [Tasks]
            Move the yellow box from the white table to the gray table
            [Environment]
            Unknown
            [Robot Information]
            Unkown
            
            [output]
            [
                "Goto white table",
                "Pick yellow box",
                "Goto grey table",
                "Place yellow box",
                "Done"
            ]

            [Tasks]
            Go to desk to pick up a cup of coffee
            [Environment]
            Desk has rubber, ball and coffee on it.
            [Robot Information]
            Unknown
            [output]
            [
                "Goto desk",
                "Pick coffee",
                "Done"
            ]
            
            [Tasks]
            Go to living room to pick up a cup
            [Environment]
            bedroom is linked to the front_aisle, a living room is linked to the end_aisle, a cup is on the living room
            [Robot Information]
            Robot is currently at the bedroom
            [output]
            [
                "Goto front_aisle",
                "Goto end_aisle",
                "Goto living room",
                "Pick cup",
                "Done"
            ]
        Output MUST be purely python list AND keep symbol correct 
        """

        system_message = SystemMessage(content=prompt_system)

        information_template = """
            [Tasks]
            {Tasks}
            [Environment]
            {env_info}
            [Robot Information]
            {robot_info}
        """
        information = HumanMessagePromptTemplate.from_template(information_template)
        prompt = ChatPromptTemplate.from_messages([system_message, information])
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def execute(self, tasks, env_info, robot_info, count,sub_tasks_dependence):
        sub_tasks_dependence = sub_tasks_dependence#[x-1 for x in sub_tasks_dependence]
        response = self.chain.run(
            {"Tasks": tasks, "env_info": env_info, "robot_info": robot_info}
        )
        response = eval(response)  # json.loads(response)
        if count in sub_tasks_dependence:
            response = response[:-1]
        return response

if __name__ == "__main__":
    sub_tasks = [
        "bring box from table1 to table2",
        "bring rubber from table1 to table2",
        "bring pencil from table2 to table1",
    ]
    chain = ActionChain()
    # tasks = "'bring box from table1 to table2'"
    envs = "there are one box, one rubber on the table1. on the far back of the robot, there are another table call table2, there’s a pencil on the table2"
    robot_info = "robot stands in front of table1"
    for sub_task in sub_tasks:
        actions = chain.execute(sub_task, envs, robot_info)
        print(actions)
