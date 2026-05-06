На этой странице
Hermes Agent поддерживает как синтез речи из текста (TTS), так и транскрипцию голосовых сообщений на всех платформах обмена сообщениями.

Подписчики Nous
Если у вас есть платная подписка [Nous Portal](https://portal.nousresearch.com), OpenAI TTS доступен через **[Tool Gateway](/docs/user-guide/features/tool-gateway)** без отдельного ключа API OpenAI. Выполните `hermes model` или `hermes tools` для его включения.

## Преобразование текста в речь (Text-to-Speech)[​](#text-to-speech "Прямая ссылка на Преобразование текста в речь")

Преобразуйте текст в речь с помощью десяти провайдеров:

| Провайдер | Качество | Стоимость | API-ключ |
|---|---|---|---|
| **Edge TTS** (по умолчанию) | Хорошее | Бесплатно | Не требуется |
| **ElevenLabs** | Отличное | Платно | `ELEVENLABS_API_KEY` |
| **OpenAI TTS** | Хорошее | Платно | `VOICE_TOOLS_OPENAI_KEY` |
| **MiniMax TTS** | Отличное | Платно | `MINIMAX_API_KEY` |
| **Mistral (Voxtral TTS)** | Отличное | Платно | `MISTRAL_API_KEY` |
| **Google Gemini TTS** | Отличное | Бесплатный лимит | `GEMINI_API_KEY` |
| **xAI TTS** | Отличное | Платно | `XAI_API_KEY` |
| **NeuTTS** | Хорошее | Бесплатно (локально) | Не требуется |
| **KittenTTS** | Хорошее | Бесплатно (локально) | Не требуется |
| **Piper** | Хорошее | Бесплатно (локально) | Не требуется |

### Доставка на платформы[​](#platform-delivery "Прямая ссылка на Доставка на платформы")

| Платформа | Доставка | Формат |
|---|---|---|
| Telegram | Голосовое сообщение (воспроизводится в чате) | Opus `.ogg` |
| Discord | Голосовое сообщение (Opus/OGG), с понижением до файлового вложения | Opus/MP3 |
| WhatsApp | Аудиофайл вложением | MP3 |
| CLI | Сохраняется в `~/.hermes/audio_cache/` | MP3 |

### Конфигурация[​](#configuration "Прямая ссылка на Конфигурация")

```yaml
# В ~/.hermes/config.yaml
tts:
  provider: "edge"              # "edge" | "elevenlabs" | "openai" | "minimax" | "mistral" | "gemini" | "xai" | "neutts" | "kittentts" | "piper"
  speed: 1.0                    # Глобальный множитель скорости (настройки провайдера переопределяют его)
  edge:
    voice: "en-US-AriaNeural"   # 322 голоса, 74 языка
    speed: 1.0                  # Преобразуется в процент скорости (+/-%)
  elevenlabs:
    voice_id: "pNInz6obpgDQGcFmaJgB"  # Adam
    model_id: "eleven_multilingual_v2"
  openai:
    model: "gpt-4o-mini-tts"
    voice: "alloy"              # alloy, echo, fable, onyx, nova, shimmer
    base_url: "https://api.openai.com/v1"  # Переопределение для TTS-совместимых конечных точек OpenAI
    speed: 1.0                  # 0.25 – 4.0
  minimax:
    model: "speech-2.8-hd"     # speech-2.8-hd (по умолчанию), speech-2.8-turbo
    voice_id: "English_Graceful_Lady"  # См. https://platform.minimax.io/faq/system-voice-id
    speed: 1                    # 0.5 – 2.0
    vol: 1                      # 0 – 10
    pitch: 0                    # -12 – 12
  mistral:
    model: "voxtral-mini-tts-2603"
    voice_id: "c69964a6-ab8b-4f8a-9465-ec0925096ec8"  # Paul – Neutral (по умолчанию)
  gemini:
    model: "gemini-2.5-flash-preview-tts"  # или gemini-2.5-pro-preview-tts
    voice: "Kore"               # 30 предустановленных голосов: Zephyr, Puck, Kore, Enceladus, Gacrux и др.
  xai:
    voice_id: "eve"             # или пользовательский ID голоса — см. документацию ниже
    language: "en"              # Код ISO 639-1
    sample_rate: 24000          # 22050 / 24000 (по умолч.) / 44100 / 48000
    bit_rate: 128000            # Битрейт MP3; применяется только при codec=mp3
    # base_url: "https://api.x.ai/v1"   # Переопределение через переменную окружения XAI_BASE_URL
  neutts:
    ref_audio: ''
    ref_text: ''
    model: neuphonic/neutts-air-q4-gguf
    device: cpu
  kittentts:
    model: KittenML/kitten-tts-nano-0.8-int8   # 25MB int8; также: kitten-tts-micro-0.8 (41MB), kitten-tts-mini-0.8 (80MB)
    voice: Jasper                               # Jasper, Bella, Luna, Bruno, Rosie, Hugo, Kiki, Leo
    speed: 1.0                                  # 0.5 – 2.0
    clean_text: true                            # Раскрывать числа, валюты, единицы измерения
  piper:
    voice: en_US-lessac-medium                  # Имя голоса (авто-загрузка) или абсолютный путь к .onnx
    # voices_dir: ''                            # по умолч.: ~/.hermes/cache/piper-voices/
    # use_cuda: false                           # требует onnxruntime-gpu
    # length_scale: 1.0                         # 2.0 = вдвое медленнее
    # noise_scale: 0.667
    # noise_w_scale: 0.8
    # volume: 1.0                               # 0.5 = вдвое тише
    # normalize_audio: true
```

**Управление скоростью**: Глобальное значение `tts.speed` применяется ко всем провайдерам по умолчанию. Каждый провайдер может переопределить его собственной настройкой `speed` (например, `tts.openai.speed: 1.5`). Скорость конкретного провайдера имеет приоритет над глобальным значением. Значение по умолчанию: `1.0` (нормальная скорость).

### Ограничения длины входного текста[​](#input-length-limits "Прямая ссылка на Ограничения длины входного текста")

У каждого провайдера есть задокументированное ограничение на количество символов в одном запросе. Hermes усекает текст перед вызовом провайдера, чтобы запросы никогда не завершались ошибкой из-за превышения длины:

| Провайдер | Лимит по умолчанию (символов) |
|---|---|
| Edge TTS | 5000 |
| OpenAI | 4096 |
| xAI | 15000 |
| MiniMax | 10000 |
| Mistral | 4000 |
| Google Gemini | 5000 |
| ElevenLabs | Зависит от модели (см. ниже) |
| NeuTTS | 2000 |
| KittenTTS | 2000 |

**ElevenLabs** выбирает лимит в зависимости от настроенного `model_id`:

| `model_id` | Лимит (символов) |
|---|---|
| `eleven_flash_v2_5` | 40000 |
| `eleven_flash_v2` | 30000 |
| `eleven_multilingual_v2` (по умолч.), `eleven_multilingual_v1`, `eleven_english_sts_v2`, `eleven_english_sts_v1` | 10000 |
| `eleven_v3`, `eleven_ttv_v3` | 5000 |
| Неизвестная модель | Возврат к лимиту провайдера по умолчанию (10000) |

**Переопределение для каждого провайдера** с помощью `max_text_length:` в разделе провайдера вашей TTS-конфигурации:

```yaml
tts:
  openai:
    max_text_length: 8192   # повышение или понижение лимита провайдера
```

Учитываются только целые положительные числа. Ноль, отрицательные, нечисловые или булевы значения приводят к возврату к лимиту провайдера по умолчанию, поэтому некорректная конфигурация не может случайно отключить усечение.

### Голосовые сообщения Telegram и ffmpeg[​](#telegram-voice-bubbles--ffmpeg "Прямая ссылка на Голосовые сообщения Telegram и ffmpeg")

Голосовые сообщения Telegram требуют формат Opus/OGG:

* **OpenAI, ElevenLabs и Mistral** создают Opus нативно — дополнительная настройка не требуется
* **Edge TTS** (по умолчанию) выводит MP3 и требует **ffmpeg** для конвертации
* **MiniMax TTS** выводит MP3 и требует **ffmpeg** для конвертации в голосовые сообщения Telegram
* **Google Gemini TTS** выводит сырой PCM и использует **ffmpeg** для прямой кодировки в Opus для голосовых сообщений Telegram
* **xAI TTS** выводит MP3 и требует **ffmpeg** для конвертации в голосовые сообщения Telegram
* **NeuTTS** выводит WAV и также требует **ffmpeg** для конвертации в голосовые сообщения Telegram
* **KittenTTS** выводит WAV и также требует **ffmpeg** для конвертации в голосовые сообщения Telegram
* **Piper** выводит WAV и также требует **ffmpeg** для конвертации в голосовые сообщения Telegram

```bash
# Ubuntu/Debian
sudo apt install ffmpeg
  
# macOS
brew install ffmpeg
  
# Fedora
sudo dnf install ffmpeg
```

Без ffmpeg аудио от Edge TTS, MiniMax TTS, NeuTTS, KittenTTS и Piper отправляется как обычные аудиофайлы (воспроизводятся, но отображаются как прямоугольный плеер вместо голосового сообщения).

> **Совет**
> Если вы хотите голосовые сообщения без установки ffmpeg, переключитесь на провайдера OpenAI, ElevenLabs или Mistral.

### Пользовательские голоса xAI (клонирование голоса)[​](#xai-custom-voices-voice-cloning "Прямая ссылка на Пользовательские голоса xAI (клонирование голоса)")

xAI поддерживает клонирование вашего голоса и его использование в TTS. Создайте пользовательский голос в [консоли xAI](https://console.x.ai/team/default/voice/voice-library), затем укажите полученный `voice_id` в вашей конфигурации:

```yaml
tts:
  provider: xai
  xai:
    voice_id: "nlbqfwie"   # ваш пользовательский ID голоса
```

Подробнее о записи, поддерживаемых форматах и ограничениях см. в [документации xAI Custom Voices](https://docs.x.ai/developers/model-capabilities/audio/custom-voices).

### Piper (локально, 44 языка)[​](#piper-local-44-languages "Прямая ссылка на Piper (локально, 44 языка)")

Piper — это быстрый локальный нейросетевой TTS-движок от Open Home Foundation (сопровождающие Home Assistant). Он работает полностью на CPU, поддерживает **44 языка** с предварительно обученными голосами и не требует API-ключа.

**Установка через `hermes tools`** → Voice & TTS → Piper — Hermes сам выполняет `pip install piper-tts`. Или установите вручную: `pip install piper-tts`.

**Переключение на Piper:**

```yaml
tts:
  provider: piper
  piper:
    voice: en_US-lessac-medium
```

При первом TTS-запросе для голоса, отсутствующего в локальном кеше, Hermes выполняет `python -m piper.download_voices <name>` и загружает модель (~20-90MB в зависимости от качества) в `~/.hermes/cache/piper-voices/`. Последующие запросы используют кешированную модель.

**Выбор голоса.** [Полный каталог голосов](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md) охватывает английский, испанский, французский, немецкий, итальянский, нидерландский, португальский, русский, польский, турецкий, китайский, арабский, хинди и другие — каждый с уровнями качества `x_low` / `low` / `medium` / `high`. Примеры голосов: [rhasspy.github.io/piper-samples](https://rhasspy.github.io/piper-samples/).

**Использование предварительно загруженного голоса.** Установите `tts.piper.voice` как абсолютный путь, заканчивающийся на `.onnx`:

```yaml
tts:
  piper:
    voice: /path/to/my-custom-voice.onnx
```

**Расширенные настройки** (`tts.piper.length_scale` / `noise_scale` / `noise_w_scale` / `volume` / `normalize_audio`, `use_cuda`) соответствуют 1:1 `SynthesisConfig` Piper. Они игнорируются на старых версиях `piper-tts`.

### Пользовательские провайдеры команд[​](#custom-command-providers "Прямая ссылка на Пользовательские провайдеры команд")

Если нужный вам TTS-движок не поддерживается нативно (VoxCPM, MLX-Kokoro, XTTS CLI, скрипт клонирования голоса или любой другой, предоставляющий CLI), вы можете подключить его как **провайдера командного типа** без написания Python-кода. Hermes записывает входной текст во временный UTF-8 файл, выполняет вашу shell-команду и читает аудиофайл, созданный командой.

Объявите одного или несколько провайдеров в `tts.providers.<name>` и переключайтесь между ними с помощью `tts.provider: <name>` — так же, как вы переключаетесь между встроенными провайдерами вроде `edge` и `openai`.

```yaml
tts:
  provider: voxcpm                 # выберите любое имя в разделе tts.providers
  providers:
    voxcpm:
      type: command
      command: "voxcpm --ref ~/voice.wav --text-file {input_path} --out {output_path}"
      output_format: mp3
      timeout: 180
      voice_compatible: true       # попытаться доставить как голосовое сообщение Telegram
  
    mlx-kokoro:
      type: command
      command: "python -m mlx_kokoro --in {input_path} --out {output_path} --voice {voice}"
      voice: af_sky
      output_format: wav
  
    piper-custom:                  # встроенный Piper также поддерживает собственные .onnx через tts.piper.voice
      type: command
      command: "piper -m /path/to/custom.onnx -f {output_path} < {input_path}"
      output_format: wav
```

#### Пример: Doubao (китайский seed-tts-2.0)[​](#example-doubao-chinese-seed-tts-20 "Прямая ссылка на Пример: Doubao (китайский seed-tts-2.0)")

Для высококачественного китайского TTS через [seed-tts-2.0](https://www.volcengine.com/docs/6561/1257544) от ByteDance с двунаправленным потоковым API, установите пакет [`doubao-speech`](https://pypi.org/project/doubao-speech/) и подключите его как командного провайдера:

```bash
pip install doubao-speech
export VOLCENGINE_APP_ID="your-app-id"
export VOLCENGINE_ACCESS_TOKEN="your-access-token"
```

```yaml
tts:
  provider: doubao
  providers:
    doubao:
      type: command
      command: "doubao-speech say --text-file {input_path} --out {output_path}"
      output_format: mp3
      max_text_length: 1024
      timeout: 30
```

Учётные данные берутся из вашего shell-окружения (`VOLCENGINE_APP_ID` / `VOLCENGINE_ACCESS_TOKEN`) или из `~/.doubao-speech/config.yaml`. Выберите голос, добавив `--voice zh-female-warm` (или любой другой псевдоним из `doubao-speech list-voices`) в команду. `doubao-speech` также включает потоковое ASR — см. [раздел STT ниже](#example-doubao--volcengine-asr) для интеграции с Hermes. Исходный код и полная документация: [github.com/Hypnus-Yuan/doubao-speech](https://github.com/Hypnus-Yuan/doubao-speech).

#### Плейсхолдеры[​](#placeholders "Прямая ссылка на Плейсхолдеры")

Ваш шаблон команды может ссылаться на следующие плейсхолдеры. Hermes подставляет их во время выполнения и экранирует shell-кавычками для соответствующего контекста (голый / одинарные кавычки / двойные кавычки), так что пути с пробелами и другими чувствительными для shell символами остаются в безопасности.

| Плейсхолдер | Значение |
|---|---|
| `{input_path}` | Путь к временному UTF-8 текстовому файлу, созданному Hermes |
| `{text_path}` | Псевдоним для `{input_path}` |
| `{output_path}` | Путь, куда команда должна записать аудио |
| `{format}` | `mp3` / `wav` / `ogg` / `flac` |
| `{voice}` | `tts.providers.<name>.voice`, пусто, если не задано |
| `{model}` | `tts.providers.<name>.model` |
| `{speed}` | Разрешённый множитель скорости (провайдера или глобальный) |

Используйте `{{` и `}}` для литеральных фигурных скобок.

#### Опциональные ключи[​](#optional-keys "Прямая ссылка на Опциональные ключи")

| Ключ | По умолчанию | Значение |
|---|---|---|
| `timeout` | `120` | Секунды; дерево процессов уничтожается по истечении (Unix `killpg`, Windows `taskkill /T`). |
| `output_format` | `mp3` | Один из `mp3` / `wav` / `ogg` / `flac`. Автоопределяется по расширению выходного файла, если Hermes выбирает путь. |
| `voice_compatible` | `false` | Если `true`, Hermes конвертирует MP3/WAV в Opus/OGG через ffmpeg, чтобы Telegram отображал голосовое сообщение. |
| `max_text_length` | `5000` | Входной текст усекается до этой длины перед выполнением команды. |
| `voice` / `model` | пусто | Передаются в команду только как значения плейсхолдеров. |

#### Замечания по поведению[​](#behavior-notes "Прямая ссылка на Замечания по поведению")

* **Встроенные имена всегда имеют приоритет.** Запись `tts.providers.openai` никогда не переопределяет встроенный провайдер OpenAI, поэтому никакая пользовательская конфигурация не может незаметно заменить встроенный.
* **Доставка по умолчанию — документ.** Командные провайдеры доставляют аудио как обычные вложения на всех платформах. Опционально включите доставку в виде голосового сообщения для каждого провайдера с помощью `voice_compatible: true`.
* **Сбои команд отображаются агенту.** Ненулевой код возврата, пустой вывод или тайм-аут возвращают ошибку с stderr/stdout команды, чтобы вы могли отладить провайдера прямо из диалога.
* **`type: command` является значением по умолчанию, если указан `command:`.** Явное указание `type: command` — хорошая практика, но не обязательна; запись с непустой строкой `command` рассматривается как командный провайдер.
* **`{input_path}` / `{text_path}` взаимозаменяемы.** Используйте тот, который лучше читается в вашей команде.

#### Безопасность[​](#security "Прямая ссылка на Безопасность")

Командные провайдеры выполняют любую shell-команду, которую вы настроили, с правами вашего пользователя. Hermes экранирует значения плейсхолдеров и соблюдает настроенный тайм-аут, но сам шаблон команды является доверенным локальным вводом — относитесь к нему так же, как к shell-скрипту на вашем PATH.

## Транскрипция голосовых сообщений (STT)[​](#voice-message-transcription-stt "Прямая ссылка на Транскрипция голосовых сообщений (STT)")

Голосовые сообщения, отправленные в Telegram, Discord, WhatsApp, Slack или Signal, автоматически транскрибируются и вставляются в виде текста в диалог. Агент видит транскрипт как обычный текст.

| Провайдер | Качество | Стоимость | API-ключ |
|---|---|---|---|
| **Локальный Whisper** (по умолчанию) | Хорошее | Бесплатно | Не требуется |
| **Groq Whisper API** | Хорошее–Лучшее | Бесплатный лимит | `GROQ_API_KEY` |
| **OpenAI Whisper API** | Хорошее–Лучшее | Платно | `VOICE_TOOLS_OPENAI_KEY` или `OPENAI_API_KEY` |

Нулевая конфигурация

Локальная транскрипция работает «из коробки», если установлен `faster-whisper`. Если он недоступен, Hermes также может использовать локальный CLI `whisper` из стандартных мест установки (например, `/opt/homebrew/bin`) или пользовательскую команду через `HERMES_LOCAL_STT_COMMAND`.

### Конфигурация[​](#configuration-1 "Прямая ссылка на Конфигурация")

```yaml
# В ~/.hermes/config.yaml
stt:
  provider: "local"           # "local" | "groq" | "openai" | "mistral" | "xai"
  local:
    model: "base"             # tiny, base, small, medium, large-v3
  openai:
    model: "whisper-1"        # whisper-1, gpt-4o-mini-transcribe, gpt-4o-transcribe
  mistral:
    model: "voxtral-mini-latest"  # voxtral-mini-latest, voxtral-mini-2602
  xai:
    model: "grok-stt"         # xAI Grok STT
```

### Детали провайдеров[​](#provider-details "Прямая ссылка на Детали провайдеров")

**Локальный (faster-whisper)** — Запускает Whisper локально через [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Использует CPU по умолчанию, GPU — при наличии. Размеры моделей:

| Модель | Размер | Скорость | Качество |
|---|---|---|---|
| `tiny` | ~75 MB | Наивысшая | Базовое |
| `base` | ~150 MB | Высокая | Хорошее (по умолч.) |
| `small` | ~500 MB | Средняя | Лучше |
| `medium` | ~1.5 GB | Низкая | Отличное |
| `large-v3` | ~3 GB | Наинизшая | Наилучшее |

**Groq API** — Требует `GROQ_API_KEY`. Хорошее облачное решение, когда нужен бесплатный хостинг для STT.

**OpenAI API** — Сначала проверяет `VOICE_TOOLS_OPENAI_KEY`, затем `OPENAI_API_KEY` как запасной вариант. Поддерживает `whisper-1`, `gpt-4o-mini-transcribe` и `gpt-4o-transcribe`.

**Mistral API (Voxtral Transcribe)** — Требует `MISTRAL_API_KEY`. Использует модели [Voxtral Transcribe](https://docs.mistral.ai/capabilities/audio/speech_to_text/) от Mistral. Поддерживает 13 языков, диаризацию дикторов и посекундные временные метки слов. Установка: `pip install hermes-agent[mistral]`.

**xAI Grok STT** — Требует `XAI_API_KEY`. Отправляет POST-запрос на `https://api.x.ai/v1/stt` в формате multipart/form-data. Хороший выбор, если вы уже используете xAI для чата или TTS и хотите один API-ключ для всего. Порядок автоопределения ставит его после Groq — явно укажите `stt.provider: xai`, чтобы принудительно использовать его.

**Пользовательский локальный CLI как запасной вариант** — Установите `HERMES_LOCAL_STT_COMMAND`, если хотите, чтобы Hermes напрямую вызывал локальную команду транскрипции. Шаблон команды поддерживает плейсхолдеры `{input_path}`, `{output_dir}`, `{language}` и `{model}`. Ваша команда должна записать транскрипт в формате `.txt` где-то в `{output_dir}`.

#### Пример: Doubao / Volcengine ASR[​](#example-doubao--volcengine-asr "Прямая ссылка на Пример: Doubao / Volcengine ASR")

Если вы используете [`doubao-speech`](https://pypi.org/project/doubao-speech/) для Doubao TTS (см. [выше](#example-doubao-chinese-seed-tts-20)), тот же пакет обрабатывает распознавание речи через поверхность локальных команд STT:

```bash
pip install doubao-speech
export VOLCENGINE_APP_ID="your-app-id"
export VOLCENGINE_ACCESS_TOKEN="your-access-token"
export HERMES_LOCAL_STT_COMMAND='doubao-speech transcribe {input_path} --out {output_dir}/transcript.txt'
```

```yaml
stt:
  provider: local_command
```

Hermes записывает входящее голосовое сообщение в `{input_path}`, выполняет команду и читает файл `.txt`, созданный в `{output_dir}`. Язык определяется автоматически через endpoint Volcengine bigmodel.

### Поведение при откате[​](#fallback-behavior "Прямая ссылка на Поведение при откате")

Если настроенный провайдер недоступен, Hermes автоматически выбирает запасной вариант:

* **Локальный faster-whisper недоступен** → Пытается использовать локальный CLI `whisper` или `HERMES_LOCAL_STT_COMMAND` перед облачными провайдерами
* **Ключ Groq не установлен** → Откат к локальной транскрипции, затем OpenAI
* **Ключ OpenAI не установлен** → Откат к локальной транскрипции, затем Groq
* **Ключ/SDK Mistral не установлен** → Пропускается при автоопределении; переходит к следующему доступному провайдеру
* **Ничего не доступно** → Голосовые сообщения передаются с точным уведомлением пользователю

* [Преобразование текста в речь (Text-to-Speech)](#text-to-speech)
  * [Доставка на платформы](#platform-delivery)
  * [Конфигурация](#configuration)
  * [Ограничения длины входного текста](#input-length-limits)
  * [Голосовые сообщения Telegram и ffmpeg](#telegram-voice-bubbles--ffmpeg)
  * [Пользовательские голоса xAI (клонирование голоса)](#xai-custom-voices-voice-cloning)
  * [Piper (локально, 44 языка)](#piper-local-44-languages)
  * [Пользовательские провайдеры команд](#custom-command-providers)
* [Транскрипция голосовых сообщений (STT)](#voice-message-transcription-stt)
  * [Конфигурация](#configuration-1)
  * [Детали провайдеров](#provider-details)
  * [Поведение при откате](#fallback-behavior)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/tts -->
