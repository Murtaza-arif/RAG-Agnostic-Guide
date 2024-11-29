# Basic RAG with Ollama

A simple implementation of a RAG (Retrieval Augmented Generation) system using Ollama as the LLM backend.

## Prerequisites

1. Install Ollama following instructions at [Ollama.ai](https://ollama.ai)
2. Pull the Llama2 model:
```bash
ollama pull llama2
```

## Setup

### Option 1: Using Conda (Recommended)
1. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate ollama-rag
```

### Option 2: Using venv
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Common Setup Steps
1. Create a documents directory and add your text files:
```bash
mkdir documents
# Add your .txt files to the documents directory
```

## Usage

1. Run the example:
```bash
python rag_with_ollama.py
```

The script will:
- Load documents from the `documents` directory
- Create embeddings using Sentence Transformers
- Store vectors in ChromaDB
- Set up a QA chain using Ollama
- Answer questions based on your documents

## Features

- Uses Ollama for local LLM inference
- Sentence Transformers for embeddings
- ChromaDB for vector storage
- LangChain for orchestration
- Automatic document chunking and processing
- Persistent vector store
- Source document retrieval

## Customization

You can customize the following in `rag_with_ollama.py`:
- Ollama model (default: llama2)
- Embedding model (default: all-MiniLM-L6-v2)
- Chunk size and overlap
- Number of retrieved documents (k)

## Environment Management

### Update Conda Environment
```bash
conda env update -f environment.yml --prune
```

### Export Environment
```bash
# Export conda environment
conda env export > environment.yml

# Export pip requirements
pip freeze > requirements.txt
```

## Example Documents

Add your `.txt` files to the `documents` directory. The system will process all text files recursively.

## Next Steps

Consider:
1. Adding streaming responses
2. Implementing multi-modal support
3. Creating a web interface
4. Adding document preprocessing for different file types
