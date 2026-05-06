On this page
AudioCraft: MusicGen преобразование текста в музыку, AudioGen преобразование текста в звук.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Встроенный (установлен по умолчанию)  |
|Путь| `skills/mlops/models/audiocraft`  |
|Версия| `1.0.0`  |
|Автор| Orchestra Research  |
|Лицензия| MIT  |
|Зависимости| `audiocraft`, `torch>=2.0.0`, `transformers>=4.30.0`  |
|Теги| `Multimodal`, `Audio Generation`, `Text-to-Music`, `Text-to-Audio`, `MusicGen`  |
|## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# AudioCraft: Генерация аудио
Исчерпывающее руководство по использованию AudioCraft от Meta для генерации музыки и звука из текста с помощью MusicGen, AudioGen и EnCodec.
## Когда использовать AudioCraft[​](<#when-to-use-audiocraft> "Прямая ссылка на Когда использовать AudioCraft")
**Используйте AudioCraft, когда:**
  * Нужно сгенерировать музыку из текстовых описаний
  * Создаются звуковые эффекты и окружающий аудиоконтент
  * Строятся приложения для генерации музыки
  * Нужна генерация музыки с conditioned мелодией
  * Требуется стерео-аудио на выходе
  * Необходима управляемая генерация музыки с переносом стиля


**Ключевые возможности:**
  * **MusicGen** : Преобразование текста в музыку с conditioned мелодией
  * **AudioGen** : Генерация звуковых эффектов из текста
  * **EnCodec** : Высококачественный нейронный аудиокодек
  * **Несколько размеров моделей** : от Small (300M) до Large (3.3B)
  * **Поддержка стерео** : Полноценная генерация стерео-аудио
  * **Управление стилем** : MusicGen-Style для генерации по образцу


**Альтернативы:**
  * **Stable Audio** : Для генерации более длинной коммерческой музыки
  * **Bark** : Для синтеза речи с музыкой и звуковыми эффектами
  * **Riffusion** : Для генерации музыки на основе спектрограмм
  * **OpenAI Jukebox** : Для генерации звука с текстом песен


## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")
### Установка[​](<#installation> "Прямая ссылка на Установка")
[code] 
    # Из PyPI  
    pip install audiocraft  
      
    # Из GitHub (последняя версия)  
    pip install git+https://github.com/facebookresearch/audiocraft.git  
      
    # Или используйте HuggingFace Transformers  
    pip install transformers torch torchaudio  
    
[/code]
### Базовое преобразование текста в музыку (AudioCraft)[​](<#basic-text-to-music-audiocraft> "Прямая ссылка на Базовое преобразование текста в музыку \\(AudioCraft\\)")
[code] 
    import torchaudio  
    from audiocraft.models import MusicGen  
      
    # Загрузка модели  
    model = MusicGen.get_pretrained('facebook/musicgen-small')  
      
    # Настройка параметров генерации  
    model.set_generation_params(  
        duration=8,  # секунды  
        top_k=250,  
        temperature=1.0  
    )  
      
    # Генерация из текста  
    descriptions = ["happy upbeat electronic dance music with synths"]  
    wav = model.generate(descriptions)  
      
    # Сохранение аудио  
    torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)  
    
[/code]
### Использование HuggingFace Transformers[​](<#using-huggingface-transformers> "Прямая ссылка на Использование HuggingFace Transformers")
[code] 
    from transformers import AutoProcessor, MusicgenForConditionalGeneration  
    import scipy  
      
    # Загрузка модели и процессора  
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")  
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")  
    model.to("cuda")  
      
    # Генерация музыки  
    inputs = processor(  
        text=["80s pop track with bassy drums and synth"],  
        padding=True,  
        return_tensors="pt"  
    ).to("cuda")  
      
    audio_values = model.generate(  
        **inputs,  
        do_sample=True,  
        guidance_scale=3,  
        max_new_tokens=256  
    )  
      
    # Сохранение  
    sampling_rate = model.config.audio_encoder.sampling_rate  
    scipy.io.wavfile.write("output.wav", rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())  
    
[/code]
### Преобразование текста в звук с AudioGen[​](<#text-to-sound-with-audiogen> "Прямая ссылка на Преобразование текста в звук с AudioGen")
[code] 
    from audiocraft.models import AudioGen  
      
    # Загрузка AudioGen  
    model = AudioGen.get_pretrained('facebook/audiogen-medium')  
      
    model.set_generation_params(duration=5)  
      
    # Генерация звуковых эффектов  
    descriptions = ["dog barking in a park with birds chirping"]  
    wav = model.generate(descriptions)  
      
    torchaudio.save("sound.wav", wav[0].cpu(), sample_rate=16000)  
    
[/code]
## Основные концепции[​](<#core-concepts> "Прямая ссылка на Основные концепции")
### Обзор архитектуры[​](<#architecture-overview> "Прямая ссылка на Обзор архитектуры")
[code] 
    AudioCraft Architecture:  
    ┌──────────────────────────────────────────────────────────────┐  
    │                    Text Encoder (T5)                          │  
    │                         │                                     │  
    │                    Text Embeddings                            │  
    └────────────────────────┬─────────────────────────────────────┘  
                             │  
    ┌────────────────────────▼─────────────────────────────────────┐  
    │              Transformer Decoder (LM)                         │  
    │     Auto-regressively generates audio tokens                  │  
    │     Using efficient token interleaving patterns               │  
    └────────────────────────┬─────────────────────────────────────┘  
                             │  
    ┌────────────────────────▼─────────────────────────────────────┐  
    │                EnCodec Audio Decoder                          │  
    │        Converts tokens back to audio waveform                 │  
    └──────────────────────────────────────────────────────────────┘  
    
[/code]
### Варианты моделей[​](<#model-variants> "Прямая ссылка на Варианты моделей")
Модель| Размер| Описание| Применение  
|---|---|---|---  
`musicgen-small`| 300M| Текст в музыку| Быстрая генерация  
`musicgen-medium`| 1.5B| Текст в музыку| Сбалансированный вариант  
`musicgen-large`| 3.3B| Текст в музыку| Наилучшее качество  
`musicgen-melody`| 1.5B| Текст + мелодия| Учет мелодии  
`musicgen-melody-large`| 3.3B| Текст + мелодия| Лучшая работа с мелодией  
`musicgen-stereo-*`| Разный| Стерео-выход| Стерео-генерация  
`musicgen-style`| 1.5B| Перенос стиля| Генерация по образцу  
`audiogen-medium`| 1.5B| Текст в звук| Звуковые эффекты  
### Параметры генерации[​](<#generation-parameters> "Прямая ссылка на Параметры генерации")
Параметр| По умолчанию| Описание  
|---|---|---  
`duration`| 8.0| Длительность в секундах (1-120)  
`top_k`| 250| Top-k сэмплирование  
`top_p`| 0.0| Nucleus сэмплирование (0 = отключено)  
`temperature`| 1.0| Температура сэмплирования  
`cfg_coef`| 3.0| Classifier-free guidance (бесклассовое направление)  
## Использование MusicGen[​](<#musicgen-usage> "Прямая ссылка на Использование MusicGen")
### Генерация музыки из текста[​](<#text-to-music-generation> "Прямая ссылка на Генерация музыки из текста")
[code] 
    from audiocraft.models import MusicGen  
    import torchaudio  
      
    model = MusicGen.get_pretrained('facebook/musicgen-medium')  
      
    # Настройка генерации  
    model.set_generation_params(  
        duration=30,          # До 30 секунд  
        top_k=250,            # Разнообразие сэмплирования  
        top_p=0.0,            # 0 = использовать только top_k  
        temperature=1.0,      # Креативность (выше = разнообразнее)  
        cfg_coef=3.0          # Приверженность тексту (выше = строже)  
    )  
      
    # Генерация нескольких образцов  
    descriptions = [  
        "epic orchestral soundtrack with strings and brass",  
        "chill lo-fi hip hop beat with jazzy piano",  
        "energetic rock song with electric guitar"  
    ]  
      
    # Генерация (возвращает [batch, channels, samples])  
    wav = model.generate(descriptions)  
      
    # Сохранение каждого  
    for i, audio in enumerate(wav):  
        torchaudio.save(f"music_{i}.wav", audio.cpu(), sample_rate=32000)  
    
[/code]
### Генерация с conditioned мелодией[​](<#melody-conditioned-generation> "Прямая ссылка на Генерация с conditioned мелодией")
[code] 
    from audiocraft.models import MusicGen  
    import torchaudio  
      
    # Загрузка модели с мелодией  
    model = MusicGen.get_pretrained('facebook/musicgen-melody')  
    model.set_generation_params(duration=30)  
      
    # Загрузка мелодии  
    melody, sr = torchaudio.load("melody.wav")  
      
    # Генерация с учетом мелодии  
    descriptions = ["acoustic guitar folk song"]  
    wav = model.generate_with_chroma(descriptions, melody, sr)  
      
    torchaudio.save("melody_conditioned.wav", wav[0].cpu(), sample_rate=32000)  
    
[/code]
### Стерео-генерация[​](<#stereo-generation> "Прямая ссылка на Стерео-генерация")
[code] 
    from audiocraft.models import MusicGen  
      
    # Загрузка стерео-модели  
    model = MusicGen.get_pretrained('facebook/musicgen-stereo-medium')  
    model.set_generation_params(duration=15)  
      
    descriptions = ["ambient electronic music with wide stereo panning"]  
    wav = model.generate(descriptions)  
      
    # wav shape: [batch, 2, samples] для стерео  
    print(f"Stereo shape: {wav.shape}")  # [1, 2, 480000]  
    torchaudio.save("stereo.wav", wav[0].cpu(), sample_rate=32000)  
    
[/code]
### Продолжение аудио[​](<#audio-continuation> "Прямая ссылка на Продолжение аудио")
[code] 
    from transformers import AutoProcessor, MusicgenForConditionalGeneration  
      
    processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")  
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")  
      
    # Загрузка аудио для продолжения  
    import torchaudio  
    audio, sr = torchaudio.load("intro.wav")  
      
    # Обработка с текстом и аудио  
    inputs = processor(  
        audio=audio.squeeze().numpy(),  
        sampling_rate=sr,  
        text=["continue with a epic chorus"],  
        padding=True,  
        return_tensors="pt"  
    )  
      
    # Генерация продолжения  
    audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=512)  
    
[/code]
## Использование MusicGen-Style[​](<#musicgen-style-usage> "Прямая ссылка на Использование MusicGen-Style")
### Генерация с conditioned стилем[​](<#style-conditioned-generation> "Прямая ссылка на Генерация с conditioned стилем")
[code] 
    from audiocraft.models import MusicGen  
      
    # Загрузка модели стиля  
    model = MusicGen.get_pretrained('facebook/musicgen-style')  
      
    # Настройка генерации со стилем  
    model.set_generation_params(  
        duration=30,  
        cfg_coef=3.0,  
        cfg_coef_beta=5.0  # Влияние стиля  
    )  
      
    # Настройка параметров стиля  
    model.set_style_conditioner_params(  
        eval_q=3,          # RVQ квантователи (1-6)  
        excerpt_length=3.0  # Длина фрагмента стиля  
    )  
      
    # Загрузка референса стиля  
    style_audio, sr = torchaudio.load("reference_style.wav")  
      
    # Генерация с текстом + стилем  
    descriptions = ["upbeat dance track"]  
    wav = model.generate_with_style(descriptions, style_audio, sr)  
    
[/code]
### Генерация только по стилю (без текста)[​](<#style-only-generation-no-text> "Прямая ссылка на Генерация только по стилю \\(без текста\\)")
[code] 
    # Генерация, соответствующая стилю, без текстового запроса  
    model.set_generation_params(  
        duration=30,  
        cfg_coef=3.0,  
        cfg_coef_beta=None  # Отключение двойного CFG для режима только стиля  
    )  
      
    wav = model.generate_with_style([None], style_audio, sr)  
    
[/code]
## Использование AudioGen[​](<#audiogen-usage> "Прямая ссылка на Использование AudioGen")
### Генерация звуковых эффектов[​](<#sound-effect-generation> "Прямая ссылка на Генерация звуковых эффектов")
[code] 
    from audiocraft.models import AudioGen  
    import torchaudio  
      
    model = AudioGen.get_pretrained('facebook/audiogen-medium')  
    model.set_generation_params(duration=10)  
      
    # Генерация различных звуков  
    descriptions = [  
        "thunderstorm with heavy rain and lightning",  
        "busy city traffic with car horns",  
        "ocean waves crashing on rocks",  
        "crackling campfire in forest"  
    ]  
      
    wav = model.generate(descriptions)  
      
    for i, audio in enumerate(wav):  
        torchaudio.save(f"sound_{i}.wav", audio.cpu(), sample_rate=16000)  
    
[/code]
## Использование EnCodec[​](<#encodec-usage> "Прямая ссылка на Использование EnCodec")
### Сжатие аудио[​](<#audio-compression> "Прямая ссылка на Сжатие аудио")
[code] 
    from audiocraft.models import CompressionModel  
    import torch  
    import torchaudio  
      
    # Загрузка EnCodec  
    model = CompressionModel.get_pretrained('facebook/encodec_32khz')  
      
    # Загрузка аудио  
    wav, sr = torchaudio.load("audio.wav")  
      
    # Проверка частоты дискретизации  
    if sr != 32000:  
        resampler = torchaudio.transforms.Resample(sr, 32000)  
        wav = resampler(wav)  
      
    # Кодирование в токены  
    with torch.no_grad():  
        encoded = model.encode(wav.unsqueeze(0))  
        codes = encoded[0]  # Аудио-коды  
      
    # Декодирование обратно в аудио  
    with torch.no_grad():  
        decoded = model.decode(codes)  
      
    torchaudio.save("reconstructed.wav", decoded[0].cpu(), sample_rate=32000)  
    
[/code]
## Типовые рабочие процессы[​](<#common-workflows> "Прямая ссылка на Типовые рабочие процессы")
### Рабочий процесс 1: Конвейер генерации музыки[​](<#workflow-1-music-generation-pipeline> "Прямая ссылка на Рабочий процесс 1: Конвейер генерации музыки")
[code] 
    import torch  
    import torchaudio  
    from audiocraft.models import MusicGen  
      
    class MusicGenerator:  
        def __init__(self, model_name="facebook/musicgen-medium"):  
            self.model = MusicGen.get_pretrained(model_name)  
            self.sample_rate = 32000  
      
        def generate(self, prompt, duration=30, temperature=1.0, cfg=3.0):  
            self.model.set_generation_params(  
                duration=duration,  
                top_k=250,  
                temperature=temperature,  
                cfg_coef=cfg  
            )  
      
            with torch.no_grad():  
                wav = self.model.generate([prompt])  
      
            return wav[0].cpu()  
      
        def generate_batch(self, prompts, duration=30):  
            self.model.set_generation_params(duration=duration)  
      
            with torch.no_grad():  
                wav = self.model.generate(prompts)  
      
            return wav.cpu()  
      
        def save(self, audio, path):  
            torchaudio.save(path, audio, sample_rate=self.sample_rate)  
      
    # Использование  
    generator = MusicGenerator()  
    audio = generator.generate(  
        "epic cinematic orchestral music",  
        duration=30,  
        temperature=1.0  
    )  
    generator.save(audio, "epic_music.wav")  
    
[/code]
### Рабочий процесс 2: Пакетная обработка звукового дизайна[​](<#workflow-2-sound-design-batch-processing> "Прямая ссылка на Рабочий процесс 2: Пакетная обработка звукового дизайна")
[code] 
    import json  
    from pathlib import Path  
    from audiocraft.models import AudioGen  
    import torchaudio  
      
    def batch_generate_sounds(sound_specs, output_dir):  
        """  
        Генерация нескольких звуков по спецификациям.  
      
        Args:  
            sound_specs: список {"name": str, "description": str, "duration": float}  
            output_dir: путь к выходной директории  
        """  
        model = AudioGen.get_pretrained('facebook/audiogen-medium')  
        output_dir = Path(output_dir)  
        output_dir.mkdir(exist_ok=True)  
      
        results = []  
      
        for spec in sound_specs:  
            model.set_generation_params(duration=spec.get("duration", 5))  
      
            wav = model.generate([spec["description"]])  
      
            output_path = output_dir / f"{spec['name']}.wav"  
            torchaudio.save(str(output_path), wav[0].cpu(), sample_rate=16000)  
      
            results.append({  
                "name": spec["name"],  
                "path": str(output_path),  
                "description": spec["description"]  
            })  
      
        return results  
      
    # Использование  
    sounds = [  
        {"name": "explosion", "description": "massive explosion with debris", "duration": 3},  
        {"name": "footsteps", "description": "footsteps on wooden floor", "duration": 5},  
        {"name": "door", "description": "wooden door creaking and closing", "duration": 2}  
    ]  
      
    results = batch_generate_sounds(sounds, "sound_effects/")  
    
[/code]
### Рабочий процесс 3: Демо в Gradio[​](<#workflow-3-gradio-demo> "Прямая ссылка на Рабочий процесс 3: Демо в Gradio")
[code] 
    import gradio as gr  
    import torch  
    import torchaudio  
    from audiocraft.models import MusicGen  
      
    model = MusicGen.get_pretrained('facebook/musicgen-small')  
      
    def generate_music(prompt, duration, temperature, cfg_coef):  
        model.set_generation_params(  
            duration=duration,  
            temperature=temperature,  
            cfg_coef=cfg_coef  
        )  
      
        with torch.no_grad():  
            wav = model.generate([prompt])  
      
        # Сохранение во временный файл  
        path = "temp_output.wav"  
        torchaudio.save(path, wav[0].cpu(), sample_rate=32000)  
        return path  
      
    demo = gr.Interface(  
        fn=generate_music,  
        inputs=[  
            gr.Textbox(label="Описание музыки", placeholder="upbeat electronic dance music"),  
            gr.Slider(1, 30, value=8, label="Длительность (секунды)"),  
            gr.Slider(0.5, 2.0, value=1.0, label="Температура"),  
            gr.Slider(1.0, 10.0, value=3.0, label="Коэффициент CFG")  
        ],  
        outputs=gr.Audio(label="Сгенерированная музыка"),  
        title="MusicGen Demo"  
    )  
      
    demo.launch()  
    
[/code]
## Оптимизация производительности[​](<#performance-optimization> "Прямая ссылка на Оптимизация производительности")
### Оптимизация памяти[​](<#memory-optimization> "Прямая ссылка на Оптимизация памяти")
[code] 
    # Используйте меньшую модель  
    model = MusicGen.get_pretrained('facebook/musicgen-small')  
      
    # Очищайте кэш между генерациями  
    torch.cuda.empty_cache()  
      
    # Генерируйте более короткие длительности  
    model.set_generation_params(duration=10)  # Вместо 30  
      
    # Используйте половинную точность  
    model = model.half()  
    
[/code]
### Эффективность пакетной обработки[​](<#batch-processing-efficiency> "Прямая ссылка на Эффективность пакетной обработки")
[code] 
    # Обработка нескольких запросов за раз (более эффективно)  
    descriptions = ["prompt1", "prompt2", "prompt3", "prompt4"]  
    wav = model.generate(descriptions)  # Единый пакет  
      
    # Вместо  
    for desc in descriptions:  
        wav = model.generate([desc])  # Множественные пакеты (медленнее)  
    
[/code]
### Требования к видеопамяти GPU[​](<#gpu-memory-requirements> "Прямая ссылка на Требования к видеопамяти GPU")
Модель| FP32 VRAM| FP16 VRAM  
|---|---|---  
musicgen-small| ~4 ГБ| ~2 ГБ  
musicgen-medium| ~8 ГБ| ~4 ГБ  
musicgen-large| ~16 ГБ| ~8 ГБ  
## Часто встречающиеся проблемы[​](<#common-issues> "Прямая ссылка на Часто встречающиеся проблемы")
Проблема| Решение  
|---|---  
CUDA OOM| Используйте меньшую модель, уменьшите длительность  
Низкое качество| Увеличьте cfg_coef, улучшите промпты  
Генерация слишком короткая| Проверьте максимальную длительность  
Артефакты аудио| Попробуйте другую температуру  
Стерео не работает| Используйте стерео-вариант модели  
## Ссылки[​](<#references> "Прямая ссылка на Ссылки")
  * **[Расширенное использование](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/models/audiocraft/references/advanced-usage.md>)** \\- Обучение, дообучение, развертывание
  * **[Устранение неполадок](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/models/audiocraft/references/troubleshooting.md>)** \\- Частые проблемы и решения


## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")
  * **GitHub** : <https://github.com/facebookresearch/audiocraft>
  * **Статья (MusicGen)** : <https://arxiv.org/abs/2306.05284>
  * **Статья (AudioGen)** : <https://arxiv.org/abs/2209.15352>
  * **HuggingFace** : <https://huggingface.co/facebook/musicgen-small>
  * **Демо** : <https://huggingface.co/spaces/facebook/MusicGen>


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать AudioCraft](<#when-to-use-audiocraft>)
  * [Быстрый старт](<#quick-start>)
    * [Установка](<#installation>)
    * [Базовое преобразование текста в музыку (AudioCraft)](<#basic-text-to-music-audiocraft>)
    * [Использование HuggingFace Transformers](<#using-huggingface-transformers>)
    * [Преобразование текста в звук с AudioGen](<#text-to-sound-with-audiogen>)
  * [Основные концепции](<#core-concepts>)
    * [Обзор архитектуры](<#architecture-overview>)
    * [Варианты моделей](<#model-variants>)
    * [Параметры генерации](<#generation-parameters>)
  * [Использование MusicGen](<#musicgen-usage>)
    * [Генерация музыки из текста](<#text-to-music-generation>)
    * [Генерация с conditioned мелодией](<#melody-conditioned-generation>)
    * [Стерео-генерация](<#stereo-generation>)
    * [Продолжение аудио](<#audio-continuation>)
  * [Использование MusicGen-Style](<#musicgen-style-usage>)
    * [Генерация с conditioned стилем](<#style-conditioned-generation>)
    * [Генерация только по стилю (без текста)](<#style-only-generation-no-text>)
  * [Использование AudioGen](<#audiogen-usage>)
    * [Генерация звуковых эффектов](<#sound-effect-generation>)
  * [Использование EnCodec](<#encodec-usage>)
    * [Сжатие аудио](<#audio-compression>)
  * [Типовые рабочие процессы](<#common-workflows>)
    * [Рабочий процесс 1: Конвейер генерации музыки](<#workflow-1-music-generation-pipeline>)
    * [Рабочий процесс 2: Пакетная обработка звукового дизайна](<#workflow-2-sound-design-batch-processing>)
    * [Рабочий процесс 3: Демо в Gradio](<#workflow-3-gradio-demo>)
  * [Оптимизация производительности](<#performance-optimization>)
    * [Оптимизация памяти](<#memory-optimization>)
    * [Эффективность пакетной обработки](<#batch-processing-efficiency>)
    * [Требования к видеопамяти GPU](<#gpu-memory-requirements>)
  * [Часто встречающиеся проблемы](<#common-issues>)
  * [Ссылки](<#references>)
  * [Ресурсы](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-models-audiocraft -->
