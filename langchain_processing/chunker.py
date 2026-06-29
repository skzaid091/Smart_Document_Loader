from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter


class LangChainChunker:
    """
    Splits LangChain Documents into smaller semantic chunks.
    """

    def __init__(self, chunking_config):

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunking_config["chunk_size"],

            chunk_overlap=chunking_config["chunk_overlap"],

            separators=chunking_config["separators"],

            keep_separator=chunking_config["keep_separator"],

            add_start_index=chunking_config["add_start_index"],

            strip_whitespace=chunking_config["strip_whitespace"]
        )


    def process(self, documents):
        """
        Split LangChain Documents into chunks.

        Parameters
        ----------
        documents : list[Document]

        Returns
        -------
        list[Document]
        """
        
        chunks = self.text_splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):

            chunk.metadata["chunk_id"] = str(uuid4()).split("-")[-1]
            chunk.metadata["chunk_index"] = index

        return chunks