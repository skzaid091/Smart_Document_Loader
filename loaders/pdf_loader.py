import os
import pymupdf
import subprocess

from ..data_models import *
from .base_loader import BaseLoader


class PDFLoader(BaseLoader):

    def __init__(self, workspace):
        
        self.workspace = workspace

    
    def load(self, path, converted_file=False):
        
        if not converted_file:
            path = self.workspace.save_document(path)
            
        document_id = self.workspace.create()

        try:
            # Open PDF using PyMuPDF.
            with pymupdf.open(path) as doc:

                # Extract document-level metadata.
                raw_metadata = dict(doc.metadata)
                metadata = {
                    "title": raw_metadata.get("title"),
                    "author": raw_metadata.get("author"),
                    "subject": raw_metadata.get("subject")
                }

                pages = []

                for page in doc:

                    # Extract page text.
                    text = page.get_text("text").strip()

                    # Determine whether the page
                    # contains a native text layer.
                    page_has_text_layer = bool(text)

                    # Extract structured text blocks.
                    text_blocks = self._extract_text_blocks(page)

                    # Original PDF page dimensions.
                    rect = page.rect

                    pages.append(
                        PageContent(
                            page_number=page.number + 1,
                            has_text_layer=page_has_text_layer,

                            text_blocks=text_blocks,

                            original_width=rect.width,
                            original_height=rect.height,
                        )
                    )

                return Document(
                    document_id=document_id,
                    document_type="pdf",

                    file_path=path,
                    metadata=metadata,

                    page_count=len(doc),
                    pages=pages,

                    error=None
                )
        

        except Exception as e:

            return Document(
                document_id=document_id,
                document_type="pdf",

                file_path=path,
                metadata={},

                page_count=0,
                pages=[],

                error=f"Failed to open PDF: {e}"
            )


    def _extract_text_blocks(self, page):
        """
        Extract text blocks together with their bounding boxes.

        These blocks preserve layout information and are useful
        for downstream tasks such as:
        - Layout analysis
        - OCR fallback
        - Chunking
        - Context reconstruction
        """

        blocks = []

        for block in page.get_text("dict")["blocks"]:

            # Skip image-only blocks.
            if "lines" not in block:
                continue

            text_parts = []

            # Collect all text spans belonging
            # to the current block.
            for line in block["lines"]:
                for span in line["spans"]:
                    text_parts.append(span["text"])

            text = " ".join(text_parts).strip()

            # Ignore empty blocks.
            if not text:
                continue

            blocks.append(
                {
                    "text": text,
                    "bbox": block["bbox"]
                }
            )

        return blocks
    

    def convert_to_pdf(self, file_path):
        """
        Convert a document into PDF using LibreOffice.

        Args:
            file_path:
                Path to the source document.

        Returns:
            str:
                Path to the generated PDF.

        Raises:
            FileNotFoundError:
                If the source file does not exist.

            RuntimeError:
                If conversion fails or the PDF
                cannot be located afterwards.
        """

        # Ensure the source file exists.
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_name = os.path.basename(file_path)
        output_dir = self.workspace.documents_dir

        try:

            # Run LibreOffice in headless mode to
            # convert the document into PDF.
            subprocess.run(
                [
                    "libreoffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    file_path,
                    "--outdir",
                    str(output_dir)
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Expected PDF output path.
            pdf_name = os.path.splitext(file_name)[0] + ".pdf"
            pdf_path = output_dir / pdf_name

            # Verify that the conversion actually
            # produced a PDF file.
            if not os.path.exists(pdf_path):

                raise RuntimeError(
                    "PDF conversion succeeded "
                    "but output file was not found."
                )

            return pdf_path

        except subprocess.CalledProcessError as e:

            # Surface LibreOffice error messages
            # to the caller.
            raise RuntimeError(
                "Failed to convert document to PDF: "
                f"{e.stderr.decode(errors='ignore')}"
            ) from e