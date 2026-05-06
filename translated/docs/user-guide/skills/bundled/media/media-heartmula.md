На этой странице
HeartMuLa: генерация песен по тексту + тегам, похожая на Suno.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|
|Источник| Встроенный (устанавливается по умолчанию)  
|Путь| `skills/media/heartmula`  
|Версия| `1.0.0`  
|Теги| `music`, `audio`, `generation`, `ai`, `heartmula`, `heartcodec`, `lyrics`, `songs`  
|Связанные навыки| `audiocraft`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное описание навыка, которое загружает Hermes при его активации. Это те инструкции, которые видит агент, когда навык активен.
# HeartMuLa — Генерация музыки с открытым исходным кодом
## Обзор[​](<#overview> "Прямая ссылка на Обзор")
HeartMuLa — это семейство открытых фундаментальных моделей музыки (Apache-2.0), которые генерируют музыку по тексту и тегам с поддержкой нескольких языков. Создаёт полноценные песни на основе текста + тегов. Сопоставима с Suno в мире открытого кода. Включает:
  * **HeartMuLa** \\- Языковая модель музыки (3B/7B) для генерации по тексту + тегам
  * **HeartCodec** \\- Музыкальный кодек 12.5 Гц для высококачественной реконструкции аудио
  * **HeartTranscriptor** \\- Транскрипция текста на основе Whisper
  * **HeartCLAP** \\- Модель выравнивания аудио-текста


## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")
  * Пользователь хочет сгенерировать музыку/песни по текстовому описанию
  * Пользователь хочет открытую альтернативу Suno
  * Пользователь хочет локальную/офлайн-генерацию музыки
  * Пользователь спрашивает о HeartMuLa, heartlib или AI-генерации музыки


## Требования к оборудованию[​](<#hardware-requirements> "Прямая ссылка на Требования к оборудованию")
  * **Минимум**: 8 ГБ VRAM с `--lazy_load true` (загружает/выгружает модели последовательно)
  * **Рекомендуется**: 16+ ГБ VRAM для комфортного использования на одной видеокарте
  * **Несколько GPU**: Используйте `--mula_device cuda:0 --codec_device cuda:1` для распределения между GPU
  * Модель 3B с lazy_load пиково использует ~6.2 ГБ VRAM


## Шаги по установке[​](<#installation-steps> "Прямая ссылка на Шаги по установке")
### 1\\. Клонирование репозитория[​](<#1-clone-repository> "Прямая ссылка на 1. Клонирование репозитория")
[code] 
    cd ~/  # или нужный каталог  
    git clone https://github.com/HeartMuLa/heartlib.git  
    cd heartlib  
    
[/code]
### 2\\. Создание виртуального окружения (требуется Python 3.10)[​](<#2-create-virtual-environment-python-310-required> "Прямая ссылка на 2. Создание виртуального окружения \\(требуется Python 3.10\\)")
[code] 
    uv venv --python 3.10 .venv  
    . .venv/bin/activate  
    uv pip install -e .  
    
[/code]
### 3\\. Исправление проблем совместимости зависимостей[​](<#3-fix-dependency-compatibility-issues> "Прямая ссылка на 3. Исправление проблем совместимости зависимостей")
**ВАЖНО**: по состоянию на февраль 2026 г. закреплённые зависимости конфликтуют с более новыми пакетами. Примените следующие исправления:
[code] 
    # Обновление datasets (старая версия несовместима с текущим pyarrow)  
    uv pip install --upgrade datasets  
      
    # Обновление transformers (нужно для совместимости с huggingface-hub 1.x)  
    uv pip install --upgrade transformers  
    
[/code]
### 4\\. Патч исходного кода (требуется для transformers 5.x)[​](<#4-patch-source-code-required-for-transformers-5x> "Прямая ссылка на 4. Патч исходного кода \\(требуется для transformers 5.x\\)")
**Патч 1 — исправление кэша RoPE** в `src/heartlib/heartmula/modeling_heartmula.py`:
В методе `setup_caches` класса `HeartMuLa` добавьте переинициализацию RoPE после блока try/except для `reset_caches` и перед блоком `with device:`:
[code] 
    # Re-initialize RoPE caches that were skipped during meta-device loading  
    from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE  
    for module in self.modules():  
        if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:  
            module.rope_init()  
            module.to(device)  
    
[/code]
**Почему**: `from_pretrained` создаёт модель сначала на meta-устройстве; `Llama3ScaledRoPE.rope_init()` пропускает сборку кэша на meta-тензорах, а затем кэш никогда не перестраивается после загрузки весов на реальное устройство.
**Патч 2 — исправление загрузки HeartCodec** в `src/heartlib/pipelines/music_generation.py`:
Добавьте `ignore_mismatched_sizes=True` во ВСЕ вызовы `HeartCodec.from_pretrained()` (их 2: eager-загрузка в `__init__` и ленивая загрузка в свойстве `codec`).
**Почему**: буферы `initted` VQ-книги имеют форму `[1]` в контрольной точке vs `[]` в модели. Те же данные, просто скаляр против 0-мерного тензора. Безопасно игнорировать.
### 5\\. Загрузка контрольных точек модели[​](<#5-download-model-checkpoints> "Прямая ссылка на 5. Загрузка контрольных точек модели")
[code] 
    cd heartlib  # корень проекта  
    hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'  
    hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'  
    hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'  
    
[/code]
Все 3 можно загружать параллельно. Общий размер — несколько ГБ.
## GPU / CUDA[​](<#gpu--cuda> "Прямая ссылка на GPU / CUDA")
HeartMuLa по умолчанию использует CUDA (`--mula_device cuda --codec_device cuda`). Дополнительная настройка не требуется, если у пользователя есть GPU NVIDIA с установленной поддержкой PyTorch CUDA.
  * Установленный `torch==2.4.1` включает поддержку CUDA 12.1 из коробки
  * `torchtune` может показывать версию `0.4.0+cpu` — это лишь метаданные пакета, он всё равно использует CUDA через PyTorch
  * Чтобы проверить, используется ли GPU, ищите строки с «CUDA memory» в выводе (например, «CUDA memory before unloading: 6.20 GB»)
  * **Нет GPU?** Можно запустить на CPU с параметрами `--mula_device cpu --codec_device cpu`, но генерация будет **чрезвычайно медленной** (возможно, 30–60+ минут на одну песню против ~4 минут на GPU). Режим CPU также требует значительного объёма RAM (~12+ ГБ свободно). Если у пользователя нет GPU NVIDIA, рекомендуйте использовать облачный GPU-сервис (бесплатный уровень Google Colab с T4, Lambda Labs и т.п.) или онлайн-демо по адресу <https://heartmula.github.io/>.


## Использование[​](<#usage> "Прямая ссылка на Использование")
### Базовая генерация[​](<#basic-generation> "Прямая ссылка на Базовая генерация")
[code] 
    cd heartlib  
    . .venv/bin/activate  
    python ./examples/run_music_generation.py \\  
      --model_path=./ckpt \\  
      --version="3B" \\  
      --lyrics="./assets/lyrics.txt" \\  
      --tags="./assets/tags.txt" \\  
      --save_path="./assets/output.mp3" \\  
      --lazy_load true  
    
[/code]
### Форматирование входных данных[​](<#input-formatting> "Прямая ссылка на Форматирование входных данных")
**Теги** (через запятую, без пробелов):
[code] 
    piano,happy,wedding,synthesizer,romantic  
    
[/code]
или
[code] 
    rock,energetic,guitar,drums,male-vocal  
    
[/code]
**Текст песни** (используйте структурные теги в скобках):
[code] 
    [Intro]  
      
    [Verse]  
    Ваш текст здесь...  
      
    [Chorus]  
    Текст припева...  
      
    [Bridge]  
    Текст бриджа...  
      
    [Outro]  
    
[/code]
### Ключевые параметры[​](<#key-parameters> "Прямая ссылка на Ключевые параметры")
Параметр| По умолчанию| Описание  
---|---|---  
`--max_audio_length_ms`| 240000| Максимальная длина в мс (240 с = 4 мин)  
`--topk`| 50| Top-k сэмплирование  
`--temperature`| 1.0| Температура сэмплирования  
`--cfg_scale`| 1.5| Коэффициент направляющей без классификатора  
`--lazy_load`| false| Загружать/выгружать модели по требованию (экономит VRAM)  
`--mula_dtype`| bfloat16| Тип данных для HeartMuLa (рекомендуется bf16)  
`--codec_dtype`| float32| Тип данных для HeartCodec (рекомендуется fp32 для качества)  
### Производительность[​](<#performance> "Прямая ссылка на Производительность")
  * RTF (Real-Time Factor) ≈ 1.0 — песня длительностью 4 минуты генерируется ~4 минуты
  * Выходной формат: MP3, 48 кГц, стерео, 128 кбит/с


## Подводные камни[​](<#pitfalls> "Прямая ссылка на Подводные камни")
  1. **НЕ используйте bf16 для HeartCodec** — ухудшает качество аудио. Используйте fp32 (по умолчанию).
  2. **Теги могут игнорироваться** — известная проблема (#90). Текст песни обычно доминирует; поэкспериментируйте с порядком тегов.
  3. **Triton недоступен на macOS** — ускорение на GPU только для Linux/CUDA.
  4. **Несовместимость с RTX 5080** сообщается в issues upstream.
  5. Конфликты фиксации зависимостей требуют ручного обновления и патчей, описанных выше.


## Ссылки[​](<#links> "Прямая ссылка на Ссылки")
  * Репозиторий: <https://github.com/HeartMuLa/heartlib>
  * Модели: <https://huggingface.co/HeartMuLa>
  * Статья: <https://arxiv.org/abs/2601.10547>
  * Лицензия: Apache-2.0


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Обзор](<#overview>)
  * [Когда использовать](<#when-to-use>)
  * [Требования к оборудованию](<#hardware-requirements>)
  * [Шаги по установке](<#installation-steps>)
    * [1\\. Клонирование репозитория](<#1-clone-repository>)
    * [2\\. Создание виртуального окружения (требуется Python 3.10)](<#2-create-virtual-environment-python-310-required>)
    * [3\\. Исправление проблем совместимости зависимостей](<#3-fix-dependency-compatibility-issues>)
    * [4\\. Патч исходного кода (требуется для transformers 5.x)](<#4-patch-source-code-required-for-transformers-5x>)
    * [5\\. Загрузка контрольных точек модели](<#5-download-model-checkpoints>)
  * [GPU / CUDA](<#gpu--cuda>)
  * [Использование](<#usage>)
    * [Базовая генерация](<#basic-generation>)
    * [Форматирование входных данных](<#input-formatting>)
    * [Ключевые параметры](<#key-parameters>)
    * [Производительность](<#performance>)
  * [Подводные камни](<#pitfalls>)
  * [Ссылки](<#links>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/media/media-heartmula -->
