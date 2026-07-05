# Smart Document Loader

> **🚧 Project Status:** Under Active Development

Smart Document Loader is a modular, layout-aware document understanding framework built for LangChain applications. It transforms complex documents into high-quality semantic chunks for Retrieval-Augmented Generation (RAG), AI Agents, and enterprise document processing.

Unlike traditional document loaders that primarily extract plain text, Smart Document Loader combines layout detection, OCR, table extraction, figure understanding, semantic section building, and intelligent chunking while preserving the document's structural meaning.

## Features

### Custom Processing Pipeline

- Digital PDF support
- Scanned PDF support
- Image document support
- Microsoft Office document support (DOC, DOCX, PPT, PPTX, ODT, ODP)
- Automatic Office → PDF conversion
- High-resolution page rendering
- Layout detection using DocLayout-YOLO
- OCR-based text extraction
- LLM-powered OCR correction
- Table extraction and reconstruction
- Figure understanding using Vision Language Models
- Formula extraction *(In Progress)*
- Document cleaning and normalization
- Reading order reconstruction
- Section detection
- Semantic chunk generation

### LangChain Integration

Native support for:

- TXT
- Markdown
- HTML
- CSV
- Excel
- JSON / JSONL
- XML

All outputs are returned as standard LangChain `Document` objects.

---

## Processing Pipeline

### Custom Pipeline

```text
Input Document
      │
      ▼
Document Loader
      │
      ▼
Document Conversion (if required)
      │
      ▼
Page Rendering
      │
      ▼
Layout Detection
      │
      ▼
Element Extraction
      │
      ▼
OCR / Native Text Extraction
      │
      ▼
Table & Figure Extraction
      │
      ▼
Document Cleaning
      │
      ▼
Reading Order Reconstruction
      │
      ▼
Section Building
      │
      ▼
Semantic Chunk Generation
      │
      ▼
LangChain Documents
```

### LangChain Pipeline

```text
Input Document
      │
      ▼
LangChain Loader
      │
      ▼
Text Splitter
      │
      ▼
LangChain Documents
```

---

## Project Structure

```text
document_loader/
├── chunking/
├── cleaner/
├── extraction/
├── language_models/
├── langchain_processing/
├── layout/
├── loaders/
├── models/
├── reading_order/
├── rendering/
├── section_building/
├── workspace/
├── config/
├── smart_document_loader.py
└── __init__.py
```

---

## Supported Document Types

### Custom Pipeline

- PDF
- PNG
- JPG
- JPEG
- TIFF
- BMP
- WEBP
- DOC / DOCX
- PPT / PPTX
- ODT / ODP

### LangChain Pipeline

- TXT
- Markdown
- HTML
- CSV
- XLS / XLSX / ODS
- JSON / JSONL
- XML

---

## Roadmap

### ✅ Completed

- Modular Smart Document Loader
- PDF, Image & Office Document Loaders
- Workspace Management
- Page Rendering
- Layout Detection
- OCR Pipeline
- OCR Correction
- Table Extraction
- Figure Extraction
- Document Cleaning
- Reading Order Reconstruction
- Section Builder
- Semantic Chunk Builder
- LangChain Integration

### 🚧 In Progress

- Formula Extraction
- Bounding Box Preservation
- Improved Table Reconstruction
- Performance Optimization

### 📌 Planned

- Visual Source Citation
- Batch & Async Processing
- Streaming Document Processing
- Hybrid Retrieval Support
- LangGraph Integration
- Evaluation Framework

---

## Tech Stack

- Python
- LangChain
- PyMuPDF
- EasyOCR / PaddleOCR
- DocLayout-YOLO
- Hugging Face Transformers
- Vision Language Models
- Groq API

---

## Goal

The goal of Smart Document Loader is to provide a reusable, production-ready document understanding framework capable of handling complex documents while seamlessly integrating with LangChain, vector databases, and modern LLM-powered applications.
