На этой странице

Large Language and Vision Assistant (LLaVA). Обеспечивает визуальную настройку инструкций и диалоги на основе изображений. Объединяет CLIP-видеокодер с языковыми моделями Vicuna/LLaMA. Поддерживает многопоточный чат с изображениями, визуальные ответы на вопросы и следование инструкциям. Используйте для создания чат-ботов вида «язык+зрение» или задач понимания изображений. Лучше всего подходит для диалогового анализа изображений.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |
|---|
|Source| Опционально — установка: `hermes skills install official/mlops/llava`  |
|Path| `optional-skills/mlops/llava`  |
|Version| `1.0.0`  |
|Author| Orchestra Research  |
|License| MIT  |
|Dependencies| `transformers`, `torch`, `pillow`  |
|Tags| `LLaVA`, `Vision-Language`, `Multimodal`, `Visual Question Answering`, `Image Chat`, `CLIP`, `Vicuna`, `Conversational AI`, `Instruction Tuning`, `VQA`  |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.

# LLaVA — Large Language and Vision Assistant

Модель «зрение-язык» с открытым исходным кодом для диалогового понимания изображений.

## Когда использовать LLaVA[​](<#when-to-use-llava> "Прямая ссылка на Когда использовать LLaVA")

**Используйте когда:**
  * Строите чат-ботов вида «зрение-язык»
  * Нужны визуальные ответы на вопросы (VQA)
  * Требуется описание и подписи к изображениям
  * Ведёте многопоточные диалоги об изображениях
  * Нужно следование визуальным инструкциям
  * Работаете с документами, содержащими изображения


**Показатели:**
  * **23 000+ звёзд на GitHub**
  * Возможности на уровне GPT-4V (целевой показатель)
  * Лицензия Apache 2.0
  * Несколько размеров модели (7B–34B параметров)


**Альтернативы:**
  * **GPT-4V** : Наивысшее качество, на основе API
  * **CLIP** : Простая zero-shot классификация
  * **BLIP-2** : Лучше только для подписей
  * **Flamingo** : Исследовательская, не open-source


## Быстрый старт[​](<#quick-start> "Прямая ссылка на Быстрый старт")

### Установка[​](<#installation> "Прямая ссылка на Установка")

[code] 
    # Clone repository  
    git clone https://github.com/haotian-liu/LLaVA  
    cd LLaVA  
      
    # Install  
    pip install -e .  
    
[/code]

### Базовое использование[​](<#basic-usage> "Прямая ссылка на Базовое использование")

[code] 
    from llava.model.builder import load_pretrained_model  
    from llava.mm_utils import get_model_name_from_path, process_images, tokenizer_image_token  
    from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN  
    from llava.conversation import conv_templates  
    from PIL import Image  
    import torch  
      
    # Load model  
    model_path = "liuhaotian/llava-v1.5-7b"  
    tokenizer, model, image_processor, context_len = load_pretrained_model(  
        model_path=model_path,  
        model_base=None,  
        model_name=get_model_name_from_path(model_path)  
    )  
      
    # Load image  
    image = Image.open("image.jpg")  
    image_tensor = process_images([image], image_processor, model.config)  
    image_tensor = image_tensor.to(model.device, dtype=torch.float16)  
      
    # Create conversation  
    conv = conv_templates["llava_v1"].copy()  
    conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\nWhat is in this image?")  
    conv.append_message(conv.roles[1], None)  
    prompt = conv.get_prompt()  
      
    # Generate response  
    input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(model.device)  
      
    with torch.inference_mode():  
        output_ids = model.generate(  
            input_ids,  
            images=image_tensor,  
            do_sample=True,  
            temperature=0.2,  
            max_new_tokens=512  
        )  
      
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()  
    print(response)  
    
[/code]

## Доступные модели[​](<#available-models> "Прямая ссылка на Доступные модели")

Модель| Параметры| VRAM| Качество  
---|---|---|---|---  
LLaVA-v1.5-7B| 7B| ~14 ГБ| Хорошее  
LLaVA-v1.5-13B| 13B| ~28 ГБ| Лучше  
LLaVA-v1.6-34B| 34B| ~70 ГБ| Наилучшее

[code] 
    # Load different models  
    model_7b = "liuhaotian/llava-v1.5-7b"  
    model_13b = "liuhaotian/llava-v1.5-13b"  
    model_34b = "liuhaotian/llava-v1.6-34b"  
      
    # 4-bit quantization for lower VRAM  
    load_4bit = True  # Reduces VRAM by ~4×  
    
[/code]  

## Использование в CLI[​](<#cli-usage> "Прямая ссылка на Использование в CLI")

[code] 
    # Single image query  
    python -m llava.serve.cli \  
        --model-path liuhaotian/llava-v1.5-7b \  
        --image-file image.jpg \  
        --query "What is in this image?"  
      
    # Multi-turn conversation  
    python -m llava.serve.cli \  
        --model-path liuhaotian/llava-v1.5-7b \  
        --image-file image.jpg  
    # Then type questions interactively  
    
[/code]

## Веб-интерфейс (Gradio)[​](<#web-ui-gradio> "Прямая ссылка на Веб-интерфейс (Gradio)")

[code] 
    # Launch Gradio interface  
    python -m llava.serve.gradio_web_server \  
        --model-path liuhaotian/llava-v1.5-7b \  
        --load-4bit  # Optional: reduce VRAM  
      
    # Access at http://localhost:7860  
    
[/code]

## Многопоточные диалоги[​](<#multi-turn-conversations> "Прямая ссылка на Многопоточные диалоги")

[code] 
    # Initialize conversation  
    conv = conv_templates["llava_v1"].copy()  
      
    # Turn 1  
    conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\nWhat is in this image?")  
    conv.append_message(conv.roles[1], None)  
    response1 = generate(conv, model, image)  # "A dog playing in a park"  
      
    # Turn 2  
    conv.messages[-1][1] = response1  # Add previous response  
    conv.append_message(conv.roles[0], "What breed is the dog?")  
    conv.append_message(conv.roles[1], None)  
    response2 = generate(conv, model, image)  # "Golden Retriever"  
      
    # Turn 3  
    conv.messages[-1][1] = response2  
    conv.append_message(conv.roles[0], "What time of day is it?")  
    conv.append_message(conv.roles[1], None)  
    response3 = generate(conv, model, image)  
    
[/code]

## Типовые задачи[​](<#common-tasks> "Прямая ссылка на Типовые задачи")

### Описание изображений[​](<#image-captioning> "Прямая ссылка на Описание изображений")

[code] 
    question = "Describe this image in detail."  
    response = ask(model, image, question)  
    
[/code]

### Визуальные ответы на вопросы[​](<#visual-question-answering> "Прямая ссылка на Визуальные ответы на вопросы")

[code] 
    question = "How many people are in the image?"  
    response = ask(model, image, question)  
    
[/code]

### Обнаружение объектов (текстовое)[​](<#object-detection-textual> "Прямая ссылка на Обнаружение объектов (текстовое)")

[code] 
    question = "List all the objects you can see in this image."  
    response = ask(model, image, question)  
    
[/code]

### Понимание сцены[​](<#scene-understanding> "Прямая ссылка на Понимание сцены")

[code] 
    question = "What is happening in this scene?"  
    response = ask(model, image, question)  
    
[/code]

### Понимание документов[​](<#document-understanding> "Прямая ссылка на Понимание документов")

[code] 
    question = "What is the main topic of this document?"  
    response = ask(model, document_image, question)  
    
[/code]

## Обучение собственной модели[​](<#training-custom-model> "Прямая ссылка на Обучение собственной модели")

[code] 
    # Stage 1: Feature alignment (558K image-caption pairs)  
    bash scripts/v1_5/pretrain.sh  
      
    # Stage 2: Visual instruction tuning (150K instruction data)  
    bash scripts/v1_5/finetune.sh  
    
[/code]

## Квантование (снижение VRAM)[​](<#quantization-reduce-vram> "Прямая ссылка на Квантование (снижение VRAM)")

[code] 
    # 4-bit quantization  
    tokenizer, model, image_processor, context_len = load_pretrained_model(  
        model_path="liuhaotian/llava-v1.5-13b",  
        model_base=None,  
        model_name=get_model_name_from_path("liuhaotian/llava-v1.5-13b"),  
        load_4bit=True  # Reduces VRAM ~4×  
    )  
      
    # 8-bit quantization  
    load_8bit=True  # Reduces VRAM ~2×  
    
[/code]

## Рекомендации[​](<#best-practices> "Прямая ссылка на Рекомендации")

  1. **Начните с модели 7B** — хорошее качество, умеренный расход VRAM
  2. **Используйте 4-битное квантование** — существенно снижает потребление VRAM
  3. **Требуется GPU** — инференс на CPU крайне медленный
  4. **Чёткие промпты** — конкретные вопросы дают лучшие ответы
  5. **Многопоточные диалоги** — сохраняйте контекст беседы
  6. **Temperature 0.2–0.7** — баланс между креативностью и согласованностью
  7. **max_new_tokens 512–1024** — для развёрнутых ответов
  8. **Пакетная обработка** — обрабатывайте несколько изображений последовательно


## Производительность[​](<#performance> "Прямая ссылка на Производительность")

Модель| VRAM (FP16)| VRAM (4-bit)| Скорость (токен/с)  
---|---|---|---|---  
7B| ~14 ГБ| ~4 ГБ| ~20  
13B| ~28 ГБ| ~8 ГБ| ~12  
34B| ~70 ГБ| ~18 ГБ| ~5  
_На GPU A100_

## Бенчмарки[​](<#benchmarks> "Прямая ссылка на Бенчмарки")

LLaVA достигает конкурентных показателей на:
  * **VQAv2** : 78,5%
  * **GQA** : 62,0%
  * **MM-Vet** : 35,4%
  * **MMBench** : 64,3%


## Ограничения[​](<#limitations> "Прямая ссылка на Ограничения")

  1. **Галлюцинации** — может описывать то, чего нет на изображении
  2. **Пространственное мышление** — плохо справляется с точным определением местоположения
  3. **Мелкий текст** — сложности с чтением мелкого шрифта
  4. **Подсчёт объектов** — неточен при большом количестве объектов
  5. **Требования к VRAM** — необходим мощный GPU
  6. **Скорость инференса** — медленнее, чем CLIP


## Интеграция с фреймворками[​](<#integration-with-frameworks> "Прямая ссылка на Интеграция с фреймворками")

### LangChain[​](<#langchain> "Прямая ссылка на LangChain")

[code] 
    from langchain.llms.base import LLM  
      
    class LLaVALLM(LLM):  
        def _call(self, prompt, stop=None):  
            # Custom LLaVA inference  
            return response  
      
    llm = LLaVALLM()  
    
[/code]

### Gradio App[​](<#gradio-app> "Прямая ссылка на Gradio App")

[code] 
    import gradio as gr  
      
    def chat(image, text, history):  
        response = ask_llava(model, image, text)  
        return response  
      
    demo = gr.ChatInterface(  
        chat,  
        additional_inputs=[gr.Image(type="pil")],  
        title="LLaVA Chat"  
    )  
    demo.launch()  
    
[/code]

## Ресурсы[​](<#resources> "Прямая ссылка на Ресурсы")

  * **GitHub** : <https://github.com/haotian-liu/LLaVA> ⭐ 23 000+
  * **Статья** : <https://arxiv.org/abs/2304.08485>
  * **Демо** : <https://llava.hliu.cc>
  * **Модели** : <https://huggingface.co/liuhaotian>
  * **Лицензия** : Apache 2.0


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать LLaVA](<#when-to-use-llava>)
  * [Быстрый старт](<#quick-start>)
    * [Установка](<#installation>)
    * [Базовое использование](<#basic-usage>)
  * [Доступные модели](<#available-models>)
  * [Использование в CLI](<#cli-usage>)
  * [Веб-интерфейс (Gradio)](<#web-ui-gradio>)
  * [Многопоточные диалоги](<#multi-turn-conversations>)
  * [Типовые задачи](<#common-tasks>)
    * [Описание изображений](<#image-captioning>)
    * [Визуальные ответы на вопросы](<#visual-question-answering>)
    * [Обнаружение объектов (текстовое)](<#object-detection-textual>)
    * [Понимание сцены](<#scene-understanding>)
    * [Понимание документов](<#document-understanding>)
  * [Обучение собственной модели](<#training-custom-model>)
  * [Квантование (снижение VRAM)](<#quantization-reduce-vram>)
  * [Рекомендации](<#best-practices>)
  * [Производительность](<#performance>)
  * [Бенчмарки](<#benchmarks>)
  * [Ограничения](<#limitations>)
  * [Интеграция с фреймворками](<#integration-with-frameworks>)
    * [LangChain](<#langchain>)
    * [Gradio App](<#gradio-app>)
  * [Ресурсы](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-llava -->
