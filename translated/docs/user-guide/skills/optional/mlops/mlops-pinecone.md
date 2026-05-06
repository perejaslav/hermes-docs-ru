On this page
Управляемая векторная база данных для производственных AI-приложений. Полностью управляемая, с авто-масштабированием, гибридным поиском (плотные + разреженные векторы), фильтрацией по метаданным и пространствами имён. Низкая задержка (<100ms p95). Используйте для продакшен RAG, рекомендательных систем или семантического поиска в масштабе. Лучший выбор для бессерверной, управляемой инфраструктуры.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на Skill metadata")

|---|---  
Source| Опциональный — установка: `hermes skills install official/mlops/pinecone`  
Path| `optional-skills/mlops/pinecone`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `pinecone-client`  
Tags| `RAG`, `Pinecone`, `Vector Database`, `Managed Service`, `Serverless`, `Hybrid Search`, `Production`, `Auto-Scaling`, `Low Latency`, `Recommendations`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Именно эти инструкции видит агент, когда навык активен.
# Pinecone — управляемая векторная база данных
Векторная база данных для производственных AI-приложений.
## Когда использовать Pinecone[​](<#when-to-use-pinecone> "Прямая ссылка на Когда использовать Pinecone")
**Используйте когда:**
  * Нужна управляемая бессерверная векторная база данных
  * Продакшен RAG-приложения
  * Требуется авто-масштабирование
  * Критична низкая задержка (<100ms)
  * Нет желания управлять инфраструктурой
  * Нужен гибридный поиск (плотные + разреженные векторы)


**Метрики** :
  * Полностью управляемый SaaS
  * Авто-масштабирование до миллиардов векторов
  * **p95 задержка <100ms**
  * 99.9% SLA доступности


**Вместо этого используйте альтернативы** :
  * **Chroma** : Самостоятельный хостинг, открытый исходный код
  * **FAISS** : Офлайн, чистый поиск по сходству
  * **Weaviate** : Самостоятельный хостинг с расширенными возможностями


## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
### Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    pip install pinecone-client  
    
[/code]
### Базовое использование[​](<#basic-usage> "Прямая ссылка на Базовое использование")
[code] 
    from pinecone import Pinecone, ServerlessSpec  
      
    # Инициализация  
    pc = Pinecone(api_key="your-api-key")  
      
    # Создание индекса  
    pc.create_index(  
        name="my-index",  
        dimension=1536,  # Должно совпадать с размерностью эмбеддингов  
        metric="cosine",  # или "euclidean", "dotproduct"  
        spec=ServerlessSpec(cloud="aws", region="us-east-1")  
    )  
      
    # Подключение к индексу  
    index = pc.Index("my-index")  
      
    # Загрузка векторов  
    index.upsert(vectors=[  
        {"id": "vec1", "values": [0.1, 0.2, ...], "metadata": {"category": "A"}},  
        {"id": "vec2", "values": [0.3, 0.4, ...], "metadata": {"category": "B"}}  
    ])  
      
    # Запрос  
    results = index.query(  
        vector=[0.1, 0.2, ...],  
        top_k=5,  
        include_metadata=True  
    )  
      
    print(results["matches"])  
    
[/code]
## Основные операции[​](<#core-operations> "Прямая ссылка на Основные операции")
### Создание индекса[​](<#create-index> "Прямая ссылка на Создание индекса")
[code] 
    # Serverless (рекомендуется)  
    pc.create_index(  
        name="my-index",  
        dimension=1536,  
        metric="cosine",  
        spec=ServerlessSpec(  
            cloud="aws",         # или "gcp", "azure"  
            region="us-east-1"  
        )  
    )  
      
    # Pod-based (для стабильной производительности)  
    from pinecone import PodSpec  
      
    pc.create_index(  
        name="my-index",  
        dimension=1536,  
        metric="cosine",  
        spec=PodSpec(  
            environment="us-east1-gcp",  
            pod_type="p1.x1"  
        )  
    )  
    
[/code]
### Загрузка векторов (Upsert)[​](<#upsert-vectors> "Прямая ссылка на Загрузка векторов")
[code] 
    # Одиночная загрузка  
    index.upsert(vectors=[  
        {  
            "id": "doc1",  
            "values": [0.1, 0.2, ...],  # 1536 измерений  
            "metadata": {  
                "text": "Содержимое документа",  
                "category": "tutorial",  
                "timestamp": "2025-01-01"  
            }  
        }  
    ])  
      
    # Пакетная загрузка (рекомендуется)  
    vectors = [  
        {"id": f"vec{i}", "values": embedding, "metadata": metadata}  
        for i, (embedding, metadata) in enumerate(zip(embeddings, metadatas))  
    ]  
      
    index.upsert(vectors=vectors, batch_size=100)  
    
[/code]
### Запрос векторов[​](<#query-vectors> "Прямая ссылка на Запрос векторов")
[code] 
    # Базовый запрос  
    results = index.query(  
        vector=[0.1, 0.2, ...],  
        top_k=10,  
        include_metadata=True,  
        include_values=False  
    )  
      
    # С фильтрацией по метаданным  
    results = index.query(  
        vector=[0.1, 0.2, ...],  
        top_k=5,  
        filter={"category": {"$eq": "tutorial"}}  
    )  
      
    # Запрос в пространстве имён  
    results = index.query(  
        vector=[0.1, 0.2, ...],  
        top_k=5,  
        namespace="production"  
    )  
      
    # Доступ к результатам  
    for match in results["matches"]:  
        print(f"ID: {match['id']}")  
        print(f"Score: {match['score']}")  
        print(f"Metadata: {match['metadata']}")  
    
[/code]
### Фильтрация по метаданным[​](<#metadata-filtering> "Прямая ссылка на Фильтрация по метаданным")
[code] 
    # Точное совпадение  
    filter = {"category": "tutorial"}  
      
    # Сравнение  
    filter = {"price": {"$gte": 100}}  # $gt, $gte, $lt, $lte, $ne  
      
    # Логические операторы  
    filter = {  
        "$and": [  
            {"category": "tutorial"},  
            {"difficulty": {"$lte": 3}}  
        ]  
    }  # Также: $or  
      
    # Оператор in  
    filter = {"tags": {"$in": ["python", "ml"]}}  
    
[/code]
## Пространства имён[​](<#namespaces> "Прямая ссылка на Пространства имён")
[code] 
    # Разделение данных по пространствам имён  
    index.upsert(  
        vectors=[{"id": "vec1", "values": [...]}],  
        namespace="user-123"  
    )  
      
    # Запрос в конкретном пространстве имён  
    results = index.query(  
        vector=[...],  
        namespace="user-123",  
        top_k=5  
    )  
      
    # Список пространств имён  
    stats = index.describe_index_stats()  
    print(stats['namespaces'])  
    
[/code]
## Гибридный поиск (плотные + разреженные векторы)[​](<#hybrid-search-dense--sparse> "Прямая ссылка на Гибридный поиск (плотные + разреженные векторы)")
[code] 
    # Загрузка с разреженными векторами  
    index.upsert(vectors=[  
        {  
            "id": "doc1",  
            "values": [0.1, 0.2, ...],  # Плотный вектор  
            "sparse_values": {  
                "indices": [10, 45, 123],  # ID токенов  
                "values": [0.5, 0.3, 0.8]   # TF-IDF оценки  
            },  
            "metadata": {"text": "..."}  
        }  
    ])  
      
    # Гибридный запрос  
    results = index.query(  
        vector=[0.1, 0.2, ...],  
        sparse_vector={  
            "indices": [10, 45],  
            "values": [0.5, 0.3]  
        },  
        top_k=5,  
        alpha=0.5  # 0=разреженный, 1=плотный, 0.5=гибридный  
    )  
    
[/code]
## Интеграция с LangChain[​](<#langchain-integration> "Прямая ссылка на Интеграция с LangChain")
[code] 
    from langchain_pinecone import PineconeVectorStore  
    from langchain_openai import OpenAIEmbeddings  
      
    # Создание векторного хранилища  
    vectorstore = PineconeVectorStore.from_documents(  
        documents=docs,  
        embedding=OpenAIEmbeddings(),  
        index_name="my-index"  
    )  
      
    # Запрос  
    results = vectorstore.similarity_search("query", k=5)  
      
    # С фильтром по метаданным  
    results = vectorstore.similarity_search(  
        "query",  
        k=5,  
        filter={"category": "tutorial"}  
    )  
      
    # Как ретривер  
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})  
    
[/code]
## Интеграция с LlamaIndex[​](<#llamaindex-integration> "Прямая ссылка на Интеграция с LlamaIndex")
[code] 
    from llama_index.vector_stores.pinecone import PineconeVectorStore  
      
    # Подключение к Pinecone  
    pc = Pinecone(api_key="your-key")  
    pinecone_index = pc.Index("my-index")  
      
    # Создание векторного хранилища  
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)  
      
    # Использование в LlamaIndex  
    from llama_index.core import StorageContext, VectorStoreIndex  
      
    storage_context = StorageContext.from_defaults(vector_store=vector_store)  
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)  
    
[/code]
## Управление индексами[​](<#index-management> "Прямая ссылка на Управление индексами")
[code] 
    # Список индексов  
    indexes = pc.list_indexes()  
      
    # Описание индекса  
    index_info = pc.describe_index("my-index")  
    print(index_info)  
      
    # Статистика индекса  
    stats = index.describe_index_stats()  
    print(f"Всего векторов: {stats['total_vector_count']}")  
    print(f"Пространства имён: {stats['namespaces']}")  
      
    # Удаление индекса  
    pc.delete_index("my-index")  
    
[/code]
## Удаление векторов[​](<#delete-vectors> "Прямая ссылка на Удаление векторов")
[code] 
    # Удаление по ID  
    index.delete(ids=["vec1", "vec2"])  
      
    # Удаление по фильтру  
    index.delete(filter={"category": "old"})  
      
    # Удаление всего в пространстве имён  
    index.delete(delete_all=True, namespace="test")  
      
    # Удаление всего индекса  
    index.delete(delete_all=True)  
    
[/code]
## Лучшие практики[​](<#best-practices> "Прямая ссылка на Лучшие практики")
  1. **Используйте serverless** \\- Авто-масштабирование, экономичность
  2. **Пакетная загрузка** \\- Эффективнее (100-200 за пакет)
  3. **Добавляйте метаданные** \\- Включайте фильтрацию
  4. **Используйте пространства имён** \\- Изолируйте данные по пользователю/арендатору
  5. **Отслеживайте использование** \\- Проверяйте панель управления Pinecone
  6. **Оптимизируйте фильтры** \\- Индексируйте часто фильтруемые поля
  7. **Тестируйте с бесплатным тарифом** \\- 1 индекс, 100K векторов бесплатно
  8. **Используйте гибридный поиск** \\- Лучшее качество
  9. **Устанавливайте корректную размерность** \\- Соответствие модели эмбеддингов
  10. **Регулярное резервное копирование** \\- Экспортируйте важные данные


## Производительность[​](<#performance> "Прямая ссылка на Производительность")
Операция| Задержка| Примечания  
---|---|---  
Upsert| ~50-100ms| На пакет  
Query (p50)| ~50ms| Зависит от размера индекса  
Query (p95)| ~100ms| Целевой SLA  
Фильтр метаданных| ~+10-20ms| Дополнительные накладные расходы  
## Цены (по состоянию на 2025)[​](<#pricing-as-of-2025> "Прямая ссылка на Цены (по состоянию на 2025)")
**Serverless** :
  * $0.096 за миллион единиц чтения
  * $0.06 за миллион единиц записи
  * $0.06 за ГБ хранилища в месяц


**Бесплатный тариф** :
  * 1 serverless индекс
  * 100K векторов (1536 измерений)
  * Отлично для прототипирования


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **Веб-сайт** : <https://www.pinecone.io>
  * **Документация** : <https://docs.pinecone.io>
  * **Консоль** : <https://app.pinecone.io>
  * **Цены** : <https://www.pinecone.io/pricing>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать Pinecone](<#when-to-use-pinecone>)
  * [Быстрый старт](<#quick-start>)
    * [Установка](<#installation>)
    * [Базовое использование](<#basic-usage>)
  * [Основные операции](<#core-operations>)
    * [Создание индекса](<#create-index>)
    * [Загрузка векторов](<#upsert-vectors>)
    * [Запрос векторов](<#query-vectors>)
    * [Фильтрация по метаданным](<#metadata-filtering>)
  * [Пространства имён](<#namespaces>)
  * [Гибридный поиск (плотные + разреженные векторы)](<#hybrid-search-dense--sparse>)
  * [Интеграция с LangChain](<#langchain-integration>)
  * [Интеграция с LlamaIndex](<#llamaindex-integration>)
  * [Управление индексами](<#index-management>)
  * [Удаление векторов](<#delete-vectors>)
  * [Лучшие практики](<#best-practices>)
  * [Производительность](<#performance>)
  * [Цены (по состоянию на 2025)](<#pricing-as-of-2025>)
  * [Ресурсы](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-pinecone -->
