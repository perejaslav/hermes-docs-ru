На этой странице
Отладка Node.js через --inspect + Chrome DevTools Protocol CLI.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Встроенный (устанавливается по умолчанию)  |
|Путь| `skills/software-development/node-inspect-debugger`  |
|Версия| `1.0.0`  |
|Автор| Hermes Agent  |
|Лицензия| MIT  |
|Теги| `debugging`, `nodejs`, `node-inspect`, `cdp`, `breakpoints`, `ui-tui`  |
|Связанные навыки| [`systematic-debugging`](</docs/user-guide/skills/bundled/software-development/software-development-systematic-debugging>), [`python-debugpy`](</docs/user-guide/skills/bundled/software-development/software-development-python-debugpy>), [`debugging-hermes-tui-commands`](</docs/user-guide/skills/bundled/software-development/software-development-debugging-hermes-tui-commands>)  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что видит агент в качестве инструкций, когда навык активен.
# Node.js Inspect Debugger
## Обзор[​](<#overview> "Прямая ссылка на Обзор")
Когда `console.log` недостаточно, управляйте встроенным V8 inspector'ом Node программно из терминала. Вы получаете настоящие точки останова, шаг с заходом/без захода/с выходом, просмотр стека вызовов, дамп локальных и замыкающих переменных, а также вычисление произвольных выражений в приостановленном фрейме.
Два инструмента — выбирайте:
  * **`node inspect`** — встроенный, без установки, REPL в CLI. Лучше всего для быстрых проверок.
  * **`ndb` / CDP через `chrome-remote-interface`** — скриптуемый из Node/Python; лучший выбор для автоматизации множества точек останова, сбора состояния между запусками или неинтерактивной отладки из цикла агента.


**Отдавайте предпочтение `node inspect`.** Он всегда доступен, и REPL работает быстро.
## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")
  * Node-тест падает, и нужно увидеть промежуточное состояние
  * ui-tui падает или ведёт себя неправильно, и нужно проверить состояние React/Ink до рендера
  * Дочерние процессы tui_gateway (`_SlashWorker`, PTY-мосты) работают некорректно
  * Нужно проверить значение в замыкании, до которого `console.log` не добраться без модификации кода
  * Производительность: подключиться к запущенному процессу, чтобы снять CPU-профиль или снапшот кучи


**Не используйте для:** того, что `console.log` решает менее чем за минуту. Отладка с точками останова — более тяжёлый метод; применяйте его, когда отдача действительно оправдана.
## Краткий справочник: REPL `node inspect`[​](<#quick-reference-node-inspect-repl> "Прямая ссылка на quick-reference-node-inspect-repl")
Запуск с остановкой на первой строке:
[code] 
    node inspect path/to/script.js  
    # или с tsx  
    node --inspect-brk $(which tsx) path/to/script.ts  
    
[/code]
Приглашение `debug>` принимает:
Команда| Действие  
|---|---  
`c` или `cont`| продолжить  
`n` или `next`| шаг без захода  
`s` или `step`| шаг с заходом  
`o` или `out`| шаг с выходом  
`pause`| приостановить выполняющийся код  
`sb('file.js', 42)`| установить точку останова в file.js, строка 42  
`sb(42)`| установить точку останова на строке 42 текущего файла  
`sb('functionName')`| срабатывать при вызове функции  
`cb('file.js', 42)`| удалить точку останова  
`breakpoints`| список всех точек останова  
`bt`| backtrace (стек вызовов)  
`list(5)`| показать 5 строк исходного кода вокруг текущей позиции  
`watch('expr')`| вычислять выражение на каждой паузе  
`watchers`| показать отслеживаемые выражения  
`repl`| войти в REPL в текущей области видимости (Ctrl+C для выхода из REPL)  
`exec expr`| вычислить выражение один раз  
`restart`| перезапустить скрипт  
`kill`| завершить скрипт  
`.exit`| выйти из отладчика  
**В подрежиме `repl`:** вводите любые JS-выражения, включая доступ к локальным переменным и переменным замыканий. `Ctrl+C` возвращает обратно в `debug>`.
## Подключение к запущенному процессу[​](<#attaching-to-a-running-process> "Прямая ссылка на Подключение к запущенному процессу")
Когда процесс уже запущен (например, долгоживущий dev-сервер или шлюз TUI):
[code] 
    # 1. Отправить SIGUSR1, чтобы включить inspector в существующем процессе  
    kill -SIGUSR1 <pid>  
    # Node выводит: Debugger listening on ws://127.0.0.1:9229/<uuid>  
      
    # 2. Подключить отладчик CLI  
    node inspect -p <pid>  
    # или по URL  
    node inspect ws://127.0.0.1:9229/<uuid>  
    
[/code]
Запуск процесса с inspector'ом с самого начала:
[code] 
    node --inspect script.js           # слушать на 127.0.0.1:9229, продолжить выполнение  
    node --inspect-brk script.js       # слушать И остановиться на первой строке  
    node --inspect=0.0.0.0:9230 script.js   # свой хост:порт  
    
[/code]
Для TypeScript через tsx:
[code] 
    node --inspect-brk --import tsx script.ts  
    # или старая версия tsx  
    node --inspect-brk -r tsx/cjs script.ts  
    
[/code]
## Программный CDP (скриптинг из терминала)[​](<#programmatic-cdp-scripting-from-terminal> "Прямая ссылка на Программный CDP \\(скриптинг из терминала\\)")
Когда нужно автоматизировать — установить много точек останова, захватить состояние области видимости, запрограммировать воспроизведение — используйте `chrome-remote-interface`:
[code] 
    npm i -g chrome-remote-interface        # или локально в проекте  
    # Запустите ваш целевой скрипт:  
    node --inspect-brk=9229 target.js &  
    
[/code]
Скрипт-драйвер (сохранить как `/tmp/cdp-debug.js`):
[code] 
    const CDP = require('chrome-remote-interface');  
      
    (async () => {  
      const client = await CDP({ port: 9229 });  
      const { Debugger, Runtime } = client;  
      
      Debugger.paused(async ({ callFrames, reason }) => {  
        const top = callFrames[0];  
        console.log(`PAUSED: ${reason} @ ${top.url}:${top.location.lineNumber + 1}`);  
      
        // Обход областей видимости для локальных переменных  
        for (const scope of top.scopeChain) {  
          if (scope.type === 'local' || scope.type === 'closure') {  
            const { result } = await Runtime.getProperties({  
              objectId: scope.object.objectId,  
              ownProperties: true,  
            });  
            for (const p of result) {  
              console.log(`  ${scope.type}.${p.name} =`, p.value?.value ?? p.value?.description);  
            }  
          }  
        }  
      
        // Вычисление выражения в приостановленном фрейме  
        const { result } = await Debugger.evaluateOnCallFrame({  
          callFrameId: top.callFrameId,  
          expression: 'typeof state !== "undefined" ? JSON.stringify(state) : "n/a"',  
        });  
        console.log('state =', result.value ?? result.description);  
      
        await Debugger.resume();  
      });  
      
      await Runtime.enable();  
      await Debugger.enable();  
      
      // Установка точки останова по регулярному выражению URL + строка  
      await Debugger.setBreakpointByUrl({  
        urlRegex: '.*app\\\\.tsx$',  
        lineNumber: 119,       // 0-индексация  
        columnNumber: 0,  
      });  
      
      await Runtime.runIfWaitingForDebugger();  
    })();  
    
[/code]
Запустите:
[code] 
    node /tmp/cdp-debug.js  
    
[/code]
Примечание для Hermes: `chrome-remote-interface` НЕ входит в `ui-tui/package.json`. Установите его во временную директорию, если не хотите засорять проект:
[code] 
    mkdir -p /tmp/cdp-tools && cd /tmp/cdp-tools && npm i chrome-remote-interface  
    NODE_PATH=/tmp/cdp-tools/node_modules node /tmp/cdp-debug.js  
    
[/code]
## Отладка Hermes ui-tui[​](<#debugging-hermes-ui-tui> "Прямая ссылка на Отладка Hermes ui-tui")
TUI построен на Ink + tsx. Два распространённых сценария:
### Отладка отдельного Ink-компонента в процессе разработки[​](<#debugging-a-single-ink-component-under-dev> "Прямая ссылка на Отладка отдельного Ink-компонента в процессе разработки")
В `ui-tui/package.json` есть `npm run dev` (tsx --watch). Добавьте `--inspect-brk`, запустив tsx напрямую:
[code] 
    cd /home/bb/hermes-agent/ui-tui  
    npm run build    # собрать dist/ один раз, чтобы не транспилировать при первой загрузке  
    node --inspect-brk dist/entry.js  
    # В другом терминале:  
    node inspect -p <node pid>  
    
[/code]
Затем внутри `debug>`:
[code] 
    sb('dist/app.js', 220)     # или там, где подозрительный рендер  
    cont  
    
[/code]
Когда выполнение остановится, `repl` → инспектируйте `props`, ссылки на state, значения обработчиков `useInput` и т.д.
### Отладка запущенного `hermes --tui`[​](<#debugging-a-running-hermes---tui> "Прямая ссылка на Отладка запущенного `hermes --tui`")
TUI запускает Node из Python CLI. Самый простой путь:
[code] 
    # 1. Запустить TUI  
    hermes --tui &  
    TUI_PID=$(pgrep -f 'ui-tui/dist/entry' | head -1)  
      
    # 2. Включить inspector на этом Node PID  
    kill -SIGUSR1 "$TUI_PID"  
      
    # 3. Найти WS URL  
    curl -s http://127.0.0.1:9229/json/list | jq -r '.[0].webSocketDebuggerUrl'  
      
    # 4. Подключиться  
    node inspect ws://127.0.0.1:9229/<uuid>  
    
[/code]
Взаимодействие с TUI (ввод в его окне) продолжает выполнение; ваш отладчик может остановить его на точке останова в любом `sb(...)`.
### Отладка дочерних процессов `_SlashWorker` / PTY[​](<#debugging-_slashworker--pty-child-processes> "Прямая ссылка на debugging-_slashworker--pty-child-processes")
Это Python, а не Node — используйте навык `python-debugpy`. Только части на Node (Ink UI, клиент tui_gateway, тесты tsx в `ui-tui/`) используют этот навык.
## Запуск тестов Vitest под отладчиком[​](<#running-vitest-tests-under-the-debugger> "Прямая ссылка на Запуск тестов Vitest под отладчиком")
[code] 
    cd /home/bb/hermes-agent/ui-tui  
    # Запустить один тестовый файл с остановкой на входе  
    node --inspect-brk ./node_modules/vitest/vitest.mjs run --no-file-parallelism src/app/foo.test.tsx  
    
[/code]
В другом терминале: `node inspect -p <pid>`, затем `sb('src/app/foo.tsx', 42)`, `cont`.
Используйте `--no-file-parallelism` (vitest) или `--runInBand` (jest), чтобы работал только один воркер — отладка пула процессов мучительна.
## Снапшоты кучи и CPU-профили (неинтерактивно)[​](<#heap-snapshots--cpu-profiles-non-interactive> "Прямая ссылка на Снапшоты кучи и CPU-профили \\(Неинтерактивно\\)")
Из CDP-драйвера выше замените Debugger на `HeapProfiler` / `Profiler`:
[code] 
    // CPU профиль на 5 секунд  
    await client.Profiler.enable();  
    await client.Profiler.start();  
    await new Promise(r => setTimeout(r, 5000));  
    const { profile } = await client.Profiler.stop();  
    require('fs').writeFileSync('/tmp/cpu.cpuprofile', JSON.stringify(profile));  
    // Открыть /tmp/cpu.cpuprofile в Chrome DevTools → вкладка Performance  
    
[/code]
[code] 
    // Снапшот кучи  
    await client.HeapProfiler.enable();  
    const chunks = [];  
    client.HeapProfiler.addHeapSnapshotChunk(({ chunk }) => chunks.push(chunk));  
    await client.HeapProfiler.takeHeapSnapshot({ reportProgress: false });  
    require('fs').writeFileSync('/tmp/heap.heapsnapshot', chunks.join(''));  
    
[/code]
## Частые проблемы[​](<#common-pitfalls> "Прямая ссылка на Частые проблемы")
  1. **Неверные номера строк в TS-исходниках.** Точки останова срабатывают на скомпилированном JS, а не на `.ts`. Либо (а) ставьте точки останова в собранных `dist/*.js`, либо (б) включите sourcemaps (`node --enable-source-maps`) и используйте `sb('src/app.tsx', N)` — но только с CDP-клиентами, поддерживающими sourcemaps. CLI `node inspect` их не поддерживает.
  2. **`--inspect` vs `--inspect-brk`.** `--inspect` запускает inspector, но не приостанавливает выполнение; ваш скрипт может пройти мимо первой точки останова, если вы подключитесь слишком поздно. Используйте `--inspect-brk`, когда нужно установить точки останова до выполнения любого кода.
  3. **Конфликты портов.** По умолчанию используется `9229`. Если несколько Node-процессов работают с inspector'ом, передайте `--inspect=0` (случайный порт) и прочитайте фактический URL из `/json/list`:
[code] curl -s http://127.0.0.1:9229/json/list   # список всех инспектируемых целей на хосте  
         
[/code]
  4. **Дочерние процессы.** `--inspect` на родительском процессе НЕ инспектирует его дочерние процессы. Используйте `NODE_OPTIONS='--inspect-brk' node parent.js`, чтобы передать параметр каждому дочернему процессу; учтите, что всем нужны уникальные порты (Node автоматически увеличивает порт, когда наследуется `NODE_OPTIONS='--inspect'`).
  5. **Фоновые завершения.** Если вы нажмёте `Ctrl+C` в `node inspect`, пока целевой процесс приостановлен, целевой процесс останется висеть в состоянии паузы. Либо сначала выполните `cont`, либо явно завершите целевой процесс через `kill`.
  6. **Запуск `node inspect` через терминал агента.** Это PTY-совместимый REPL. В Hermes запускайте его с `terminal(pty=true)` или `background=true` + `process(action='submit', data='...')`. Не-PTY режим переднего плана подойдёт для разовых команд, но не для интерактивного пошагового выполнения.
  7. **Безопасность.** `--inspect=0.0.0.0:9229` открывает возможность выполнения произвольного кода. Всегда привязывайтесь к `127.0.0.1` (значение по умолчанию), если только у вас не изолированная сеть.


## Контрольный список проверки[​](<#verification-checklist> "Прямая ссылка на Контрольный список проверки")
После настройки сеанса отладки проверьте:
  * `curl -s http://127.0.0.1:9229/json/list` возвращает именно ту цель, которую вы ожидаете
  * Первая точка останова действительно срабатывает (если нет — вы, вероятно, пропустили `--inspect-brk` или подключились после завершения выполнения)
  * Показ исходного кода на паузе отображает правильный файл (несовпадение = проблема с sourcemaps, см. проблему 1)
  * `exec process.pid` в `repl` возвращает PID, к которому вы намеревались подключиться


## Разовые рецепты[​](<#one-shot-recipes> "Прямая ссылка на Разовые рецепты")
**«Почему эта переменная undefined на строке X?»**
[code] 
    node --inspect-brk script.js &  
    node inspect -p $!  
    # debug>  
    sb('script.js', X)  
    cont  
    # paused. Теперь:  
    repl  
    > myVariable  
    > Object.keys(this)  
    
[/code]
**«Какой путь вызова ведёт в эту функцию?»**
[code] 
    debug> sb('suspectFn')  
    debug> cont  
    # остановились на входе  
    debug> bt  
    
[/code]
**«Эта асинхронная цепочка зависает — где?»**
[code] 
    # Запустите с --inspect (без -brk), дайте выполниться до зависания, затем:  
    debug> pause  
    debug> bt  
    # Теперь вы видите застрявший фрейм  
    
[/code]
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Обзор](<#overview>)
  * [Когда использовать](<#when-to-use>)
  * [Краткий справочник: REPL `node inspect`](<#quick-reference-node-inspect-repl>)
  * [Подключение к запущенному процессу](<#attaching-to-a-running-process>)
  * [Программный CDP (скриптинг из терминала)](<#programmatic-cdp-scripting-from-terminal>)
  * [Отладка Hermes ui-tui](<#debugging-hermes-ui-tui>)
    * [Отладка отдельного Ink-компонента в процессе разработки](<#debugging-a-single-ink-component-under-dev>)
    * [Отладка запущенного `hermes --tui`](<#debugging-a-running-hermes---tui>)
    * [Отладка дочерних процессов `_SlashWorker` / PTY](<#debugging-_slashworker--pty-child-processes>)
  * [Запуск тестов Vitest под отладчиком](<#running-vitest-tests-under-the-debugger>)
  * [Снапшоты кучи и CPU-профили (неинтерактивно)](<#heap-snapshots--cpu-profiles-non-interactive>)
  * [Частые проблемы](<#common-pitfalls>)
  * [Контрольный список проверки](<#verification-checklist>)
  * [Разовые рецепты](<#one-shot-recipes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-node-inspect-debugger -->
