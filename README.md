# Smart Document Loader

> **Status:** 🚧 Active Development

A production-oriented multimodal document ingestion and understanding pipeline designed for Retrieval-Augmented Generation (RAG), Enterprise Search, Agentic AI, and Document Intelligence applications.

Unlike traditional document loaders that primarily extract plain text, this project aims to understand the complete semantic structure of documents by combining OCR, document layout analysis, table understanding, figure understanding, section reconstruction, and semantic chunking.

The final output is a collection of standard **LangChain Documents**, making the pipeline compatible with LangChain, LangGraph, vector databases, and modern LLM applications.

---

# Motivation

Enterprise documents rarely contain plain text alone.

A single document may contain:

* Titles
* Headings
* Paragraphs
* Tables
* Charts
* Figures
* Mathematical formulas
* Footnotes
* Headers & Footers
* Multi-column layouts
* Scanned pages
* Mixed digital/scanned content

Traditional document loaders lose much of this information during extraction.

The goal of this project is to preserve as much document structure as possible before generating semantic chunks for downstream LLM applications.

---

# Features

## Custom Document Processing

Supports:

* Digital PDF
* Scanned PDF
* Mixed PDF
* Images
* Microsoft Office Documents

  * DOC
  * DOCX
  * PPT
  * PPTX
  * ODT
  * ODP

Office documents are automatically converted into PDF before entering the processing pipeline.

---

## LangChain Integration

Supports native LangChain loading for:

### Text Documents

* TXT
* Markdown
* HTML

### Structured Documents

* CSV
* XLS
* XLSX
* ODS
* JSON
* JSONL
* XML

These documents are processed using LangChain document loaders and Recursive Character Text Splitter.

---

# Custom Processing Pipeline

```
Document
      │
      ▼
Workspace Creation
      │
      ▼
Page Rendering
      │
      ▼
Layout Detection
      │
      ▼
Text Extraction
      │
      ▼
OCR Correction
      │
      ▼
Layout Cleaning
      │
      ▼
Figure Understanding
      │
      ▼
Table Extraction
      │
      ▼
Document Cleaning
      │
      ▼
Section Builder
      │
      ▼
Semantic Chunk Builder
      │
      ▼
LangChain Documents
```

---

# Current Components

## SmartDocumentLoader

Main entry point responsible for:

* Document validation
* Loader selection
* Pipeline routing
* Returning LangChain Documents

---

## Workspace Manager

Temporary workspace for every processed document.

```
temp/

└── document_id/
    ├── document.pdf
    ├── rendered_pages/
    └── element_crops/
```

Temporary resources are automatically managed during processing.

---

## PDF Loader

Extracts:

* Document metadata
* Page information
* Native text layer
* Text blocks
* Page dimensions

---

## Image Loader

Extracts:

* Image metadata
* Dimensions
* Format
* Color mode

Images are represented internally as single-page documents.

---

## Office Loader

Converts Office documents into PDF before entering the custom pipeline.

---

## Page Renderer

Generates high-resolution page images from PDFs.

Updates every page with:

* Rendered image path
* Rendered dimensions

---

## Layout Detector

Uses **DocLayout-YOLO** for detecting document structure.

Supported layout elements include:

* Title
* Plain Text
* Figure
* Figure Caption
* Table
* Table Caption
* Formula
* Formula Caption
* Header
* Footer
* Footnote

---

## Text Extractor

Supports both:

* Native PDF text extraction
* OCR for scanned documents

OCR correction is optionally performed using an LLM.

---

## Figure Extractor

Uses a Vision Language Model to generate:

* Figure description
* Caption
* Summary
* Figure type

---

## Table Extractor

Extracts structured tables including:

* Headers
* Rows
* Individual cells
* Cell text
* Table metadata

---

## Document Cleaner

Responsible for:

* Removing duplicate elements
* Cleaning extracted content
* Preparing elements for section reconstruction

---

## Section Builder

Reconstructs document hierarchy.

Examples:

```
Title

↓

Abstract

↓

Introduction

↓

Methods

↓

Results

↓

Conclusion
```

---

## Chunk Builder

Generates semantic chunks preserving document structure.

Each chunk contains metadata such as:

* Document ID
* Chunk ID
* Chunk Index
* Source Document
* Page Number
* Section Title
* Chunk Type

The output format is compatible with LangChain.

---

# LangChain Pipeline

For text and structured documents:

```
LangChain Loader

↓

Recursive Character Text Splitter

↓

LangChain Documents
```

---

# Supported Document Types

## Custom Pipeline

| Format | Supported |
| ------ | --------- |
| PDF    | ✅         |
| PNG    | ✅         |
| JPG    | ✅         |
| JPEG   | ✅         |
| TIFF   | ✅         |
| DOC    | ✅         |
| DOCX   | ✅         |
| PPT    | ✅         |
| PPTX   | ✅         |
| ODT    | ✅         |
| ODP    | ✅         |

---

## LangChain Pipeline

| Format   | Supported |
| -------- | --------- |
| TXT      | ✅         |
| Markdown | ✅         |
| HTML     | ✅         |
| CSV      | ✅         |
| XLS      | ✅         |
| XLSX     | ✅         |
| ODS      | ✅         |
| JSON     | ✅         |
| JSONL    | ✅         |
| XML      | ✅         |

---

# Current Output

Both processing pipelines return:

```python
list[langchain_core.documents.Document]
```

making the output directly compatible with:

* LangChain
* LangGraph
* Vector Databases
* Hybrid Retrieval
* RAG Pipelines
* Agentic AI Applications

---

# Project Structure

```
document_loader/

├── loaders/
├── layout/
├── extraction/
│   ├── figure/
│   └── table/
├── cleaner/
├── chunking/
├── section_building/
├── language_models/
├── langchain_processing/
├── models/
├── temp/
├── workspace.py
├── config.py
└── smart_document_loader.py
```

---

# Roadmap

## Completed

* Smart Document Loader
* Workspace Manager
* PDF Loader
* Image Loader
* Office Document Support
* Page Rendering
* Layout Detection
* OCR Pipeline
* OCR Correction
* Figure Extraction
* Table Extraction
* Document Cleaning
* Section Builder
* Semantic Chunk Builder
* LangChain Integration

---

## In Progress

* Formula Understanding
* Formula Extraction
* Improved Table Reconstruction
* Reading Order Optimization
* Multi-column Document Handling
* Advanced OCR Correction
* Performance Optimization

---

## Planned

* Visual Source Citation
* Bounding Box Preservation
* PDF Highlighting
* Streaming Document Processing
* Batch Processing
* Async Processing
* Document Database Integration
* Incremental Indexing
* Metadata Store
* Hybrid Retrieval
* Multi-modal Embeddings
* LangGraph Integration
* Evaluation Pipeline
* Benchmarking Suite

---

# Future Vision

The long-term goal is to build a production-ready multimodal document understanding framework capable of serving as the document ingestion layer for:

* Enterprise RAG
* Knowledge Management Systems
* Research Paper Understanding
* Contract Intelligence
* Financial Document Analysis
* Medical Document Understanding
* Agentic AI Systems
* Enterprise Search
* AI Assistants

The framework is being designed with modularity in mind, allowing each component to evolve independently while maintaining compatibility with the broader LangChain ecosystem.

---

# Development Status

🚧 This project is currently under active development.

Core document ingestion and processing components have been implemented, while advanced document understanding capabilities, visual citations, retrieval optimization, and database integration are planned for future releases.
