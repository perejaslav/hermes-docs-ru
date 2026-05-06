On this page
Facebook's library for efficient similarity search and clustering of dense vectors. Supports billions of vectors, GPU acceleration, and various index types (Flat, IVF, HNSW). Use for fast k-NN search, large-scale vector retrieval, or when you need pure similarity search without metadata. Best for high-performance applications.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/faiss`  
Path| `optional-skills/mlops/faiss`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `faiss-cpu`, `faiss-gpu`, `numpy`  
Tags| `RAG`, `FAISS`, `Similarity Search`, `Vector Search`, `Facebook AI`, `GPU Acceleration`, `Billion-Scale`, `K-NN`, `HNSW`, `High Performance`, `Large Scale`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# FAISS - Efficient Similarity Search
Facebook AI's library for billion-scale vector similarity search.
## When to use FAISS[​](<#when-to-use-faiss> "Direct link to When to use FAISS")
**Use FAISS when:**
  * Need fast similarity search on large vector datasets (millions/billions)
  * GPU acceleration required
  * Pure vector similarity (no metadata filtering needed)
  * High throughput, low latency critical
  * Offline/batch processing of embeddings


**Metrics** :
  * **31,700+ GitHub stars**
  * Meta/Facebook AI Research
  * **Handles billions of vectors**
  * **C++** with Python bindings


**Use alternatives instead** :
  * **Chroma/Pinecone** : Need metadata filtering
  * **Weaviate** : Need full database features
  * **Annoy** : Simpler, fewer features


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    # CPU only  
    pip install faiss-cpu  
      
    # GPU support  
    pip install faiss-gpu  
    
[/code]
### Basic usage[​](<#basic-usage> "Direct link to Basic usage")
[code] 
    import faiss  
    import numpy as np  
      
    # Create sample data (1000 vectors, 128 dimensions)  
    d = 128  
    nb = 1000  
    vectors = np.random.random((nb, d)).astype('float32')  
      
    # Create index  
    index = faiss.IndexFlatL2(d)  # L2 distance  
    index.add(vectors)             # Add vectors  
      
    # Search  
    k = 5  # Find 5 nearest neighbors  
    query = np.random.random((1, d)).astype('float32')  
    distances, indices = index.search(query, k)  
      
    print(f"Nearest neighbors: {indices}")  
    print(f"Distances: {distances}")  
    
[/code]
## Index types[​](<#index-types> "Direct link to Index types")
### 1\. Flat (exact search)[​](<#1-flat-exact-search> "Direct link to 1. Flat \(exact search\)")
[code] 
    # L2 (Euclidean) distance  
    index = faiss.IndexFlatL2(d)  
      
    # Inner product (cosine similarity if normalized)  
    index = faiss.IndexFlatIP(d)  
      
    # Slowest, most accurate  
    
[/code]
### 2\. IVF (inverted file) - Fast approximate[​](<#2-ivf-inverted-file---fast-approximate> "Direct link to 2. IVF \(inverted file\) - Fast approximate")
[code] 
    # Create quantizer  
    quantizer = faiss.IndexFlatL2(d)  
      
    # IVF index with 100 clusters  
    nlist = 100  
    index = faiss.IndexIVFFlat(quantizer, d, nlist)  
      
    # Train on data  
    index.train(vectors)  
      
    # Add vectors  
    index.add(vectors)  
      
    # Search (nprobe = clusters to search)  
    index.nprobe = 10  
    distances, indices = index.search(query, k)  
    
[/code]
### 3\. HNSW (Hierarchical NSW) - Best quality/speed[​](<#3-hnsw-hierarchical-nsw---best-qualityspeed> "Direct link to 3. HNSW \(Hierarchical NSW\) - Best quality/speed")
[code] 
    # HNSW index  
    M = 32  # Number of connections per layer  
    index = faiss.IndexHNSWFlat(d, M)  
      
    # No training needed  
    index.add(vectors)  
      
    # Search  
    distances, indices = index.search(query, k)  
    
[/code]
### 4\. Product Quantization - Memory efficient[​](<#4-product-quantization---memory-efficient> "Direct link to 4. Product Quantization - Memory efficient")
[code] 
    # PQ reduces memory by 16-32×  
    m = 8   # Number of subquantizers  
    nbits = 8  
    index = faiss.IndexPQ(d, m, nbits)  
      
    # Train and add  
    index.train(vectors)  
    index.add(vectors)  
    
[/code]
## Save and load[​](<#save-and-load> "Direct link to Save and load")
[code] 
    # Save index  
    faiss.write_index(index, "large.index")  
      
    # Load index  
    index = faiss.read_index("large.index")  
      
    # Continue using  
    distances, indices = index.search(query, k)  
    
[/code]
## GPU acceleration[​](<#gpu-acceleration> "Direct link to GPU acceleration")
[code] 
    # Single GPU  
    res = faiss.StandardGpuResources()  
    index_cpu = faiss.IndexFlatL2(d)  
    index_gpu = faiss.index_cpu_to_gpu(res, 0, index_cpu)  # GPU 0  
      
    # Multi-GPU  
    index_gpu = faiss.index_cpu_to_all_gpus(index_cpu)  
      
    # 10-100× faster than CPU  
    
[/code]
## LangChain integration[​](<#langchain-integration> "Direct link to LangChain integration")
[code] 
    from langchain_community.vectorstores import FAISS  
    from langchain_openai import OpenAIEmbeddings  
      
    # Create FAISS vector store  
    vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())  
      
    # Save  
    vectorstore.save_local("faiss_index")  
      
    # Load  
    vectorstore = FAISS.load_local(  
        "faiss_index",  
        OpenAIEmbeddings(),  
        allow_dangerous_deserialization=True  
    )  
      
    # Search  
    results = vectorstore.similarity_search("query", k=5)  
    
[/code]
## LlamaIndex integration[​](<#llamaindex-integration> "Direct link to LlamaIndex integration")
[code] 
    from llama_index.vector_stores.faiss import FaissVectorStore  
    import faiss  
      
    # Create FAISS index  
    d = 1536  
    faiss_index = faiss.IndexFlatL2(d)  
      
    vector_store = FaissVectorStore(faiss_index=faiss_index)  
    
[/code]
## Best practices[​](<#best-practices> "Direct link to Best practices")
  1. **Choose right index type** \- Flat for <10K, IVF for 10K-1M, HNSW for quality
  2. **Normalize for cosine** \- Use IndexFlatIP with normalized vectors
  3. **Use GPU for large datasets** \- 10-100× faster
  4. **Save trained indices** \- Training is expensive
  5. **Tune nprobe/ef_search** \- Balance speed/accuracy
  6. **Monitor memory** \- PQ for large datasets
  7. **Batch queries** \- Better GPU utilization


## Performance[​](<#performance> "Direct link to Performance")
Index Type| Build Time| Search Time| Memory| Accuracy  
---|---|---|---|---  
Flat| Fast| Slow| High| 100%  
IVF| Medium| Fast| Medium| 95-99%  
HNSW| Slow| Fastest| High| 99%  
PQ| Medium| Fast| Low| 90-95%  
## Resources[​](<#resources> "Direct link to Resources")
  * **GitHub** : <https://github.com/facebookresearch/faiss> ⭐ 31,700+
  * **Wiki** : <https://github.com/facebookresearch/faiss/wiki>
  * **License** : MIT


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use FAISS](<#when-to-use-faiss>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Basic usage](<#basic-usage>)
  * [Index types](<#index-types>)
    * [1\. Flat (exact search)](<#1-flat-exact-search>)
    * [2\. IVF (inverted file) - Fast approximate](<#2-ivf-inverted-file---fast-approximate>)
    * [3\. HNSW (Hierarchical NSW) - Best quality/speed](<#3-hnsw-hierarchical-nsw---best-qualityspeed>)
    * [4\. Product Quantization - Memory efficient](<#4-product-quantization---memory-efficient>)
  * [Save and load](<#save-and-load>)
  * [GPU acceleration](<#gpu-acceleration>)
  * [LangChain integration](<#langchain-integration>)
  * [LlamaIndex integration](<#llamaindex-integration>)
  * [Best practices](<#best-practices>)
  * [Performance](<#performance>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-faiss -->
