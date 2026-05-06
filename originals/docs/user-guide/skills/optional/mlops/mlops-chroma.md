On this page
Open-source embedding database for AI applications. Store embeddings and metadata, perform vector and full-text search, filter by metadata. Simple 4-function API. Scales from notebooks to production clusters. Use for semantic search, RAG applications, or document retrieval. Best for local development and open-source projects.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/chroma`  
Path| `optional-skills/mlops/chroma`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `chromadb`, `sentence-transformers`  
Tags| `RAG`, `Chroma`, `Vector Database`, `Embeddings`, `Semantic Search`, `Open Source`, `Self-Hosted`, `Document Retrieval`, `Metadata Filtering`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Chroma - Open-Source Embedding Database
The AI-native database for building LLM applications with memory.
## When to use Chroma[​](<#when-to-use-chroma> "Direct link to When to use Chroma")
**Use Chroma when:**
  * Building RAG (retrieval-augmented generation) applications
  * Need local/self-hosted vector database
  * Want open-source solution (Apache 2.0)
  * Prototyping in notebooks
  * Semantic search over documents
  * Storing embeddings with metadata


**Metrics** :
  * **24,300+ GitHub stars**
  * **1,900+ forks**
  * **v1.3.3** (stable, weekly releases)
  * **Apache 2.0 license**


**Use alternatives instead** :
  * **Pinecone** : Managed cloud, auto-scaling
  * **FAISS** : Pure similarity search, no metadata
  * **Weaviate** : Production ML-native database
  * **Qdrant** : High performance, Rust-based


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Python  
    pip install chromadb  
      
    # JavaScript/TypeScript  
    npm install chromadb @chroma-core/default-embed  
    
[/code]
### Basic usage (Python)[​](<#basic-usage-python> "Direct link to Basic usage \(Python\)")
[code] 
    import chromadb  
      
    # Create client  
    client = chromadb.Client()  
      
    # Create collection  
    collection = client.create_collection(name="my_collection")  
      
    # Add documents  
    collection.add(  
        documents=["This is document 1", "This is document 2"],  
        metadatas=[{"source": "doc1"}, {"source": "doc2"}],  
        ids=["id1", "id2"]  
    )  
      
    # Query  
    results = collection.query(  
        query_texts=["document about topic"],  
        n_results=2  
    )  
      
    print(results)  
    
[/code]
## Core operations[​](<#core-operations> "Direct link to Core operations")
### 1\. Create collection[​](<#1-create-collection> "Direct link to 1. Create collection")
[code] 
    # Simple collection  
    collection = client.create_collection("my_docs")  
      
    # With custom embedding function  
    from chromadb.utils import embedding_functions  
      
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(  
        api_key="your-key",  
        model_name="text-embedding-3-small"  
    )  
      
    collection = client.create_collection(  
        name="my_docs",  
        embedding_function=openai_ef  
    )  
      
    # Get existing collection  
    collection = client.get_collection("my_docs")  
      
    # Delete collection  
    client.delete_collection("my_docs")  
    
[/code]
### 2\. Add documents[​](<#2-add-documents> "Direct link to 2. Add documents")
[code] 
    # Add with auto-generated IDs  
    collection.add(  
        documents=["Doc 1", "Doc 2", "Doc 3"],  
        metadatas=[  
            {"source": "web", "category": "tutorial"},  
            {"source": "pdf", "page": 5},  
            {"source": "api", "timestamp": "2025-01-01"}  
        ],  
        ids=["id1", "id2", "id3"]  
    )  
      
    # Add with custom embeddings  
    collection.add(  
        embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],  
        documents=["Doc 1", "Doc 2"],  
        ids=["id1", "id2"]  
    )  
    
[/code]
### 3\. Query (similarity search)[​](<#3-query-similarity-search> "Direct link to 3. Query \(similarity search\)")
[code] 
    # Basic query  
    results = collection.query(  
        query_texts=["machine learning tutorial"],  
        n_results=5  
    )  
      
    # Query with filters  
    results = collection.query(  
        query_texts=["Python programming"],  
        n_results=3,  
        where={"source": "web"}  
    )  
      
    # Query with metadata filters  
    results = collection.query(  
        query_texts=["advanced topics"],  
        where={  
            "$and": [  
                {"category": "tutorial"},  
                {"difficulty": {"$gte": 3}}  
            ]  
        }  
    )  
      
    # Access results  
    print(results["documents"])      # List of matching documents  
    print(results["metadatas"])      # Metadata for each doc  
    print(results["distances"])      # Similarity scores  
    print(results["ids"])            # Document IDs  
    
[/code]
### 4\. Get documents[​](<#4-get-documents> "Direct link to 4. Get documents")
[code] 
    # Get by IDs  
    docs = collection.get(  
        ids=["id1", "id2"]  
    )  
      
    # Get with filters  
    docs = collection.get(  
        where={"category": "tutorial"},  
        limit=10  
    )  
      
    # Get all documents  
    docs = collection.get()  
    
[/code]
### 5\. Update documents[​](<#5-update-documents> "Direct link to 5. Update documents")
[code] 
    # Update document content  
    collection.update(  
        ids=["id1"],  
        documents=["Updated content"],  
        metadatas=[{"source": "updated"}]  
    )  
    
[/code]
### 6\. Delete documents[​](<#6-delete-documents> "Direct link to 6. Delete documents")
[code] 
    # Delete by IDs  
    collection.delete(ids=["id1", "id2"])  
      
    # Delete with filter  
    collection.delete(  
        where={"source": "outdated"}  
    )  
    
[/code]
## Persistent storage[​](<#persistent-storage> "Direct link to Persistent storage")
[code] 
    # Persist to disk  
    client = chromadb.PersistentClient(path="./chroma_db")  
      
    collection = client.create_collection("my_docs")  
    collection.add(documents=["Doc 1"], ids=["id1"])  
      
    # Data persisted automatically  
    # Reload later with same path  
    client = chromadb.PersistentClient(path="./chroma_db")  
    collection = client.get_collection("my_docs")  
    
[/code]
## Embedding functions[​](<#embedding-functions> "Direct link to Embedding functions")
### Default (Sentence Transformers)[​](<#default-sentence-transformers> "Direct link to Default \(Sentence Transformers\)")
[code] 
    # Uses sentence-transformers by default  
    collection = client.create_collection("my_docs")  
    # Default model: all-MiniLM-L6-v2  
    
[/code]
### OpenAI[​](<#openai> "Direct link to OpenAI")
[code] 
    from chromadb.utils import embedding_functions  
      
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(  
        api_key="your-key",  
        model_name="text-embedding-3-small"  
    )  
      
    collection = client.create_collection(  
        name="openai_docs",  
        embedding_function=openai_ef  
    )  
    
[/code]
### HuggingFace[​](<#huggingface> "Direct link to HuggingFace")
[code] 
    huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(  
        api_key="your-key",  
        model_name="sentence-transformers/all-mpnet-base-v2"  
    )  
      
    collection = client.create_collection(  
        name="hf_docs",  
        embedding_function=huggingface_ef  
    )  
    
[/code]
### Custom embedding function[​](<#custom-embedding-function> "Direct link to Custom embedding function")
[code] 
    from chromadb import Documents, EmbeddingFunction, Embeddings  
      
    class MyEmbeddingFunction(EmbeddingFunction):  
        def __call__(self, input: Documents) -> Embeddings:  
            # Your embedding logic  
            return embeddings  
      
    my_ef = MyEmbeddingFunction()  
    collection = client.create_collection(  
        name="custom_docs",  
        embedding_function=my_ef  
    )  
    
[/code]
## Metadata filtering[​](<#metadata-filtering> "Direct link to Metadata filtering")
[code] 
    # Exact match  
    results = collection.query(  
        query_texts=["query"],  
        where={"category": "tutorial"}  
    )  
      
    # Comparison operators  
    results = collection.query(  
        query_texts=["query"],  
        where={"page": {"$gt": 10}}  # $gt, $gte, $lt, $lte, $ne  
    )  
      
    # Logical operators  
    results = collection.query(  
        query_texts=["query"],  
        where={  
            "$and": [  
                {"category": "tutorial"},  
                {"difficulty": {"$lte": 3}}  
            ]  
        }  # Also: $or  
    )  
      
    # Contains  
    results = collection.query(  
        query_texts=["query"],  
        where={"tags": {"$in": ["python", "ml"]}}  
    )  
    
[/code]
## LangChain integration[​](<#langchain-integration> "Direct link to LangChain integration")
[code] 
    from langchain_chroma import Chroma  
    from langchain_openai import OpenAIEmbeddings  
    from langchain.text_splitter import RecursiveCharacterTextSplitter  
      
    # Split documents  
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)  
    docs = text_splitter.split_documents(documents)  
      
    # Create Chroma vector store  
    vectorstore = Chroma.from_documents(  
        documents=docs,  
        embedding=OpenAIEmbeddings(),  
        persist_directory="./chroma_db"  
    )  
      
    # Query  
    results = vectorstore.similarity_search("machine learning", k=3)  
      
    # As retriever  
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  
    
[/code]
## LlamaIndex integration[​](<#llamaindex-integration> "Direct link to LlamaIndex integration")
[code] 
    from llama_index.vector_stores.chroma import ChromaVectorStore  
    from llama_index.core import VectorStoreIndex, StorageContext  
    import chromadb  
      
    # Initialize Chroma  
    db = chromadb.PersistentClient(path="./chroma_db")  
    collection = db.get_or_create_collection("my_collection")  
      
    # Create vector store  
    vector_store = ChromaVectorStore(chroma_collection=collection)  
    storage_context = StorageContext.from_defaults(vector_store=vector_store)  
      
    # Create index  
    index = VectorStoreIndex.from_documents(  
        documents,  
        storage_context=storage_context  
    )  
      
    # Query  
    query_engine = index.as_query_engine()  
    response = query_engine.query("What is machine learning?")  
    
[/code]
## Server mode[​](<#server-mode> "Direct link to Server mode")
[code] 
    # Run Chroma server  
    # Terminal: chroma run --path ./chroma_db --port 8000  
      
    # Connect to server  
    import chromadb  
    from chromadb.config import Settings  
      
    client = chromadb.HttpClient(  
        host="localhost",  
        port=8000,  
        settings=Settings(anonymized_telemetry=False)  
    )  
      
    # Use as normal  
    collection = client.get_or_create_collection("my_docs")  
    
[/code]
## Best practices[​](<#best-practices> "Direct link to Best practices")
  1. **Use persistent client** \- Don't lose data on restart
  2. **Add metadata** \- Enables filtering and tracking
  3. **Batch operations** \- Add multiple docs at once
  4. **Choose right embedding model** \- Balance speed/quality
  5. **Use filters** \- Narrow search space
  6. **Unique IDs** \- Avoid collisions
  7. **Regular backups** \- Copy chroma_db directory
  8. **Monitor collection size** \- Scale up if needed
  9. **Test embedding functions** \- Ensure quality
  10. **Use server mode for production** \- Better for multi-user


## Performance[​](<#performance> "Direct link to Performance")
Operation| Latency| Notes  
---|---|---  
Add 100 docs| ~1-3s| With embedding  
Query (top 10)| ~50-200ms| Depends on collection size  
Metadata filter| ~10-50ms| Fast with proper indexing  
## Resources[​](<#resources> "Direct link to Resources")
  * **GitHub** : <https://github.com/chroma-core/chroma> ⭐ 24,300+
  * **Docs** : <https://docs.trychroma.com>
  * **Discord** : <https://discord.gg/MMeYNTmh3x>
  * **Version** : 1.3.3+
  * **License** : Apache 2.0


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use Chroma](<#when-to-use-chroma>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Basic usage (Python)](<#basic-usage-python>)
  * [Core operations](<#core-operations>)
    * [1\. Create collection](<#1-create-collection>)
    * [2\. Add documents](<#2-add-documents>)
    * [3\. Query (similarity search)](<#3-query-similarity-search>)
    * [4\. Get documents](<#4-get-documents>)
    * [5\. Update documents](<#5-update-documents>)
    * [6\. Delete documents](<#6-delete-documents>)
  * [Persistent storage](<#persistent-storage>)
  * [Embedding functions](<#embedding-functions>)
    * [Default (Sentence Transformers)](<#default-sentence-transformers>)
    * [OpenAI](<#openai>)
    * [HuggingFace](<#huggingface>)
    * [Custom embedding function](<#custom-embedding-function>)
  * [Metadata filtering](<#metadata-filtering>)
  * [LangChain integration](<#langchain-integration>)
  * [LlamaIndex integration](<#llamaindex-integration>)
  * [Server mode](<#server-mode>)
  * [Best practices](<#best-practices>)
  * [Performance](<#performance>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-chroma -->
