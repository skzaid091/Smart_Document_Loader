from uuid import uuid4
from langchain_core.documents import Document


class FormulaChunker:
    """
    Build retrievable LangChain documents from formulas.

    Responsibilities:
    - Convert extracted formulas into semantic chunks.
    - Preserve section context.
    - Preserve page information.
    - Create one chunk per formula.
    """

    def __init__(self):
        self.formula_no = 1


    def _build_content(self, formula_data, formula_no):
        """
        Convert structured formula information into text
        suitable for embedding and retrieval.
        """

        parts = []

        formula = getattr(formula_data, "formula", None)
        explanation = getattr(formula_data, "explanation", None)

        # -------------------------
        # Formula Number
        # -------------------------
        if formula_no:
            parts.append(f"Formula Number: {formula_no}")

        # -------------------------
        # Formula
        # -------------------------
        if formula and str(formula).strip():
            parts.append(f"Formula: {formula}")

        # -------------------------
        # Explanation
        # -------------------------
        if explanation and str(explanation).strip():
            parts.append(f"Explanation: {explanation}")

        # -------------------------
        # Fallback
        # -------------------------
        if not parts:
            parts.append("Formula present. Description unavailable.")

        return "\n\n".join(parts)


    def process(self, element, section, document_id, document_path):
        """
        Convert a formula element into a LangChain document.

        Parameters
        ----------
        element
            Formula document element.

        section
            Parent section containing the formula.

        Returns
        -------
        list[Document]
            A single LangChain document representing the formula.
        """

        formula_data = element.formula_data

        if not formula_data:
            return []
        
        content = self._build_content(formula_data, self.formula_no)

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
                "chunk_type": "formula",
                "formula_no": self.formula_no
            }
        )

        self.formula_no += 1

        return [chunk]