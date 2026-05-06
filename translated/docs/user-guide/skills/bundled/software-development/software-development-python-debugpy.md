На этой странице
Отладка Python: pdb REPL + debugpy удалённо (DAP).
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Встроенный (установлен по умолчанию) |
|Путь| `skills/software-development/python-debugpy` |
|Версия| `1.0.0` |
|Автор| Hermes Agent |
|Лицензия| MIT |
|Теги| `отладка`, `python`, `pdb`, `debugpy`, `точки_останова`, `dap`, `post-mortem` |
|Связанные навыки| [`systematic-debugging`](</docs/user-guide/skills/bundled/software-development/software-development-systematic-debugging>), [`node-inspect-debugger`](</docs/user-guide/skills/bundled/software-development/software-development-node-inspect-debugger>), [`debugging-hermes-tui-commands`](</docs/user-guide/skills/bundled/software-development/software-development-debugging-hermes-tui-commands>) |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Именно эти инструкции видит агент, когда навык активен.
# Отладчик Python (pdb + debugpy)
## Обзор[​](<#overview> "Прямая ссылка на Обзор")
Три инструмента, выбираемых по ситуации:
Инструмент| Когда
---|---
**`breakpoint()` + pdb**| Локально, интерактивно, проще всего. Добавьте `breakpoint()` в исходный код, запустите обычным образом — получите REPL на этой строке.
**`python -m pdb`**| Запуск существующего скрипта под pdb без изменения исходного кода. Полезно для быстрой проверки.
**`debugpy`**| Удалённая / безголовая / «подключение к уже запущенному процессу» отладка. Использует протокол DAP, управляется из терминала, подходит для долгоживущих процессов (gateway, daemon, PTY-дочерние процессы).
**Начните с `breakpoint()`.** Это самое дешёвое решение, которое работает.
## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")
  * Тест падает, и трассировка не показывает, почему значение неверно
  * Нужно пройти по функции шаг за шагом и наблюдать за изменением коллекции
  * Долгоживущий процесс (hermes gateway, tui_gateway) работает некорректно, и вы не можете его перезапустить
  * Посмертный анализ: исключение возникло в коде, близком к production, и вы хотите изучить локальные переменные в месте сбоя
  * Дочерний процесс / подпроцесс (Python `_SlashWorker`, PTY bridge worker) является actual местом ошибки


**Не использовать для:** вещей, которые `print()` / `logging.debug` решают меньше чем за минуту, или того, что уже показывает `pytest -vv --tb=long --showlocals`.
## Краткий справочник по pdb[​](<#pdb-quick-reference> "Прямая ссылка на Краткий справочник по pdb")
Внутри любого приглашения pdb (`(Pdb)`):
Команда| Действие
---|---
`h` / `h cmd`| справка
`n`| следующая строка (шаг с обходом)
`s`| шаг с заходом
`r`| выход из текущей функции
`c`| продолжение
`unt N`| продолжать до строки N
`j N`| перейти к строке N (только в той же функции)
`l` / `ll`| показать исходный код вокруг текущей строки / всю функцию
`w`| где (стек вызовов)
`u` / `d`| переместиться вверх / вниз по стеку
`a`| вывести аргументы текущей функции
`p expr` / `pp expr`| вывести / красиво вывести выражение
`display expr`| автоматически выводить выражение на каждой остановке
`b file:line`| установить точку останова
`b func`| остановиться при входе в функцию
`b file:line, cond`| условная точка останова
`cl N`| удалить точку останова N
`tbreak file:line`| одноразовая точка останова
`!stmt`| выполнить произвольный Python (включая присваивания)
`interact`| перейти в полноценный Python REPL в текущей области видимости (Ctrl+D для выхода)
`q`| выход
Команда `interact` — самая мощная: вы можете импортировать что угодно, исследовать сложные объекты, даже вызывать методы, изменяющие состояние. Локальные переменные по умолчанию доступны только для чтения; используйте `!x = 42` из приглашения `(Pdb)` для изменения.
## Рецепт 1: Локальная точка останова[​](<#recipe-1-local-breakpoint> "Прямая ссылка на Рецепт 1: Локальная точка останова")
Проще всего. Отредактируйте файл:
[code] 
    def compute(x, y):  
        result = some_helper(x)  
        breakpoint()           # <-- drops into pdb here  
        return result + y  
    
[/code]
Запустите код обычным образом. Вы окажетесь на строке с `breakpoint()` с полным доступом к локальным переменным.
**Не забудьте удалить `breakpoint()` перед коммитом.** Используйте `git diff` или pre-commit grep:
[code] 
    rg -n 'breakpoint\\(\\)' --type py  
    
[/code]
## Рецепт 2: Запуск скрипта под pdb (без изменения исходного кода)[​](<#recipe-2-launch-a-script-under-pdb-no-source-edits> "Прямая ссылка на Рецепт 2: Запуск скрипта под pdb \\(без изменения исходного кода\\)")
[code] 
    python -m pdb path/to/script.py arg1 arg2  
    # Lands at first line of script  
    (Pdb) b path/to/script.py:42  
    (Pdb) c  
    
[/code]
## Рецепт 3: Отладка pytest-теста[​](<#recipe-3-debug-a-pytest-test> "Прямая ссылка на Рецепт 3: Отладка pytest-теста")
Тестовый раннер Hermes и pytest поддерживают это:
[code] 
    # Drop to pdb on failure (or on any raised exception):  
    scripts/run_tests.sh tests/path/to/test_file.py::test_name --pdb  
      
    # Drop to pdb at the START of the test:  
    scripts/run_tests.sh tests/path/to/test_file.py::test_name --trace  
      
    # Show locals in tracebacks without pdb:  
    scripts/run_tests.sh tests/path/to/test_file.py --showlocals --tb=long  
    
[/code]
Примечание: `scripts/run_tests.sh` по умолчанию использует xdist (`-n 4`), а pdb НЕ работает под xdist. Добавьте `-p no:xdist` или запустите один тест с `-n 0`:
[code] 
    scripts/run_tests.sh tests/foo_test.py::test_bar --pdb -p no:xdist  
    # or  
    source .venv/bin/activate  
    python -m pytest tests/foo_test.py::test_bar --pdb  
    
[/code]
Это обходит гарантии изолированной среды — нормально для отладки, но перед отправкой перезапустите под обёрткой для подтверждения.
## Рецепт 4: Посмертный анализ любого исключения[​](<#recipe-4-post-mortem-on-any-exception> "Прямая ссылка на Рецепт 4: Посмертный анализ любого исключения")
[code] 
    import pdb, sys  
    try:  
        run_the_thing()  
    except Exception:  
        pdb.post_mortem(sys.exc_info()[2])  
    
[/code]
Или оберните весь скрипт:
[code] 
    python -m pdb -c continue script.py  
    # When it crashes, pdb catches it and you're in the frame of the exception  
    
[/code]
Или установите глобальный хук в repl/jupyter:
[code] 
    import sys  
    def excepthook(etype, value, tb):  
        import pdb; pdb.post_mortem(tb)  
    sys.excepthook = excepthook  
    
[/code]
## Рецепт 5: Удалённая отладка с debugpy (подключение к работающему процессу)[​](<#recipe-5-remote-debug-with-debugpy-attach-to-running-process> "Прямая ссылка на Рецепт 5: Удалённая отладка с debugpy \\(подключение к работающему процессу\\)")
Для долгоживущих процессов: Hermes gateway, tui_gateway, демон, процесс, который уже работает некорректно и не может быть чисто перезапущен.
### Настройка[​](<#setup> "Прямая ссылка на Настройка")
[code] 
    source /home/bb/hermes-agent/.venv/bin/activate  
    pip install debugpy  
    
[/code]
### Паттерн A: Изменение исходного кода — процесс ждёт отладчик при запуске[​](<#pattern-a-source-edit--process-waits-for-debugger-at-launch> "Прямая ссылка на Паттерн A: Изменение исходного кода — процесс ждёт отладчик при запуске")
Добавьте в начале точки входа (или внутри функции, которую хотите отладить):
[code] 
    import debugpy  
    debugpy.listen(("127.0.0.1", 5678))  
    print("debugpy listening on 5678, waiting for client...", flush=True)  
    debugpy.wait_for_client()  
    debugpy.breakpoint()       # optional: pause immediately once attached  
    
[/code]
Запустите процесс; он заблокируется на `wait_for_client()`.
### Паттерн B: Без изменения исходного кода — запуск с `-m debugpy`[​](<#pattern-b-no-source-edit--launch-with--m-debugpy> "Прямая ссылка на Паттерн B: Без изменения исходного кода — запуск с `-m debugpy`")
[code] 
    python -m debugpy --listen 127.0.0.1:5678 --wait-for-client your_script.py arg1  
    
[/code]
Аналогично для точек входа в виде модуля:
[code] 
    python -m debugpy --listen 127.0.0.1:5678 --wait-for-client -m your.module  
    
[/code]
### Паттерн C: Подключение к уже запущенному процессу[​](<#pattern-c-attach-to-an-already-running-process> "Прямая ссылка на Паттерн C: Подключение к уже запущенному процессу")
Требует PID и предустановленный debugpy в окружении целевого процесса:
[code] 
    python -m debugpy --listen 127.0.0.1:5678 --pid <pid>  
    # debugpy injects itself into the process. Then attach a client as below.  
    
[/code]
Некоторые ядра/настройки безопасности блокируют внедрение на основе ptrace (`/proc/sys/kernel/yama/ptrace_scope`). Исправление:
[code] 
    echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope  
    
[/code]
### Подключение клиента из терминала[​](<#connecting-a-client-from-the-terminal> "Прямая ссылка на Подключение клиента из терминала")
Самый простой терминальный DAP-клиент — это CLI VS Code или небольшой скрипт. Внутри Hermes у вас есть два практических варианта:
**Вариант 1: Собственный CLI REPL `debugpy`** — не официальная функция, а крошечный DAP-клиентский скрипт:
[code] 
    # /tmp/dap_client.py  
    import socket, json, itertools, time, sys  
      
    HOST, PORT = "127.0.0.1", 5678  
    s = socket.create_connection((HOST, PORT))  
    seq = itertools.count(1)  
      
    def send(msg):  
        msg["seq"] = next(seq)  
        body = json.dumps(msg).encode()  
        s.sendall(f"Content-Length: {len(body)}\\r\\n\\r\\n".encode() + body)  
      
    def recv():  
        header = b""  
        while b"\\r\\n\\r\\n" not in header:  
            header += s.recv(1)  
        length = int(header.decode().split("Content-Length:")[1].split("\\r\\n")[0].strip())  
        body = b""  
        while len(body) < length:  
            body += s.recv(length - len(body))  
        return json.loads(body)  
      
    send({"type": "request", "command": "initialize", "arguments": {"adapterID": "python"}})  
    print(recv())  
    send({"type": "request", "command": "attach", "arguments": {}})  
    print(recv())  
    send({"type": "request", "command": "setBreakpoints",  
          "arguments": {"source": {"path": sys.argv[1]},  
                        "breakpoints": [{"line": int(sys.argv[2])}]}})  
    print(recv())  
    send({"type": "request", "command": "configurationDone"})  
    # ... loop reading events and sending continue/stepIn/etc.  
    
[/code]
Это нормально для разовой автоматизации, но неудобно как интерактивный интерфейс.
**Вариант 2: Подключение из VS Code / Cursor / Zed** — если у пользователя открыт один из них, он может добавить `launch.json`:
[code] 
    {  
      "name": "Attach to Hermes",  
      "type": "debugpy",  
      "request": "attach",  
      "connect": { "host": "127.0.0.1", "port": 5678 },  
      "justMyCode": false,  
      "pathMappings": [  
        { "localRoot": "${workspaceFolder}", "remoteRoot": "/home/bb/hermes-agent" }  
      ]  
    }  
    
[/code]
**Вариант 3: Откажитесь от DAP, используйте `remote-pdb`** — обычно это то, что вам на самом деле нужно от терминального агента:
[code] 
    pip install remote-pdb  
    
[/code]
В вашем коде:
[code] 
    from remote_pdb import set_trace  
    set_trace(host="127.0.0.1", port=4444)   # blocks until connection  
    
[/code]
Затем из терминала:
[code] 
    nc 127.0.0.1 4444  
    # You get a (Pdb) prompt exactly as if debugging locally.  
    
[/code]
`remote-pdb` — самый чистый выбор, удобный для агента, когда протокол DAP от `debugpy` избыточен. Используйте `debugpy` только когда вам действительно нужна интеграция с IDE.
## Отладка процессов, специфичных для Hermes[​](<#debugging-hermes-specific-processes> "Прямая ссылка на Отладка процессов, специфичных для Hermes")
### Тесты[​](<#tests> "Прямая ссылка на Тесты")
См. Рецепт 3. Всегда добавляйте `-p no:xdist` или запускайте отдельные тесты без xdist.
### `run_agent.py` / CLI — одноразовый запуск[​](<#run_agentpy--cli--one-shot> "Прямая ссылка на run_agentpy--cli--one-shot")
Проще всего: добавьте `breakpoint()` рядом с подозрительной строкой, затем запустите `hermes` обычным образом. Управление вернётся в ваш терминал в точке остановки.
### Подпроцесс `tui_gateway` (запускается `hermes --tui`)[​](<#tui_gateway-subprocess-spawned-by-hermes---tui> "Прямая ссылка на tui_gateway-subprocess-spawned-by-hermes---tui")
Gateway работает как дочерний процесс Node TUI. Варианты:
**A. Изменение исходного кода gateway:**
[code] 
    # tui_gateway/server.py near the top of serve()  
    import debugpy  
    debugpy.listen(("127.0.0.1", 5678))  
    debugpy.wait_for_client()  
    
[/code]
Запустите `hermes --tui`. TUI будет выглядеть замороженным (его бэкенд ожидает). Подключите клиент; выполнение возобновится, когда вы нажмёте `continue`.
**B. Использование `remote-pdb` в конкретном обработчике:**
[code] 
    from remote_pdb import set_trace  
    set_trace(host="127.0.0.1", port=4444)   # in the RPC handler you want to trap  
    
[/code]
Вызовите соответствующую слэш-команду из TUI, затем `nc 127.0.0.1 4444` в другом терминале.
### Подпроцесс `_SlashWorker`[​](<#_slashworker-subprocess> "Прямая ссылка на _slashworker-subprocess")
Тот же паттерн — `remote-pdb` с `set_trace()` внутри пути `exec` рабочего процесса. Рабочий процесс сохраняется между слэш-командами, поэтому первый запуск блокируется до вашего подключения; последующие слэш-команды проходят обычно, если вы не активируете точку останова снова.
### Gateway (`gateway/run.py`)[​](<#gateway-gatewayrunpy> "Прямая ссылка на gateway-gatewayrunpy")
Долгоживущий процесс. Используйте `remote-pdb` в обработчике или `debugpy` с `--wait-for-client`, если вы всё равно перезапускаете gateway.
## Частые проблемы[​](<#common-pitfalls> "Прямая ссылка на Частые проблемы")
  1. **pdb под pytest-xdist молча ничего не делает.** Вы не увидите приглашения, тест просто зависнет. Всегда используйте `-p no:xdist` или `-n 0`.
  2. **`breakpoint()` в CI / не-TTY контекстах вешает процесс.** Безопасно локально; никогда не коммитьте это. Добавьте pre-commit grep как страховку.
  3. **`PYTHONBREAKPOINT=0`** отключает все вызовы `breakpoint()`. Проверьте переменную окружения, если ваша точка останова не срабатывает:
[code] echo $PYTHONBREAKPOINT  
          
[/code]
  4. **`debugpy.listen` блокирует только если вы также вызвали `wait_for_client()`.** Без неё выполнение продолжается, и ваша первая точка останова может сработать до подключения клиента.
  5. **Подключение к PID не работает на усиленных ядрах.** `ptrace_scope=1` (по умолчанию в Ubuntu) разрешает ptrace только дочерних процессов того же пользователя. Обход: `echo 0 > /proc/sys/kernel/yama/ptrace_scope` (требуются права root) или запускайте под `debugpy` с самого начала.
  6. **Потоки.** `pdb` отлаживает только текущий поток. Для многопоточного кода используйте `debugpy` (DAP с поддержкой потоков) или установите `threading.settrace()` для каждого потока.
  7. **asyncio.** `pdb` работает в корутинах, но `await` внутри pdb требует Python 3.13+ или `await` из режима `interact` на старых версиях. Для 3.11/3.12 используйте трюки с `asyncio.run_coroutine_threadsafe` или `!stmt`-основанные await через `asyncio.ensure_future`.
  8. **`scripts/run_tests.sh` удаляет учётные данные и устанавливает `HOME=<tmpdir>`.** Если ваша ошибка зависит от конфигурации пользователя или реальных API-ключей, она не воспроизведётся под обёрткой. Сначала отлаживайте с чистым `pytest` для воспроизведения, затем перепроверьте под обёрткой.
  9. **Форки / multiprocessing.** pdb не следит за форками. Каждый дочерний процесс требует собственного `breakpoint()` или `set_trace()`. Для подагентов Hermes отлаживайте по одному процессу за раз.


## Контрольный список проверки[​](<#verification-checklist> "Прямая ссылка на Контрольный список проверки")
  * После `pip install debugpy` проверьте: `python -c "import debugpy; print(debugpy.__version__)"`
  * Для удалённой отладки проверьте, что порт действительно слушает: `ss -tlnp | grep 5678`
  * Первая точка останова действительно срабатывает (если нет, вероятно, установлено `PYTHONBREAKPOINT=0`, вы под xdist или выполнение завершилось до подключения)
  * `where` / `w` показывает ожидаемый стек вызовов
  * Очистка после отладки: никаких забытых `breakpoint()` / `set_trace()` в закоммиченном коде
[code] rg -n 'breakpoint\\(\\)|set_trace\\(|debugpy\\.listen' --type py  
        
[/code]


## Одноразовые рецепты[​](<#one-shot-recipes> "Прямая ссылка на Одноразовые рецепты")
**«Почему в этом словаре отсутствует ключ?»**
[code] 
    # add above the KeyError site  
    breakpoint()  
    # then in pdb:  
    (Pdb) pp d  
    (Pdb) pp list(d.keys())  
    (Pdb) w                # how did we get here  
    
[/code]
**«Этот тест проходит изолированно, но падает в наборе тестов.»**
[code] 
    scripts/run_tests.sh tests/the_test.py --pdb -p no:xdist  
    # But if it only fails WITH other tests:  
    source .venv/bin/activate  
    python -m pytest tests/ -x --pdb -p no:xdist  
    # Now it pdb-traps at the exact failing test after state accumulated.  
    
[/code]
**«Мой асинхронный обработчик взаимоблокируется.»**
[code] 
    # Add at handler entry  
    import remote_pdb; remote_pdb.set_trace(host="127.0.0.1", port=4444)  
    
[/code]
Запустите обработчик. `nc 127.0.0.1 4444`, затем `w` чтобы увидеть приостановленный фрейм, `!import asyncio; asyncio.all_tasks()` чтобы увидеть, что ещё ожидает выполнения.
**«Посмертный анализ сбоя в дочернем процессе Ink / подпроцессе.»**
[code] 
    PYTHONFAULTHANDLER=1 python -m pdb -c continue path/to/entrypoint.py  
    # On crash, pdb lands at the frame of the exception with full locals  
    
[/code]
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Обзор](<#overview>)
  * [Когда использовать](<#when-to-use>)
  * [Краткий справочник по pdb](<#pdb-quick-reference>)
  * [Рецепт 1: Локальная точка останова](<#recipe-1-local-breakpoint>)
  * [Рецепт 2: Запуск скрипта под pdb (без изменения исходного кода)](<#recipe-2-launch-a-script-under-pdb-no-source-edits>)
  * [Рецепт 3: Отладка pytest-теста](<#recipe-3-debug-a-pytest-test>)
  * [Рецепт 4: Посмертный анализ любого исключения](<#recipe-4-post-mortem-on-any-exception>)
  * [Рецепт 5: Удалённая отладка с debugpy (подключение к работающему процессу)](<#recipe-5-remote-debug-with-debugpy-attach-to-running-process>)
    * [Настройка](<#setup>)
    * [Паттерн A: Изменение исходного кода — процесс ждёт отладчик при запуске](<#pattern-a-source-edit--process-waits-for-debugger-at-launch>)
    * [Паттерн B: Без изменения исходного кода — запуск с `-m debugpy`](<#pattern-b-no-source-edit--launch-with--m-debugpy>)
    * [Паттерн C: Подключение к уже запущенному процессу](<#pattern-c-attach-to-an-already-running-process>)
    * [Подключение клиента из терминала](<#connecting-a-client-from-the-terminal>)
  * [Отладка процессов, специфичных для Hermes](<#debugging-hermes-specific-processes>)
    * [Тесты](<#tests>)
    * [`run_agent.py` / CLI — одноразовый запуск](<#run_agentpy--cli--one-shot>)
    * [`tui_gateway` подпроцесс (запускается `hermes --tui`)](<#tui_gateway-subprocess-spawned-by-hermes---tui>)
    * [Подпроцесс `_SlashWorker`](<#_slashworker-subprocess>)
    * [Gateway (`gateway/run.py`)](<#gateway-gatewayrunpy>)
  * [Частые проблемы](<#common-pitfalls>)
  * [Контрольный список проверки](<#verification-checklist>)
  * [Одноразовые рецепты](<#one-shot-recipes>)


<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-python-debugpy -->
