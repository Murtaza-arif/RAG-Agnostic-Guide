from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from sample_products import SAMPLE_PRODUCTS
import random
class ProductSearch:
    def __init__(self):
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Initialize Milvus Lite connection
        self.db_path = os.path.join('data',str(random.randint(10,1000)) + 'milvus.db')
        connections.connect(
            alias="default",
            uri=self.db_path,
            using='milvus_lite',
            local_path=self.db_path
        )
        
        # Initialize the sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Define collection schema
        self.collection_name = "product_search"
        self.dim = 384  # dimension of the sentence-transformer model

        if utility.has_collection(self.collection_name):
            utility.drop_collection(self.collection_name)

        self._create_collection()
        self._create_index()
        self._insert_sample_data()

    def _create_collection(self):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="product_id", dtype=DataType.INT64),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
            FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=200),
            FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=500),
            FieldSchema(name="price", dtype=DataType.DOUBLE),
            FieldSchema(name="rating", dtype=DataType.DOUBLE)
        ]
        schema = CollectionSchema(fields=fields, description="Product search collection")
        self.collection = Collection(name=self.collection_name, schema=schema)

    def _create_index(self):
        index_params = {
            "metric_type": "COSINE",
            "index_type": "HNSW",
            "params": {
                "M": 16,  # Number of bi-directional links created for each new element during construction
                "efConstruction": 200  # Size of the dynamic candidate list for constructing the graph
            }
        }
        self.collection.create_index(field_name="embedding", index_params=index_params)
        self.collection.load()

    def _get_embedding(self, text):
        return self.model.encode(text)

    def _insert_sample_data(self):
        product_ids = []
        embeddings = []
        names = []
        descriptions = []
        prices = []
        ratings = []

        for product in SAMPLE_PRODUCTS:
            # Combine name and description for better semantic understanding
            text_to_embed = f"{product['name']} {product['description']}"
            embedding = self._get_embedding(text_to_embed)
            
            product_ids.append(product['id'])
            embeddings.append(embedding)
            names.append(product['name'])
            descriptions.append(product['description'])
            prices.append(product['price'])
            ratings.append(product['rating'])

        entities = [
            product_ids,  # Also use as primary key
            product_ids,
            embeddings,
            names,
            descriptions,
            prices,
            ratings
        ]
        
        self.collection.insert(entities)

    def search(self, query, top_k=3, threshold=0.5):
        """
        Search for products using semantic similarity
        Args:
            query: Search query
            top_k: Number of results to return
            threshold: Minimum similarity score threshold (0 to 1)
        Returns:
            List of products that meet the threshold criteria
        """
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Search parameters
        search_params = {
            "metric_type": "COSINE",
            "params": {"ef": 32}
        }
        
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["product_id", "name", "description", "price", "rating"]
        )

        filtered_results = []
        for hits in results:
            for hit in hits:
                if hit.score >= threshold:  # Only include results above threshold
                    filtered_results.append({
                        "id": hit.entity.get('product_id'),
                        "name": hit.entity.get('name'),
                        "description": hit.entity.get('description'),
                        "price": hit.entity.get('price'),
                        "rating": hit.entity.get('rating'),
                        "similarity": hit.score
                    })
        
        return filtered_results

    def cleanup(self):
        """
        Clean up Milvus resources
        """
        connections.disconnect(alias="default")

if __name__ == "__main__":
    # Initialize the search engine
    search_engine = ProductSearch()

    # Example searches
    example_queries = [
        "wireless audio devices",
        "high quality camera for professional photography",
        "gaming devices with good performance",
        "portable entertainment gadgets"
    ]

    print("\nProduct Search Demo")
    print("==================")
    
    for query in example_queries:
        print(f"\nSearch Query: '{query}'")
        print("-" * 50)
        
        results = search_engine.search(query, top_k=3, threshold=0.5)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['name']}")
            print(f"   Price: ${result['price']:.2f}")
            print(f"   Rating: {result['rating']}/5.0")
            print(f"   Similarity Score: {result['similarity']:.4f}")
            print(f"   Description: {result['description']}")

    # Cleanup
    search_engine.cleanup()
