На этой странице
База данных векторных эмбеддингов с открытым исходным кодом для AI-приложений. Храните эмбеддинги и метаданные, выполняйте векторный и полнотекстовый поиск, фильтруйте по метаданным. Простой API из 4 функций. Масштабируется от ноутбуков до производственных кластеров. Используйте для семантического поиска, RAG-приложений или поиска документов. Лучшее решение для локальной разработки и проектов с открытым исходным кодом.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Опционально — установите с помощью `hermes skills install official/mlops/chroma` |
|Путь| `optional-skills/mlops/chroma` |
|Версия| `1.0.0` |
|Автор| Orchestra Research |
|Лицензия| MIT |
|Зависимости| `chromadb`, `sentence-transformers` |
|Теги| `RAG`, `Chroma`, `Vector Database`, `Embeddings`, `Semantic Search`, `Open Source`, `Self-Hosted`, `Document Retrieval`, `Metadata Filtering` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит в качестве инструкций, когда навык активен.
# Chroma — база данных эмбеддингов с открытым исходным кодом
AI-ориентированная база данных для создания LLM-приложений с памятью.
## Когда использовать Chroma[​](<#when-to-use-chroma> "Прямая ссылка на Когда использовать Chroma")
**Используйте Chroma когда:**
  * Создаёте RAG-приложения (retrieval-augmented generation)
  * Нужна локальная/самостоятельно размещённая векторная база данных
  * Хотите решение с открытым исходным кодом (Apache 2.0)
  * Прототипируете в ноутбуках
  * Нужен семантический поиск по документам
  * Храните эмбеддинги с метаданными

**Метрики:**
  * **24 300+ звёзд на GitHub**
  * **1 900+ форков**
  * **v1.3.3** (стабильная, еженедельные релизы)
  * **Лицензия Apache 2.0**

**Вместо этого используйте альтернативы:**
  * **Pinecone**: Управляемое облачное решение, авто-масштабирование
  * **FAISS**: Чистый поиск по сходству, без метаданных
  * **Weaviate**: Продуктовая ML-ориентированная база данных
  * **Qdrant**: Высокая производительность, на Rust

## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
### Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    # Python  
    pip install chromadb  
      
    # JavaScript/TypeScript  
    npm install chromadb @chroma-core/default-embed  
    
[/code]
### Базовое использование (Python)[​](<#basic-usage-python> "Прямая ссылка на Базовое использование \\(Python\\)")
[code] 
    import chromadb  
      
    # Создание клиента  
    client = chromadb.Client()  
      
    # Создание коллекции  
    collection = client.create_collection(name="my_collection")  
      
    # Добавление документов  
    collection.add(  
        documents=["Это документ 1", "Это документ 2"],  
        metadatas=[{"source": "doc1"}, {"source": "doc2"}],  
        ids=["id1", "id2"]  
    )  
      
    # Запрос  
    results = collection.query(  
        query_texts=["документ по теме"],  
        n_results=2  
    )  
      
    print(results)  
    
[/code]
## Основные операции[​](<#core-operations> "Прямая ссылка на Основные операции")
### 1\\. Создание коллекции[​](<#1-create-collection> "Прямая ссылка на 1. Создание коллекции")
[code] 
    # Простая коллекция  
    collection = client.create_collection("my_docs")  
      
    # С пользовательской функцией эмбеддинга  
    from chromadb.utils import embedding_functions  
      
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(  
        api_key="your-key",  
        model_name="text-embedding-3-small"  
    )  
      
    collection = client.create_collection(  
        name="my_docs",  
        embedding_function=openai_ef  
    )  
      
    # Получение существующей коллекции  
    collection = client.get_collection("my_docs")  
      
    # Удаление коллекции  
    client.delete_collection("my_docs")  
    
[/code]
### 2\\. Добавление документов[​](<#2-add-documents> "Прямая ссылка на 2. Добавление документов")
[code] 
    # Добавление с авто-генерируемыми ID  
    collection.add(  
        documents=["Док 1", "Док 2", "Док 3"],  
        metadatas=[  
            {"source": "web", "category": "tutorial"},  
            {"source": "pdf", "page": 5},  
            {"source": "api", "timestamp": "2025-01-01"}  
        ],  
        ids=["id1", "id2", "id3"]  
    )  
      
    # Добавление с пользовательскими эмбеддингами  
    collection.add(  
        embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],  
        documents=["Док 1", "Док 2"],  
        ids=["id1", "id2"]  
    )  
    
[/code]
### 3\\. Запрос (поиск по сходству)[​](<#3-query-similarity-search> "Прямая ссылка на 3. Запрос \\(поиск по сходству\\)")
[code] 
    # Базовый запрос  
    results = collection.query(  
        query_texts=["обучающий материал по машинному обучению"],  
        n_results=5  
    )  
      
    # Запрос с фильтрами  
    results = collection.query(  
        query_texts=["программирование на Python"],  
        n_results=3,  
        where={"source": "web"}  
    )  
      
    # Запрос с фильтрами по метаданным  
    results = collection.query(  
        query_texts=["продвинутые темы"],  
        where={  
            "$and": [  
                {"category": "tutorial"},  
                {"difficulty": {"$gte": 3}}  
            ]  
        }  
    )  
      
    # Доступ к результатам  
    print(results["documents"])      # Список совпадающих документов  
    print(results["metadatas"])      # Метаданные для каждого документа  
    print(results["distances"])      # Оценки сходства  
    print(results["ids"])            # ID документов  
    
[/code]
### 4\\. Получение документов[​](<#4-get-documents> "Прямая ссылка на 4. Получение документов")
[code] 
    # Получение по ID  
    docs = collection.get(  
        ids=["id1", "id2"]  
    )  
      
    # Получение с фильтрами  
    docs = collection.get(  
        where={"category": "tutorial"},  
        limit=10  
    )  
      
    # Получение всех документов  
    docs = collection.get()  
    
[/code]
### 5\\. Обновление документов[​](<#5-update-documents> "Прямая ссылка на 5. Обновление документов")
[code] 
    # Обновление содержимого документа  
    collection.update(  
        ids=["id1"],  
        documents=["Обновлённое содержимое"],  
        metadatas=[{"source": "updated"}]  
    )  
    
[/code]
### 6\\. Удаление документов[​](<#6-delete-documents> "Прямая ссылка на 6. Удаление документов")
[code] 
    # Удаление по ID  
    collection.delete(ids=["id1", "id2"])  
      
    # Удаление с фильтром  
    collection.delete(  
        where={"source": "outdated"}  
    )  
    
[/code]
## Постоянное хранение[​](<#persistent-storage> "Прямая ссылка на Постоянное хранение")
[code] 
    # Сохранение на диск  
    client = chromadb.PersistentClient(path="./chroma_db")  
      
    collection = client.create_collection("my_docs")  
    collection.add(documents=["Док 1"], ids=["id1"])  
      
    # Данные сохраняются автоматически  
    # Перезагрузка с тем же путём  
    client = chromadb.PersistentClient(path="./chroma_db")  
    collection = client.get_collection("my_docs")  
    
[/code]
## Функции эмбеддинга[​](<#embedding-functions> "Прямая ссылка на Функции эмбеддинга")
### По умолчанию (Sentence Transformers)[​](<#default-sentence-transformers> "Прямая ссылка на По умолчанию \\(Sentence Transformers\\)")
[code] 
    # По умолчанию используется sentence-transformers  
    collection = client.create_collection("my_docs")  
    # Модель по умолчанию: all-MiniLM-L6-v2  
    
[/code]
### OpenAI[​](<#openai> "Прямая ссылка на OpenAI")
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
### HuggingFace[​](<#huggingface> "Прямая ссылка на HuggingFace")
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
### Пользовательская функция эмбеддинга[​](<#custom-embedding-function> "Прямая ссылка на Пользовательская функция эмбеддинга")
[code] 
    from chromadb import Documents, EmbeddingFunction, Embeddings  
      
    class MyEmbeddingFunction(EmbeddingFunction):  
        def __call__(self, input: Documents) -> Embeddings:  
            # Ваша логика эмбеддинга  
            return embeddings  
      
    my_ef = MyEmbeddingFunction()  
    collection = client.create_collection(  
        name="custom_docs",  
        embedding_function=my_ef  
    )  
    
[/code]
## Фильтрация по метаданным[​](<#metadata-filtering> "Прямая ссылка на Фильтрация по метаданным")
[code] 
    # Точное совпадение  
    results = collection.query(  
        query_texts=["запрос"],  
        where={"category": "tutorial"}  
    )  
      
    # Операторы сравнения  
    results = collection.query(  
        query_texts=["запрос"],  
        where={"page": {"$gt": 10}}  # $gt, $gte, $lt, $lte, $ne  
    )  
      
    # Логические операторы  
    results = collection.query(  
        query_texts=["запрос"],  
        where={  
            "$and": [  
                {"category": "tutorial"},  
                {"difficulty": {"$lte": 3}}  
            ]  
        }  # Также: $or  
    )  
      
    # Содержит  
    results = collection.query(  
        query_texts=["запрос"],  
        where={"tags": {"$in": ["python", "ml"]}}  
    )  
    
[/code]
## Интеграция с LangChain[​](<#langchain-integration> "Прямая ссылка на Интеграция с LangChain")
[code] 
    from langchain_chroma import Chroma  
    from langchain_openai import OpenAIEmbeddings  
    from langchain.text_splitter import RecursiveCharacterTextSplitter  
      
    # Разделение документов  
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)  
    docs = text_splitter.split_documents(documents)  
      
    # Создание векторного хранилища Chroma  
    vectorstore = Chroma.from_documents(  
        documents=docs,  
        embedding=OpenAIEmbeddings(),  
        persist_directory="./chroma_db"  
    )  
      
    # Запрос  
    results = vectorstore.similarity_search("машинное обучение", k=3)  
      
    # В качестве ретривера  
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  
    
[/code]
## Интеграция с LlamaIndex[​](<#llamaindex-integration> "Прямая ссылка на Интеграция с LlamaIndex")
[code] 
    from llama_index.vector_stores.chroma import ChromaVectorStore  
    from llama_index.core import VectorStoreIndex, StorageContext  
    import chromadb  
      
    # Инициализация Chroma  
    db = chromadb.PersistentClient(path="./chroma_db")  
    collection = db.get_or_create_collection("my_collection")  
      
    # Создание векторного хранилища  
    vector_store = ChromaVectorStore(chroma_collection=collection)  
    storage_context = StorageContext.from_defaults(vector_store=vector_store)  
      
    # Создание индекса  
    index = VectorStoreIndex.from_documents(  
        documents,  
        storage_context=storage_context  
    )  
      
    # Запрос  
    query_engine = index.as_query_engine()  
    response = query_engine.query("Что такое машинное обучение?")  
    
[/code]
## Режим сервера[​](<#server-mode> "Прямая ссылка на Режим сервера")
[code] 
    # Запуск сервера Chroma  
    # Терминал: chroma run --path ./chroma_db --port 8000  
      
    # Подключение к серверу  
    import chromadb  
    from chromadb.config import Settings  
      
    client = chromadb.HttpClient(  
        host="localhost",  
        port=8000,  
        settings=Settings(anonymized_telemetry=False)  
    )  
      
    # Использование как обычно  
    collection = client.get_or_create_collection("my_docs")  
    
[/code]
## Лучшие практики[​](<#best-practices> "Прямая ссылка на Лучшие практики")
  1. **Используйте постоянный клиент** — не теряйте данные при перезапуске
  2. **Добавляйте метаданные** — это обеспечивает фильтрацию и отслеживание
  3. **Пакетные операции** — добавляйте несколько документов за раз
  4. **Выбирайте правильную модель эмбеддинга** — баланс скорости и качества
  5. **Используйте фильтры** — сужайте пространство поиска
  6. **Уникальные ID** — избегайте коллизий
  7. **Регулярные резервные копии** — копируйте директорию chroma_db
  8. **Следите за размером коллекции** — масштабируйте при необходимости
  9. **Тестируйте функции эмбеддинга** — обеспечивайте качество
  10. **Используйте серверный режим для продакшена** — лучше для многопользовательской работы

## Производительность[​](<#performance> "Прямая ссылка на Производительность")
|Операция| Задержка| Примечания |
|---|---|---|
|Добавление 100 документов| ~1–3 с| С эмбеддингом |
|Запрос (топ 10)| ~50–200 мс| Зависит от размера коллекции |
|Фильтрация по метаданным| ~10–50 мс| Быстро при правильной индексации |
## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **GitHub**: <https://github.com/chroma-core/chroma> ⭐ 24 300+
  * **Документация**: <https://docs.trychroma.com>
  * **Discord**: <https://discord.gg/MMeYNTmh3x>
  * **Версия**: 1.3.3+
  * **Лицензия**: Apache 2.0

  * [Метаданные навыка](#skill-metadata)
  * [Справочник: полный SKILL.md](#reference-full-skillmd)
  * [Когда использовать Chroma](#when-to-use-chroma)
  * [Быстрый старт](#quick-start)
    * [Установка](#installation)
    * [Базовое использование (Python)](#basic-usage-python)
  * [Основные операции](#core-operations)
    * [1\\. Создание коллекции](#1-create-collection)
    * [2\\. Добавление документов](#2-add-documents)
    * [3\\. Запрос (поиск по сходству)](#3-query-similarity-search)
    * [4\\. Получение документов](#4-get-documents)
    * [5\\. Обновление документов](#5-update-documents)
    * [6\\. Удаление документов](#6-delete-documents)
  * [Постоянное хранение](#persistent-storage)
  * [Функции эмбеддинга](#embedding-functions)
    * [По умолчанию (Sentence Transformers)](#default-sentence-transformers)
    * [OpenAI](#openai)
    * [HuggingFace](#huggingface)
    * [Пользовательская функция эмбеддинга](#custom-embedding-function)
  * [Фильтрация по метаданным](#metadata-filtering)
  * [Интеграция с LangChain](#langchain-integration)
  * [Интеграция с LlamaIndex](#llamaindex-integration)
  * [Режим сервера](#server-mode)
  * [Лучшие практики](#best-practices)
  * [Производительность](#performance)
  * [Ресурсы](#resources)


<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-chroma -->
