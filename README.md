# RAG-Agnostic-Guide

A comprehensive guide to building Retrieval-Augmented Generation (RAG) systems using various open-source tools.

## Popular Open-Source Tools for RAG Systems

### Local LLM Tools
1. **Ollama**
   - Run large language models locally
   - Easy model management and deployment
   - Support for popular models (Llama 2, CodeLlama, Mistral)
   - Custom model creation and fine-tuning
   - REST API for integration
   - GPU acceleration support

2. **LocalAI**
   - Local OpenAI-compatible API
   - Multiple model formats support
   - CPU and GPU inference
   - Drop-in replacement for OpenAI endpoints

3. **LMStudio**
   - Desktop application for running LLMs
   - User-friendly interface
   - OpenAI-compatible API
   - Model download and management
   - Quantization options

4. **vLLM**
   - High-throughput LLM inference
   - PagedAttention for efficient memory usage
   - OpenAI-compatible API
   - Supports multiple model architectures
   - Continuous batching

5. **OpenLit**
   - Fast inference engine for LLMs
   - Built on top of PyTorch with CUDA optimization
   - Support for quantized models (4-bit, 8-bit)
   - Efficient memory management
   - Streaming support
   - Easy model conversion and deployment
   - Optimized for consumer GPUs
   - Compatible with Hugging Face models

### RAG Orchestration & Workflows
1. **RAGFlow**
   - End-to-end RAG pipeline orchestration
   - Modular components
   - Easy integration with various vector stores

2. **LlamaHub**
   - Collection of data loaders
   - Pre-built RAG templates
   - Community-driven integrations
   - Easy to extend

### Vector Databases
1. **Milvus**
   - Distributed vector database
   - Highly scalable
   - Supports complex vector search algorithms
   - Good for large-scale production deployments

2. **Weaviate**
   - Vector search engine
   - GraphQL API
   - Multi-modal data support
   - Built-in vectorization modules

3. **FAISS (Facebook AI Similarity Search)**
   - Efficient similarity search library
   - Optimized for speed and memory usage
   - Supports GPU acceleration
   - Great for large-scale vector search

### Text Processing & Embedding Generation
1. **LangChain**
   - Framework for developing LLM applications
   - Comprehensive RAG pipelines
   - Multiple integration options
   - Active community

2. **Llama Index (GPT Index)**
   - Data framework for LLM applications
   - Built-in RAG capabilities
   - Various data connectors
   - Structured data handling

### Document Processing
1. **PyPDF2**
   - PDF processing
   - Text extraction
   - Document manipulation
   - Lightweight and easy to use

### RAG Evaluation & Testing
1. **RAGAS**
   - Comprehensive RAG evaluation framework
   - Multiple evaluation metrics
   - Context relevancy scoring
   - Answer faithfulness testing

2. **DeepEval**
   - LLM evaluation toolkit
   - RAG-specific metrics
   - Automated testing
   - Custom evaluation pipelines
   - [Documentation](https://docs.confident-ai.com/)

## Example Projects

### [Resume Screener](./resume_screener)
A practical implementation of RAG using LlamaIndex and OpenAI to create an AI-powered resume screening application. This project demonstrates how to:
- Process PDF documents
- Use embeddings for document analysis
- Create an interactive web interface with Streamlit
- Implement practical RAG workflows

## Contributing
We welcome contributions! Please feel free to submit a Pull Request.