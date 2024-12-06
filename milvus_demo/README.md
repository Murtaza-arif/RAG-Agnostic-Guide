# E-commerce Product Search with Milvus

This demo showcases how to implement semantic product search using Milvus, similar to Tokopedia's approach. It demonstrates how to use vector similarity search for better product discovery and ranking.

## Features

- Semantic search using sentence transformers
- Vector similarity search with Milvus (SQLite backend)
- HNSW index for efficient similarity search
- Product ranking based on semantic relevance
- Sample product dataset
- Persistent storage in SQLite database

## Prerequisites

- Python 3.8+
- Conda (recommended) or pip

## Setup

### Using Conda (Recommended)

1. If you're creating a new environment:
```bash
conda env create -f environment.yml
```

   If the environment already exists, you can update it:
```bash
conda env update -f environment.yml --prune
```

2. Activate the environment:
```bash
conda activate milvus-product-search
```

### Using pip

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install the requirements:
```bash
pip install -r requirements.txt
```

## Running the Demo

1. Run the demo:
```bash
python product_search.py
```

The script will:
- Create a `data` directory if it doesn't exist
- Initialize a SQLite database in `data/milvus.db`
- Load the sample products and create embeddings
- Perform example searches

## How It Works

1. **Product Embedding**: The system uses the `sentence-transformers` model to convert product names and descriptions into meaningful vector embeddings.

2. **Vector Storage**: These embeddings are stored in a SQLite database along with product metadata (name, description, price, rating).

3. **HNSW Index**: The system uses Hierarchical Navigable Small World (HNSW) index, which is:
   - Optimized for approximate nearest neighbor search
   - Provides excellent search performance
   - Well-suited for high-dimensional vector data

4. **Semantic Search**: When a user searches:
   - The search query is converted to a vector embedding
   - Milvus finds the most similar product embeddings using cosine similarity
   - Results are ranked by similarity score

5. **Sample Data**: The demo includes a sample dataset of electronic products to demonstrate the search capabilities.

## Example Queries

The demo includes example searches for:
- "wireless audio devices"
- "high quality camera for professional photography"
- "gaming devices with good performance"
- "portable entertainment gadgets"

## Architecture

- **Database**: SQLite-based Milvus storage
- **Sentence Transformers**: Pre-trained model for generating semantic embeddings
- **Vector Dimension**: 384 (using all-MiniLM-L6-v2 model)
- **Index Type**: HNSW (Hierarchical Navigable Small World) with COSINE similarity metric
- **Index Parameters**:
  - M: 16 (number of bi-directional links)
  - efConstruction: 200 (construction-time parameter)
  - ef: 100 (search-time parameter)

## Notes

- The sentence transformer model provides good semantic understanding of product descriptions
- Results include similarity scores to show how well each product matches the search query
- The SQLite database is stored in the `data` directory for persistence
- You can delete the `data` directory to start fresh with a new database
- HNSW index provides a good balance between search accuracy and performance
