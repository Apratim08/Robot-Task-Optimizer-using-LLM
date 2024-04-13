from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


class Retriever:
    def __init__(self, db_path, index):
        self.embedding_process = OpenAIEmbeddings(deployment="text-embedding-ada-002")
        self._db = FAISS.load_local(db_path, self.embedding_process, index)

    def _post_process(self, retrieval_result):
        # TODO do some postprocess to increase accuracy
        # for now do noting
        return retrieval_result

    def search(self, query):
        docs = self._db.similarity_search(query)
        docs = self._post_process(docs)
        return docs


if __name__ == "__main__":
    db_path = "./db"
    index = "guidebook"

    ret = Retriever(db_path, index)
    query = "you are standing in a room, you see few boxes and red triangle symbol"
    out = ret.search(query)
    # print(out)
    output_text = ""
    for doc in out:
        output_text+=doc.page_content +'\n'

    print(output_text)

    from langchain.schema import SystemMessage, HumanMessage

    prompt_system = """
        You are a planner for a robot. Your output MUST be one of the following format:
        * Go to {somewhere}
        * Pick {something}
        * Place {something}
        * Done
        
        Here are some examples:

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

    system_message = SystemMessage(content=prompt_system)

    environment_message = HumanMessage(
        content="""
            Environment: room1 is linked to the front_aisle, room2 is connected to the end_aisle.
            A gray table locate in the room1 and a brown table inside the room2. 
            There are two boxes on the gray table, one is green box, another is red box.
            you seen a red triangle symbol at the wall
        """
    )
    state_message = HumanMessage(content="Robot already in room1 at start ")
    task_message = HumanMessage(content="Task: move the boxes to room2's brown table")

    from langchain import PromptTemplate

    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        AIMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    safety_information_template = """
    According to the environment information provide by the robot:\n
    {env_info}\n
    we find out following information in the safety guidebooks:
    {retrievals}\n
    find out the relevant information to help better plan the task
    """
    # safety_information_template = PromptTemplate.from_template(
    #     safety_information_template
    # )
    safety_prompt = HumanMessagePromptTemplate.from_template(
        safety_information_template
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            system_message,
            environment_message,
            state_message,
            safety_prompt,
            task_message,
        ]
    )

    from langchain.chains import LLMChain
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    response = chain.run(
        {"env_info": environment_message.content, "retrievals": output_text }
    )
    # print(out)
    print(response)
