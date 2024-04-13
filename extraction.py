from kor import create_extraction_chain, Object, Text, Number, Selection, Option
from langchain.llms import AzureOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.embeddings import OpenAIEmbeddings
import tqdm
import json
import uuid
from pathlib import Path
from langchain.chains import LLMChain
import re


class InformationExtraction:
    def __init__(self):
        self._text_splitter = None
        self._embedding_process = OpenAIEmbeddings(
            deployment="text-embedding-ada-002"
        ).embed_query

    def chunk_split(
        self,
        documents,
        _chunk_size=512,
        _chunk_overlap=100,
    ) -> List:
        if not self._text_splitter:
            self._text_splitter = RecursiveCharacterTextSplitter(
                chunk_overlap=_chunk_overlap,
                length_function=len,
                chunk_size=_chunk_size,
            )
        chunks = []
        return chunks

    def information_extraction(
        self, chunks, saved=True, format="json", save_dir="./storage"
    ):
        output = []
        for single_chunk in tqdm.tqdm(chunks):
            nodes = single_chunk["nodes"]
            id = id["id"]

            for node in nodes:
                # try:
                parse_result = self._extraction_qa_chain.run(node)
                parse_result = eval(parse_result)

                if len(parse_result) == 0:
                    raise ValueError("No information can be extracted")

                for single_highlight in parse_result:
                    vector_result = self._embedding_process(str(single_highlight))
                    # keyword = list(set(parse_result))
                    output.append(
                        {
                            "uuid": str(uuid.uuid4()),
                            "text": node,
                            "id": id,
                            "vector": vector_result,
                        }
                    )

        if saved:
            if format == "json":
                doc = {}
                vector = {}
                keywords = {}

                for item in output:
                    doc[item["uuid"]] = {
                        "text": item["text"],
                        "filename": item["filename"],
                    }
                    vector[item["uuid"]] = item["vector"]

                with open(Path(save_dir) / "doc.json", "w") as f:
                    json.dump(doc, f)
                with open(Path(save_dir) / "vector.json", "w") as f:
                    json.dump(vector, f)

            else:
                print(
                    "Other saved methods are not support yet, saved to json as default"
                )


if __name__ == "__main__":
    import logging
    import sys
    import argparse

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("--storage_path", type=str, default="docs/")
    parser.add_argument("--output_path", type=str, default="./storage")
    # parser.add_argument("--filter", type=str, default=None)

    args = parser.parse_args()
    
    # print(loaded_data[1])

    from langchain.chat_models import ChatOpenAI
    from langchain import OpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)
    extractor = InformationExtraction(qa_pair_generate_prompt, llm)
    out = extractor.chunk_split(loaded_data)
    print(out)
    print(len(out))
    out = extractor.information_extraction(out, save_dir=args.output_path)
