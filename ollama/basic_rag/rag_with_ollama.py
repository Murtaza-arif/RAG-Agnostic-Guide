import os
from typing import List, Dict
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama

class OllamaRAG:
    def __init__(self, model_name: str = "llama3.2", embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG system with Ollama
        Args:
            model_name: Name of the Ollama model to use
            embedding_model: Name of the HuggingFace embedding model
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.llm = Ollama(model=model_name)
        self.vector_store = None
        self.qa_chain = None
        self.chat_history = []

    def load_documents(self, docs_dir: str) -> List[Dict]:
        """
        Load documents from a directory
        Args:
            docs_dir: Path to directory containing documents
        Returns:
            List of processed documents
        """
        # Load documents
        loader = DirectoryLoader(docs_dir, glob="**/*.txt", loader_cls=TextLoader)
        documents = loader.load()

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_documents(documents)
        
        return texts

    def create_vector_store(self, texts: List[Dict], persist_directory: str = "chroma_db"):
        """
        Create and persist vector store
        Args:
            texts: List of processed documents
            persist_directory: Directory to persist vector store
        """
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )
        self.vector_store.persist()

    def load_vector_store(self, persist_directory: str = "chroma_db"):
        """
        Load existing vector store
        Args:
            persist_directory: Directory where vector store is persisted
        """
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

    def setup_qa_chain(self):
        """Setup the QA chain with retrieval"""
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
        )

    def query(self, question: str) -> Dict:
        """
        Query the RAG system
        Args:
            question: Question to ask
        Returns:
            Dictionary containing answer and source documents
        """
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Call setup_qa_chain() first.")
        
        result = self.qa_chain({"question": question, "chat_history": self.chat_history})
        
        # Update chat history
        self.chat_history.append((question, result["answer"]))
        
        return {
            "answer": result["answer"],
            "sources": [doc.page_content for doc in result["source_documents"]]
        }

def main():
    # Initialize RAG system
    rag = OllamaRAG()

    # Example usage
    docs_dir = "documents"
    
    # Check if vector store exists
    if not os.path.exists("chroma_db"):
        # Create documents directory if it doesn't exist
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
            print(f"Created documents directory: {docs_dir}")
            print("Please add your .txt files to this directory and run again.")
            return
            
        # Load and process documents
        texts = rag.load_documents(docs_dir)
        if not texts:
            print(f"No text files found in {docs_dir}. Please add some .txt files and try again.")
            return
            
        # Create vector store
        rag.create_vector_store(texts)
        print("Created new vector store from documents.")
    else:
        # Load existing vector store
        rag.load_vector_store()
        print("Loaded existing vector store.")

    # Setup QA chain
    rag.setup_qa_chain()
    print("RAG system ready for questions!")

    # Interactive question-answering
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        try:
            result = rag.query(question)
            print(f"\nAnswer: {result['answer']}")
            print("\nSources:")
            for i, source in enumerate(result['sources'], 1):
                print(f"\nSource {i}:")
                print(source)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
