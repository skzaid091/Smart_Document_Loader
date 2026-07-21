"""
Example: Using SmartDocumentLoader

This example demonstrates how to process a document using
SmartDocumentLoader and generate LangChain Document chunks
that can be used in Retrieval-Augmented Generation (RAG)
pipelines, vector databases, or other downstream applications.
"""

from Smart_Document_Loader.loader import SmartDocumentLoader


# ---------------------------------------------------------------------
# Initialize the document loader.
#
# Parameters
# ----------
# llm_config : dict
#     Configuration for the language model used by the loader.
#
# vlm_config : dict
#     Configuration for the vision-language model used for
#     figure understanding and formula extraction.
#
# storage : dict
#     Configuration for storing raw documents, processed chunks,
#     and document metadata.
# ---------------------------------------------------------------------
loader = SmartDocumentLoader(

    llm_config={
        "provider": "groq",
        "api_key": "<GROQ_API_KEY>",
    },

    vlm_config={
        "provider": "gemini",
        "api_key": "<GOOGLE_API_KEY>",
    },

    storage={

        # Root storage directory.
        "root": "./storage",

        # Directory where original documents are stored.
        "raw_documents_dir": "raw_documents",

        # Metadata storage configuration.
        "metadata": {
            "type": "mongodb",
            "uri": "mongodb://localhost:27017",
            "database": "documents",
            "collection": "metadata",
        },

        # Chunk storage configuration.
        "chunks": {
            "type": "filesystem",
            "output_directory": "processed_documents",
        },
    },
)


# ---------------------------------------------------------------------
# Path to the input document.
#
# Supported formats include:
#
# - PDF
# - Images
# - Microsoft Word
# - PowerPoint
# - Excel
# - HTML
# - Markdown
# - CSV
# - JSON
# - XML
# - Text
# ---------------------------------------------------------------------
document_path = "examples/documents/attention_is_all_you_need_Paper.pdf"


# ---------------------------------------------------------------------
# Process the document.
#
# The document understanding pipeline includes:
#
#   1. Document loading
#   2. Office-to-PDF conversion (if required)
#   3. Layout detection
#   4. OCR
#   5. Reading-order reconstruction
#   6. Table extraction
#   7. Figure understanding
#   8. Formula extraction
#   9. Metadata generation
#  10. Semantic chunk creation
#  11. Chunk persistence
#  12. Metadata persistence
#
# Returns
# -------
# List[langchain_core.documents.Document]
# ---------------------------------------------------------------------
document_chunks = loader.invoke(document_path)

print(f"Generated {len(document_chunks)} document chunks.")

for chunk in document_chunks:

    print("=" * 80)
    print(f"Chunk Type : {chunk.metadata['chunk_type']}")
    print(f"Page       : {chunk.metadata['page_number']}")

    section_title = chunk.metadata.get("section_title", "")
    if section_title:
        print(f"Section    : {section_title}")

    print()
    print(chunk.page_content)
    print()