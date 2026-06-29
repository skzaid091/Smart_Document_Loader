from uuid import uuid4
from langchain_core.documents import Document


class FigureChunker:
    """
    Build retrievable chunks from figures.

    Responsibilities:
    - Convert figure information into text.
    - Preserve section context.
    - Preserve figure metadata.
    - Create a single chunk per figure.
    """

    def __init__(self):
        self.figure_no = 1


    def process(self, element, section, document_id, document_name):
        """
        Create a chunk from a figure element.

        Parameters:
            element: Figure element.

            section: Parent section.

        Returns:
            List[DocumentChunk]
        """

        figure_data = element.figure_data

        if not figure_data:
            return []

        content = self._build_content(figure_data, self.figure_no)

        chunk = Document(
            page_content=content,
            metadata={
                # Identification
                "document_id": document_id,
                "chunk_id": str(uuid4()).split("-")[-1],
                "chunk_index": -1,

                # Source citation
                "source": document_name,
                "page_number": element.page_number,
                "section_title": section["title"],

                # Chunk information
                "chunk_type": "figure",
                "figure_no": self.figure_no
            }
        )

        self.figure_no += 1

        return [chunk]


    def _build_content(self, figure_data, figure_no):
        """
        Convert figure information
        into retrievable text.
        """

        parts = []

        caption = getattr(figure_data, "caption", None)
        summary = getattr(figure_data, "summary", None)

        # -------------------------
        # Figure No
        # -------------------------
        if figure_no:
            parts.append(f"Figure Number: {figure_no}")

        # -------------------------
        # Caption
        # -------------------------
        if caption and "failed" not in caption.lower():
            parts.append(f"Figure Caption: {caption}")

        # -------------------------
        # Summary
        # -------------------------
        if summary and str(summary).strip():
            parts.append(f"Figure Summary: {summary}")


        # -------------------------
        # Fallback
        # -------------------------

        if not parts:
            parts.append("Figure present. Caption unavailable.")

        return "\n\n".join(parts)