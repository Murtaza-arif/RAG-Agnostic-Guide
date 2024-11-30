import requests
import json

# Initialize the client with LocalAI endpoint

def test_rerank():
    # Test reranking endpoint
    url = "http://localhost:8080/v1/rerank"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": "cross-encoder",  # Using our configured model name
        "query": "Organic skincare products for sensitive skin",
        "documents": [
            "Eco-friendly kitchenware for modern homes",
            "Biodegradable cleaning supplies for eco-conscious consumers",
            "Organic cotton baby clothes for sensitive skin",
            "Natural organic skincare range for sensitive skin",
            "Tech gadgets for smart homes: 2024 edition",
            "Sustainable gardening tools and compost solutions",
            "Sensitive skin-friendly facial cleansers and toners",
            "Organic food wraps and storage solutions",
            "All-natural pet food for dogs with allergies",
            "Yoga mats made from recycled materials"
        ],
        "top_n": 3
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("\nReranking Results:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # test_completion()
    test_rerank()
