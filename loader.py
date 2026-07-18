from pathlib import Path

from langchain_core.runnables import Runnable

from .config import CONFIG, BASE_DIR
from .prerequisites import download_prerequisites

# ---------------------------------------------------------------------
# Document Loaders
# ---------------------------------------------------------------------
from .loaders.pdf_loader import PDFLoader
from .loaders.image_loader import ImageLoader
from .loaders.structured_loader import StructuredLoader
from .loaders.text_loader import TextLoader
from .loaders.archive_loader import ArchiveLoader

# ---------------------------------------------------------------------
# Language Models
# ---------------------------------------------------------------------
from .language_models.llm_service import LLMService
from .language_models.vlm_service import VLM_Service

# ---------------------------------------------------------------------
# Processing Components
# ---------------------------------------------------------------------
from .layout.layout_detector import LayoutDetector

from .page_renderrer import PageRenderer

from .extraction.text_extractor import TextExtractor
from .extraction.figure.figure_extractor import FigureExtractor
from .extraction.table.table_extractor import TableExtractor
from .extraction.formula.formula_extractor import FormulaExtractor

from .cleaner.pre_element_cleaner import PreElementCleaner
from .cleaner.document_cleaner import DocumentCleaner

from .section_building.section_builder import SectionBuilder
from .chunking.chunk_builder import ChunkBuilder

from .langchain_processing.chunker import LangChainChunker

from .workspace import Workspace


class SmartDocumentLoader(Runnable[str, list]):
    """
    Smart document loader supporting both custom multimodal processing
    and LangChain-native document loading.

    Custom Pipeline
    ---------------
    PDF
    Office Documents
    Images
        ↓
    Page Rendering
        ↓
    Layout Detection
        ↓
    Text Extraction
        ↓
    Figure Extraction
        ↓
    Table Extraction
        ↓
    Document Cleaning
        ↓
    Section Building
        ↓
    Semantic Chunking

    LangChain Pipeline
    ------------------
    TXT
    Markdown
    HTML
    CSV
    Excel
    JSON
    XML
        ↓
    LangChain Loader
        ↓
    Recursive Text Splitting

    Both pipelines return:

        list[langchain_core.documents.Document]
    """

    def __init__(
            self, 
            groq_api_key,
            documents_dir, 
            ocr_config=None, 
            target_chunk_size=None, 
            min_chunk_size=None, 
            overlap_size=None,
        ):
        """
        Initialize the Smart Document Loader.
        """

        super().__init__()

        if ocr_config is None:
            ocr_config = {}

        # Merge user supplied OCR configuration with defaults.
        for key, value in CONFIG["ocr"].items():
            ocr_config.setdefault(key, value)
        
        CONFIG["chunking"]["target_chunk_size"] = target_chunk_size if target_chunk_size else CONFIG["chunking"]["target_chunk_size"]
        CONFIG["chunking"]["min_chunk_size"] = min_chunk_size if min_chunk_size else CONFIG["chunking"]["min_chunk_size"]
        CONFIG["chunking"]["overlap_size"] = overlap_size if overlap_size else CONFIG["chunking"]["overlap_size"]

        # Download required models and resources.
        download_prerequisites()

        # ------------------------------------------------------------------
        # Documents Storage.
        # ------------------------------------------------------------------
        self.documents_dir = documents_dir

        # ------------------------------------------------------------------
        # Workspace
        # ------------------------------------------------------------------
        self.workspace = Workspace(BASE_DIR, self.documents_dir)

        # ------------------------------------------------------------------
        # Document Loaders
        # ------------------------------------------------------------------
        self.pdf_loader = PDFLoader(self.workspace)
        self.image_loader = ImageLoader(self.workspace)

        self.structured_loader = StructuredLoader(self.workspace)
        self.text_loader = TextLoader(self.workspace)
        self.archive_loader = ArchiveLoader()

        # ------------------------------------------------------------------
        # Language Models
        # ------------------------------------------------------------------
        self.llm_service = LLMService(
            CONFIG["language_models"]["llm"],
            groq_api_key
        )

        self.vlm_service = VLM_Service(
            CONFIG["language_models"]["vlm"],
            groq_api_key
        )

        # ------------------------------------------------------------------
        # Processing Components
        # ------------------------------------------------------------------
        self.page_renderer = PageRenderer(self.workspace)

        self.layout_detector = LayoutDetector(
            CONFIG["layout_detection"]
        )

        self.text_extractor = TextExtractor(
            self.llm_service,
            ocr_config,
            CONFIG["layout_detection"]["text_element_types"]
        )

        self.figure_extractor = FigureExtractor(
            self.workspace,
            self.vlm_service
        )

        self.table_extractor = TableExtractor(
            self.workspace,
            self.llm_service,
            ocr_config,
            CONFIG["layout_detection"]["text_element_types"],
            CONFIG["table_cell_padding"]
        )

        self.formula_extractor = FormulaExtractor(
            self.workspace, 
            self.llm_service, 
            self.vlm_service, 
            CONFIG["formula_extraction"]["formula_elements"], 
            ocr_config,
            CONFIG["layout_detection"]["text_element_types"]
        )

        self.element_cleaner = PreElementCleaner(
            CONFIG["layout_detection"]["text_element_types"]
        )

        self.document_cleaner = DocumentCleaner()

        self.section_builder = SectionBuilder()

        self.chunk_builder = ChunkBuilder(
            CONFIG["chunking"]
        )

        self.langchain_chunker = LangChainChunker(
            CONFIG["chunking"]
        )

        # ------------------------------------------------------------------
        # Custom Processing Pipeline
        # ------------------------------------------------------------------
        self.custom_pipeline_steps = [
            self.page_renderer.render,
            self.layout_detector.process,
            self.text_extractor.process,
            # self.element_cleaner.process,
            # self.figure_extractor.process,
            # self.table_extractor.process,
            # self.formula_extractor.process,
            # self.document_cleaner.process,
            # self.section_builder.process,
            # self.chunk_builder.process,
        ]


    def invoke(self, input, config=None, **kwargs):
        """
        Load a document and process it using the appropriate pipeline.

        Parameters
        ----------
        input : str | Path
            Path to the input document.

        Returns
        -------
        list[Document]
            LangChain Documents ready for retrieval.
        """

        path = self._validate(BASE_DIR / input)

        return self._dispatch(path)


    def _validate(self, input) -> Path:
        """
        Validate the supplied input document.
        """

        if not isinstance(input, (str, Path)):
            raise TypeError(
                "Input must be a file path of type str or pathlib.Path."
            )

        path = Path(input)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Expected a file but received: {path}"
            )

        if not path.suffix:
            raise ValueError(
                f"File has no extension: {path}"
            )

        return path


    def _dispatch(self, path):
        """
        Load the document using the appropriate loader and dispatch
        it to the corresponding processing pipeline.
        """

        extension = path.suffix.lower()

        if extension in CONFIG["document_types"]["pdf"]:
            document = self.pdf_loader.load(path)

        elif extension in CONFIG["document_types"]["office"]:
            path = self.pdf_loader.convert_to_pdf(path)
            document = self.pdf_loader.load(path, converted_file=True)

        elif extension in CONFIG["document_types"]["images"]:
            document = self.image_loader.load(path)

        elif extension in CONFIG["document_types"]["structured"]:
            document = self.structured_loader.load(path)

        elif extension in CONFIG["document_types"]["text"]:
            document = self.text_loader.load(path)

        elif extension in CONFIG["document_types"]["archives"]:
            document = self.archive_loader.load(path)

        else:
            raise ValueError(
                f"Unsupported file format: {extension}"
            )

        if extension in CONFIG["document_types"]["custom"]:
            return self.custom_pipeline(document)

        return self.langchain_pipeline(document)


    def custom_pipeline(self, document):
        """
        Execute the custom multimodal document understanding pipeline.
        """
        
        for step in self.custom_pipeline_steps:
            document = step(document)
        
        # self.clean_up(document)

        return document


    def langchain_pipeline(self, documents):
        """
        Execute the LangChain processing pipeline.

        Applies recursive text splitting to documents returned by
        LangChain loaders.
        """

        return self.langchain_chunker.process(documents)


    def clean_up(self, chunks):
        try:
            document_id = chunks[0].metadata.get("document_id", None)
        except:
            document_id = None

        if document_id:
            self.workspace.cleanup(document_id)