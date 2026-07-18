from .text_chunker import TextChunker
from .table_chunker import TableChunker
from .figure_chunker import FigureChunker
from .formula_chunker import FormulaChunker


class ChunkBuilder:
    """
    Build all chunk types for a document.

    Responsibilities:
    - Generate text chunks
    - Generate table chunks
    - Generate figure chunks
    - Generate formula chunks

    Produces a unified chunk collection
    for indexing and retrieval.
    """

    def __init__(self, chunking_config):

        self.text_chunker = TextChunker(chunking_config)
        self.table_chunker = TableChunker()
        self.figure_chunker = FigureChunker()
        self.formula_chunker = FormulaChunker()


    def process(self, document):

        chunks = []
        document_id = document.document_id
        document_path = document.file_path

        for section in document.sections:

            for element in section["elements"]:

                if element.element_type == "plain text":
                    chunks.extend(
                        self.text_chunker.process(element, section, document_id, document_path)
                    )

                elif element.element_type == "table":

                    chunks.extend(self.text_chunker.flush(document_id, document_path))
                    chunks.extend(
                        self.table_chunker.process(element, section, document_id, document_path)
                    )

                elif element.element_type == "figure":
                    chunks.extend(self.text_chunker.flush(document_id, document_path))
                    chunks.extend(
                        self.figure_chunker.process(element, section, document_id, document_path)
                    )

                elif element.element_type in ["isolate_formula", "formula"]:
                    chunks.extend(self.text_chunker.flush(document_id, document_path))
                    chunks.extend(
                        self.formula_chunker.process(element, section, document_id, document_path)
                    )
            
        # Final flush for remaining text
        chunks.extend(
            self.text_chunker.flush(document_id, document_path)
        )

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index
 
        return chunks