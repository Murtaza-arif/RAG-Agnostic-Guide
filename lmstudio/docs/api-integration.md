# API Integration Guide

## Server Setup

### Starting the Server
1. Open LMStudio
2. Navigate to API Server tab
3. Configure server settings:
   - Port number (default: 1234)
   - Host address (default: localhost)
   - Access controls
4. Click "Start Server"

### Server Configuration
```python
# Server defaults
HOST = "localhost"
PORT = 1234
BASE_URL = f"http://{HOST}:{PORT}/v1"
```

## API Endpoints

### Available Endpoints

1. **/chat/completions**
   - ChatGPT-style completions
   - Streaming support
   - System messages
   ```python
   POST /v1/chat/completions
   {
     "model": "any-model-name",
     "messages": [
       {"role": "system", "content": "You are a helpful assistant."},
       {"role": "user", "content": "Hello!"}
     ]
   }
   ```

2. **/completions**
   - Text completions
   - Legacy format
   ```python
   POST /v1/completions
   {
     "model": "any-model-name",
     "prompt": "Complete this sentence: The quick brown fox",
     "max_tokens": 50
   }
   ```

3. **/models**
   - List available models
   - Model information
   ```python
   GET /v1/models
   ```

4. **/embeddings**
   - Generate embeddings
   - Vector representations
   ```python
   POST /v1/embeddings
   {
     "model": "any-model-name",
     "input": "Text to embed"
   }
   ```

## Integration Examples

### Python with OpenAI Library
```python
import openai

# Configure client
openai.api_key = "not-needed"
openai.api_base = "http://localhost:1234/v1"

# Chat completion
def get_chat_response(prompt):
    response = openai.ChatCompletion.create(
        model="any-model-name",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Text completion
def get_completion(prompt):
    response = openai.Completion.create(
        model="any-model-name",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text

# Embeddings
def get_embedding(text):
    response = openai.Embedding.create(
        model="any-model-name",
        input=text
    )
    return response.data[0].embedding
```

### Python with Requests
```python
import requests

BASE_URL = "http://localhost:1234/v1"

def chat_completion(prompt):
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        json={
            "model": "any-model-name",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )
    return response.json()

def get_models():
    response = requests.get(f"{BASE_URL}/models")
    return response.json()
```

### Streaming Responses
```python
import openai

def stream_chat_response(prompt):
    response = openai.ChatCompletion.create(
        model="any-model-name",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in response:
        if chunk and chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

## Integration Patterns

### RAG Implementation
```python
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Configure LangChain
llm = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

embeddings = OpenAIEmbeddings(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

# Create vector store
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
```

### Error Handling
```python
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def robust_chat_completion(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="any-model-name",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except openai.error.APIError as e:
        print(f"API error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
```

## Best Practices

### Performance
1. **Connection Management**
   - Reuse connections
   - Implement timeouts
   - Handle rate limiting

2. **Resource Usage**
   - Monitor memory
   - Track API calls
   - Optimize batch sizes

3. **Error Handling**
   - Implement retries
   - Log errors
   - Graceful degradation

### Security
1. **Network Security**
   - Use HTTPS when exposed
   - Implement authentication
   - Rate limiting

2. **Input Validation**
   - Sanitize inputs
   - Validate parameters
   - Check response integrity

### Monitoring
1. **Performance Metrics**
   - Response times
   - Error rates
   - Resource usage

2. **Logging**
   - Request/response logging
   - Error tracking
   - Usage statistics

## Troubleshooting

### Common Issues
1. **Connection Problems**
   - Check server status
   - Verify endpoint URLs
   - Check network connectivity

2. **Performance Issues**
   - Monitor response times
   - Check resource usage
   - Optimize requests

3. **Error Handling**
   - Implement proper retries
   - Log detailed errors
   - Monitor error patterns

## Next Steps
1. Set up server
2. Test basic endpoints
3. Implement integration
4. Add error handling
5. Monitor performance
