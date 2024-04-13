import langchain
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


class Decomposer:
    def __init__(self) ->None:
        prompt_system = """
        You task is to decompose the tasks into multiple sub-tasks. make sure the output is concise and strictly follow the templates.
        output template would be looks like:
        {
        "possible_subtasks": [
        "subtask1",
        "subtask2"
        ],
        "dependence":
        {
        "subtask2":"subtask1" # only means the subtask2 depends on subtask1, not just mean sequential action
        },
        "objects":[] # object in each subtask, the object sequence should follow the "possible_subtasks" part, not the dependence
        }

        There are some examples:
        [input]
        [envs]
        there are coffee, toy car, red box and blue box on the table1, a green box on the table2
        [tasks]
        carry all the boxes from table1 to the table2, and go to table3
        [output]
        {
        "possible_subtasks": [
        "bring red box from table1 to the table2",
        "bring blue box from table1 to table2",
        "go to table3"
        ],
        "dependence":{
            
        },
        "objects":["red box", "blue box",""]
        }

        [input]
        [envs]
        rubber and pencil are on the table1
        [tasks]
        move all the items on table1 to the red box and brought green box back
        [output]
        {
        "possible_subtasks": [
        "move rubber on the red box ",
        "move pencil on the red box ",
        "brought green box back"
        ],
        "dependence":{
            
        },
        "objects":["rubber","pencil","green box"]
        
        }
        [input]
        [envs]
        "There's a ball on table1, coffee at table 2"
        [tasks]
        "bring the ball to table2, then bring all the items in table2 to desk"
        [output]
        {
        "possible_subtasks": [
        "bring ball to table2",
        "bring ball to desk ",
        "bring coffee back to desk"
        ],
        "dependence":{
            "bring ball to desk :"bring ball to table2"
        },
        "objects":["ball","ball","coffee"]
        }
        
        DON'T show "[output]" in response
        """
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        system_message = SystemMessage(content=prompt_system)

        information_template = """
        [envs]
        {envs}
        [tasks]
        {tasks}
        """

        information = HumanMessagePromptTemplate.from_template(information_template)
        prompt = ChatPromptTemplate.from_messages([system_message, information])
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def process(self, envs, query) -> dict:
        response = self.chain.run({"envs": envs, "tasks": query})
        try:
            response = eval(response)
        except:
            response = {"possible_subtasks": [], "dependence": {},'objects':[]}
        # if len(response['dependence'])>0:
        #     bases = list(response["dependence"].values())
        #     depends = list(response["dependence"].keys())
        #     for sub_depend in depends:
        #         if sub_depend in bases:
        #             i = bases.index(sub_depend)
        #             response["dependence"][bases[i]] = response["dependence"][
        #                 sub_depend
        #             ]

        return response


if __name__ == "__main__":
    decomposer = Decomposer()
    envs = "there are one box, one rubber on the table1. on the far back of the robot, there are another table call table2, there’s a pencil on the table2"
    query = "Bring all the items on table1 to table2, and bring pencil to table1"
    ans = decomposer.process(envs, query)
    print(ans)
