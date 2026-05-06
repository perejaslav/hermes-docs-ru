На этой странице
Интерактивный Python через живой Jupyter-ядро (hamelnb).
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |   |
|---|---|
|Источник| Встроенный (установлен по умолчанию)  |
|Путь| `skills/data-science/jupyter-live-kernel`  |
|Версия| `1.0.0`  |
|Автор| Hermes Agent  |
|Лицензия| MIT  |
|Теги| `jupyter`, `notebook`, `repl`, `data-science`, `exploration`, `iterative`  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
> info
> Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.

# Jupyter Live Kernel (hamelnb)
Предоставляет вам **интерактивную REPL-среду Python** через живое Jupyter-ядро. Переменные сохраняются между запусками. Используйте этот навык вместо `execute_code`, когда нужно накапливать состояние постепенно, исследовать API, анализировать DataFrame или итеративно дорабатывать сложный код.
## Когда использовать этот навык vs другие инструменты[​](<#when-to-use-this-vs-other-tools> "Прямая ссылка на Когда использовать этот навык vs другие инструменты")
| Инструмент | Когда использовать  |
|---|---|
| **Этот навык** | Итеративное исследование, состояние между шагами, наука о данных, ML, «дай-ка попробую и проверю»  |
| `execute_code` | Одноразовые скрипты, которым нужен доступ к инструментам Hermes (web_search, файловые операции). Без сохранения состояния.  |
| `terminal` | Команды оболочки, сборка, установка, git, управление процессами  |
| **Эмпирическое правило:** Если вы хотели бы использовать Jupyter notebook для задачи — используйте этот навык. |
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  1. **uv** должен быть установлен (проверка: `which uv`)
  2. **JupyterLab** должен быть установлен: `uv tool install jupyterlab`
  3. Должен быть запущен Jupyter-сервер (см. Настройку ниже)


## Настройка[​](<#setup> "Прямая ссылка на Настройка")
Расположение скрипта hamelnb:
[code] 
    SCRIPT="$HOME/.agent-skills/hamelnb/skills/jupyter-live-kernel/scripts/jupyter_live_kernel.py"  
    
[/code]
Если репозиторий ещё не склонирован:
[code] 
    git clone https://github.com/hamelsmu/hamelnb.git ~/.agent-skills/hamelnb  
    
[/code]
### Запуск JupyterLab[​](<#starting-jupyterlab> "Прямая ссылка на Запуск JupyterLab")
Проверьте, не запущен ли уже сервер:
[code] 
    uv run "$SCRIPT" servers  
    
[/code]
Если серверов не найдено, запустите один:
[code] 
    jupyter-lab --no-browser --port=8888 --notebook-dir=$HOME/notebooks \  
      --IdentityProvider.token='' --ServerApp.password='' > /tmp/jupyter.log 2>&1 &  
    sleep 3  
    
[/code]
Примечание: Токен/пароль отключены для локального доступа агента. Сервер работает в фоновом режиме без графического интерфейса.
### Создание Notebook для использования в качестве REPL[​](<#creating-a-notebook-for-repl-use> "Прямая ссылка на Создание Notebook для использования в качестве REPL")
Если вам нужна просто REPL-среда (нет существующего notebook), создайте минимальный файл notebook:
[code] 
    mkdir -p ~/notebooks  
    
[/code]
Запишите минимальный JSON-файл .ipynb с одной пустой ячейкой кода, затем запустите сессию ядра через Jupyter REST API:
[code] 
    curl -s -X POST http://127.0.0.1:8888/api/sessions \  
      -H "Content-Type: application/json" \  
      -d '{"path":"scratch.ipynb","type":"notebook","name":"scratch.ipynb","kernel":{"name":"python3"}}'  
    
[/code]
## Основной рабочий процесс[​](<#core-workflow> "Прямая ссылка на Основной рабочий процесс")
Все команды возвращают структурированный JSON. Всегда используйте `--compact` для экономии токенов.
### 1. Обнаружение серверов и notebooks[​](<#1-discover-servers-and-notebooks> "Прямая ссылка на 1. Обнаружение серверов и notebooks")
[code] 
    uv run "$SCRIPT" servers --compact  
    uv run "$SCRIPT" notebooks --compact  
    
[/code]
### 2. Выполнение кода (основная операция)[​](<#2-execute-code-primary-operation> "Прямая ссылка на 2. Выполнение кода (основная операция)")
[code] 
    uv run "$SCRIPT" execute --path <notebook.ipynb> --code '<python code>' --compact  
    
[/code]
Состояние сохраняется между вызовами execute. Переменные, импорты, объекты — всё сохраняется.
Многострочный код работает с экранированием $'...':
[code] 
    uv run "$SCRIPT" execute --path scratch.ipynb --code $'import os\nfiles = os.listdir(".")\nprint(f"Found {len(files)} files")' --compact  
    
[/code]
### 3. Просмотр активных переменных[​](<#3-inspect-live-variables> "Прямая ссылка на 3. Просмотр активных переменных")
[code] 
    uv run "$SCRIPT" variables --path <notebook.ipynb> list --compact  
    uv run "$SCRIPT" variables --path <notebook.ipynb> preview --name <varname> --compact  
    
[/code]
### 4. Редактирование ячеек notebook[​](<#4-edit-notebook-cells> "Прямая ссылка на 4. Редактирование ячеек notebook")
[code] 
    # Просмотр текущих ячеек  
    uv run "$SCRIPT" contents --path <notebook.ipynb> --compact  
      
    # Вставка новой ячейки  
    uv run "$SCRIPT" edit --path <notebook.ipynb> insert \  
      --at-index <N> --cell-type code --source '<code>' --compact  
      
    # Замена содержимого ячейки (используйте cell-id из вывода contents)  
    uv run "$SCRIPT" edit --path <notebook.ipynb> replace-source \  
      --cell-id <id> --source '<new code>' --compact  
      
    # Удаление ячейки  
    uv run "$SCRIPT" edit --path <notebook.ipynb> delete --cell-id <id> --compact  
    
[/code]
### 5. Верификация (перезапуск и выполнение всего)[​](<#5-verification-restart--run-all> "Прямая ссылка на 5. Верификация (перезапуск и выполнение всего)")
Используйте только когда пользователь просит выполнить чистую верификацию или вам нужно убедиться, что notebook выполняется целиком сверху вниз:
[code] 
    uv run "$SCRIPT" restart-run-all --path <notebook.ipynb> --save-outputs --compact  
    
[/code]
## Практические советы из опыта[​](<#practical-tips-from-experience> "Прямая ссылка на Практические советы из опыта")
  1. **Первое выполнение после запуска сервера может завершиться тайм-аутом** — ядру нужно время для инициализации. Если возникает тайм-аут, просто повторите попытку.
  2. **Python ядра — это Python JupyterLab** — пакеты должны быть установлены в этом окружении. Если вам нужны дополнительные пакеты, сначала установите их в окружение инструмента JupyterLab.
  3. **Флаг --compact значительно экономит токены** — всегда используйте его. Без него JSON-вывод может быть очень многословным.
  4. **Для чистого использования REPL** создайте scratch.ipynb и не заморачивайтесь с редактированием ячеек. Просто используйте `execute` многократно.
  5. **Порядок аргументов имеет значение** — флаги подкоманд, такие как `--path`, ставятся ПЕРЕД под-подкомандой. Например: `variables --path nb.ipynb list`, а не `variables list --path nb.ipynb`.
  6. **Если сессия ещё не существует**, нужно запустить её через REST API (см. раздел Настройка). Инструмент не может выполнять код без активной сессии ядра.
  7. **Ошибки возвращаются в формате JSON** с traceback — читайте поля `ename` и `evalue`, чтобы понять, что пошло не так.
  8. **Иногда возникают тайм-ауты websocket** — некоторые операции могут не выполниться с первой попытки, особенно после перезапуска ядра. Повторите попытку один раз, прежде чем эскалировать.


## Тайм-ауты по умолчанию[​](<#timeout-defaults> "Прямая ссылка на Тайм-ауты по умолчанию")
Скрипт имеет тайм-аут по умолчанию 30 секунд на одно выполнение. Для длительных операций передавайте `--timeout 120`. Используйте щедрые тайм-ауты (60+) для начальной настройки или тяжёлых вычислений.
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать этот навык vs другие инструменты](<#when-to-use-this-vs-other-tools>)
  * [Предварительные требования](<#prerequisites>)
  * [Настройка](<#setup>)
    * [Запуск JupyterLab](<#starting-jupyterlab>)
    * [Создание Notebook для использования в качестве REPL](<#creating-a-notebook-for-repl-use>)
  * [Основной рабочий процесс](<#core-workflow>)
    * [1. Обнаружение серверов и notebooks](<#1-discover-servers-and-notebooks>)
    * [2. Выполнение кода (основная операция)](<#2-execute-code-primary-operation>)
    * [3. Просмотр активных переменных](<#3-inspect-live-variables>)
    * [4. Редактирование ячеек notebook](<#4-edit-notebook-cells>)
    * [5. Верификация (перезапуск и выполнение всего)](<#5-verification-restart--run-all>)
  * [Практические советы из опыта](<#practical-tips-from-experience>)
  * [Тайм-ауты по умолчанию](<#timeout-defaults>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/data-science/data-science-jupyter-live-kernel -->
