from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

CONFIG = {

    # -------------------------------------------------------------------------
    # Document Processing
    # -------------------------------------------------------------------------
    "document_types": {

        # Documents processed through the custom document pipeline.
        "custom": {
            ".pdf",
            ".png", ".jpg", ".jpeg", ".tiff",
            ".doc", ".docx", ".ppt", ".pptx", ".odt", ".odp"
        },

        # Documents handled using LangChain loaders.
        "langchain": {
            ".csv", ".xls", ".xlsx", ".ods",
            ".json", ".jsonl", ".xml",
            ".txt", ".md", ".html"
        },

        # Archive documents requiring extraction.
        "archives": {
            ".zip", ".tar", ".7z"
        },

        # Individual document categories.
        "pdf": {
            ".pdf"
        },

        "images": {
            ".png", ".jpg", ".jpeg", ".tiff"
        },

        "office": {
            ".doc", ".docx", ".ppt", ".pptx", ".odt", ".odp"
        },

        "structured": {
            ".csv", ".xls", ".xlsx", ".ods",
            ".json", ".jsonl", ".xml"
        },

        "text": {
            ".txt", ".md", ".html"
        }
    },

    # -------------------------------------------------------------------------
    # OCR Configuration
    # -------------------------------------------------------------------------
    "ocr": {

        # Enable LLM-based OCR correction.
        "enable_ocr_correction": True,

        # OCR engine.
        "ocr_type": "EasyOCR",

        # OCR language(s).
        "ocr_language": "en", 

        # Enable angle classification to automatically detect rotated text.
        "ocr_use_angle_cls": True
    },

    # -------------------------------------------------------------------------
    # Models
    # -------------------------------------------------------------------------
    "language_models": {

        # Vision-Language Model.
        "vlm": "meta-llama/llama-4-scout-17b-16e-instruct",

        # Large Language Model.
        "llm": "llama-3.3-70b-versatile"
    },

    # -------------------------------------------------------------------------
    # Layout Detection
    # -------------------------------------------------------------------------
    "layout_detection": {

        # Layout model base path
        "layout_model_base_path": BASE_DIR / "models" / "layout",

        # Path to the trained document layout detection model.
        "layout_model_path": BASE_DIR / "models" / "layout" / "doclayout_yolo_ft.pt",

        # Minimum confidence score required to retain a detected layout element.
        "layout_confidence_threshold": 0.25,

        # IoU threshold for removing overlapping duplicate detections using NMS.
        "duplicate_removal_iou_threshold": 0.6,

        # Layout classes treated as textual content
        "text_element_types": [

            "plain text",
            "title",
            "header",
            "footer",

            "figure_caption",
            "table_caption",
            "formula_caption"
        ],
    },

    "table_cell_padding": 2, 
    

    # ==========================================================
    # Formula Extracton Config
    # ==========================================================
    "formula_extraction": {
        "formula_elements": [
            "formula",
            "isolate_formula"
        ]
    },

    # ==========================================================
    # Chunking
    # ==========================================================
    "chunking": {

        # Desired chunk size
        "target_chunk_size": 400,

        # Minimum acceptable chunk size
        "min_chunk_size": 100,

        # Overlap between adjacent chunks
        "overlap_size": 30,

        # Order of separators used during recursive splitting.
        "separators": [
            "\n\n",
            "\n",
            " ",
            ""
        ],

        # Keep separators with the preceding chunk.
        "keep_separator": True,

        # Store the starting character index of each chunk.
        "add_start_index": True,

        # Remove leading and trailing whitespace from chunks.
        "strip_whitespace": True
    },
}