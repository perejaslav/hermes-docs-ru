On this page
Быстрые токенизаторы, оптимизированные для исследований и продакшна. Реализация на Rust токенизирует 1 ГБ менее чем за 20 секунд. Поддерживает алгоритмы BPE, WordPiece и Unigram. Обучение собственного словаря, отслеживание выравниваний (alignment), обработка дополнения (padding) и усечения (truncation). Бесшовная интеграция с transformers. Используйте, когда требуется высокопроизводительная токенизация или обучение собственного токенизатора.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на «Метаданные навыка»")
|   |
|---|---|
|Источник| Опционально — установка: `hermes skills install official/mlops/huggingface-tokenizers`|
|Путь| `optional-skills/mlops/huggingface-tokenizers`|
|Версия| `1.0.0`|
|Автор| Orchestra Research|
|Лицензия| MIT|
|Зависимости| `tokenizers`, `transformers`, `datasets`|
|Теги| `Tokenization`, `HuggingFace`, `BPE`, `WordPiece`, `Unigram`, `Fast Tokenization`, `Rust`, `Custom Tokenizer`, `Alignment Tracking`, `Production`|
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на «Справочник: полный SKILL.md»")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# HuggingFace Tokenizers — Быстрая токенизация для NLP
Быстрые, готовые к продакшну токенизаторы с производительностью Rust и удобством Python.
## Когда использовать HuggingFace Tokenizers[​](<#when-to-use-huggingface-tokenizers> "Прямая ссылка на «Когда использовать HuggingFace Tokenizers»")
**Используйте HuggingFace Tokenizers, когда:**
  * требуется чрезвычайно быстрая токенизация (<20 с на 1 ГБ текста)
  * нужно обучить собственный токенизатор с нуля
  * нужно отслеживание выравнивания (token → позиция в исходном тексте)
  * строится продакшн-пайплайн NLP
  * требуется эффективно токенизировать большие корпуса


**Производительность:**
  * **Скорость:** <20 секунд на токенизацию 1 ГБ на CPU
  * **Реализация:** ядро на Rust с обёртками для Python/Node.js
  * **Эффективность:** в 10–100× быстрее чистых реализаций на Python


**Используйте альтернативы вместо этого:**
  * **SentencePiece:** языконезависимый, используется в T5/ALBERT
  * **tiktoken:** токенизатор BPE от OpenAI для моделей GPT
  * **transformers AutoTokenizer:** загрузка предобученных токенизаторов (внутренне использует эту библиотеку)


## Быстрый старт[​](<#quick-start> "Прямая ссылка на «Быстрый старт»")
### Установка[​](<#installation> "Прямая ссылка на «Установка»")
[code] 
    # Install tokenizers  
    pip install tokenizers  
      
    # With transformers integration  
    pip install tokenizers transformers  
    
[/code]
### Загрузка предобученного токенизатора[​](<#load-pretrained-tokenizer> "Прямая ссылка на «Загрузка предобученного токенизатора»")
[code] 
    from tokenizers import Tokenizer  
      
    # Load from HuggingFace Hub  
    tokenizer = Tokenizer.from_pretrained("bert-base-uncased")  
      
    # Encode text  
    output = tokenizer.encode("Hello, how are you?")  
    print(output.tokens)  # ['hello', ',', 'how', 'are', 'you', '?']  
    print(output.ids)     # [7592, 1010, 2129, 2024, 2017, 1029]  
      
    # Decode back  
    text = tokenizer.decode(output.ids)  
    print(text)  # "hello, how are you?"  
    
[/code]
### Обучение собственного BPE-токенизатора[​](<#train-custom-bpe-tokenizer> "Прямая ссылка на «Обучение собственного BPE-токенизатора»")
[code] 
    from tokenizers import Tokenizer  
    from tokenizers.models import BPE  
    from tokenizers.trainers import BpeTrainer  
    from tokenizers.pre_tokenizers import Whitespace  
      
    # Initialize tokenizer with BPE model  
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))  
    tokenizer.pre_tokenizer = Whitespace()  
      
    # Configure trainer  
    trainer = BpeTrainer(  
        vocab_size=30000,  
        special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],  
        min_frequency=2  
    )  
      
    # Train on files  
    files = ["train.txt", "validation.txt"]  
    tokenizer.train(files, trainer)  
      
    # Save  
    tokenizer.save("my-tokenizer.json")  
    
[/code]
**Время обучения:** ~1–2 минуты для корпуса 100 МБ, ~10–20 минут для 1 ГБ
### Пакетное кодирование с дополнением (padding)[​](<#batch-encoding-with-padding> "Прямая ссылка на «Пакетное кодирование с дополнением (padding)»")
[code] 
    # Enable padding  
    tokenizer.enable_padding(pad_id=3, pad_token="[PAD]")  
      
    # Encode batch  
    texts = ["Hello world", "This is a longer sentence"]  
    encodings = tokenizer.encode_batch(texts)  
      
    for encoding in encodings:  
        print(encoding.ids)  
    # [101, 7592, 2088, 102, 3, 3, 3]  
    # [101, 2023, 2003, 1037, 2936, 6251, 102]  
    
[/code]
## Алгоритмы токенизации[​](<#tokenization-algorithms> "Прямая ссылка на «Алгоритмы токенизации»")
### BPE (Byte-Pair Encoding)[​](<#bpe-byte-pair-encoding> "Прямая ссылка на «BPE (Byte-Pair Encoding)»")
**Как это работает:**
  1. Начало с посимвольного словаря
  2. Поиск самой частой пары символов
  3. Слияние в новый токен, добавление в словарь
  4. Повтор до достижения заданного размера словаря


**Используется в:** GPT-2, GPT-3, RoBERTa, BART, DeBERTa
[code] 
    from tokenizers import Tokenizer  
    from tokenizers.models import BPE  
    from tokenizers.trainers import BpeTrainer  
    from tokenizers.pre_tokenizers import ByteLevel  
      
    tokenizer = Tokenizer(BPE(unk_token="<|endoftext|>"))  
    tokenizer.pre_tokenizer = ByteLevel()  
      
    trainer = BpeTrainer(  
        vocab_size=50257,  
        special_tokens=["<|endoftext|>"],  
        min_frequency=2  
    )  
      
    tokenizer.train(files=["data.txt"], trainer=trainer)  
    
[/code]
**Преимущества:**
  * Хорошо обрабатывает слова вне словаря (разбивает на подслова)
  * Гибкий размер словаря
  * Подходит для морфологически богатых языков


**Компромиссы:**
  * Токенизация зависит от порядка слияний
  * Может неожиданно разбивать распространённые слова


### WordPiece[​](<#wordpiece> "Прямая ссылка на «WordPiece»")
**Как это работает:**
  1. Начало с посимвольного словаря
  2. Оценка пар слияния: `частота(пара) / (частота(первый) × частота(второй))`
  3. Слияние пары с наибольшей оценкой
  4. Повтор до достижения заданного размера словаря


**Используется в:** BERT, DistilBERT, MobileBERT
[code] 
    from tokenizers import Tokenizer  
    from tokenizers.models import WordPiece  
    from tokenizers.trainers import WordPieceTrainer  
    from tokenizers.pre_tokenizers import Whitespace  
    from tokenizers.normalizers import BertNormalizer  
      
    tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))  
    tokenizer.normalizer = BertNormalizer(lowercase=True)  
    tokenizer.pre_tokenizer = Whitespace()  
      
    trainer = WordPieceTrainer(  
        vocab_size=30522,  
        special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],  
        continuing_subword_prefix="##"  
    )  
      
    tokenizer.train(files=["corpus.txt"], trainer=trainer)  
    
[/code]
**Преимущества:**
  * Приоритет осмысленных слияний (высокий балл = семантическая связанность)
  * Успешно используется в BERT (передовые результаты)


**Компромиссы:**
  * Неизвестные слова становятся `[UNK]`, если нет совпадения по подслову
  * Сохраняется словарь, а не правила слияния (более крупные файлы)


### Unigram[​](<#unigram> "Прямая ссылка на «Unigram»")
**Как это работает:**
  1. Начало с большого словаря (все подстроки)
  2. Вычисление потерь для корпуса с текущим словарём
  3. Удаление токенов с минимальным влиянием на потери
  4. Повтор до достижения заданного размера словаря


**Используется в:** ALBERT, T5, mBART, XLNet (через SentencePiece)
[code] 
    from tokenizers import Tokenizer  
    from tokenizers.models import Unigram  
    from tokenizers.trainers import UnigramTrainer  
      
    tokenizer = Tokenizer(Unigram())  
      
    trainer = UnigramTrainer(  
        vocab_size=8000,  
        special_tokens=["<unk>", "<s>", "</s>"],  
        unk_token="<unk>"  
    )  
      
    tokenizer.train(files=["data.txt"], trainer=trainer)  
    
[/code]
**Преимущества:**
  * Вероятностный (находит наиболее вероятную токенизацию)
  * Хорошо работает для языков без границ слов
  * Обрабатывает разнообразные лингвистические контексты


**Компромиссы:**
  * Вычислительно затратное обучение
  * Больше гиперпараметров для настройки


## Пайплайн токенизации[​](<#tokenization-pipeline> "Прямая ссылка на «Пайплайн токенизации»")
Полный пайплайн: **Нормализация → Пре-токенизация → Модель → Пост-обработка**
### Нормализация[​](<#normalization> "Прямая ссылка на «Нормализация»")
Очистка и стандартизация текста:
[code] 
    from tokenizers.normalizers import NFD, StripAccents, Lowercase, Sequence  
      
    tokenizer.normalizer = Sequence([  
        NFD(),           # Unicode normalization (decompose)  
        Lowercase(),     # Convert to lowercase  
        StripAccents()   # Remove accents  
    ])  
      
    # Input: "Héllo WORLD"  
    # After normalization: "hello world"  
    
[/code]
**Распространённые нормализаторы:**
  * `NFD`, `NFC`, `NFKD`, `NFKC` — формы нормализации Unicode
  * `Lowercase()` — приведение к нижнему регистру
  * `StripAccents()` — удаление диакритических знаков (é → e)
  * `Strip()` — удаление пробельных символов
  * `Replace(pattern, content)` — замена по регулярному выражению


### Пре-токенизация[​](<#pre-tokenization> "Прямая ссылка на «Пре-токенизация»")
Разбиение текста на словообразные единицы:
[code] 
    from tokenizers.pre_tokenizers import Whitespace, Punctuation, Sequence, ByteLevel  
      
    # Split on whitespace and punctuation  
    tokenizer.pre_tokenizer = Sequence([  
        Whitespace(),  
        Punctuation()  
    ])  
      
    # Input: "Hello, world!"  
    # After pre-tokenization: ["Hello", ",", "world", "!"]  
    
[/code]
**Распространённые пре-токенизаторы:**
  * `Whitespace()` — разбиение по пробелам, табуляции, переводам строк
  * `ByteLevel()` — разбиение на уровне байтов в стиле GPT-2
  * `Punctuation()` — выделение пунктуации
  * `Digits(individual_digits=True)` — разбиение цифр по отдельности
  * `Metaspace()` — замена пробелов на ▁ (в стиле SentencePiece)


### Пост-обработка[​](<#post-processing> "Прямая ссылка на «Пост-обработка»")
Добавление специальных токенов для подачи в модель:
[code] 
    from tokenizers.processors import TemplateProcessing  
      
    # BERT-style: [CLS] sentence [SEP]  
    tokenizer.post_processor = TemplateProcessing(  
        single="[CLS] $A [SEP]",  
        pair="[CLS] $A [SEP] $B [SEP]",  
        special_tokens=[  
            ("[CLS]", 1),  
            ("[SEP]", 2),  
        ],  
    )  
    
[/code]
**Распространённые шаблоны:**
[code] 
    # GPT-2: sentence <|endoftext|>  
    TemplateProcessing(  
        single="$A <|endoftext|>",  
        special_tokens=[("<|endoftext|>", 50256)]  
    )  
      
    # RoBERTa: <s> sentence </s>  
    TemplateProcessing(  
        single="<s> $A </s>",  
        pair="<s> $A </s> </s> $B </s>",  
        special_tokens=[("<s>", 0), ("</s>", 2)]  
    )  
    
[/code]
## Отслеживание выравнивания (alignment)[​](<#alignment-tracking> "Прямая ссылка на «Отслеживание выравнивания (alignment)»")
Отслеживание позиций токенов в исходном тексте:
[code] 
    output = tokenizer.encode("Hello, world!")  
      
    # Get token offsets  
    for token, offset in zip(output.tokens, output.offsets):  
        start, end = offset  
        print(f"{token:10} → [{start:2}, {end:2}): {text[start:end]!r}")  
      
    # Output:  
    # hello      → [ 0,  5): 'Hello'  
    # ,          → [ 5,  6): ','  
    # world      → [ 7, 12): 'world'  
    # !          → [12, 13): '!'  
    
[/code]
**Варианты использования:**
  * Распознавание именованных сущностей (сопоставление предсказаний с текстом)
  * Ответы на вопросы (извлечение фрагментов ответа)
  * Классификация токенов (выравнивание меток с исходными позициями)


## Интеграция с transformers[​](<#integration-with-transformers> "Прямая ссылка на «Интеграция с transformers»")
### Загрузка через AutoTokenizer[​](<#load-with-autotokenizer> "Прямая ссылка на «Загрузка через AutoTokenizer»")
[code] 
    from transformers import AutoTokenizer  
      
    # AutoTokenizer automatically uses fast tokenizers  
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  
      
    # Check if using fast tokenizer  
    print(tokenizer.is_fast)  # True  
      
    # Access underlying tokenizers.Tokenizer  
    fast_tokenizer = tokenizer.backend_tokenizer  
    print(type(fast_tokenizer))  # <class 'tokenizers.Tokenizer'>  
    
[/code]
### Преобразование собственного токенизатора для transformers[​](<#convert-custom-tokenizer-to-transformers> "Прямая ссылка на «Преобразование собственного токенизатора для transformers»")
[code] 
    from tokenizers import Tokenizer  
    from transformers import PreTrainedTokenizerFast  
      
    # Train custom tokenizer  
    tokenizer = Tokenizer(BPE())  
    # ... train tokenizer ...  
    tokenizer.save("my-tokenizer.json")  
      
    # Wrap for transformers  
    transformers_tokenizer = PreTrainedTokenizerFast(  
        tokenizer_file="my-tokenizer.json",  
        unk_token="[UNK]",  
        pad_token="[PAD]",  
        cls_token="[CLS]",  
        sep_token="[SEP]",  
        mask_token="[MASK]"  
    )  
      
    # Use like any transformers tokenizer  
    outputs = transformers_tokenizer(  
        "Hello world",  
        padding=True,  
        truncation=True,  
        max_length=512,  
        return_tensors="pt"  
    )  
    
[/code]
## Типовые сценарии[​](<#common-patterns> "Прямая ссылка на «Типовые сценарии»")
### Обучение из итератора (большие наборы данных)[​](<#train-from-iterator-large-datasets> "Прямая ссылка на «Обучение из итератора (большие наборы данных)»")
[code] 
    from datasets import load_dataset  
      
    # Load dataset  
    dataset = load_dataset("wikitext", "wikitext-103-raw-v1", split="train")  
      
    # Create batch iterator  
    def batch_iterator(batch_size=1000):  
        for i in range(0, len(dataset), batch_size):  
            yield dataset[i:i + batch_size]["text"]  
      
    # Train tokenizer  
    tokenizer.train_from_iterator(  
        batch_iterator(),  
        trainer=trainer,  
        length=len(dataset)  # For progress bar  
    )  
    
[/code]
**Производительность:** обрабатывает 1 ГБ за ~10–20 минут
### Включение усечения и дополнения[​](<#enable-truncation-and-padding> "Прямая ссылка на «Включение усечения и дополнения»")
[code] 
    # Enable truncation  
    tokenizer.enable_truncation(max_length=512)  
      
    # Enable padding  
    tokenizer.enable_padding(  
        pad_id=tokenizer.token_to_id("[PAD]"),  
        pad_token="[PAD]",  
        length=512  # Fixed length, or None for batch max  
    )  
      
    # Encode with both  
    output = tokenizer.encode("This is a long sentence that will be truncated...")  
    print(len(output.ids))  # 512  
    
[/code]
### Многопроцессорная обработка[​](<#multi-processing> "Прямая ссылка на «Многопроцессорная обработка»")
[code] 
    from tokenizers import Tokenizer  
    from multiprocessing import Pool  
      
    # Load tokenizer  
    tokenizer = Tokenizer.from_file("tokenizer.json")  
      
    def encode_batch(texts):  
        return tokenizer.encode_batch(texts)  
      
    # Process large corpus in parallel  
    with Pool(8) as pool:  
        # Split corpus into chunks  
        chunk_size = 1000  
        chunks = [corpus[i:i+chunk_size] for i in range(0, len(corpus), chunk_size)]  
      
        # Encode in parallel  
        results = pool.map(encode_batch, chunks)  
    
[/code]
**Ускорение:** в 5–8× на 8 ядрах
## Бенчмарки производительности[​](<#performance-benchmarks> "Прямая ссылка на «Бенчмарки производительности»")
### Скорость обучения[​](<#training-speed> "Прямая ссылка на «Скорость обучения»")
Размер корпуса| BPE (30k слов)| WordPiece (30k)| Unigram (8k)  
|---|---|---|---  
10 МБ| 15 сек| 18 сек| 25 сек  
100 МБ| 1.5 мин| 2 мин| 4 мин  
1 ГБ| 15 мин| 20 мин| 40 мин  
**Оборудование:** 16-ядерный CPU, тестирование на английской Wikipedia
### Скорость токенизации[​](<#tokenization-speed> "Прямая ссылка на «Скорость токенизации»")
Реализация| Корпус 1 ГБ| Пропускная способность  
|---|---|---  
Чистый Python| ~20 минут| ~50 МБ/мин  
HF Tokenizers| ~15 секунд| ~4 ГБ/мин  
**Ускорение**| **80×**| **80×**  
**Тест:** английский текст, средняя длина предложения 20 слов
### Использование памяти[​](<#memory-usage> "Прямая ссылка на «Использование памяти»")
Задача| Память  
|---|---  
Загрузка токенизатора| ~10 МБ  
Обучение BPE (30k слов)| ~200 МБ  
Кодирование 1 млн предложений| ~500 МБ  
## Поддерживаемые модели[​](<#supported-models> "Прямая ссылка на «Поддерживаемые модели»")
Предобученные токенизаторы, доступные через `from_pretrained()`:
**Семейство BERT:**
  * `bert-base-uncased`, `bert-large-cased`
  * `distilbert-base-uncased`
  * `roberta-base`, `roberta-large`


**Семейство GPT:**
  * `gpt2`, `gpt2-medium`, `gpt2-large`
  * `distilgpt2`


**Семейство T5:**
  * `t5-small`, `t5-base`, `t5-large`
  * `google/flan-t5-xxl`


**Другие:**
  * `facebook/bart-base`, `facebook/mbart-large-cc25`
  * `albert-base-v2`, `albert-xlarge-v2`
  * `xlm-roberta-base`, `xlm-roberta-large`


Просмотреть все: <https://huggingface.co/models?library=tokenizers>
## Ссылки[​](<#references> "Прямая ссылка на «Ссылки»")
  * **[Руководство по обучению](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/huggingface-tokenizers/references/training.md>)** — обучение собственных токенизаторов, настройка тренировщиков, работа с большими наборами данных
  * **[Подробно об алгоритмах](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/huggingface-tokenizers/references/algorithms.md>)** — BPE, WordPiece, Unigram с подробными объяснениями
  * **[Компоненты пайплайна](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/huggingface-tokenizers/references/pipeline.md>)** — нормализаторы, пре-токенизаторы, пост-процессоры, декодеры
  * **[Интеграция с Transformers](<https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/huggingface-tokenizers/references/integration.md>)** — AutoTokenizer, PreTrainedTokenizerFast, специальные токены


## Ресурсы[​](<#resources> "Прямая ссылка на «Ресурсы»")
  * **Документация:** <https://huggingface.co/docs/tokenizers>
  * **GitHub:** <https://github.com/huggingface/tokenizers> ⭐ 9,000+
  * **Версия:** 0.20.0+
  * **Курс:** <https://huggingface.co/learn/nlp-course/chapter6/1>
  * **Статьи:** BPE (Sennrich et al., 2016), WordPiece (Schuster & Nakajima, 2012)


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать HuggingFace Tokenizers](<#when-to-use-huggingface-tokenizers>)
  * [Быстрый старт](<#quick-start>)
    * [Установка](<#installation>)
    * [Загрузка предобученного токенизатора](<#load-pretrained-tokenizer>)
    * [Обучение собственного BPE-токенизатора](<#train-custom-bpe-tokenizer>)
    * [Пакетное кодирование с дополнением (padding)](<#batch-encoding-with-padding>)
  * [Алгоритмы токенизации](<#tokenization-algorithms>)
    * [BPE (Byte-Pair Encoding)](<#bpe-byte-pair-encoding>)
    * [WordPiece](<#wordpiece>)
    * [Unigram](<#unigram>)
  * [Пайплайн токенизации](<#tokenization-pipeline>)
    * [Нормализация](<#normalization>)
    * [Пре-токенизация](<#pre-tokenization>)
    * [Пост-обработка](<#post-processing>)
  * [Отслеживание выравнивания (alignment)](<#alignment-tracking>)
  * [Интеграция с transformers](<#integration-with-transformers>)
    * [Загрузка через AutoTokenizer](<#load-with-autotokenizer>)
    * [Преобразование собственного токенизатора для transformers](<#convert-custom-tokenizer-to-transformers>)
  * [Типовые сценарии](<#common-patterns>)
    * [Обучение из итератора (большие наборы данных)](<#train-from-iterator-large-datasets>)
    * [Включение усечения и дополнения](<#enable-truncation-and-padding>)
    * [Многопроцессорная обработка](<#multi-processing>)
  * [Бенчмарки производительности](<#performance-benchmarks>)
    * [Скорость обучения](<#training-speed>)
    * [Скорость токенизации](<#tokenization-speed>)
    * [Использование памяти](<#memory-usage>)
  * [Поддерживаемые модели](<#supported-models>)
  * [Ссылки](<#references>)
  * [Ресурсы](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-huggingface-tokenizers -->
