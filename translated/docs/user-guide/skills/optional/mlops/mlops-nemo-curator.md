On this page
Курирование данных с ускорением на GPU для обучения LLM. Поддерживает текст, изображения, видео, аудио. Включает нечёткую дедупликацию (в 16× быстрее), фильтрацию качества (30+ эвристик), семантическую дедупликацию, редактирование PII, обнаружение NSFW. Масштабируется на нескольких GPU с помощью RAPIDS. Используется для подготовки высококачественных обучающих датасетов, очистки веб-данных или дедупликации больших корпусов.
## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Источник| Опциональный — установка через `hermes skills install official/mlops/nemo-curator`|
|Путь| `optional-skills/mlops/nemo-curator`|
|Версия| `1.0.0`|
|Автор| Orchestra Research|
|Лицензия| MIT|
|Зависимости| `nemo-curator`, `cudf`, `dask`, `rapids`|
|Теги| `Data Processing`, `NeMo Curator`, `Data Curation`, `GPU Acceleration`, `Deduplication`, `Quality Filtering`, `NVIDIA`, `RAPIDS`, `PII Redaction`, `Multimodal`, `LLM Training Data`|
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# NeMo Curator — Курирование данных с ускорением на GPU
Инструментарий NVIDIA для подготовки высококачественных обучающих данных для LLM.
## Когда использовать NeMo Curator[​](<#when-to-use-nemo-curator> "Direct link to When to use NeMo Curator")
**Используйте NeMo Curator когда:**
  * Нужно подготовить данные для обучения LLM из веб-скрапов (Common Crawl)
  * Требуется быстрая дедупликация (в 16× быстрее, чем на CPU)
  * Вы курируете мультимодальные датасеты (текст, изображения, видео, аудио)
  * Нужно фильтровать низкокачественный или токсичный контент
  * Требуется масштабирование обработки данных на кластере GPU


**Производительность:**
  * **В 16× быстрее** нечёткая дедупликация (8 ТБ RedPajama v2)
  * **На 40% ниже TCO** по сравнению с CPU-альтернативами
  * **Почти линейное масштабирование** на узлах GPU


**Используйте альтернативы когда:**
  * **datatrove**: CPU-ориентированная, открытая обработка данных
  * **dolma**: Инструментарий данных от Allen AI
  * **Ray Data**: Общая обработка ML-данных (без фокуса на курирование)


## Быстрый старт[​](<#quick-start> "Direct link to Quick start")
### Установка[​](<#installation> "Direct link to Installation")
[code] 
    # Текстовая курация (CUDA 12)  
    uv pip install "nemo-curator[text_cuda12]"  
      
    # Все модальности  
    uv pip install "nemo-curator[all_cuda12]"  
      
    # Только CPU (медленнее)  
    uv pip install "nemo-curator[cpu]"  
    
[/code]
### Базовый пайплайн текстовой курации[​](<#basic-text-curation-pipeline> "Direct link to Basic text curation pipeline")
[code] 
    from nemo_curator import ScoreFilter, Modify  
    from nemo_curator.datasets import DocumentDataset  
    import pandas as pd  
      
    # Загрузка данных  
    df = pd.DataFrame({"text": ["Good document", "Bad doc", "Excellent text"]})  
    dataset = DocumentDataset(df)  
      
    # Фильтрация качества  
    def quality_score(doc):  
        return len(doc["text"].split()) > 5  # Фильтр коротких документов  
      
    filtered = ScoreFilter(quality_score)(dataset)  
      
    # Дедупликация  
    from nemo_curator.modules import ExactDuplicates  
    deduped = ExactDuplicates()(filtered)  
      
    # Сохранение  
    deduped.to_parquet("curated_data/")  
    
[/code]
## Пайплайн курации данных[​](<#data-curation-pipeline> "Direct link to Data curation pipeline")
### Этап 1: Фильтрация качества[​](<#stage-1-quality-filtering> "Direct link to Stage 1: Quality filtering")
[code] 
    from nemo_curator.filters import (  
        WordCountFilter,  
        RepeatedLinesFilter,  
        UrlRatioFilter,  
        NonAlphaNumericFilter  
    )  
      
    # Применение 30+ эвристических фильтров  
    from nemo_curator import ScoreFilter  
      
    # Фильтр по количеству слов  
    dataset = dataset.filter(WordCountFilter(min_words=50, max_words=100000))  
      
    # Удаление повторяющегося контента  
    dataset = dataset.filter(RepeatedLinesFilter(max_repeated_line_fraction=0.3))  
      
    # Фильтр по доле URL  
    dataset = dataset.filter(UrlRatioFilter(max_url_ratio=0.2))  
    
[/code]
### Этап 2: Дедупликация[​](<#stage-2-deduplication> "Direct link to Stage 2: Deduplication")
**Точная дедупликация:**
[code] 
    from nemo_curator.modules import ExactDuplicates  
      
    # Удаление точных дубликатов  
    deduped = ExactDuplicates(id_field="id", text_field="text")(dataset)  
    
[/code]
**Нечёткая дедупликация** (в 16× быстрее на GPU):
[code] 
    from nemo_curator.modules import FuzzyDuplicates  
      
    # MinHash + LSH дедупликация  
    fuzzy_dedup = FuzzyDuplicates(  
        id_field="id",  
        text_field="text",  
        num_hashes=260,      # Параметры MinHash  
        num_buckets=20,  
        hash_method="md5"  
    )  
      
    deduped = fuzzy_dedup(dataset)  
    
[/code]
**Семантическая дедупликация:**
[code] 
    from nemo_curator.modules import SemanticDuplicates  
      
    # Дедупликация на основе эмбеддингов  
    semantic_dedup = SemanticDuplicates(  
        id_field="id",  
        text_field="text",  
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",  
        threshold=0.8  # Порог косинусного сходства  
    )  
      
    deduped = semantic_dedup(dataset)  
    
[/code]
### Этап 3: Редактирование PII[​](<#stage-3-pii-redaction> "Direct link to Stage 3: PII redaction")
[code] 
    from nemo_curator.modules import Modify  
    from nemo_curator.modifiers import PIIRedactor  
      
    # Редактирование личной информации  
    pii_redactor = PIIRedactor(  
        supported_entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON", "LOCATION"],  
        anonymize_action="replace"  # или "redact"  
    )  
      
    redacted = Modify(pii_redactor)(dataset)  
    
[/code]
### Этап 4: Фильтрация классификатором[​](<#stage-4-classifier-filtering> "Direct link to Stage 4: Classifier filtering")
[code] 
    from nemo_curator.classifiers import QualityClassifier  
      
    # Классификация качества  
    quality_clf = QualityClassifier(  
        model_path="nvidia/quality-classifier-deberta",  
        batch_size=256,  
        device="cuda"  
    )  
      
    # Фильтрация низкокачественных документов  
    high_quality = dataset.filter(lambda doc: quality_clf(doc["text"]) > 0.5)  
    
[/code]
## Ускорение на GPU[​](<#gpu-acceleration> "Direct link to GPU acceleration")
### Производительность GPU vs CPU[​](<#gpu-vs-cpu-performance> "Direct link to GPU vs CPU performance")
Операция| CPU (16 ядер)| GPU (A100)| Ускорение  
---|---|---|---|---  
Нечёткая дедупл. (8 ТБ)| 120 часов| 7.5 часов| 16×  
Точная дедупл. (1 ТБ)| 8 часов| 0.5 часов| 16×  
Фильтрация качества| 2 часа| 0.2 часа| 10×  
### Масштабирование на нескольких GPU[​](<#multi-gpu-scaling> "Direct link to Multi-GPU scaling")
[code] 
    from nemo_curator import get_client  
    import dask_cuda  
      
    # Инициализация GPU-кластера  
    client = get_client(cluster_type="gpu", n_workers=8)  
      
    # Обработка на 8 GPU  
    deduped = FuzzyDuplicates(...)(dataset)  
    
[/code]
## Мультимодальная курация[​](<#multi-modal-curation> "Direct link to Multi-modal curation")
### Курация изображений[​](<#image-curation> "Direct link to Image curation")
[code] 
    from nemo_curator.image import (  
        AestheticFilter,  
        NSFWFilter,  
        CLIPEmbedder  
    )  
      
    # Оценка эстетики  
    aesthetic_filter = AestheticFilter(threshold=5.0)  
    filtered_images = aesthetic_filter(image_dataset)  
      
    # Обнаружение NSFW  
    nsfw_filter = NSFWFilter(threshold=0.9)  
    safe_images = nsfw_filter(filtered_images)  
      
    # Генерация CLIP-эмбеддингов  
    clip_embedder = CLIPEmbedder(model="openai/clip-vit-base-patch32")  
    image_embeddings = clip_embedder(safe_images)  
    
[/code]
### Курация видео[​](<#video-curation> "Direct link to Video curation")
[code] 
    from nemo_curator.video import (  
        SceneDetector,  
        ClipExtractor,  
        InternVideo2Embedder  
    )  
      
    # Обнаружение сцен  
    scene_detector = SceneDetector(threshold=27.0)  
    scenes = scene_detector(video_dataset)  
      
    # Извлечение клипов  
    clip_extractor = ClipExtractor(min_duration=2.0, max_duration=10.0)  
    clips = clip_extractor(scenes)  
      
    # Генерация эмбеддингов  
    video_embedder = InternVideo2Embedder()  
    video_embeddings = video_embedder(clips)  
    
[/code]
### Курация аудио[​](<#audio-curation> "Direct link to Audio curation")
[code] 
    from nemo_curator.audio import (  
        ASRInference,  
        WERFilter,  
        DurationFilter  
    )  
      
    # ASR транскрипция  
    asr = ASRInference(model="nvidia/stt_en_fastconformer_hybrid_large_pc")  
    transcribed = asr(audio_dataset)  
      
    # Фильтрация по WER (коэффициент ошибок в словах)  
    wer_filter = WERFilter(max_wer=0.3)  
    high_quality_audio = wer_filter(transcribed)  
      
    # Фильтрация по длительности  
    duration_filter = DurationFilter(min_duration=1.0, max_duration=30.0)  
    filtered_audio = duration_filter(high_quality_audio)  
    
[/code]
## Типовые сценарии[​](<#common-patterns> "Direct link to Common patterns")
### Курация веб-скрапов (Common Crawl)[​](<#web-scrape-curation-common-crawl> "Direct link to Web scrape curation \\(Common Crawl\\)")
[code] 
    from nemo_curator import ScoreFilter, Modify  
    from nemo_curator.filters import *  
    from nemo_curator.modules import *  
    from nemo_curator.datasets import DocumentDataset  
      
    # Загрузка данных Common Crawl  
    dataset = DocumentDataset.read_parquet("common_crawl/*.parquet")  
      
    # Пайплайн  
    pipeline = [  
        # 1. Фильтрация качества  
        WordCountFilter(min_words=100, max_words=50000),  
        RepeatedLinesFilter(max_repeated_line_fraction=0.2),  
        SymbolToWordRatioFilter(max_symbol_to_word_ratio=0.3),  
        UrlRatioFilter(max_url_ratio=0.3),  
      
        # 2. Языковая фильтрация  
        LanguageIdentificationFilter(target_languages=["en"]),  
      
        # 3. Дедупликация  
        ExactDuplicates(id_field="id", text_field="text"),  
        FuzzyDuplicates(id_field="id", text_field="text", num_hashes=260),  
      
        # 4. Редактирование PII  
        PIIRedactor(),  
      
        # 5. NSFW фильтрация  
        NSFWClassifier(threshold=0.8)  
    ]  
      
    # Выполнение  
    for stage in pipeline:  
        dataset = stage(dataset)  
      
    # Сохранение  
    dataset.to_parquet("curated_common_crawl/")  
    
[/code]
### Распределённая обработка[​](<#distributed-processing> "Direct link to Distributed processing")
[code] 
    from nemo_curator import get_client  
    from dask_cuda import LocalCUDACluster  
      
    # Много-GPU кластер  
    cluster = LocalCUDACluster(n_workers=8)  
    client = get_client(cluster=cluster)  
      
    # Обработка большого датасета  
    dataset = DocumentDataset.read_parquet("s3://large_dataset/*.parquet")  
    deduped = FuzzyDuplicates(...)(dataset)  
      
    # Очистка  
    client.close()  
    cluster.close()  
    
[/code]
## Бенчмарки производительности[​](<#performance-benchmarks> "Direct link to Performance benchmarks")
### Нечёткая дедупликация (8 ТБ RedPajama v2)[​](<#fuzzy-deduplication-8tb-redpajama-v2> "Direct link to Fuzzy deduplication \\(8TB RedPajama v2\\)")
  * **CPU (256 ядер):** 120 часов
  * **GPU (8× A100):** 7.5 часов
  * **Ускорение:** 16×


### Точная дедупликация (1 ТБ)[​](<#exact-deduplication-1tb> "Direct link to Exact deduplication \\(1TB\\)")
  * **CPU (64 ядра):** 8 часов
  * **GPU (4× A100):** 0.5 часов
  * **Ускорение:** 16×


### Фильтрация качества (100 ГБ)[​](<#quality-filtering-100gb> "Direct link to Quality filtering \\(100GB\\)")
  * **CPU (32 ядра):** 2 часа
  * **GPU (2× A100):** 0.2 часа
  * **Ускорение:** 10×


## Сравнение стоимости[​](<#cost-comparison> "Direct link to Cost comparison")
**Курация на CPU** (AWS c5.18xlarge × 10):
  * Стоимость: $3.60/час × 10 = $36/час
  * Время для 8 ТБ: 120 часов
  * **Итого:** $4,320


**Курация на GPU** (AWS p4d.24xlarge × 2):
  * Стоимость: $32.77/час × 2 = $65.54/час
  * Время для 8 ТБ: 7.5 часов
  * **Итого:** $491.55


**Экономия:** 89% (сэкономлено $3,828)
## Поддерживаемые форматы данных[​](<#supported-data-formats> "Direct link to Supported data formats")
  * **Входные:** Parquet, JSONL, CSV
  * **Выходные:** Parquet (рекомендуется), JSONL
  * **WebDataset:** TAR-архивы для мультимодальных данных


## Варианты использования[​](<#use-cases> "Direct link to Use cases")
**Продуктовые развёртывания:**
  * NVIDIA использовала NeMo Curator для подготовки данных обучения Nemotron-4
  * Курированные датасеты с открытым исходным кодом: RedPajama v2, The Pile


## Ссылки[​](<#references> "Direct link to References")
  * **[Руководство по фильтрации](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/nemo-curator/references/filtering.md>)** \\- 30+ фильтров качества, эвристики
  * **[Руководство по дедупликации](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/nemo-curator/references/deduplication.md>)** \\- Точные, нечёткие и семантические методы


## Ресурсы[​](<#resources> "Direct link to Resources")
  * **GitHub:** <https://github.com/NVIDIA/NeMo-Curator> ⭐ 500+
  * **Документация:** <https://docs.nvidia.com/nemo-framework/user-guide/latest/datacuration/>
  * **Версия:** 0.4.0+
  * **Лицензия:** Apache 2.0


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать NeMo Curator](<#when-to-use-nemo-curator>)
  * [Быстрый старт](<#quick-start>)
    * [Установка](<#installation>)
    * [Базовый пайплайн текстовой курации](<#basic-text-curation-pipeline>)
  * [Пайплайн курации данных](<#data-curation-pipeline>)
    * [Этап 1: Фильтрация качества](<#stage-1-quality-filtering>)
    * [Этап 2: Дедупликация](<#stage-2-deduplication>)
    * [Этап 3: Редактирование PII](<#stage-3-pii-redaction>)
    * [Этап 4: Фильтрация классификатором](<#stage-4-classifier-filtering>)
  * [Ускорение на GPU](<#gpu-acceleration>)
    * [Производительность GPU vs CPU](<#gpu-vs-cpu-performance>)
    * [Масштабирование на нескольких GPU](<#multi-gpu-scaling>)
  * [Мультимодальная курация](<#multi-modal-curation>)
    * [Курация изображений](<#image-curation>)
    * [Курация видео](<#video-curation>)
    * [Курация аудио](<#audio-curation>)
  * [Типовые сценарии](<#common-patterns>)
    * [Курация веб-скрапов (Common Crawl)](<#web-scrape-curation-common-crawl>)
    * [Распределённая обработка](<#distributed-processing>)
  * [Бенчмарки производительности](<#performance-benchmarks>)
    * [Нечёткая дедупликация (8 ТБ RedPajama v2)](<#fuzzy-deduplication-8tb-redpajama-v2>)
    * [Точная дедупликация (1 ТБ)](<#exact-deduplication-1tb>)
    * [Фильтрация качества (100 ГБ)](<#quality-filtering-100gb>)
  * [Сравнение стоимости](<#cost-comparison>)
  * [Поддерживаемые форматы данных](<#supported-data-formats>)
  * [Варианты использования](<#use-cases>)
  * [Ссылки](<#references>)
  * [Ресурсы](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-nemo-curator -->
