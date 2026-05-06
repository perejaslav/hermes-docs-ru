On this page
Интеграция с Canvas LMS — получение списка курсов и заданий с использованием аутентификации по API-токену.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")
|   
|---|---  
Source| Optional — install with `hermes skills install official/productivity/canvas`  
Path| `optional-skills/productivity/canvas`  
Version| `1.0.0`  
Author| community  
License| MIT  
Tags| `Canvas`, `LMS`, `Education`, `Courses`, `Assignments`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# Canvas LMS — Course & Assignment Access
Доступ только для чтения к Canvas LMS для просмотра курсов и заданий.
## Scripts[​](<#scripts> "Прямая ссылка на скрипты")
  * `scripts/canvas_api.py` — Python CLI для вызовов Canvas API


## Setup[​](<#setup> "Прямая ссылка на настройку")
  1. Войдите в свой аккаунт Canvas в браузере
  2. Перейдите в **Account → Settings** (нажмите на иконку профиля, затем Settings)
  3. Прокрутите до **Approved Integrations** и нажмите **\+ New Access Token**
  4. Дайте токену имя (например, "Hermes Agent"), установите опциональный срок действия и нажмите **Generate Token**
  5. Скопируйте токен и добавьте в `~/.hermes/.env`:


[code] 
    CANVAS_API_TOKEN=your_token_here  
    CANVAS_BASE_URL=https://yourschool.instructure.com  
    
[/code]
Базовый URL — это адрес, который отображается в браузере, когда вы вошли в Canvas (без завершающего слеша).
## Usage[​](<#usage> "Прямая ссылка на использование")
[code] 
    CANVAS="python $HERMES_HOME/skills/productivity/canvas/scripts/canvas_api.py"  
      
    # List all active courses  
    $CANVAS list_courses --enrollment-state active  
      
    # List all courses (any state)  
    $CANVAS list_courses  
      
    # List assignments for a specific course  
    $CANVAS list_assignments 12345  
      
    # List assignments ordered by due date  
    $CANVAS list_assignments 12345 --order-by due_at  
    
[/code]
## Output Format[​](<#output-format> "Прямая ссылка на формат вывода")
**list_courses** возвращает:
[code] 
    [{"id": 12345, "name": "Intro to CS", "course_code": "CS101", "workflow_state": "available", "start_at": "...", "end_at": "..."}]  
    
[/code]
**list_assignments** возвращает:
[code] 
    [{"id": 67890, "name": "Homework 1", "due_at": "2025-02-15T23:59:00Z", "points_possible": 100, "submission_types": ["online_upload"], "html_url": "...", "description": "...", "course_id": 12345}]  
    
[/code]
Примечание: описания заданий обрезаются до 500 символов. Поле `html_url` ведёт на полную страницу задания в Canvas.
## API Reference (curl)[​](<#api-reference-curl> "Прямая ссылка на API Reference \\(curl\\)")
[code] 
    # List courses  
    curl -s -H "Authorization: Bearer $CANVAS_API_TOKEN" \  
      "$CANVAS_BASE_URL/api/v1/courses?enrollment_state=active&per_page=10"  
      
    # List assignments for a course  
    curl -s -H "Authorization: Bearer $CANVAS_API_TOKEN" \  
      "$CANVAS_BASE_URL/api/v1/courses/COURSE_ID/assignments?per_page=10&order_by=due_at"  
    
[/code]
Canvas использует заголовки `Link` для пагинации. Python-скрипт обрабатывает пагинацию автоматически.
## Rules[​](<#rules> "Прямая ссылка на правила")
  * Навык работает **только на чтение** — он только получает данные, никогда не изменяет курсы или задания
  * При первом использовании проверьте аутентификацию, запустив `$CANVAS list_courses` — если он завершается с ошибкой 401, проведите пользователя через настройку
  * Canvas ограничивает запросы до ~700 за 10 минут; проверяйте заголовок `X-Rate-Limit-Remaining` при приближении к лимиту


## Troubleshooting[​](<#troubleshooting> "Прямая ссылка на устранение неполадок")
Проблема| Исправление  
---|---  
401 Unauthorized| Токен недействителен или истёк — создайте новый в настройках Canvas  
403 Forbidden| У токена нет прав для этого курса  
Empty course list| Попробуйте `--enrollment-state active` или опустите флаг, чтобы увидеть все состояния  
Wrong institution| Проверьте, что `CANVAS_BASE_URL` соответствует URL в вашем браузере  
Timeout errors| Проверьте сетевое подключение к вашему экземпляру Canvas  
  * [Метаданные навыка](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Скрипты](<#scripts>)
  * [Настройка](<#setup>)
  * [Использование](<#usage>)
  * [Формат вывода](<#output-format>)
  * [API Reference (curl)](<#api-reference-curl>)
  * [Правила](<#rules>)
  * [Устранение неполадок](<#troubleshooting>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-canvas -->
