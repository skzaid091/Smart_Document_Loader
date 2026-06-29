# Smart Document Loader

> **🚧 Project Status:** Under Active Development

A modular multimodal document loading framework built for LangChain applications. The project focuses on extracting structured information from complex documents such as PDFs, scanned documents, images, and Office files while preserving document semantics for Retrieval-Augmented Generation (RAG) and Agentic AI applications.

Unlike traditional document loaders that only extract plain text, this project combines layout detection, OCR, figure understanding, table extraction, and semantic chunking to generate high-quality LangChain Documents.

## Features

### Custom Processing Pipeline

* Digital PDF support
* Scanned PDF support
* Image document support
* Microsoft Office document support (DOC, DOCX, PPT, PPTX, ODT, ODP)
* Automatic Office to PDF conversion
* Page rendering
* Layout detection using DocLayout-YOLO
* OCR-based text extraction
* LLM-powered OCR correction
* Figure understanding using Vision Language Models
* Table extraction and reconstruction
* Document cleaning
* Section detection
* Semantic chunk generation

### LangChain Integration

Native support for:

* TXT
* Markdown
* HTML
* CSV
* Excel
* JSON / JSONL
* XML

using LangChain document loaders and text splitters.

## Processing Pipeline

```text
Input Document
      │
      ▼
Document Loader
      │
      ▼
Custom Pipeline / LangChain Pipeline
      │
      ▼
Semantic Chunks
      │
      ▼
LangChain Documents
```

## Current Project Structure

```text
document_loader/
├── loaders/
├── extraction/
├── layout/
├── cleaner/
├── chunking/
├── section_building/
├── language_models/
├── langchain_processing/
├── models/
├── workspace.py
├── config.py
└── smart_document_loader.py
```

## Supported Document Types

### Custom Pipeline

* PDF
* PNG
* JPG
* JPEG
* TIFF
* DOC / DOCX
* PPT / PPTX
* ODT / ODP

### LangChain Pipeline

* TXT
* Markdown
* HTML
* CSV
* XLS / XLSX / ODS
* JSON / JSONL
* XML

## Roadmap

### ✅ Completed

* Smart Document Loader
* PDF Loader
* Image Loader
* Office Document Support
* Workspace Management
* Page Rendering
* Layout Detection
* OCR Pipeline
* Table Extraction
* Figure Extraction
* Document Cleaning
* Section Builder
* Semantic Chunk Builder
* LangChain Integration

### 🚧 In Progress

* Formula Extraction
* Reading Order Optimization
* Bounding Box Preservation
* Improved Table Reconstruction
* Performance Optimization

### 📌 Planned

* Visual Source Citation
* Hybrid Retrieval Support
* Database Integration
* Batch Processing
* Async Processing
* LangGraph Integration
* Evaluation Framework
* Streaming Document Processing

## Tech Stack

* Python
* LangChain
* PyMuPDF
* EasyOCR / PaddleOCR
* DocLayout-YOLO
* Hugging Face Transformers
* Vision Language Models
* Groq API

## Goal

The goal of this project is to provide a reusable, production-ready document ingestion framework capable of handling complex enterprise documents while seamlessly integrating with LangChain, vector databases, and modern LLM-based applications.
