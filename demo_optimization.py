from multi_tasks_optimization import MultiTasksManagement
import langchain
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


def OriginalCall(query, envs):
    prompt_system = """
    You are a planner for a robot. Your output MUST be one of the following format:
    * Go to {somewhere}
    * Pick {something}
    * Place {something}
    * Done
        

    Environment: Unknown
    Task: Move the yellow box from the white table to the gray table
    1. Go to the white table
    2. Pick the yellow box
    3. Go to the gray table
    4. Place the yellow box
    5. Done

    Environment: Unknown
    Task: Move the yellow box from the white table to the gray table
    1. Go to the white table
    [Status] not near the white table.
    2. Go to the white table
    3. Pick the yellow box
    4. Go to the gray table
    5. Place the yellow box
    6. Done
        
    Environment: Unknown
    Task:   Go forward
    1. Go forward
    2. Done
    
    Environment: Unknown
    Task: Turn left
    1. Turn left
    2. Done
        
    Environment: Unknown
    Task: Turn left
    1. Turn left
    [Status] Not turning left
    2. Turn left
    3. Done
        
    Environment: Unknown
    Task: Turn right
    1. Turn right
    2. Done

    Environment: bedroom is linked to the front_aisle, a living room is linked to the end_aisle, a cup is on the living room
    Task: Go from bedroom to living room to pick up a cup
    1. Go to the front_aisle
    2. Go to the end_aisle
    3. Go to the living room
    4. Pick the cup

        """

    # loop = asyncio.get_event_loop()

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
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"envs": envs, "tasks": query})
    response = response.split("\n")
    return response


mtm = MultiTasksManagement()

# query = "Bring all the items on table1 to table2, and bring pencil to table1"
# envs = "there are one box, one rubber on the table1. on the far back of the robot, there are another table call table2, there’s a pencil on the table2"
# robot_info = ""
# ori_response = OriginalCall(query, envs)
# # print(ori_response)
# improved_response = mtm.arrangement(envs, robot_info, query)
# # print(improved_response)
# print(f"Query: {query}")
# print(f"Envs: {envs}")
# print(f"original anwser:\n{ori_response}")
# print(f"improved anwser:\n{improved_response}")
# print(
#     f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
# )
# print("-" * 20)

# envs = "There's a red box on table1, tea at table 2"
# query = "bring the red box to table2, then bring all the items in table2 to table3"
# robot_info = ""
# ori_response = OriginalCall(query, envs)
# # print(ori_response)
# improved_response = mtm.arrangement(envs, robot_info, query)
# # print(improved_response)
# print(f"Query: {query}")
# print(f"Envs: {envs}")
# print(f"original anwser:\n{ori_response}")
# print(f"improved anwser:\n{improved_response}")
# print(
#     f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
# )
# print("-" * 20)

# envs = "There's a red box on table3, a coffee and tea at table 1,  a green and a blue box at table2"
# query = "bring green box to table4, take coffee to table3, bring red box to table2 and bring blue box to table1,tea to table2"
# robot_info = ""
# ori_response = OriginalCall(query, envs)
# # print(ori_response)
# improved_response = mtm.arrangement(envs, robot_info, query)
# # print(improved_response)
# print(f"Query: {query}")
# print(f"Envs: {envs}")
# print(f"original anwser:\n{ori_response}")
# print(f"improved anwser:\n{improved_response}")
# print(
#     f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
# )
# print("-" * 20)

# envs = "There's a red box on table3, a coffee and tea at table 1,  a green and a blue box at table2"
# query = "take coffee to table 3, come back to table 1, and carry red-box to table 1"
# robot_info = ""
# ori_response = OriginalCall(query, envs)
# # print(ori_response)
# improved_response = mtm.arrangement(envs, robot_info, query)
# # print(improved_response)
# print(f"Query: {query}")
# print(f"Envs: {envs}")
# print(f"original anwser:\n{ori_response}")
# print(f"improved anwser:\n{improved_response}")
# print(
#     f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
# )
# print("-" * 20)
# TODO it can't work
# envs = "there’s room with a dining desk, refrigerator and chair, there’s a piece of beef on the kitchen table. There are onions, pork in the refrigerators"
# query = "find all non vegetarian and bring to the refrigerator"
# robot_info = ""
# ori_response = OriginalCall(query, envs)
# # print(ori_response)
# improved_response = mtm.arrangement(envs, robot_info, query)
# # print(improved_response)
# print(f"Query: {query}")
# print(f"Envs: {envs}")
# print(f"original anwser:\n{ori_response}")
# print(f"improved anwser:\n{improved_response}")
# print(
#     f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
# )
# print("-" * 20)


# envs = "a desk with three blank paper, a paper with words on the chair"
# query = "I printed a document but I don’t know which printer has it. Find the document and bring back to desk"
# robot_info = ""
# ori_response = OriginalCall(query, envs)
# # print(ori_response)
# improved_response = mtm.arrangement(envs, robot_info, query)
# # print(improved_response)
# print(f"Query: {query}")
# print(f"Envs: {envs}")
# print(f"original anwser:\n{ori_response}")
# print(f"improved anwser:\n{improved_response}")
# print(
#     f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
# )
# print("-" * 20)

# envs = "a room with 2 tables,a trash bin and a refrigerator. There are an empty cole can and used napkins in table1, a rotted apple and carrot on table2, a expired onion and a banana in the refrigerator"
# query = (
#     "can you help me clear up the room and bring a banana to table1"
# )
# robot_info = ""
# ori_response = OriginalCall(query, envs)
# # print(ori_response)
# improved_response = mtm.arrangement(envs, robot_info, query)
# # print(improved_response)
# print(f"Query: {query}")
# print(f"Envs: {envs}")
# print(f"original anwser:\n{ori_response}")
# print(f"improved anwser:\n{improved_response}")
# print(
#     f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
# )
# print("-" * 20)

envs = "room 1 is connected to room 2, room 2 connects to room 3 and room 4, room 3 is connected to room 6, room 6 is connected to room 4, room  4 is connected to room 5, room 5 is conncted to room3"
query = "find the path robot can go through all the rooms"
robot_info = "robot at room 1"
ori_response = OriginalCall(query, envs)
# print(ori_response)
improved_response = mtm.arrangement(envs, robot_info, query)
# print(improved_response)
print(f"Query: {query}")
print(f"Envs: {envs}")
print(f"original anwser:\n{ori_response}")
print(f"improved anwser:\n{improved_response}")
print(
    f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
)
print("-" * 20)

# envs = """a room with a table has beef, pork, and noodle on it. A kitchen desk has two stoves, stove1 and stove2. A beef takes 10 mins to cook, a pork take 15 mins  and a noodle takes 5 mins to cook, one stove can only cook one item at once"""
# query = "cook beef, pork and noodle in the shorest time, and bring the cooked meat back to table "
# robot_info = ""
# ori_response = OriginalCall(query, envs)
# # print(ori_response)
# improved_response = mtm.arrangement(envs, robot_info, query)
# # print(improved_response)
# print(f"Query: {query}")
# print(f"Envs: {envs}")
# print(f"original anwser:\n{ori_response}")
# print(f"improved anwser:\n{improved_response}")
# print(
#     f"Improved version reduce uncessary {len(ori_response)-len(improved_response)} nodes"
# )
# print("-" * 20)
