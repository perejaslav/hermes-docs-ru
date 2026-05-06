На этой странице
Высокопроизводительный движок векторного поиска по сходству для RAG и семантического поиска. Используйте при создании production RAG-систем, требующих быстрого поиска ближайших соседей, гибридного поиска с фильтрацией или масштабируемого векторного хранилища с производительностью на Rust.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|---|---  
|Источник| Опционально — установка через `hermes skills install official/mlops/qdrant`  
|Путь| `optional-skills/mlops/qdrant`  
|Версия| `1.0.0`  
|Автор| Orchestra Research  
|Лицензия| MIT  
|Зависимости| `qdrant-client>=1.12.0`  
|Теги| `RAG`, `Vector Search`, `Qdrant`, `Semantic Search`, `Embeddings`, `Similarity Search`, `HNSW`, `Production`, `Distributed`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Qdrant — Движок векторного поиска по сходству
Высокопроизводительная векторная база данных, написанная на Rust, для production RAG и семантического поиска.
## Когда использовать Qdrant[​](<#when-to-use-qdrant> "Прямая ссылка на Когда использовать Qdrant")
**Используйте Qdrant когда:**
  * Строите production RAG-системы, требующие низкой задержки
  * Нужен гибридный поиск (векторы + фильтрация по метаданным)
  * Требуется горизонтальное масштабирование с шардированием/репликацией
  * Нужно on-premise развертывание с полным контролем над данными
  * Требуется хранение нескольких векторов на запись (плотные + разреженные)
  * Строите системы рекомендаций в реальном времени


**Ключевые возможности:**
  * **На Rust** : Безопасная работа с памятью, высокая производительность
  * **Богатая фильтрация** : Фильтрация по любому полю полезной нагрузки во время поиска
  * **Несколько векторов** : Плотные, разреженные, множественные плотные на точку
  * **Квантование** : Скалярное, произведение, бинарное для экономии памяти
  * **Распределённость** : Консенсус Raft, шардирование, репликация
  * **REST + gRPC** : Оба API с полной функциональной эквивалентностью


**Альтернативы:**
  * **Chroma** : Более простая настройка, встраиваемые сценарии
  * **FAISS** : Максимальная сырая скорость, исследования/пакетная обработка
  * **Pinecone** : Полностью управляемый, предпочтителен при нулевом администрировании
  * **Weaviate** : Предпочтение GraphQL, встроенные векторизаторы


## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
### Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    # Python client  
    pip install qdrant-client  
      
    # Docker (рекомендуется для разработки)  
    docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant  
      
    # Docker с постоянным хранилищем  
    docker run -p 6333:6333 -p 6334:6334 \  
        -v $(pwd)/qdrant_storage:/qdrant/storage \  
        qdrant/qdrant  
    
[/code]
### Базовое использование[​](<#basic-usage> "Прямая ссылка на Базовое использование")
[code] 
    from qdrant_client import QdrantClient  
    from qdrant_client.models import Distance, VectorParams, PointStruct  
      
    # Подключение к Qdrant  
    client = QdrantClient(host="localhost", port=6333)  
      
    # Создание коллекции  
    client.create_collection(  
        collection_name="documents",  
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)  
    )  
      
    # Вставка векторов с полезной нагрузкой  
    client.upsert(  
        collection_name="documents",  
        points=[  
            PointStruct(  
                id=1,  
                vector=[0.1, 0.2, ...],  # 384-мерный вектор  
                payload={"title": "Doc 1", "category": "tech"}  
            ),  
            PointStruct(  
                id=2,  
                vector=[0.3, 0.4, ...],  
                payload={"title": "Doc 2", "category": "science"}  
            )  
        ]  
    )  
      
    # Поиск с фильтрацией  
    results = client.search(  
        collection_name="documents",  
        query_vector=[0.15, 0.25, ...],  
        query_filter={  
            "must": [{"key": "category", "match": {"value": "tech"}}]  
        },  
        limit=10  
    )  
      
    for point in results:  
        print(f"ID: {point.id}, Score: {point.score}, Payload: {point.payload}")  
    
[/code]
## Основные концепции[​](<#core-concepts> "Прямая ссылка на Основные концепции")
### Точки — базовая единица данных[​](<#points---basic-data-unit> "Прямая ссылка на Точки — базовая единица данных")
[code] 
    from qdrant_client.models import PointStruct  
      
    # Точка = ID + Вектор(ы) + Полезная нагрузка  
    point = PointStruct(  
        id=123,                              # Целое число или UUID строка  
        vector=[0.1, 0.2, 0.3, ...],        # Плотный вектор  
        payload={                            # Произвольные JSON метаданные  
            "title": "Document title",  
            "category": "tech",  
            "timestamp": 1699900000,  
            "tags": ["python", "ml"]  
        }  
    )  
      
    # Пакетная вставка (рекомендуется)  
    client.upsert(  
        collection_name="documents",  
        points=[point1, point2, point3],  
        wait=True  # Ожидать индексации  
    )  
    
[/code]
### Коллекции — контейнеры векторов[​](<#collections---vector-containers> "Прямая ссылка на Коллекции — контейнеры векторов")
[code] 
    from qdrant_client.models import VectorParams, Distance, HnswConfigDiff  
      
    # Создание с конфигурацией HNSW  
    client.create_collection(  
        collection_name="documents",  
        vectors_config=VectorParams(  
            size=384,                        # Размерность векторов  
            distance=Distance.COSINE         # COSINE, EUCLID, DOT, MANHATTAN  
        ),  
        hnsw_config=HnswConfigDiff(  
            m=16,                            # Связей на узел (по умолчанию 16)  
            ef_construct=100,                # Точность при построении (по умолчанию 100)  
            full_scan_threshold=10000        # Переключение на полный перебор ниже этого  
        ),  
        on_disk_payload=True                 # Хранить полезную нагрузку на диске  
    )  
      
    # Информация о коллекции  
    info = client.get_collection("documents")  
    print(f"Точек: {info.points_count}, Векторов: {info.vectors_count}")  
    
[/code]
### Метрики расстояния[​](<#distance-metrics> "Прямая ссылка на Метрики расстояния")
Метрика| Сценарий использования| Диапазон  
---|---|---  
`COSINE`| Текстовые эмбеддинги, нормализованные векторы| 0 до 2  
`EUCLID`| Пространственные данные, признаки изображений| 0 до ∞  
`DOT`| Рекомендации, ненормализованные| -∞ до ∞  
`MANHATTAN`| Разреженные признаки, дискретные данные| 0 до ∞  
## Операции поиска[​](<#search-operations> "Прямая ссылка на Операции поиска")
### Базовый поиск[​](<#basic-search> "Прямая ссылка на Базовый поиск")
[code] 
    # Простой поиск ближайших соседей  
    results = client.search(  
        collection_name="documents",  
        query_vector=[0.1, 0.2, ...],  
        limit=10,  
        with_payload=True,  
        with_vectors=False  # Не возвращать векторы (быстрее)  
    )  
    
[/code]
### Поиск с фильтрацией[​](<#filtered-search> "Прямая ссылка на Поиск с фильтрацией")
[code] 
    from qdrant_client.models import Filter, FieldCondition, MatchValue, Range  
      
    # Сложная фильтрация  
    results = client.search(  
        collection_name="documents",  
        query_vector=query_embedding,  
        query_filter=Filter(  
            must=[  
                FieldCondition(key="category", match=MatchValue(value="tech")),  
                FieldCondition(key="timestamp", range=Range(gte=1699000000))  
            ],  
            must_not=[  
                FieldCondition(key="status", match=MatchValue(value="archived"))  
            ]  
        ),  
        limit=10  
    )  
      
    # Краткий синтаксис фильтра  
    results = client.search(  
        collection_name="documents",  
        query_vector=query_embedding,  
        query_filter={  
            "must": [  
                {"key": "category", "match": {"value": "tech"}},  
                {"key": "price", "range": {"gte": 10, "lte": 100}}  
            ]  
        },  
        limit=10  
    )  
    
[/code]
### Пакетный поиск[​](<#batch-search> "Прямая ссылка на Пакетный поиск")
[code] 
    from qdrant_client.models import SearchRequest  
      
    # Несколько запросов в одном вызове  
    results = client.search_batch(  
        collection_name="documents",  
        requests=[  
            SearchRequest(vector=[0.1, ...], limit=5),  
            SearchRequest(vector=[0.2, ...], limit=5, filter={"must": [...]}),  
            SearchRequest(vector=[0.3, ...], limit=10)  
        ]  
    )  
    
[/code]
## Интеграция с RAG[​](<#rag-integration> "Прямая ссылка на Интеграция с RAG")
### Со sentence-transformers[​](<#with-sentence-transformers> "Прямая ссылка на Со sentence-transformers")
[code] 
    from sentence_transformers import SentenceTransformer  
    from qdrant_client import QdrantClient  
    from qdrant_client.models import VectorParams, Distance, PointStruct  
      
    # Инициализация  
    encoder = SentenceTransformer("all-MiniLM-L6-v2")  
    client = QdrantClient(host="localhost", port=6333)  
      
    # Создание коллекции  
    client.create_collection(  
        collection_name="knowledge_base",  
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)  
    )  
      
    # Индексация документов  
    documents = [  
        {"id": 1, "text": "Python — это язык программирования", "source": "wiki"},  
        {"id": 2, "text": "Машинное обучение использует алгоритмы", "source": "textbook"},  
    ]  
      
    points = [  
        PointStruct(  
            id=doc["id"],  
            vector=encoder.encode(doc["text"]).tolist(),  
            payload={"text": doc["text"], "source": doc["source"]}  
        )  
        for doc in documents  
    ]  
    client.upsert(collection_name="knowledge_base", points=points)  
      
    # RAG-извлечение  
    def retrieve(query: str, top_k: int = 5) -> list[dict]:  
        query_vector = encoder.encode(query).tolist()  
        results = client.search(  
            collection_name="knowledge_base",  
            query_vector=query_vector,  
            limit=top_k  
        )  
        return [{"text": r.payload["text"], "score": r.score} for r in results]  
      
    # Использование в RAG-пайплайне  
    context = retrieve("Что такое Python?")  
    prompt = f"Контекст: {context}\\n\\nВопрос: Что такое Python?"  
    
[/code]
### С LangChain[​](<#with-langchain> "Прямая ссылка на С LangChain")
[code] 
    from langchain_community.vectorstores import Qdrant  
    from langchain_community.embeddings import HuggingFaceEmbeddings  
      
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  
    vectorstore = Qdrant.from_documents(documents, embeddings, url="http://localhost:6333", collection_name="docs")  
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  
    
[/code]
### С LlamaIndex[​](<#with-llamaindex> "Прямая ссылка на С LlamaIndex")
[code] 
    from llama_index.vector_stores.qdrant import QdrantVectorStore  
    from llama_index.core import VectorStoreIndex, StorageContext  
      
    vector_store = QdrantVectorStore(client=client, collection_name="llama_docs")  
    storage_context = StorageContext.from_defaults(vector_store=vector_store)  
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)  
    query_engine = index.as_query_engine()  
    
[/code]
## Поддержка нескольких векторов[​](<#multi-vector-support> "Прямая ссылка на Поддержка нескольких векторов")
### Именованные векторы (разные модели эмбеддингов)[​](<#named-vectors-different-embedding-models> "Прямая ссылка на Именованные векторы \\(разные модели эмбеддингов\\)")
[code] 
    from qdrant_client.models import VectorParams, Distance  
      
    # Коллекция с несколькими типами векторов  
    client.create_collection(  
        collection_name="hybrid_search",  
        vectors_config={  
            "dense": VectorParams(size=384, distance=Distance.COSINE),  
            "sparse": VectorParams(size=30000, distance=Distance.DOT)  
        }  
    )  
      
    # Вставка с именованными векторами  
    client.upsert(  
        collection_name="hybrid_search",  
        points=[  
            PointStruct(  
                id=1,  
                vector={  
                    "dense": dense_embedding,  
                    "sparse": sparse_embedding  
                },  
                payload={"text": "текст документа"}  
            )  
        ]  
    )  
      
    # Поиск по конкретному вектору  
    results = client.search(  
        collection_name="hybrid_search",  
        query_vector=("dense", query_dense),  # Указать, какой вектор  
        limit=10  
    )  
    
[/code]
### Разреженные векторы (BM25, SPLADE)[​](<#sparse-vectors-bm25-splade> "Прямая ссылка на Разреженные векторы \\(BM25, SPLADE\\)")
[code] 
    from qdrant_client.models import SparseVectorParams, SparseIndexParams, SparseVector  
      
    # Коллекция с разреженными векторами  
    client.create_collection(  
        collection_name="sparse_search",  
        vectors_config={},  
        sparse_vectors_config={"text": SparseVectorParams(index=SparseIndexParams(on_disk=False))}  
    )  
      
    # Вставка разреженного вектора  
    client.upsert(  
        collection_name="sparse_search",  
        points=[PointStruct(id=1, vector={"text": SparseVector(indices=[1, 5, 100], values=[0.5, 0.8, 0.2])}, payload={"text": "документ"})]  
    )  
    
[/code]
## Квантование (оптимизация памяти)[​](<#quantization-memory-optimization> "Прямая ссылка на Квантование \\(оптимизация памяти\\)")
[code] 
    from qdrant_client.models import ScalarQuantization, ScalarQuantizationConfig, ScalarType  
      
    # Скалярное квантование (уменьшение памяти в 4 раза)  
    client.create_collection(  
        collection_name="quantized",  
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),  
        quantization_config=ScalarQuantization(  
            scalar=ScalarQuantizationConfig(  
                type=ScalarType.INT8,  
                quantile=0.99,        # Отсечение выбросов  
                always_ram=True      # Держать квантованные данные в RAM  
            )  
        )  
    )  
      
    # Поиск с переоценкой  
    results = client.search(  
        collection_name="quantized",  
        query_vector=query,  
        search_params={"quantization": {"rescore": True}},  # Переоценка топ-результатов  
        limit=10  
    )  
    
[/code]
## Индексация полезной нагрузки[​](<#payload-indexing> "Прямая ссылка на Индексация полезной нагрузки")
[code] 
    from qdrant_client.models import PayloadSchemaType  
      
    # Создание индекса полезной нагрузки для ускорения фильтрации  
    client.create_payload_index(  
        collection_name="documents",  
        field_name="category",  
        field_schema=PayloadSchemaType.KEYWORD  
    )  
      
    client.create_payload_index(  
        collection_name="documents",  
        field_name="timestamp",  
        field_schema=PayloadSchemaType.INTEGER  
    )  
      
    # Типы индексов: KEYWORD, INTEGER, FLOAT, GEO, TEXT (полнотекстовый), BOOL  
    
[/code]
## Production развертывание[​](<#production-deployment> "Прямая ссылка на Production развертывание")
### Qdrant Cloud[​](<#qdrant-cloud> "Прямая ссылка на Qdrant Cloud")
[code] 
    from qdrant_client import QdrantClient  
      
    # Подключение к Qdrant Cloud  
    client = QdrantClient(  
        url="https://your-cluster.cloud.qdrant.io",  
        api_key="your-api-key"  
    )  
    
[/code]
### Настройка производительности[​](<#performance-tuning> "Прямая ссылка на Настройка производительности")
[code] 
    # Оптимизация для скорости поиска (выше точность)  
    client.update_collection(  
        collection_name="documents",  
        hnsw_config=HnswConfigDiff(ef_construct=200, m=32)  
    )  
      
    # Оптимизация для скорости индексации (массовая загрузка)  
    client.update_collection(  
        collection_name="documents",  
        optimizer_config={"indexing_threshold": 20000}  
    )  
    
[/code]
## Лучшие практики[​](<#best-practices> "Прямая ссылка на Лучшие практики")
  1. **Пакетные операции** \- Используйте пакетную вставку/поиск для эффективности
  2. **Индексация полезной нагрузки** \- Индексируйте поля, используемые в фильтрах
  3. **Квантование** \- Включайте для больших коллекций (>1M векторов)
  4. **Шардирование** \- Используйте для коллекций >10M векторов
  5. **Дисковое хранение** \- Включайте `on_disk_payload` для больших полезных нагрузок
  6. **Пул соединений** \- Переиспользуйте экземпляры клиента


## Частые проблемы[​](<#common-issues> "Прямая ссылка на Частые проблемы")
**Медленный поиск с фильтрами:**
[code] 
    # Создайте индекс полезной нагрузки для фильтруемых полей  
    client.create_payload_index(  
        collection_name="docs",  
        field_name="category",  
        field_schema=PayloadSchemaType.KEYWORD  
    )  
    
[/code]
**Нехватка памяти:**
[code] 
    # Включите квантование и дисковое хранение  
    client.create_collection(  
        collection_name="large_collection",  
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),  
        quantization_config=ScalarQuantization(...),  
        on_disk_payload=True  
    )  
    
[/code]
**Проблемы с подключением:**
[code] 
    # Используйте таймаут и повторные попытки  
    client = QdrantClient(  
        host="localhost",  
        port=6333,  
        timeout=30,  
        prefer_grpc=True  # gRPC для лучшей производительности  
    )  
    
[/code]
## Ссылки[​](<#references> "Прямая ссылка на Ссылки")
  * **[Расширенное использование](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/qdrant/references/advanced-usage.md>)** \- Распределённый режим, гибридный поиск, рекомендации
  * **[Устранение неполадок](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/qdrant/references/troubleshooting.md>)** \- Частые проблемы, отладка, настройка производительности


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **GitHub** : <https://github.com/qdrant/qdrant> (22k+ звёзд)
  * **Документация** : <https://qdrant.tech/documentation/>
  * **Python клиент** : <https://github.com/qdrant/qdrant-client>
  * **Cloud** : <https://cloud.qdrant.io>
  * **Версия** : 1.12.0+
  * **Лицензия** : Apache 2.0


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать Qdrant](<#when-to-use-qdrant>)
  * [Быстрый старт](<#quick-start>)
    * [Установка](<#installation>)
    * [Базовое использование](<#basic-usage>)
  * [Основные концепции](<#core-concepts>)
    * [Точки — базовая единица данных](<#points---basic-data-unit>)
    * [Коллекции — контейнеры векторов](<#collections---vector-containers>)
    * [Метрики расстояния](<#distance-metrics>)
  * [Операции поиска](<#search-operations>)
    * [Базовый поиск](<#basic-search>)
    * [Поиск с фильтрацией](<#filtered-search>)
    * [Пакетный поиск](<#batch-search>)
  * [Интеграция с RAG](<#rag-integration>)
    * [Со sentence-transformers](<#with-sentence-transformers>)
    * [С LangChain](<#with-langchain>)
    * [С LlamaIndex](<#with-llamaindex>)
  * [Поддержка нескольких векторов](<#multi-vector-support>)
    * [Именованные векторы (разные модели эмбеддингов)](<#named-vectors-different-embedding-models>)
    * [Разреженные векторы (BM25, SPLADE)](<#sparse-vectors-bm25-splade>)
  * [Квантование (оптимизация памяти)](<#quantization-memory-optimization>)
  * [Индексация полезной нагрузки](<#payload-indexing>)
  * [Production развертывание](<#production-deployment>)
    * [Qdrant Cloud](<#qdrant-cloud>)
    * [Настройка производительности](<#performance-tuning>)
  * [Лучшие практики](<#best-practices>)
  * [Частые проблемы](<#common-issues>)
  * [Ссылки](<#references>)
  * [Ресурсы](<#resources>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-qdrant -->
