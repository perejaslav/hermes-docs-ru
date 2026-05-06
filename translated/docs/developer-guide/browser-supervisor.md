На этой странице
**Статус:** Реализован (PR 14540) **Последнее обновление:** 2026-04-23 **Автор:** @teknium1
## Проблема[​](#problem "Прямая ссылка на Проблему")
Нативные JS-диалоги (`alert`/`confirm`/`prompt`/`beforeunload`) и iframe являются двумя самыми большими пробелами в нашем инструментарии для работы с браузером:
  1. **Диалоги блокируют JS-поток.** Любая операция на странице зависает до обработки диалога. До этой работы у агента не было способа узнать, что диалог открыт — последующие вызовы инструментов зависали или выдавали неясные ошибки.
  2. **Iframe невидимы.** Агент мог видеть узлы iframe в DOM-снимке, но не мог кликать, вводить текст или выполнять eval внутри них — особенно в кросс-доменных (OOPIF) iframe, которые работают в отдельных процессах Chromium.


[PR #12550](https://github.com/NousResearch/hermes-agent/pull/12550) предлагал stateless-обёртку `browser_dialog`. Это не решает проблему обнаружения — это более чистый CDP-вызов для случаев, когда агент уже знает (по косвенным признакам), что диалог открыт. Закрыт как заменённый.
## Матрица возможностей бэкендов (проверено 2026-04-23)[​](#backend-capability-matrix-verified-live-2026-04-23 "Прямая ссылка на Матрицу возможностей бэкендов (проверено 2026-04-23)")
Используя одноразовые пробные скрипты против страницы с data-URL, которая вызывает alert в главном фрейме и в same-origin srcdoc iframe, а также кросс-доменный iframe `https://example.com`:
Бэкенд| Обнаружение диалогов| Ответ на диалоги| Дерево фреймов| OOPIF `Runtime.evaluate` через `browser_cdp(frame_id=...)`
|---|---|---|---|---
Локальный Chrome (`--remote-debugging-port`) / `/browser connect`| ✓| ✓ полный цикл| ✓| ✓
Browserbase| ✓ (через мост)| ✓ полный цикл (через мост)| ✓| ✓ (`document.title = "Example Domain"` проверено на реальном кросс-доменном iframe)
Camofox| ✗ нет CDP (только REST)| ✗| частично через DOM-снимок| ✗
**Как работает ответ Browserbase.** CDP-прокси Browserbase использует Playwright и автоматически закрывает нативные диалоги в течение ~10 мс, поэтому `Page.handleJavaScriptDialog` не успевает сработать. Для обхода этого супервизор внедряет скрипт-мост через `Page.addScriptToEvaluateOnNewDocument`, который переопределяет `window.alert`/`confirm`/`prompt` синхронным XHR-запросом к магическому хосту (`hermes-dialog-bridge.invalid`). `Fetch.enable` перехватывает эти XHR до того, как они достигают сети — диалог становится событием `Fetch.requestPaused`, которое перехватывает супервизор, а `respond_to_dialog` отвечает через `Fetch.fulfillRequest` с JSON-телом, которое декодирует внедрённый скрипт.
Конечный результат: с точки зрения страницы, `prompt()` по-прежнему возвращает строку, предоставленную агентом. С точки зрения агента, это тот же API `browser_dialog(action=...)` в любом случае. Протестировано end-to-end на реальных сессиях Browserbase — 4/4 (alert/prompt/confirm-accept/confirm-dismiss) проходят, включая возврат значения обратно в JS страницы.
Camofox остаётся неподдерживаемым в этом PR; планируется создание upstream-issue в `jo-inc/camofox-browser` с запросом конечной точки для опроса диалогов.
## Архитектура[​](#architecture "Прямая ссылка на Архитектуру")
### CDPSupervisor[​](#cdpsupervisor "Прямая ссылка на CDPSupervisor")
Одна задача `asyncio.Task`, выполняющаяся в фоновом потоке-демоне на каждый Hermes `task_id`. Поддерживает постоянное WebSocket-соединение с CDP-конечной точкой бэкенда. Хранит:
  * **Очередь диалогов** — `List[PendingDialog]` с `{id, type, message, default_prompt, session_id, opened_at}`
  * **Дерево фреймов** — `Dict[frame_id, FrameInfo]` с родительскими связями, URL, источником, признаком кросс-доменной дочерней сессии
  * **Карта сессий** — `Dict[session_id, SessionInfo]`, чтобы инструменты взаимодействия могли направлять запросы к нужной прикреплённой сессии для операций с OOPIF
  * **Последние ошибки консоли** — кольцевой буфер на 50 записей (для диагностики PR 2)


Подписывается при подключении:
  * `Page.enable` — `javascriptDialogOpening`, `frameAttached`, `frameNavigated`, `frameDetached`
  * `Runtime.enable` — `executionContextCreated`, `consoleAPICalled`, `exceptionThrown`
  * `Target.setAutoAttach {autoAttach: true, flatten: true}` — отслеживает дочерние OOPIF-цели; супервизор включает `Page`+`Runtime` на каждой


Потокобезопасный доступ к состоянию через snapshot-блокировку; синхронные обработчики инструментов читают замороженный снимок без ожидания.
### Жизненный цикл[​](#lifecycle "Прямая ссылка на Жизненный цикл")
  * **Запуск:** `SupervisorRegistry.get_or_start(task_id, cdp_url)` — вызывается `browser_navigate`, созданием сессии Browserbase, `/browser connect`. Идемпотентно.
  * **Остановка:** завершение сессии или `/browser disconnect`. Отменяет asyncio-задачу, закрывает WebSocket, удаляет состояние.
  * **Перепривязка:** если URL CDP изменился (пользователь переподключился к новому Chrome), остановите старый супервизор и запустите новый — никогда не используйте состояние повторно между разными конечными точками.


### Политика обработки диалогов[​](#dialog-policy "Прямая ссылка на Политику обработки диалогов")
Настраивается через `config.yaml` в разделе `browser.dialog_policy`:
  * **`must_respond`** (по умолчанию) — перехватывать, отображать в `browser_snapshot`, ждать явного вызова `browser_dialog(action=...)`. После 300-секундного таймаута безопасности без ответа — автоматически отклонить и записать в лог. Предотвращает зависание агента с ошибками.
  * `auto_dismiss` — записать и сразу отклонить; агент видит это постфактум через `browser_state` внутри `browser_snapshot`.
  * `auto_accept` — записать и принять (полезно для `beforeunload`, когда пользователь хочет чисто уйти со страницы).


Политика задаётся на задачу; в версии v1 нет переопределений для отдельных диалогов.
## Поверхность для агента (PR 1)[​](#agent-surface-pr-1 "Прямая ссылка на Поверхность для агента (PR 1)")
### Один новый инструмент[​](#one-new-tool "Прямая ссылка на Один новый инструмент")
[code]
    browser_dialog(action, prompt_text=None, dialog_id=None)
    
[/code]
  * `action="accept"` / `"dismiss"` — отвечает на указанный или единственный ожидающий диалог (обязательно)
  * `prompt_text=...` — текст для передачи в диалог `prompt()`
  * `dialog_id=...` — для разрешения неоднозначности, когда в очереди несколько диалогов (редкий случай)


Инструмент предназначен только для ответа. Агент читает ожидающие диалоги из вывода `browser_snapshot` перед вызовом.
### Расширение `browser_snapshot`[​](#browser_snapshot-extension "Прямая ссылка на Расширение browser_snapshot")
Добавляет три опциональных поля в существующий вывод снимка, когда подключён супервизор:
[code]
    {
      "pending_dialogs": [
        {"id": "d-1", "type": "alert", "message": "Hello", "opened_at": 1650000000.0}
      ],
      "recent_dialogs": [
        {"id": "d-1", "type": "alert", "message": "...", "opened_at": 1650000000.0,
         "closed_at": 1650000000.1, "closed_by": "remote"}
      ],
      "frame_tree": {
        "top": {"frame_id": "FRAME_A", "url": "https://example.com/", "origin": "https://example.com"},
        "children": [
          {"frame_id": "FRAME_B", "url": "about:srcdoc", "is_oopif": false},
          {"frame_id": "FRAME_C", "url": "https://ads.example.net/", "is_oopif": true, "session_id": "SID_C"}
        ],
        "truncated": false
      }
    }
    
[/code]
  * **`pending_dialogs`**: диалоги, которые в данный момент блокируют JS-поток страницы. Агент должен вызвать `browser_dialog(action=...)` для ответа. Пусто в Browserbase, потому что их CDP-прокси автоматически закрывает диалоги в течение ~10 мс.
  * **`recent_dialogs`**: кольцевой буфер до 20 недавно закрытых диалогов с тегом `closed_by` — `"agent"` (мы ответили), `"auto_policy"` (локальный auto_dismiss/auto_accept), `"watchdog"` (таймаут must_respond сработал) или `"remote"` (браузер/бэкенд закрыл его сам, например Browserbase). Так агенты на Browserbase всё равно видят, что произошло.
  * **`frame_tree`**: структура фреймов, включая кросс-доменные (OOPIF) дочерние элементы. Ограничено 30 записями и глубиной OOPIF 2, чтобы ограничить размер снимка на страницах с большим количеством рекламы. `truncated: true` показывает, когда лимиты были превышены; агентам, которым нужно полное дерево, можно использовать `browser_cdp` с `Page.getFrameTree`.


Никакой новой схемы инструментов для всего этого — агент читает снимок, который он и так уже запрашивает.
### Условная доступность[​](#availability-gating "Прямая ссылка на Условную доступность")
Обе поверхности включаются через `_browser_cdp_check` (супервизор может работать только когда CDP-конечная точка доступна). На Camofox / сессиях без бэкенда инструмент диалогов скрыт, а снимок не включает новые поля — без раздувания схемы.
## Взаимодействие с кросс-доменными iframe[​](#cross-origin-iframe-interaction "Прямая ссылка на Взаимодействие с кросс-доменными iframe")
Развивая работу по обнаружению диалогов, `browser_cdp(frame_id=...)` направляет CDP-вызовы (в частности `Runtime.evaluate`) через уже подключённый WebSocket супервизора, используя дочерний `sessionId` OOPIF. Агенты берут frame_id из `browser_snapshot.frame_tree.children[]`, где `is_oopif=true`, и передают их в `browser_cdp`. Для same-origin iframe (без выделенной CDP-сессии) агент использует `contentWindow`/`contentDocument` из top-level `Runtime.evaluate` — супервизор выдаёт ошибку, указывающую на этот запасной вариант, когда `frame_id` принадлежит не-OOPIF.
На Browserbase это ЕДИНСТВЕННЫЙ надёжный путь для взаимодействия с iframe — stateless CDP-соединения (открываемые при каждом вызове `browser_cdp`) натыкаются на истечение срока действия подписанных URL, в то время как долгоживущее соединение супервизора сохраняет валидную сессию.
## Camofox (дальнейшее развитие)[​](#camofox-follow-up "Прямая ссылка на Camofox (дальнейшее развитие)")
Планируется issue против `jo-inc/camofox-browser` с добавлением:
  * Playwright `page.on('dialog', handler)` на каждую сессию
  * Конечная точка опроса `GET /tabs/:tabId/dialogs`
  * `POST /tabs/:tabId/dialogs/:id` для принятия/отклонения
  * Конечная точка для просмотра дерева фреймов


## Затронутые файлы (PR 1)[​](#files-touched-pr-1 "Прямая ссылка на Затронутые файлы (PR 1)")
### Новые[​](#new "Прямая ссылка на Новые")
  * `tools/browser_supervisor.py` — `CDPSupervisor`, `SupervisorRegistry`, `PendingDialog`, `FrameInfo`
  * `tools/browser_dialog_tool.py` — обработчик инструмента `browser_dialog`
  * `tests/tools/test_browser_supervisor.py` — mock CDP WebSocket сервер + тесты жизненного цикла/состояния
  * `website/docs/developer-guide/browser-supervisor.md` — этот файл


### Изменённые[​](#modified "Прямая ссылка на Изменённые")
  * `toolsets.py` — регистрация `browser_dialog` в `browser`, `hermes-acp`, `hermes-api-server`, основных наборах инструментов (включается при доступности CDP)
  * `tools/browser_tool.py`
    * `browser_navigate` start-hook: если URL CDP разрешим, `SupervisorRegistry.get_or_start(task_id, cdp_url)`
    * `browser_snapshot` (строка ~1536): объединение состояния супервизора в возвращаемый payload
    * Обработчик `/browser connect`: перезапуск супервизора с новой конечной точкой
    * Хуки завершения сессии в `_cleanup_browser_session`
  * `hermes_cli/config.py` — добавление `browser.dialog_policy` и `browser.dialog_timeout_s` в `DEFAULT_CONFIG`
  * Документация: `website/docs/user-guide/features/browser.md`, `website/docs/reference/tools-reference.md`, `website/docs/reference/toolsets-reference.md`


## Нецелевые задачи[​](#non-goals "Прямая ссылка на Нецелевые задачи")
  * Обнаружение/взаимодействие для Camofox (пробел в вышестоящем проекте; отслеживается отдельно)
  * Потоковая передача событий диалогов/фреймов пользователю в реальном времени (потребовались бы хуки шлюза)
  * Сохранение истории диалогов между сессиями (только в памяти)
  * Индивидуальные политики для каждого iframe (агент может выразить это через `dialog_id`)
  * Замена `browser_cdp` — он остаётся запасным выходом для редких случаев (cookies, viewport, network throttling)


## Тестирование[​](#testing "Прямая ссылка на Тестирование")
Модульные тесты используют asyncio mock CDP-сервер, который реализует достаточно протокола для проверки всех переходов состояния: подключение, enable, навигация, срабатывание диалога, закрытие диалога, присоединение/отсоединение фрейма, присоединение дочерней цели, завершение сессии. E2E-тестирование с реальными бэкендами (Browserbase + локальный Chrome) выполняется вручную; пробные скрипты из исследования от 2026-04-23 хранятся в репозитории в `scripts/browser_supervisor_e2e.py`, чтобы любой мог перепроверить на новых версиях бэкендов.
  * [Проблема](#problem)
  * [Матрица возможностей бэкендов (проверено 2026-04-23)](#backend-capability-matrix-verified-live-2026-04-23)
  * [Архитектура](#architecture)
    * [CDPSupervisor](#cdpsupervisor)
    * [Жизненный цикл](#lifecycle)
    * [Политика обработки диалогов](#dialog-policy)
  * [Поверхность для агента (PR 1)](#agent-surface-pr-1)
    * [Один новый инструмент](#one-new-tool)
    * [Расширение `browser_snapshot`](#browser_snapshot-extension)
    * [Условная доступность](#availability-gating)
  * [Взаимодействие с кросс-доменными iframe](#cross-origin-iframe-interaction)
  * [Camofox (дальнейшее развитие)](#camofox-follow-up)
  * [Затронутые файлы (PR 1)](#files-touched-pr-1)
    * [Новые](#new)
    * [Изменённые](#modified)
  * [Нецелевые задачи](#non-goals)
  * [Тестирование](#testing)



<!-- Source: https://hermes-agent.nousresearch.com/docs/developer-guide/browser-supervisor -->
