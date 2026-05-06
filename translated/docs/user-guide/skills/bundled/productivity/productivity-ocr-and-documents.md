На этой странице
Извлечение текста из PDF/сканов (pymupdf, marker-pdf).
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|---|---  
|Источник| Встроенный (установлен по умолчанию)  
|Путь| `skills/productivity/ocr-and-documents`  
|Версия| `2.3.0`  
|Автор| Hermes Agent  
|Лицензия| MIT  
|Теги| `PDF`, `Documents`, `Research`, `Arxiv`, `Text-Extraction`, `OCR`  
|Связанные навыки| [`powerpoint`](</docs/user-guide/skills/bundled/productivity/productivity-powerpoint>)  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Извлечение PDF и документов
Для DOCX: используйте `python-docx` (парсит реальную структуру документа, намного лучше OCR). Для PPTX: см. навык `powerpoint` (использует `python-pptx` с полной поддержкой слайдов и заметок). Этот навык охватывает **PDF и отсканированные документы**.
## Шаг 1: Доступен удалённый URL?[​](<#step-1-remote-url-available> "Прямая ссылка на Шаг 1: Доступен удалённый URL?")
Если у документа есть URL, **всегда сначала пробуйте `web_extract`**:
[code] 
    web_extract(urls=["https://arxiv.org/pdf/2402.03300"])  
    web_extract(urls=["https://example.com/report.pdf"])  
    
[/code]
Это выполняет преобразование PDF в markdown через Firecrawl без локальных зависимостей.
Используйте локальное извлечение только тогда, когда: файл локальный, web_extract не сработал, или вам нужна пакетная обработка.
## Шаг 2: Выбор локального экстрактора[​](<#step-2-choose-local-extractor> "Прямая ссылка на Шаг 2: Выбор локального экстрактора")
Возможность| pymupdf (~25МБ)| marker-pdf (~3-5ГБ)  
|---|---|---  
**Текстовый PDF**|  ✅| ✅  
**Сканированный PDF (OCR)**|  ❌| ✅ (90+ языков)  
**Таблицы**|  ✅ (базово)| ✅ (высокая точность)  
**Уравнения / LaTeX**|  ❌| ✅  
**Блоки кода**|  ❌| ✅  
**Формы**|  ❌| ✅  
**Удаление верхних/нижних колонтитулов**|  ❌| ✅  
**Определение порядка чтения**|  ❌| ✅  
**Извлечение изображений**|  ✅ (встроенные)| ✅ (с контекстом)  
**Изображения → текст (OCR)**|  ❌| ✅  
**EPUB**|  ✅| ✅  
**Вывод в Markdown**|  ✅ (через pymupdf4llm)| ✅ (нативный, выше качество)  
**Размер установки**|  ~25МБ| ~3-5ГБ (PyTorch + модели)  
**Скорость**|  Мгновенно| ~1-14 с/стр (CPU), ~0,2 с/стр (GPU)  
**Решение**: Используйте pymupdf, если вам не нужны OCR, уравнения, формы или сложный анализ макета.
Если пользователю нужны возможности marker, но в системе не хватает ~5ГБ свободного места:
> "Этот документ требует OCR/расширенного извлечения (marker-pdf), для которого необходимо ~5ГБ для PyTorch и моделей. В вашей системе свободно [X]ГБ. Варианты: освободить место, указать URL, чтобы я мог использовать web_extract, или я могу попробовать pymupdf, который работает для текстовых PDF, но не для сканированных документов или уравнений."
* * *
## pymupdf (лёгкий)[​](<#pymupdf-lightweight> "Прямая ссылка на pymupdf (лёгкий)")
[code] 
    pip install pymupdf pymupdf4llm  
    
[/code]
**Через вспомогательный скрипт**:
[code] 
    python scripts/extract_pymupdf.py document.pdf              # Простой текст  
    python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown  
    python scripts/extract_pymupdf.py document.pdf --tables      # Таблицы  
    python scripts/extract_pymupdf.py document.pdf --images out/ # Извлечение изображений  
    python scripts/extract_pymupdf.py document.pdf --metadata    # Название, автор, страницы  
    python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Конкретные страницы  
    
[/code]
**Встроенно**:
[code] 
    python3 -c "  
    import pymupdf  
    doc = pymupdf.open('document.pdf')  
    for page in doc:  
        print(page.get_text())  
    "  
    
[/code]
* * *
## marker-pdf (высококачественное OCR)[​](<#marker-pdf-high-quality-ocr> "Прямая ссылка на marker-pdf (высококачественное OCR)")
[code] 
    # Сначала проверьте место на диске  
    python scripts/extract_marker.py --check  
      
    pip install marker-pdf  
    
[/code]
**Через вспомогательный скрипт**:
[code] 
    python scripts/extract_marker.py document.pdf                # Markdown  
    python scripts/extract_marker.py document.pdf --json         # JSON с метаданными  
    python scripts/extract_marker.py document.pdf --output_dir out/  # Сохранение изображений  
    python scripts/extract_marker.py scanned.pdf                 # Сканированный PDF (OCR)  
    python scripts/extract_marker.py document.pdf --use_llm      # Повышенная точность через LLM  
    
[/code]
**CLI** (устанавливается с marker-pdf):
[code] 
    marker_single document.pdf --output_dir ./output  
    marker /path/to/folder --workers 4    # Пакетная обработка  
    
[/code]
* * *
## Статьи Arxiv[​](<#arxiv-papers> "Прямая ссылка на Статьи Arxiv")
[code] 
    # Только аннотация (быстро)  
    web_extract(urls=["https://arxiv.org/abs/2402.03300"])  
      
    # Полная статья  
    web_extract(urls=["https://arxiv.org/pdf/2402.03300"])  
      
    # Поиск  
    web_search(query="arxiv GRPO reinforcement learning 2026")  
    
[/code]
## Разделение, объединение и поиск[​](<#split-merge--search> "Прямая ссылка на Разделение, объединение и поиск")
pymupdf поддерживает это нативно — используйте `execute_code` или встроенный Python:
[code] 
    # Разделение: извлечь страницы 1-5 в новый PDF  
    import pymupdf  
    doc = pymupdf.open("report.pdf")  
    new = pymupdf.open()  
    for i in range(5):  
        new.insert_pdf(doc, from_page=i, to_page=i)  
    new.save("pages_1-5.pdf")  
    
[/code]
[code] 
    # Объединение нескольких PDF  
    import pymupdf  
    result = pymupdf.open()  
    for path in ["a.pdf", "b.pdf", "c.pdf"]:  
        result.insert_pdf(pymupdf.open(path))  
    result.save("merged.pdf")  
    
[/code]
[code] 
    # Поиск текста по всем страницам  
    import pymupdf  
    doc = pymupdf.open("report.pdf")  
    for i, page in enumerate(doc):  
        results = page.search_for("revenue")  
        if results:  
            print(f"Page {i+1}: {len(results)} match(es)")  
            print(page.get_text("text"))  
    
[/code]
Никаких дополнительных зависимостей не требуется — pymupdf покрывает разделение, объединение, поиск и извлечение текста в одном пакете.
* * *
## Примечания[​](<#notes> "Прямая ссылка на Примечания")
  * `web_extract` — всегда первый выбор для URL
  * pymupdf — безопасный вариант по умолчанию: мгновенно, без моделей, работает везде
  * marker-pdf — для OCR, сканированных документов, уравнений, сложных макетов — устанавливайте только при необходимости
  * Оба вспомогательных скрипта принимают `--help` для полной информации об использовании
  * marker-pdf загружает ~2,5ГБ моделей в `~/.cache/huggingface/` при первом запуске
  * Для Word-документов: `pip install python-docx` (лучше, чем OCR — парсит реальную структуру)
  * Для PowerPoint: см. навык `powerpoint` (использует python-pptx)


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Шаг 1: Доступен удалённый URL?](<#step-1-remote-url-available>)
  * [Шаг 2: Выбор локального экстрактора](<#step-2-choose-local-extractor>)
  * [pymupdf (лёгкий)](<#pymupdf-lightweight>)
  * [marker-pdf (высококачественное OCR)](<#marker-pdf-high-quality-ocr>)
  * [Статьи Arxiv](<#arxiv-papers>)
  * [Разделение, объединение и поиск](<#split-merge--search>)
  * [Примечания](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-ocr-and-documents -->
