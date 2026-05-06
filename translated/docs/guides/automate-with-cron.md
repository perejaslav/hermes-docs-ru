На этой странице
[Учебник по ежедневному боту-дайджесту](/docs/guides/daily-briefing-bot) охватывает основы. Это руководство идёт дальше — пять реальных шаблонов автоматизации, которые вы можете адаптировать для своих рабочих процессов.
Полную справку по функциям см. в разделе [Плановые задачи (Cron)](/docs/user-guide/features/cron).
Key Concept
Cron-задачи запускаются в новых сессиях агента без памяти о вашем текущем чате. Промпты должны быть **полностью самодостаточными** — включайте всё, что нужно знать агенту.
Не нужна LLM? Используйте режим без агента.
Для повторяющихся сторожевых задач, где скрипт уже создаёт именно то сообщение, которое вы хотите отправить (уведомления о памяти, уведомления о диске, CI-пинги, пульс), пропустите LLM полностью с помощью [cron-задач только со скриптом](/docs/guides/cron-script-only). Ноль токенов, тот же планировщик. Вы можете попросить Hermes настроить такую задачу в чате — инструмент `cronjob` знает, когда установить `no_agent=True`, и пишет скрипт за вас.
* * *
## Шаблон 1: Мониторинг изменений веб-сайта[​](#pattern-1-website-change-monitor "Прямая ссылка на Шаблон 1: Мониторинг изменений веб-сайта")
Отслеживайте URL на предмет изменений и получайте уведомления только когда что-то изменилось.
Параметр `script` — это секретное оружие. Python-скрипт запускается перед каждым выполнением, и его stdout становится контекстом для агента. Скрипт выполняет механическую работу (загрузка, сравнение); агент выполняет анализ (интересно ли это изменение?).
Создайте скрипт мониторинга:
[code] 
    mkdir -p ~/.hermes/scripts  
    
[/code]
~/.hermes/scripts/watch-site.py
[code]
    import hashlib, json, os, urllib.request  
      
    URL = "https://example.com/pricing"  
    STATE_FILE = os.path.expanduser("~/.hermes/scripts/.watch-site-state.json")  
      
    # Получение текущего содержимого  
    req = urllib.request.Request(URL, headers={"User-Agent": "Hermes-Monitor/1.0"})  
    content = urllib.request.urlopen(req, timeout=30).read().decode()  
    current_hash = hashlib.sha256(content.encode()).hexdigest()  
      
    # Загрузка предыдущего состояния  
    prev_hash = None  
    if os.path.exists(STATE_FILE):  
        with open(STATE_FILE) as f:  
            prev_hash = json.load(f).get("hash")  
      
    # Сохранение текущего состояния  
    with open(STATE_FILE, "w") as f:  
        json.dump({"hash": current_hash, "url": URL}, f)  
      
    # Вывод для агента  
    if prev_hash and prev_hash != current_hash:  
        print(f"CHANGE DETECTED on {URL}")  
        print(f"Previous hash: {prev_hash}")  
        print(f"Current hash: {current_hash}")  
        print(f"\nCurrent content (first 2000 chars):\n{content[:2000]}")  
    else:  
        print("NO_CHANGE")  
    
[/code]
Настройте cron-задачу:
[code] 
    /cron add "every 1h" "If the script output says CHANGE DETECTED, summarize what changed on the page and why it might matter. If it says NO_CHANGE, respond with just [SILENT]." --script ~/.hermes/scripts/watch-site.py --name "Pricing monitor" --deliver telegram  
    
[/code]
Трюк с [SILENT]
Когда финальный ответ агента содержит `[SILENT]`, доставка подавляется. Это означает, что вы получаете уведомления только когда что-то действительно происходит — никакого спама в тихие часы.
* * *
## Шаблон 2: Еженедельный отчёт[​](#pattern-2-weekly-report "Прямая ссылка на Шаблон 2: Еженедельный отчёт")
Собирайте информацию из нескольких источников в форматированную сводку. Запускается раз в неделю и доставляется в ваш домашний канал.
[code] 
    /cron add "0 9 * * 1" "Generate a weekly report covering:  
      
    1. Search the web for the top 5 AI news stories from the past week  
    2. Search GitHub for trending repositories in the 'machine-learning' topic  
    3. Check Hacker News for the most discussed AI/ML posts  
      
    Format as a clean summary with sections for each source. Include links.  
    Keep it under 500 words — highlight only what matters." --name "Weekly AI digest" --deliver telegram  
    
[/code]
Из CLI:
[code] 
    hermes cron create "0 9 * * 1" \  
      "Generate a weekly report covering the top AI news, trending ML GitHub repos, and most-discussed HN posts. Format with sections, include links, keep under 500 words." \  
      --name "Weekly AI digest" \  
      --deliver telegram  
    
[/code]
`0 9 * * 1` — это стандартное cron-выражение: 9:00 каждый понедельник.
* * *
## Шаблон 3: Наблюдатель репозитория GitHub[​](#pattern-3-github-repository-watcher "Прямая ссылка на Шаблон 3: Наблюдатель репозитория GitHub")
Отслеживайте репозиторий на предмет новых issues, PR или релизов.
[code] 
    /cron add "every 6h" "Check the GitHub repository NousResearch/hermes-agent for:  
    - New issues opened in the last 6 hours  
    - New PRs opened or merged in the last 6 hours  
    - Any new releases  
      
    Use the terminal to run gh commands:  
      gh issue list --repo NousResearch/hermes-agent --state open --json number,title,author,createdAt --limit 10  
      gh pr list --repo NousResearch/hermes-agent --state all --json number,title,author,createdAt,mergedAt --limit 10  
      
    Filter to only items from the last 6 hours. If nothing new, respond with [SILENT].  
    Otherwise, provide a concise summary of the activity." --name "Repo watcher" --deliver discord  
    
[/code]
Самодостаточные промпты
Обратите внимание, как промпт включает точные команды `gh`. У cron-агента нет памяти о предыдущих запусках или ваших предпочтениях — расписывайте всё подробно.
* * *
## Шаблон 4: Конвейер сбора данных[​](#pattern-4-data-collection-pipeline "Прямая ссылка на Шаблон 4: Конвейер сбора данных")
Собирайте данные через регулярные интервалы, сохраняйте в файлы и обнаруживайте тренды с течением времени. Этот шаблон объединяет скрипт (для сбора) с агентом (для анализа).
~/.hermes/scripts/collect-prices.py
[code]
    import json, os, urllib.request  
    from datetime import datetime  
      
    DATA_DIR = os.path.expanduser("~/.hermes/data/prices")  
    os.makedirs(DATA_DIR, exist_ok=True)  
      
    # Получение текущих данных (пример: крипто-цены)  
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"  
    data = json.loads(urllib.request.urlopen(url, timeout=30).read())  
      
    # Добавление в файл истории  
    entry = {"timestamp": datetime.now().isoformat(), "prices": data}  
    history_file = os.path.join(DATA_DIR, "history.jsonl")  
    with open(history_file, "a") as f:  
        f.write(json.dumps(entry) + "\n")  
      
    # Загрузка недавней истории для анализа  
    lines = open(history_file).readlines()  
    recent = [json.loads(l) for l in lines[-24:]]  # Последние 24 точки данных  
      
    # Вывод для агента  
    print(f"Current: BTC=${data['bitcoin']['usd']}, ETH=${data['ethereum']['usd']}")  
    print(f"Data points collected: {len(lines)} total, showing last {len(recent)}")  
    print(f"\nRecent history:")  
    for r in recent[-6:]:  
        print(f"  {r['timestamp']}: BTC=${r['prices']['bitcoin']['usd']}, ETH=${r['prices']['ethereum']['usd']}")  
    
[/code]
[code] 
    /cron add "every 1h" "Analyze the price data from the script output. Report:  
    1. Current prices  
    2. Trend direction over the last 6 data points (up/down/flat)  
    3. Any notable movements (>5% change)  
      
    If prices are flat and nothing notable, respond with [SILENT].  
    If there's a significant move, explain what happened." \  
      --script ~/.hermes/scripts/collect-prices.py \  
      --name "Price tracker" \  
      --deliver telegram  
    
[/code]
Скрипт выполняет механический сбор; агент добавляет уровень анализа.
* * *
## Шаблон 5: Многоэтапный рабочий процесс с навыками[​](#pattern-5-multi-skill-workflow "Прямая ссылка на Шаблон 5: Многоэтапный рабочий процесс с навыками")
Объединяйте навыки в цепочки для сложных плановых задач. Навыки загружаются по порядку перед выполнением промпта.
[code] 
    # Использование навыка arxiv для поиска статей, затем навыка obsidian для сохранения заметок  
    /cron add "0 8 * * *" "Search arXiv for the 3 most interesting papers on 'language model reasoning' from the past day. For each paper, create an Obsidian note with the title, authors, abstract summary, and key contribution." \  
      --skill arxiv \  
      --skill obsidian \  
      --name "Paper digest"  
    
[/code]
Через сам инструмент:
[code] 
    cronjob(  
        action="create",  
        skills=["arxiv", "obsidian"],  
        prompt="Search arXiv for papers on 'language model reasoning' from the past day. Save the top 3 as Obsidian notes.",  
        schedule="0 8 * * *",  
        name="Paper digest",  
        deliver="local"  
    )  
    
[/code]
Навыки загружаются по порядку — сначала `arxiv` (обучает агента поиску статей), затем `obsidian` (обучает созданию заметок). Промпт связывает их вместе.
* * *
## Управление задачами[​](#managing-your-jobs "Прямая ссылка на Управление задачами")
[code] 
    # Список всех активных задач  
    /cron list  
      
    # Запустить задачу немедленно (для тестирования)  
    /cron run <job_id>  
      
    # Приостановить задачу без удаления  
    /cron pause <job_id>  
      
    # Редактировать расписание или промпт существующей задачи  
    /cron edit <job_id> --schedule "every 4h"  
    /cron edit <job_id> --prompt "Updated task description"  
      
    # Добавить или удалить навыки из существующей задачи  
    /cron edit <job_id> --skill arxiv --skill obsidian  
    /cron edit <job_id> --clear-skills  
      
    # Удалить задачу навсегда  
    /cron remove <job_id>  
    
[/code]
* * *
## Цели доставки[​](#delivery-targets "Прямая ссылка на Цели доставки")
Флаг `--deliver` определяет, куда направляются результаты:
Цель| Пример| Сценарий использования  
---|---|---  
`origin`| `--deliver origin`| Тот же чат, который создал задачу (по умолчанию)  
`local`| `--deliver local`| Сохранить только в локальный файл  
`telegram`| `--deliver telegram`| Ваш домашний канал Telegram  
`discord`| `--deliver discord`| Ваш домашний канал Discord  
`slack`| `--deliver slack`| Ваш домашний канал Slack  
Конкретный чат| `--deliver telegram:-1001234567890`| Конкретная группа Telegram  
Ветка (тема)| `--deliver telegram:-1001234567890:17585`| Конкретная тема в Telegram  
* * *
## Советы[​](#tips "Прямая ссылка на Советы")
**Делайте промпты самодостаточными.** Агент в cron-задаче не имеет памяти о ваших разговорах. Включайте URL, имена репозиториев, предпочтения по форматированию и инструкции по доставке прямо в промпт.
**Используйте `[SILENT]` щедро.** Для задач мониторинга всегда включайте инструкции вроде «если ничего не изменилось, ответь `[SILENT]`». Это предотвращает шум от уведомлений.
**Используйте скрипты для сбора данных.** Параметр `script` позволяет Python-скрипту обрабатывать рутинные части (HTTP-запросы, файловый ввод-вывод, отслеживание состояния). Агент видит только stdout скрипта и применяет к нему анализ. Это дешевле и надёжнее, чем заставлять агента выполнять загрузку самостоятельно.
**Тестируйте с помощью `/cron run`.** Прежде чем ждать срабатывания по расписанию, используйте `/cron run <job_id>` для немедленного выполнения и проверки корректности вывода.
**Выражения расписания.** Поддерживаемые форматы: относительные задержки (`30m`), интервалы (`every 2h`), стандартные cron-выражения (`0 9 * * *`) и ISO-метки времени (`2025-06-15T09:00:00`). Естественный язык, такой как `daily at 9am`, не поддерживается — используйте вместо этого `0 9 * * *`.
* * *
_Полную справку по cron — все параметры, граничные случаи и внутреннее устройство — см. в разделе [Плановые задачи (Cron)](/docs/user-guide/features/cron)._
  * [Шаблон 1: Мониторинг изменений веб-сайта](#pattern-1-website-change-monitor)
  * [Шаблон 2: Еженедельный отчёт](#pattern-2-weekly-report)
  * [Шаблон 3: Наблюдатель репозитория GitHub](#pattern-3-github-repository-watcher)
  * [Шаблон 4: Конвейер сбора данных](#pattern-4-data-collection-pipeline)
  * [Шаблон 5: Многоэтапный рабочий процесс с навыками](#pattern-5-multi-skill-workflow)
  * [Управление задачами](#managing-your-jobs)
  * [Цели доставки](#delivery-targets)
  * [Советы](#tips)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron -->
