Библиотека Facebook для эффективного поиска похожих векторов и их кластеризации. Поддерживает миллиарды векторов, ускорение на GPU и различные типы индексов (Flat, IVF, HNSW). Используется для быстрого k-NN поиска, крупномасштабного векторного поиска или когда требуется чистый поиск по сходству без метаданных. Лучший выбор для высокопроизводительных приложений.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на Skill metadata")
|   
---|---  
Source| Опционально — установка: `hermes skills install official/mlops/faiss`  
Path| `optional-skills/mlops/faiss`  
Версия| `1.0.0`  
Автор| Orchestra Research  
Лицензия| MIT  
Зависимости| `faiss-cpu`, `faiss-gpu`, `numpy`  
Теги| `RAG`, `FAISS`, `Similarity Search`, `Vector Search`, `Facebook AI`, `GPU Acceleration`, `Billion-Scale`, `K-NN`, `HNSW`, `High Performance`, `Large Scale`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкции, когда навык активен.
# FAISS - Efficient Similarity Search
Библиотека Facebook AI для поиска похожих векторов в миллиардных масштабах.
## When to use FAISS[​](<#when-to-use-faiss> "Прямая ссылка на When to use FAISS")
**Используйте FAISS когда:**
  * Требуется быстрый поиск по сходству на больших наборах векторных данных (миллионы/миллиарды)
  * Требуется ускорение на GPU
  * Чистое векторное сходство (без фильтрации по метаданным)
  * Критичны высокая пропускная способность и низкая задержка
  * Пакетная/офлайн обработка эмбеддингов


**Показатели**:
  * **31,700+ звёзд на GitHub**
  * Meta/Facebook AI Research
  * **Работает с миллиардами векторов**
  * **C++** с биндингами для Python


**Альтернативы**:
  * **Chroma/Pinecone**: требуется фильтрация по метаданным
  * **Weaviate**: нужны полноценные возможности базы данных
  * **Annoy**: проще, меньше возможностей


## Quick start[​](<#quick-start> "Прямая ссылка на Quick start")
### Installation[​](<#installation> "Прямая ссылка на Installation")
[code] 
    # Только CPU  
    pip install faiss-cpu  
      
    # Поддержка GPU  
    pip install faiss-gpu  
    
[/code]
### Basic usage[​](<#basic-usage> "Прямая ссылка на Basic usage")
[code] 
    import faiss
    import numpy as np
      
    # Создание примера данных (1000 векторов, 128 измерений)
    d = 128
    nb = 1000
    vectors = np.random.random((nb, d)).astype('float32')
      
    # Создание индекса
    index = faiss.IndexFlatL2(d)  # L2 расстояние
    index.add(vectors)             # Добавление векторов
      
    # Поиск
    k = 5  # Найти 5 ближайших соседей
    query = np.random.random((1, d)).astype('float32')
    distances, indices = index.search(query, k)
      
    print(f"Nearest neighbors: {indices}")
    print(f"Distances: {distances}")
    
[/code]
## Index types[​](<#index-types> "Прямая ссылка на Index types")
### 1\. Flat (exact search)[​](<#1-flat-exact-search> "Прямая ссылка на 1. Flat \(exact search\)")
[code] 
    # L2 (евклидово) расстояние
    index = faiss.IndexFlatL2(d)
      
    # Скалярное произведение (косинусное сходство, если векторы нормализованы)
    index = faiss.IndexFlatIP(d)
      
    # Самый медленный, самый точный
    
[/code]
### 2\. IVF (inverted file) - Fast approximate[​](<#2-ivf-inverted-file---fast-approximate> "Прямая ссылка на 2. IVF \(inverted file\) - Fast approximate")
[code] 
    # Создание квантователя
    quantizer = faiss.IndexFlatL2(d)
      
    # IVF индекс со 100 кластерами
    nlist = 100
    index = faiss.IndexIVFFlat(quantizer, d, nlist)
      
    # Обучение на данных
    index.train(vectors)
      
    # Добавление векторов
    index.add(vectors)
      
    # Поиск (nprobe = количество кластеров для поиска)
    index.nprobe = 10
    distances, indices = index.search(query, k)
    
[/code]
### 3\. HNSW (Hierarchical NSW) - Best quality/speed[​](<#3-hnsw-hierarchical-nsw---best-qualityspeed> "Прямая ссылка на 3. HNSW \(Hierarchical NSW\) - Best quality/speed")
[code] 
    # HNSW индекс
    M = 32  # Количество связей на уровень
    index = faiss.IndexHNSWFlat(d, M)
      
    # Обучение не требуется
    index.add(vectors)
      
    # Поиск
    distances, indices = index.search(query, k)
    
[/code]
### 4\. Product Quantization - Memory efficient[​](<#4-product-quantization---memory-efficient> "Прямая ссылка на 4. Product Quantization - Memory efficient")
[code] 
    # PQ уменьшает использование памяти в 16–32 раза
    m = 8   # Количество субквантователей
    nbits = 8
    index = faiss.IndexPQ(d, m, nbits)
      
    # Обучение и добавление
    index.train(vectors)
    index.add(vectors)
    
[/code]
## Save and load[​](<#save-and-load> "Прямая ссылка на Save and load")
[code] 
    # Сохранение индекса
    faiss.write_index(index, "large.index")
      
    # Загрузка индекса
    index = faiss.read_index("large.index")
      
    # Продолжение использования
    distances, indices = index.search(query, k)
    
[/code]
## GPU acceleration[​](<#gpu-acceleration> "Прямая ссылка на GPU acceleration")
[code] 
    # Один GPU
    res = faiss.StandardGpuResources()
    index_cpu = faiss.IndexFlatL2(d)
    index_gpu = faiss.index_cpu_to_gpu(res, 0, index_cpu)  # GPU 0
      
    # Несколько GPU
    index_gpu = faiss.index_cpu_to_all_gpus(index_cpu)
      
    # В 10–100 раз быстрее CPU
    
[/code]
## LangChain integration[​](<#langchain-integration> "Прямая ссылка на LangChain integration")
[code] 
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
      
    # Создание FAISS векторного хранилища
    vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())
      
    # Сохранение
    vectorstore.save_local("faiss_index")
      
    # Загрузка
    vectorstore = FAISS.load_local(
        "faiss_index",
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True
    )
      
    # Поиск
    results = vectorstore.similarity_search("query", k=5)
    
[/code]
## LlamaIndex integration[​](<#llamaindex-integration> "Прямая ссылка на LlamaIndex integration")
[code] 
    from llama_index.vector_stores.faiss import FaissVectorStore
    import faiss
      
    # Создание FAISS индекса
    d = 1536
    faiss_index = faiss.IndexFlatL2(d)
      
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    
[/code]
## Best practices[​](<#best-practices> "Прямая ссылка на Best practices")
  1. **Выбирайте правильный тип индекса** \- Flat для <10K, IVF для 10K–1M, HNSW для качества
  2. **Нормализуйте для косинусного сходства** \- используйте IndexFlatIP с нормализованными векторами
  3. **Используйте GPU для больших наборов данных** \- в 10–100 раз быстрее
  4. **Сохраняйте обученные индексы** \- обучение требует больших вычислительных ресурсов
  5. **Настраивайте nprobe/ef_search** \- баланс между скоростью и точностью
  6. **Контролируйте память** \- используйте PQ для больших наборов данных
  7. **Пакетные запросы** \- лучшее использование GPU


## Performance[​](<#performance> "Прямая ссылка на Performance")
Index Type| Build Time| Search Time| Memory| Accuracy
---|---|---|---|---
Flat| Быстро| Медленно| Высокая| 100%
IVF| Средне| Быстро| Средняя| 95–99%
HNSW| Медленно| Быстрейший| Высокая| 99%
PQ| Средне| Быстро| Низкая| 90–95%
## Resources[​](<#resources> "Прямая ссылка на Resources")
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
    * [2\. IVF (inverted file) — Fast approximate](<#2-ivf-inverted-file---fast-approximate>)
    * [3\. HNSW (Hierarchical NSW) — Best quality/speed](<#3-hnsw-hierarchical-nsw---best-qualityspeed>)
    * [4\. Product Quantization — Memory efficient](<#4-product-quantization---memory-efficient>)
  * [Save and load](<#save-and-load>)
  * [GPU acceleration](<#gpu-acceleration>)
  * [LangChain integration](<#langchain-integration>)
  * [LlamaIndex integration](<#llamaindex-integration>)
  * [Best practices](<#best-practices>)
  * [Performance](<#performance>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-faiss -->
