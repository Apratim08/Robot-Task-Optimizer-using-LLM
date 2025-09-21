from langchain.embeddings import OpenAIEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from typing import List

from langchain.vectorstores import FAISS


class InformationExtraction:
    def __init__(self) -> None:
        self._embedding_process = OpenAIEmbeddings(deployment="text-embedding-ada-002")

    def single_textfile_load_chunksplit(
        self,
        textpath,
        _chunk_size: int = 200,
        _chunk_overlap: int = 50,
        separators: List = ["\n"],
    ) -> List:
        data = TextLoader(textpath).load()
        self._text_splitter = RecursiveCharacterTextSplitter(
            length_function=len, chunk_size=200, separators=["\n"], chunk_overlap=50
        )
        out = self._text_splitter.split_documents(data)
        logging.info(f" Split the text into {len(out)} chunks")
        return out

    def process_save(self, splitted_chunks) -> None:
        db = FAISS.from_documents(splitted_chunks, self._embedding_process)
        db.save_local("db", "guidebook")


if __name__ == "__main__":
    import logging
    import sys
    import argparse

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", type=str, default="./storage")

    args = parser.parse_args()

    extractor = InformationExtraction()

    textfile_path = "utils/guidebook.txt"

    splitted_chuncks = extractor.single_textfile_load_chunksplit(textfile_path)
    extractor.process_save(splitted_chuncks)
    
    
