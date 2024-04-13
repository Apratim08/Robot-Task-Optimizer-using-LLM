import langchain
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain import PromptTemplate

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class Retriever:
    def __init__(self, db_path, index):
        self.embedding_process = OpenAIEmbeddings(deployment="text-embedding-ada-002", openai_api_key = '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')
        self._db = FAISS.load_local(db_path, self.embedding_process, index)

    def _post_process(self, retrieval_result):
        # TODO do some postprocess to increase accuracy
        # for now do noting
        return retrieval_result

    def search(self, query):
        docs = self._db.similarity_search(query)
        docs = self._post_process(docs)
        return docs

class Decomposer:
    def __init__(self, envs) ->None:
        db_path = "./db"
        index = "guidebook"

        ret = Retriever(db_path, index)
        out = ret.search(envs)
        # print(out)
        self.output_text = ""
        for doc in out:
            self.output_text+=doc.page_content +'\n'

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
            "subtask2":"subtask1" # means the subtask2 depends on subtask1
            }
            }

            There are some examples:
            [input]
            [envs]
            there are coffee, toy car, red box and blue box on the table1, a green box on the table2
            [tasks]
            carry all the boxes from table1 to the table2
            [output]
            {
            "possible_subtasks": [
            "bring red box from table1 to the table2",
            "bring blue box from table1 to table2"
            ],
            "dependence":{
                
            }
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
            "brought green box back",
            "dependence":{
                
            }
            ]
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
            "dependence":{
                "bring ball to desk :"bring ball to table2"
            }
            ]
            }

            """
        information_template = """
            [envs]
            {envs}
            [tasks]
            {tasks}
            """
        information = HumanMessagePromptTemplate.from_template(information_template)
        system_message = SystemMessage(content=prompt_system)
        prompt = ChatPromptTemplate.from_messages([system_message, information])

        safety_information_template = """
        According to the environment information provide by the robot:\n
        {envs}\n
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
                prompt,
                safety_prompt,
            ]
        )

        from langchain.chains import LLMChain
        from langchain.chat_models import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.chain = LLMChain(llm=llm, prompt=prompt)
        
        # response = chain.run(
        #     {"env_info": prompt.content, "retrievals": output_text }
        # )
            
        # llm = ChatOpenAI(model="gpt-4", temperature=0)
        # self.chain = LLMChain(llm=llm, prompt=prompt)

    def process(self, envs, query) -> dict:
        response = self.chain.run({"envs": envs, "tasks": query, "retrievals": self.output_text})
        try:
            response = eval(response)
        except:
            response = {"possible_subtasks": [], "dependence": {}}
        return response


if __name__ == "__main__":
    decomposer = Decomposer()
    envs = "there are one box, one rubber on the table1. on the far back of the robot, there are another table call table2, there’s a pencil on the table2"
    query = "Bring all the items on table1 to table2, and bring pencil to table1"
    ans = decomposer.process(envs, query)
    print(ans)
