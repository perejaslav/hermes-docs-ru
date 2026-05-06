On this page
Hermes Agent генерирует изображения из текстовых запросов через FAL.ai. «Из коробки» поддерживается девять моделей, каждая с разными компромиссами по скорости, качеству и стоимости. Активную модель можно настроить через `hermes tools`; выбор сохраняется в `config.yaml`.
## Supported Models[​](<#supported-models> "Direct link to Supported Models")
|Модель| Скорость| Сильные стороны| Цена  |
|---|---|---|---|
|`fal-ai/flux-2/klein/9b` _(по умолчанию)_| `<1с`| Быстро, чёткий текст| $0.006/МП  |
|`fal-ai/flux-2-pro`| ~6с| Студийный фотореализм| $0.03/МП  |
|`fal-ai/z-image/turbo`| ~2с| Двуязычная EN/CN, 6B параметров| $0.005/МП  |
|`fal-ai/nano-banana-pro`| ~8с| Gemini 3 Pro, глубина рассуждения, отрисовка текста| $0.15/изображение (1K)  |
|`fal-ai/gpt-image-1.5`| ~15с| Следование промпту| $0.034/изображение  |
|`fal-ai/gpt-image-2`| ~20с| Передовая отрисовка текста + CJK, реализм с пониманием мира| $0.04–0.06/изображение  |
|`fal-ai/ideogram/v3`| ~5с| Лучшая типографика| $0.03–0.09/изображение  |
|`fal-ai/recraft/v4/pro/text-to-image`| ~8с| Дизайн, бренд-системы, готово к продакшену| $0.25/изображение  |
|`fal-ai/qwen-image`| ~12с| На основе LLM, сложный текст| $0.02/МП  |
Цены указаны по тарифам FAL на момент написания; актуальные цифры смотрите на [fal.ai](<https://fal.ai/>).
## Setup[​](<#setup> "Direct link to Setup")
Подписчики Nous
Если у вас платная подписка [Nous Portal](<https://portal.nousresearch.com>), вы можете использовать генерацию изображений через **[Tool Gateway](</docs/user-guide/features/tool-gateway>)** без ключа FAL API. Выбор модели сохраняется для обоих путей.
Если управляемый шлюз возвращает `HTTP 4xx` для конкретной модели, значит, эта модель ещё не проксирована на стороне портала — агент сообщит вам об этом и предложит варианты решения (установите `FAL_KEY` для прямого доступа или выберите другую модель).
### Get a FAL API Key[​](<#get-a-fal-api-key> "Direct link to Get a FAL API Key")
  1. Зарегистрируйтесь на [fal.ai](<https://fal.ai/>)
  2. Сгенерируйте API-ключ в панели управления


### Configure and Pick a Model[​](<#configure-and-pick-a-model> "Direct link to Configure and Pick a Model")
Запустите команду tools:
[code] 
    hermes tools  
    
[/code]
Перейдите в **🎨 Image Generation**, выберите бэкенд (Nous Subscription или FAL.ai), после чего откроется список всех поддерживаемых моделей в виде таблицы с колонками — стрелки для навигации, Enter для выбора:
[code] 
      Модель                           Скорость    Сильные стороны              Цена  
      fal-ai/flux-2/klein/9b           <1с         Быстро, чёткий текст         $0.006/МП   ← currently in use  
      fal-ai/flux-2-pro                ~6с         Студийный фотореализм        $0.03/МП  
      fal-ai/z-image/turbo             ~2с         Двуязычная EN/CN, 6B         $0.005/МП  
      ...  
    
[/code]
Ваш выбор сохраняется в `config.yaml`:
[code] 
    image_gen:  
      model: fal-ai/flux-2/klein/9b  
      use_gateway: false            # true при использовании Nous Subscription  
    
[/code]
### GPT-Image Quality[​](<#gpt-image-quality> "Direct link to GPT-Image Quality")
Качество запросов для `fal-ai/gpt-image-1.5` и `fal-ai/gpt-image-2` зафиксировано на уровне `medium` (~$0.034–$0.06/изображение при 1024×1024). Мы не выставляем уровни `low` / `high` как доступные пользователю опции, чтобы биллинг Nous Portal оставался предсказуемым для всех пользователей — разброс цен между уровнями составляет 3–22×. Если вам нужен более дешёвый вариант, выбирайте Klein 9B или Z-Image Turbo; если нужно более высокое качество — используйте Nano Banana Pro или Recraft V4 Pro.
## Usage[​](<#usage> "Direct link to Usage")
Схема взаимодействия для агента намеренно минимальна — модель подхватывает то, что вы настроили:
[code] 
    Generate an image of a serene mountain landscape with cherry blossoms  
    
[/code]
[code] 
    Create a square portrait of a wise old owl — use the typography model  
    
[/code]
[code] 
    Make me a futuristic cityscape, landscape orientation  
    
[/code]
## Aspect Ratios[​](<#aspect-ratios> "Direct link to Aspect Ratios")
Каждая модель принимает одни и те же три соотношения сторон с точки зрения агента. Внутренне собственный размер каждой модели подставляется автоматически:
|Ввод агента| image_size (flux/z-image/qwen/recraft/ideogram)| aspect_ratio (nano-banana-pro)| image_size (gpt-image-1.5)| image_size (gpt-image-2)  |
|---|---|---|---|---|
|`landscape`| `landscape_16_9`| `16:9`| `1536x1024`| `landscape_4_3` (1024×768)  |
|`square`| `square_hd`| `1:1`| `1024x1024`| `square_hd` (1024×1024)  |
|`portrait`| `portrait_16_9`| `9:16`| `1024x1536`| `portrait_4_3` (768×1024)  |
GPT Image 2 использует пресеты 4:3 вместо 16:9, потому что его минимальное количество пикселей составляет 655 360 — пресет `landscape_16_9` (1024×576 = 589 824) был бы отклонён.
Это преобразование происходит в `_build_fal_payload()` — агенту никогда не нужно знать о различиях в схемах между моделями.
## Automatic Upscaling[​](<#automatic-upscaling> "Direct link to Automatic Upscaling")
Апскейлинг через **Clarity Upscaler** от FAL включается выборочно для каждой модели:
|Модель| Апскейл?| Почему  |
|---|---|---|
|`fal-ai/flux-2-pro`| ✓| Обратная совместимость (был моделью по умолчанию до появления выбора)  |
|Все остальные| ✗| Быстрые модели потеряли бы своё преимущество в доли секунды; высокодетальные модели в нём не нуждаются  |
|Когда апскейлинг запущен, используются следующие настройки:||
|Настройка| Значение  |
|---|---|
|Коэффициент апскейла| 2×  |
|Креативность| 0.35  |
|Сходство| 0.6  |
|Масштаб guidance| 4  |
|Шагов инференса| 18  |
|Если апскейлинг не удался (сетевая проблема, ограничение запросов), возвращается исходное изображение.|
## How It Works Internally[​](<#how-it-works-internally> "Direct link to How It Works Internally")
  1. **Определение модели** — `_resolve_fal_model()` читает `image_gen.model` из `config.yaml`, затем проверяет переменную окружения `FAL_IMAGE_MODEL`, и в конце — `fal-ai/flux-2/klein/9b` как запасной вариант.
  2. **Построение payload** — `_build_fal_payload()` преобразует ваш `aspect_ratio` в родной формат модели (перечисление пресетов, перечисление соотношений сторон или литерал GPT), объединяет параметры модели по умолчанию, применяет переопределения от вызывающей стороны, затем фильтрует по белому списку `supports` модели, чтобы неподдерживаемые ключи никогда не отправлялись.
  3. **Отправка** — `_submit_fal_request()` направляет запрос через прямые учётные данные FAL или управляемый шлюз Nous.
  4. **Апскейлинг** — выполняется, только если в метаданных модели указано `upscale: True`.
  5. **Доставка** — итоговый URL изображения возвращается агенту, который отправляет тег `MEDIA:<url>`, преобразуемый адаптерами платформ в нативный медиа-контент.


## Debugging[​](<#debugging> "Direct link to Debugging")
Включите отладочное логирование:
[code] 
    export IMAGE_TOOLS_DEBUG=true  
    
[/code]
Отладочные логи сохраняются в `./logs/image_tools_debug_<session_id>.json` с деталями каждого вызова (модель, параметры, время, ошибки).
## Platform Delivery[​](<#platform-delivery> "Direct link to Platform Delivery")
|Платформа| Доставка  |
|---|---|
|**CLI**|  URL изображения выводится в виде markdown `![](url)` — нажмите, чтобы открыть  |
|**Telegram**|  Фото-сообщение с промптом в качестве подписи  |
|**Discord**|  Встроено в сообщение  |
|**Slack**|  URL разворачивается Slack  |
|**WhatsApp**|  Медиа-сообщение  |
|**Другие**|  URL в виде обычного текста  |
## Limitations[​](<#limitations> "Direct link to Limitations")
  * **Требуются учётные данные FAL** (прямой `FAL_KEY` или подписка Nous)
  * **Только текст-в-изображение** — без инпейнтинга, img2img или редактирования через этот инструмент
  * **Временные URL** — FAL возвращает хостированные URL, которые истекают через часы/дни; при необходимости сохраняйте локально
  * **Ограничения отдельных моделей** — некоторые модели не поддерживают `seed`, `num_inference_steps` и т.д. Фильтр `supports` молча отбрасывает неподдерживаемые параметры; это ожидаемое поведение


  * [Поддерживаемые модели](<#supported-models>)
  * [Настройка](<#setup>)
    * [Получение ключа FAL API](<#get-a-fal-api-key>)
    * [Настройка и выбор модели](<#configure-and-pick-a-model>)
    * [Качество GPT-Image](<#gpt-image-quality>)
  * [Использование](<#usage>)
  * [Соотношения сторон](<#aspect-ratios>)
  * [Автоматический апскейлинг](<#automatic-upscaling>)
  * [Как это работает внутри](<#how-it-works-internally>)
  * [Отладка](<#debugging>)
  * [Доставка на платформах](<#platform-delivery>)
  * [Ограничения](<#limitations>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/image-generation -->
