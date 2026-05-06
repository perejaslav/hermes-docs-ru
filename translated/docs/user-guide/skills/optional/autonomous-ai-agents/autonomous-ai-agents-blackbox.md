On this page
Делегируйте задачи по программированию CLI-агенту Blackbox AI. Мультимодельный агент со встроенным судьёй, который запускает задачи через несколько LLM и выбирает лучший результат. Требуется CLI blackbox и ключ API Blackbox AI.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Опционально — установите через `hermes skills install official/autonomous-ai-agents/blackbox` |
|Путь| `optional-skills/autonomous-ai-agents/blackbox` |
|Версия| `1.0.0` |
|Автор| Hermes Agent (Nous Research) |
|Лицензия| MIT |
|Теги| `Coding-Agent`, `Blackbox`, `Multi-Agent`, `Judge`, `Multi-Model` |
|Связанные навыки| [`claude-code`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code>), [`codex`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex>), [`hermes-agent`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent>) |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# Blackbox CLI
Делегируйте задачи по программированию [Blackbox AI](<https://www.blackbox.ai/>) через терминал Hermes. Blackbox — это мультимодельный CLI-агент для кодинга, который отправляет задачи нескольким LLM (Claude, Codex, Gemini, Blackbox Pro) и использует судью для выбора лучшей реализации.
CLI является [открытым](<https://github.com/blackboxaicode/cli>) (GPL-3.0, TypeScript, форк Gemini CLI) и поддерживает интерактивные сессии, неинтерактивные одноразовые задачи, контрольные точки (checkpointing), MCP и переключение моделей с поддержкой зрения.
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  * Установленный Node.js 20+
  * Установленный Blackbox CLI: `npm install -g @blackboxai/cli`
  * Или установка из исходников:
[code] git clone https://github.com/blackboxaicode/cli.git  
        cd cli && npm install && npm install -g .  
        
[/code]
  * Ключ API из [app.blackbox.ai/dashboard](<https://app.blackbox.ai/dashboard>)
  * Настройка: выполните `blackbox configure` и введите ваш ключ API
  * Используйте `pty=true` в вызовах terminal — Blackbox CLI — это интерактивное терминальное приложение


## Одноразовые задачи[​](<#one-shot-tasks> "Прямая ссылка на Одноразовые задачи")
[code] 
    terminal(command=\"blackbox --prompt 'Add JWT authentication with refresh tokens to the Express API'\", workdir=\"/path/to/project\", pty=true)  
    
[/code]
Для быстрой черновой работы:
[code] 
    terminal(command=\"cd $(mktemp -d) && git init && blackbox --prompt 'Build a REST API for todos with SQLite'\", pty=true)  
    
[/code]
## Фоновый режим (длительные задачи)[​](<#background-mode-long-tasks> "Прямая ссылка на Фоновый режим \\(длительные задачи\\)")
Для задач, занимающих минуты, используйте фоновый режим, чтобы отслеживать прогресс:
[code] 
    # Start in background with PTY  
    terminal(command=\"blackbox --prompt 'Refactor the auth module to use OAuth 2.0'\", workdir=\"~/project\", background=true, pty=true)  
    # Returns session_id  
      
    # Monitor progress  
    process(action=\"poll\", session_id=\"<id>\")  
    process(action=\"log\", session_id=\"<id>\")  
      
    # Send input if Blackbox asks a question  
    process(action=\"submit\", session_id=\"<id>\", data=\"yes\")  
      
    # Kill if needed  
    process(action=\"kill\", session_id=\"<id>\")  
    
[/code]
## Контрольные точки и возобновление[​](<#checkpoints--resume> "Прямая ссылка на Контрольные точки и возобновление")
Blackbox CLI имеет встроенную поддержку контрольных точек для приостановки и возобновления задач:
[code] 
    # After a task completes, Blackbox shows a checkpoint tag  
    # Resume with a follow-up task:  
    terminal(command=\"blackbox --resume-checkpoint 'task-abc123-2026-03-06' --prompt 'Now add rate limiting to the endpoints'\", workdir=\"~/project\", pty=true)  
    
[/code]
## Команды сессии[​](<#session-commands> "Прямая ссылка на Команды сессии")
Во время интерактивной сессии используйте эти команды:
|Команда| Эффект |
|---|---|
|`/compress`| Сжать историю беседы для экономии токенов |
|`/clear`| Очистить историю и начать заново |
|`/stats`| Просмотреть текущее использование токенов |
|`Ctrl+C`| Отменить текущую операцию |
## Проверка PR[​](<#pr-reviews> "Прямая ссылка на Проверка PR")
Клонируйте во временную директорию, чтобы не изменять рабочее дерево:
[code] 
    terminal(command=\"REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && blackbox --prompt 'Review this PR against main. Check for bugs, security issues, and code quality.'\", pty=true)  
    
[/code]
## Параллельная работа[​](<#parallel-work> "Прямая ссылка на Параллельная работа")
Запускайте несколько экземпляров Blackbox для независимых задач:
[code] 
    terminal(command=\"blackbox --prompt 'Fix the login bug'\", workdir=\"/tmp/issue-1\", background=true, pty=true)  
    terminal(command=\"blackbox --prompt 'Add unit tests for auth'\", workdir=\"/tmp/issue-2\", background=true, pty=true)  
      
    # Monitor all  
    process(action=\"list\")  
    
[/code]
## Мультимодельный режим[​](<#multi-model-mode> "Прямая ссылка на Мультимодельный режим")
Уникальная особенность Blackbox — выполнение одной и той же задачи через несколько моделей и оценка результатов. Настройте используемые модели через `blackbox configure` — выберите несколько провайдеров, чтобы активировать рабочий процесс с председателем/судьёй, где CLI оценивает выводы разных моделей и выбирает лучший.
## Ключевые флаги[​](<#key-flags> "Прямая ссылка на Ключевые флаги")
|Флаг| Эффект |
|---|---|
|`--prompt \"task\"`| Неинтерактивное одноразовое выполнение |
|`--resume-checkpoint \"tag\"`| Возобновить с сохранённой контрольной точки |
|`--yolo`| Автоматически одобрять все действия и переключения моделей |
|`blackbox session`| Запустить интерактивную чат-сессию |
|`blackbox configure`| Изменить настройки, провайдеров, модели |
|`blackbox info`| Отобразить информацию о системе |
## Поддержка зрения[​](<#vision-support> "Прямая ссылка на Поддержка зрения")
Blackbox автоматически обнаруживает изображения во вводе и может переключаться на мультимодальный анализ. Режимы VLM:
  * `\"once\"` — Переключить модель только для текущего запроса
  * `\"session\"` — Переключить для всей сессии
  * `\"persist\"` — Остаться на текущей модели (без переключения)


## Лимиты токенов[​](<#token-limits> "Прямая ссылка на Лимиты токенов")
Управляйте использованием токенов через `.blackboxcli/settings.json`:
[code] 
    {  
      \"sessionTokenLimit\": 32000  
    }  
    
[/code]
## Правила[​](<#rules> "Прямая ссылка на Правила")
  1. **Всегда используйте`pty=true`** — Blackbox CLI — это интерактивное терминальное приложение, которое зависнет без PTY
  2. **Используйте`workdir`** — держите агента сфокусированным на правильной директории
  3. **Фон для длительных задач** — используйте `background=true` и отслеживайте с помощью инструмента `process`
  4. **Не вмешивайтесь** — отслеживайте через `poll`/`log`, не убивайте сессии из-за того, что они медленные
  5. **Сообщайте результаты** — после завершения проверьте, что изменилось, и подведите итог для пользователя
  6. **Кредиты стоят денег** — Blackbox использует кредитную систему; мультимодельный режим расходует кредиты быстрее
  7. **Проверяйте предварительные требования** — убедитесь, что CLI `blackbox` установлен, прежде чем пытаться делегировать


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
  * [Одноразовые задачи](<#one-shot-tasks>)
  * [Фоновый режим (длительные задачи)](<#background-mode-long-tasks>)
  * [Контрольные точки и возобновление](<#checkpoints--resume>)
  * [Команды сессии](<#session-commands>)
  * [Проверка PR](<#pr-reviews>)
  * [Параллельная работа](<#parallel-work>)
  * [Мультимодельный режим](<#multi-model-mode>)
  * [Ключевые флаги](<#key-flags>)
  * [Поддержка зрения](<#vision-support>)
  * [Лимиты токенов](<#token-limits>)
  * [Правила](<#rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-blackbox -->
