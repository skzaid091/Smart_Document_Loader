from pathlib import Path

from .data_models import DocumentMetadata


def generate_document_metadata(raw_path, document_id, document_chunks, chunks_path) -> DocumentMetadata:
    """
    Generate metadata for a processed document.
    """

    raw_path = Path(raw_path)

    return DocumentMetadata(
        document_id=document_id,
        document_name=raw_path.name,
        source_path=str(raw_path),
        source_type=raw_path.suffix.lower().lstrip("."),
        file_size=raw_path.stat().st_size,
        chunks_count=len(document_chunks),
        chunks_path=str(chunks_path)
    )