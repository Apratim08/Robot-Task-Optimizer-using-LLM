from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import json
from collections import OrderedDict


class Analysis:
    def __init__(self) -> None:
        prompt_system = """
You need to analyse the provided intruction and corresponding actions, generate useful information for later optimization
Here are some examples:
[input]
{
    "Task":"Go to living room to pick up a cup and put at end_asile",
    "envs": "bedroom is linked to the front_aisle, a living room is linked to the end_aisle, a cup is on the living room",
    "robot info": "Robot is currently at the bedroom",
    "actions":
    [
        "Goto front_aisle",
        "Goto end_aisle",
        "Goto living room",
        "Pick cup",
        "Goto end_aisle",
        "Place the cup"
        "Done"
    ]
}
[output]
[
    {
        "Goto": {
            "Parameter": "front_aisle",
            "items": "",
            "environment":"front_aisle",
            "environment_items":[]
        }
    },
    {
        "Goto": {
            "Parameter": "end_aisle",
            "items": "",
            "environment":"end_aisle",
            "environment_items":[]
        }
    },
    {
        "Goto": {
            "Parameter": "living room",
            "items": "",
            "environment":"living room",
            "environment_items":[]
        }
    },
    {
        "Pick": {
            "Parameter": "cup",
            "items": "cup",
            "environment":"living room",
            "environment_items":[]
            
        }
    },
    {
        "Goto": {
            "Parameter": "end_aisle",
            "items": "cup",
            "environment":"end_aisle",
            "environment_items":[]
            
        }
    },
    {
        "Place": {
            "Parameter": "cup",
            "items": "",
            "environment":"living room",
            "environment_items":["cup"]
            
        }
    },
    
    {
        "Done": {
            "Parameter": "",
            "items": "",
            "environment":"living room",
            "environment_items":["cup"]
        }
    }
]
Output MUST be purely python list AND keep symbol correct. Don't add ANY '\n' at the front!
        """
        system_message = SystemMessage(content=prompt_system)

        from langchain.prompts.chat import (
            ChatPromptTemplate,
            HumanMessagePromptTemplate,
        )

        information_template = """
        {input}
        """
        information = HumanMessagePromptTemplate.from_template(information_template)
        prompt = ChatPromptTemplate.from_messages([system_message, information])
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def execute(self, input, index):
        response = self.chain.run({"input": str(input)})
        # response.strip("\n")
        response = eval(response)
        if response[-1].get("Done"):
            response[-1]["Done"]["Parameter"] = str(index)
        return response  # json.loads(response)


if __name__ == "__main__":
    information_extraction = Analysis()

    sub_actions = [
        ["Goto table1", "Pick box", "Goto table2", "Place box", "Done"],
        ["Goto table1", "Pick rubber", "Goto table2", "Place rubber", "Done"],
        ["Goto table2", "Pick pencil", "Goto table1", "Place pencil", "Done"],
    ]
    for i, sub_action in enumerate(sub_actions):
        input = {
            "Task": "'Bring pencil to table1'",
            "envs": "there are one box, one rubber on the table1. on the far back of the robot, there are another table call table2, there’s a pencil on the table",
            "robot info": "robot stands in front of table1",
            "actions": sub_action,
        }
        output = information_extraction.execute(input, i)
        print(output)
        print("-" * 20)
