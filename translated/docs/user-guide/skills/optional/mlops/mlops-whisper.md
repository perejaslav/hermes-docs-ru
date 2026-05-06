На этой странице
Многоцелевая модель распознавания речи от OpenAI. Поддерживает 99 языков, транскрипцию, перевод на английский и определение языка. Шесть размеров модели: от tiny (39M параметров) до large (1550M параметров). Используется для преобразования речи в текст, транскрипции подкастов или многоязычной обработки аудио. Лучший выбор для надёжного многоязычного ASR.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   
---|---  
Источник| Опционально — установка: `hermes skills install official/mlops/whisper`  
Путь| `optional-skills/mlops/whisper`  
Версия| `1.0.0`  
Автор| Orchestra Research  
Лицензия| MIT  
Зависимости| `openai-whisper`, `transformers`, `torch`  
Теги| `Whisper`, `Speech Recognition`, `ASR`, `Multimodal`, `Multilingual`, `OpenAI`, `Speech-To-Text`, `Transcription`, `Translation`, `Audio Processing`  

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит в качестве инструкций, когда навык активен.

# Whisper — надёжное распознавание речи
Многоязычная модель распознавания речи от OpenAI.

## Когда использовать Whisper[​](<#when-to-use-whisper> "Прямая ссылка на Когда использовать Whisper")

**Используйте когда:**
  * Преобразование речи в текст (99 языков)
  * Транскрипция подкастов/видео
  * Автоматизация заметок встреч
  * Перевод на английский
  * Транскрипция зашумлённого аудио
  * Многоязычная обработка аудио

**Показатели:**
  * **72 900+ звёзд на GitHub**
  * Поддержка 99 языков
  * Обучена на 680 000 часах аудио
  * Лицензия MIT

**Альтернативы вместо Whisper:**
  * **AssemblyAI:** Управляемый API, диаризация говорящих
  * **Deepgram:** Потоковое ASR в реальном времени
  * **Google Speech-to-Text:** Облачное решение

## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")

### Установка[​](<#installation> "Прямая ссылка на Установка")

[code] 
    # Requires Python 3.8-3.11  
    pip install -U openai-whisper  
      
    # Requires ffmpeg  
    # macOS: brew install ffmpeg  
    # Ubuntu: sudo apt install ffmpeg  
    # Windows: choco install ffmpeg  
    
[/code]

### Базовая транскрипция[​](<#basic-transcription> "Прямая ссылка на Базовая транскрипция")

[code] 
    import whisper  
      
    # Load model  
    model = whisper.load_model("base")  
      
    # Transcribe  
    result = model.transcribe("audio.mp3")  
      
    # Print text  
    print(result["text"])  
      
    # Access segments  
    for segment in result["segments"]:  
        print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")  
    
[/code]

## Размеры моделей[​](<#model-sizes> "Прямая ссылка на Размеры моделей")

[code] 
    # Available models  
    models = ["tiny", "base", "small", "medium", "large", "turbo"]  
      
    # Load specific model  
    model = whisper.load_model("turbo")  # Fastest, good quality  
    
[/code]

Модель| Параметры| Только английский| Многоязычная| Скорость| VRAM  
---|---|---|---|---|---  
tiny| 39M| ✓| ✓| ~32x| ~1 ГБ  
base| 74M| ✓| ✓| ~16x| ~1 ГБ  
small| 244M| ✓| ✓| ~6x| ~2 ГБ  
medium| 769M| ✓| ✓| ~2x| ~5 ГБ  
large| 1550M| ✗| ✓| 1x| ~10 ГБ  
turbo| 809M| ✗| ✓| ~8x| ~6 ГБ  

**Рекомендация:** Используйте `turbo` для лучшего соотношения скорости и качества, `base` — для прототипирования.

## Параметры транскрипции[​](<#transcription-options> "Прямая ссылка на Параметры транскрипции")

### Указание языка[​](<#language-specification> "Прямая ссылка на Указание языка")

[code] 
    # Auto-detect language  
    result = model.transcribe("audio.mp3")  
      
    # Specify language (faster)  
    result = model.transcribe("audio.mp3", language="en")  
      
    # Supported: en, es, fr, de, it, pt, ru, ja, ko, zh, and 89 more  
    
[/code]

### Выбор задачи[​](<#task-selection> "Прямая ссылка на Выбор задачи")

[code] 
    # Transcription (default)  
    result = model.transcribe("audio.mp3", task="transcribe")  
      
    # Translation to English  
    result = model.transcribe("spanish.mp3", task="translate")  
    # Input: Spanish audio → Output: English text  
    
[/code]

### Начальный промпт[​](<#initial-prompt> "Прямая ссылка на Начальный промпт")

[code] 
    # Improve accuracy with context  
    result = model.transcribe(  
        "audio.mp3",  
        initial_prompt="This is a technical podcast about machine learning and AI."  
    )  
      
    # Helps with:  
    # - Technical terms  
    # - Proper nouns  
    # - Domain-specific vocabulary  
    
[/code]

### Временные метки[​](<#timestamps> "Прямая ссылка на Временные метки")

[code] 
    # Word-level timestamps  
    result = model.transcribe("audio.mp3", word_timestamps=True)  
      
    for segment in result["segments"]:  
        for word in segment["words"]:  
            print(f"{word['word']} ({word['start']:.2f}s - {word['end']:.2f}s)")  
    
[/code]

### Температурный fallback[​](<#temperature-fallback> "Прямая ссылка на Температурный fallback")

[code] 
    # Retry with different temperatures if confidence low  
    result = model.transcribe(  
        "audio.mp3",  
        temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)  
    )  
    
[/code]

## Использование в командной строке[​](<#command-line-usage> "Прямая ссылка на Использование в командной строке")

[code] 
    # Basic transcription  
    whisper audio.mp3  
      
    # Specify model  
    whisper audio.mp3 --model turbo  
      
    # Output formats  
    whisper audio.mp3 --output_format txt     # Plain text  
    whisper audio.mp3 --output_format srt     # Subtitles  
    whisper audio.mp3 --output_format vtt     # WebVTT  
    whisper audio.mp3 --output_format json    # JSON with timestamps  
      
    # Language  
    whisper audio.mp3 --language Spanish  
      
    # Translation  
    whisper spanish.mp3 --task translate  
    
[/code]

## Пакетная обработка[​](<#batch-processing> "Прямая ссылка на Пакетная обработка")

[code] 
    import os  
      
    audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]  
      
    for audio_file in audio_files:  
        print(f"Transcribing {audio_file}...")  
        result = model.transcribe(audio_file)  
      
        # Save to file  
        output_file = audio_file.replace(".mp3", ".txt")  
        with open(output_file, "w") as f:  
            f.write(result["text"])  
    
[/code]

## Транскрипция в реальном времени[​](<#real-time-transcription> "Прямая ссылка на Транскрипция в реальном времени")

[code] 
    # For streaming audio, use faster-whisper  
    # pip install faster-whisper  
      
    from faster_whisper import WhisperModel  
      
    model = WhisperModel("base", device="cuda", compute_type="float16")  
      
    # Transcribe with streaming  
    segments, info = model.transcribe("audio.mp3", beam_size=5)  
      
    for segment in segments:  
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")  
    
[/code]

## Ускорение GPU[​](<#gpu-acceleration> "Прямая ссылка на Ускорение GPU")

[code] 
    import whisper  
      
    # Automatically uses GPU if available  
    model = whisper.load_model("turbo")  
      
    # Force CPU  
    model = whisper.load_model("turbo", device="cpu")  
      
    # Force GPU  
    model = whisper.load_model("turbo", device="cuda")  
      
    # 10-20× faster on GPU  
    
[/code]

## Интеграция с другими инструментами[​](<#integration-with-other-tools> "Прямая ссылка на Интеграция с другими инструментами")

### Генерация субтитров[​](<#subtitle-generation> "Прямая ссылка на Генерация субтитров")

[code] 
    # Generate SRT subtitles  
    whisper video.mp4 --output_format srt --language English  
      
    # Output: video.srt  
    
[/code]

### С LangChain[​](<#with-langchain> "Прямая ссылка на С LangChain")

[code] 
    from langchain.document_loaders import WhisperTranscriptionLoader  
      
    loader = WhisperTranscriptionLoader(file_path="audio.mp3")  
    docs = loader.load()  
      
    # Use transcription in RAG  
    from langchain_chroma import Chroma  
    from langchain_openai import OpenAIEmbeddings  
      
    vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())  
    
[/code]

### Извлечение аудио из видео[​](<#extract-audio-from-video> "Прямая ссылка на Извлечение аудио из видео")

[code] 
    # Use ffmpeg to extract audio  
    ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav  
      
    # Then transcribe  
    whisper audio.wav  
    
[/code]

## Рекомендации[​](<#best-practices> "Прямая ссылка на Рекомендации")

  1. **Используйте модель turbo** — лучшее соотношение скорости и качества для английского
  2. **Указывайте язык** — быстрее, чем автоопределение
  3. **Добавляйте начальный промпт** — улучшает распознавание технических терминов
  4. **Используйте GPU** — в 10-20× быстрее
  5. **Пакетная обработка** — более эффективно
  6. **Конвертируйте в WAV** — лучшая совместимость
  7. **Разбивайте длинное аудио** — чанки <30 мин
  8. **Проверяйте поддержку языка** — качество варьируется в зависимости от языка
  9. **Используйте faster-whisper** — в 4× быстрее openai-whisper
  10. **Следите за VRAM** — подбирайте размер модели под оборудование

## Производительность[​](<#performance> "Прямая ссылка на Производительность")

Модель| Коэффициент реального времени (CPU)| Коэффициент реального времени (GPU)  
---|---|---  
tiny| ~0.32| ~0.01  
base| ~0.16| ~0.01  
turbo| ~0.08| ~0.01  
large| ~1.0| ~0.05  
_Коэффициент реального времени: 0.1 = в 10× быстрее реального времени_

## Поддержка языков[​](<#language-support> "Прямая ссылка на Поддержка языков")

Языки с наилучшей поддержкой:
  * Английский (en)
  * Испанский (es)
  * Французский (fr)
  * Немецкий (de)
  * Итальянский (it)
  * Португальский (pt)
  * Русский (ru)
  * Японский (ja)
  * Корейский (ko)
  * Китайский (zh)

Полный список: всего 99 языков

## Ограничения[​](<#limitations> "Прямая ссылка на Ограничения")

  1. **Галлюцинации** — может повторять или выдумывать текст
  2. **Точность на длинных аудио** — снижается на аудио >30 мин
  3. **Идентификация говорящих** — отсутствует диаризация
  4. **Акценты** — качество варьируется
  5. **Фоновый шум** — может влиять на точность
  6. **Задержка в реальном времени** — не подходит для живых субтитров

## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")

  * **GitHub:** <https://github.com/openai/whisper> ⭐ 72 900+
  * **Статья:** <https://arxiv.org/abs/2212.04356>
  * **Карточка модели:** <https://github.com/openai/whisper/blob/main/model-card.md>
  * **Colab:** Доступен в репозитории
  * **Лицензия:** MIT

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать Whisper](<#when-to-use-whisper>)
  * [Быстрый старт](<#quick-start>)
    * [Установка](<#installation>)
    * [Базовая транскрипция](<#basic-transcription>)
  * [Размеры моделей](<#model-sizes>)
  * [Параметры транскрипции](<#transcription-options>)
    * [Указание языка](<#language-specification>)
    * [Выбор задачи](<#task-selection>)
    * [Начальный промпт](<#initial-prompt>)
    * [Временные метки](<#timestamps>)
    * [Температурный fallback](<#temperature-fallback>)
  * [Использование в командной строке](<#command-line-usage>)
  * [Пакетная обработка](<#batch-processing>)
  * [Транскрипция в реальном времени](<#real-time-transcription>)
  * [Ускорение GPU](<#gpu-acceleration>)
  * [Интеграция с другими инструментами](<#integration-with-other-tools>)
    * [Генерация субтитров](<#subtitle-generation>)
    * [С LangChain](<#with-langchain>)
    * [Извлечение аудио из видео](<#extract-audio-from-video>)
  * [Рекомендации](<#best-practices>)
  * [Производительность](<#performance>)
  * [Поддержка языков](<#language-support>)
  * [Ограничения](<#limitations>)
  * [Ресурсы](<#resources>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-whisper -->
