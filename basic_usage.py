"""
Example: Using SmartDocumentLoader

This example demonstrates the basic usage of SmartDocumentLoader
to process a document and obtain LangChain Document chunks that
can be directly used for RAG pipelines, vector stores, or other
downstream applications.
"""

import os
from dotenv import load_dotenv

from Smart_Document_Loader.loader import SmartDocumentLoader

# ---------------------------------------------------------------------
# Load environment variables (e.g., GROQ_API_KEY) from the .env file.
# ---------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------
# Initialize the SmartDocumentLoader.
#
# Required:
#   - groq_api_key: API key used for LLM/VLM-based extraction tasks.
#
# Optional configuration parameters (not shown here) can be used to
# customize OCR, layout detection, table extraction, formula extraction,
# image captioning, chunking strategy, and more.
# ---------------------------------------------------------------------
loader = SmartDocumentLoader(
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------------------------------------------------------
# Path to the document that needs to be processed.
#
# Supported formats include PDFs, images, Word documents, PowerPoint,
# Excel, text files, and other supported document types.
# ---------------------------------------------------------------------
pdf_path = "/<path_to_file>/attention_is_all_you_need_Paper.pdf"

# ---------------------------------------------------------------------
# Process the document.
#
# invoke() performs the complete document understanding pipeline:
#
#   1. Document loading
#   2. Layout detection
#   3. OCR (if required)
#   4. Reading order reconstruction
#   5. Table extraction
#   6. Formula extraction
#   7. Figure processing
#   8. Metadata generation
#   9. Chunk creation
#
# Returns:
#     List[langchain_core.documents.Document]
# ---------------------------------------------------------------------
document_chunks = loader.invoke(pdf_path)

print(f"Successfully generated {len(document_chunks)} document chunks.")