from uuid import uuid4
from langchain_core.documents import Document


class TableChunker:
    """
    Build retrievable chunks from tables.

    Responsibilities:
    - Convert table rows into text.
    - Preserve section context.
    - Preserve table metadata.
    - Create a single chunk per table.
    """

    def __init__(self):
        self.table_no = 1


    def process(self, element, section, document_id, document_path):
        """
        Create a chunk from a table element.

        Parameters:
            element: Table element.

            section: Parent section.

        Returns:
            List[DocumentChunk]
        """

        table_data = element.table_data

        if not table_data:
            return []

        rows = table_data.rows

        if not rows:
            return []

        content = self._rows_to_text(rows, self.table_no)

        chunk = Document(
            page_content=content,
            metadata={
                # Identification
                "document_id": document_id,
                "chunk_id": str(uuid4()).split("-")[-1],
                "chunk_index": -1,

                # Source citation
                "source": document_path,
                "page_number": element.page_number,
                "section_title": section["title"],

                # Chunk information
                "chunk_type": "table",
                "table_no": self.table_no
            }
        )

        self.table_no += 1

        return [chunk]
    

    def _rows_to_text(self, rows, table_no):
        """
        Convert table rows into
        retrievable text.

        Example:

            [
                ["A", "B"],
                ["1", "2"]
            ]

        Becomes:

            A | B
            1 | 2
        """
        lines = [f"Table {table_no}", ""]

        for row in rows:
            values = [str(cell).strip() for cell in row]
            lines.append(" | ".join(values))

        return "\n".join(lines)