На этой странице

Это руководство проведёт вас через создание полноценного плагина Hermes с нуля. К концу у вас будет рабочий плагин с несколькими инструментами, хуками жизненного цикла, поставляемыми файлами данных и встроенным скиллом — всё, что поддерживает система плагинов.

Не уверены, какой гайд вам нужен?

Hermes имеет несколько различных расширяемых интерфейсов — одни используют Python API `register_*`, другие управляются через конфиг или drop-in директории. Сначала воспользуйтесь этой картой:

| Если вы хотите добавить… | Читать |
|---|---|
| Пользовательские инструменты, хуки, слеш-команды, скиллы или CLI-подкоманды | **Это руководство** (общая поверхность плагинов) |
| **LLM / inference бэкенд** (новый провайдер) | [Model Provider Plugins](</docs/developer-guide/model-provider-plugin>) |
| **Канал-шлюз** (Discord/Telegram/IRC/Teams/etc.) | [Adding Platform Adapters](</docs/developer-guide/adding-platform-adapters>) |
| **Бэкенд памяти** (Honcho/Mem0/Supermemory/etc.) | [Memory Provider Plugins](</docs/developer-guide/memory-provider-plugin>) |
| **Движок сжатия контекста** | [Context Engine Plugins](</docs/developer-guide/context-engine-plugin>) |
| **Бэкенд генерации изображений** | [Image Generation Provider Plugins](</docs/developer-guide/image-gen-provider-plugin>) |
| **TTS бэкенд** (любой CLI — Piper, VoxCPM, Kokoro, клонирование голоса, …) | [TTS custom command providers](</docs/user-guide/features/tts#custom-command-providers>) — конфиг-управляемый, Python не нужен |
| **STT бэкенд** (свой whisper / ASR CLI) | [Voice Message Transcription](</docs/user-guide/features/tts#voice-message-transcription-stt>) — установите `HERMES_LOCAL_STT_COMMAND` как shell-шаблон |
| **Внешние инструменты через MCP** (файловая система, GitHub, Linear, любой MCP-сервер) | [MCP](</docs/user-guide/features/mcp>) — объявите `mcp_servers.<name>` в `config.yaml` |
| **Хуки событий шлюза** (срабатывают при запуске, событиях сессии, командах) | [Event Hooks](</docs/user-guide/features/hooks#gateway-event-hooks>) — поместите `HOOK.yaml` + `handler.py` в `~/.hermes/hooks/<name>/` |
| **Shell-хуки** (выполнить shell-команду по событиям) | [Shell Hooks](</docs/user-guide/features/hooks#shell-hooks>) — объявите в секции `hooks:` в `config.yaml` |
| **Дополнительные источники скиллов** (пользовательские GitHub репозитории, частные индексы скиллов) | [Skills](</docs/user-guide/features/skills>) — `hermes skills tap add <repo>` · [Publishing a tap](</docs/user-guide/features/skills#publishing-a-custom-skill-tap>) |
| Полноценный **core** inference-провайдер (не плагин) | [Adding Providers](</docs/developer-guide/adding-providers>) |

Полную таблицу всех точек расширения, включая конфиг-управляемые (TTS, STT, MCP, shell-хуки) и drop-in директории (хуки шлюза), см. в [Pluggable interfaces table](</docs/user-guide/features/plugins#pluggable-interfaces--where-to-go-for-each>).

## Что вы создадите[​](<#what-youre-building> "Прямая ссылка на Что вы создадите")

Плагин **калькулятор** с двумя инструментами:

* `calculate` — вычисление математических выражений (`2**16`, `sqrt(144)`, `pi * 5**2`)
* `unit_convert` — конвертация единиц измерения (`100 F → 37.78 C`, `5 km → 3.11 mi`)

Плюс хук, который логирует каждый вызов инструмента, и встроенный файл скилла.

## Шаг 1: Создайте директорию плагина[​](<#step-1-create-the-plugin-directory> "Прямая ссылка на Шаг 1: Создайте директорию плагина")

```bash
mkdir -p ~/.hermes/plugins/calculator
cd ~/.hermes/plugins/calculator
```

## Шаг 2: Напишите манифест[​](<#step-2-write-the-manifest> "Прямая ссылка на Шаг 2: Напишите манифест")

Создайте `plugin.yaml`:

```yaml
name: calculator
version: 1.0.0
description: Math calculator — evaluate expressions and convert units
provides_tools:
  - calculate
  - unit_convert
provides_hooks:
  - post_tool_call
```

Этим вы говорите Hermes: «Я плагин под названием calculator, я предоставляю инструменты и хуки». Поля `provides_tools` и `provides_hooks` — это списки того, что регистрирует плагин.

Опциональные поля, которые можно добавить:

```yaml
author: Your Name
requires_env:          # ограничивать загрузку переменными окружения; запрашивается при установке
  - SOME_API_KEY       # простой формат — плагин отключён, если переменная отсутствует
  - name: OTHER_KEY    # расширенный формат — показывает описание/ссылку при установке
    description: "Key for the Other service"
    url: "https://other.com/keys"
    secret: true
```

## Шаг 3: Напишите схемы инструментов[​](<#step-3-write-the-tool-schemas> "Прямая ссылка на Шаг 3: Напишите схемы инструментов")

Создайте `schemas.py` — это то, что читает LLM, чтобы решить, когда вызывать ваши инструменты:

```python
"""Tool schemas — what the LLM sees."""

CALCULATE = {
    "name": "calculate",
    "description": (
        "Evaluate a mathematical expression and return the result. "
        "Supports arithmetic (+, -, *, /, **), functions (sqrt, sin, cos, "
        "log, abs, round, floor, ceil), and constants (pi, e). "
        "Use this for any math the user asks about."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Math expression to evaluate (e.g., '2**10', 'sqrt(144)')",
            },
        },
        "required": ["expression"],
    },
}

UNIT_CONVERT = {
    "name": "unit_convert",
    "description": (
        "Convert a value between units. Supports length (m, km, mi, ft, in), "
        "weight (kg, lb, oz, g), temperature (C, F, K), data (B, KB, MB, GB, TB), "
        "and time (s, min, hr, day)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "value": {
                "type": "number",
                "description": "The numeric value to convert",
            },
            "from_unit": {
                "type": "string",
                "description": "Source unit (e.g., 'km', 'lb', 'F', 'GB')",
            },
            "to_unit": {
                "type": "string",
                "description": "Target unit (e.g., 'mi', 'kg', 'C', 'MB')",
            },
        },
        "required": ["value", "from_unit", "to_unit"],
    },
}
```

**Почему схемы важны:** Поле `description` определяет, когда LLM решит использовать ваш инструмент. Будьте конкретны в описании того, что делает инструмент и когда его применять. Параметры `parameters` определяют, какие аргументы LLM будет передавать.

## Шаг 4: Напишите обработчики инструментов[​](<#step-4-write-the-tool-handlers> "Прямая ссылка на Шаг 4: Напишите обработчики инструментов")

Создайте `tools.py` — это код, который выполняется, когда LLM вызывает ваши инструменты:

```python
"""Tool handlers — the code that runs when the LLM calls each tool."""

import json
import math

# Safe globals for expression evaluation — no file/network access
_SAFE_MATH = {
    "abs": abs, "round": round, "min": min, "max": max,
    "pow": pow, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
    "tan": math.tan, "log": math.log, "log2": math.log2, "log10": math.log10,
    "floor": math.floor, "ceil": math.ceil,
    "pi": math.pi, "e": math.e,
    "factorial": math.factorial,
}


def calculate(args: dict, **kwargs) -> str:
    """Evaluate a math expression safely.

    Rules for handlers:
    1. Receive args (dict) — the parameters the LLM passed
    2. Do the work
    3. Return a JSON string — ALWAYS, even on error
    4. Accept **kwargs for forward compatibility
    """
    expression = args.get("expression", "").strip()
    if not expression:
        return json.dumps({"error": "No expression provided"})

    try:
        result = eval(expression, {"__builtins__": {}}, _SAFE_MATH)
        return json.dumps({"expression": expression, "result": result})
    except ZeroDivisionError:
        return json.dumps({"expression": expression, "error": "Division by zero"})
    except Exception as e:
        return json.dumps({"expression": expression, "error": f"Invalid: {e}"})


# Conversion tables — values are in base units
_LENGTH = {"m": 1, "km": 1000, "mi": 1609.34, "ft": 0.3048, "in": 0.0254, "cm": 0.01}
_WEIGHT = {"kg": 1, "g": 0.001, "lb": 0.453592, "oz": 0.0283495}
_DATA = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
_TIME = {"s": 1, "ms": 0.001, "min": 60, "hr": 3600, "day": 86400}


def _convert_temp(value, from_u, to_u):
    # Normalize to Celsius
    c = {"F": (value - 32) * 5/9, "K": value - 273.15}.get(from_u, value)
    # Convert to target
    return {"F": c * 9/5 + 32, "K": c + 273.15}.get(to_u, c)


def unit_convert(args: dict, **kwargs) -> str:
    """Convert between units."""
    value = args.get("value")
    from_unit = args.get("from_unit", "").strip()
    to_unit = args.get("to_unit", "").strip()

    if value is None or not from_unit or not to_unit:
        return json.dumps({"error": "Need value, from_unit, and to_unit"})

    try:
        # Temperature
        if from_unit.upper() in {"C","F","K"} and to_unit.upper() in {"C","F","K"}:
            result = _convert_temp(float(value), from_unit.upper(), to_unit.upper())
            return json.dumps({"input": f"{value} {from_unit}", "result": round(result, 4),
                             "output": f"{round(result, 4)} {to_unit}"})

        # Ratio-based conversions
        for table in (_LENGTH, _WEIGHT, _DATA, _TIME):
            lc = {k.lower(): v for k, v in table.items()}
            if from_unit.lower() in lc and to_unit.lower() in lc:
                result = float(value) * lc[from_unit.lower()] / lc[to_unit.lower()]
                return json.dumps({"input": f"{value} {from_unit}",
                                 "result": round(result, 6),
                                 "output": f"{round(result, 6)} {to_unit}"})

        return json.dumps({"error": f"Cannot convert {from_unit} → {to_unit}"})
    except Exception as e:
        return json.dumps({"error": f"Conversion failed: {e}"})
```

**Ключевые правила для обработчиков:**

1. **Сигнатура:** `def my_handler(args: dict, **kwargs) -> str`
2. **Возврат:** Всегда строка JSON. И для успеха, и для ошибок.
3. **Никогда не выбрасывайте исключения:** Ловите все исключения, возвращайте JSON с ошибкой.
4. **Принимайте `**kwargs`:** Hermes может передавать дополнительный контекст в будущем.

## Шаг 5: Напишите регистрацию[​](<#step-5-write-the-registration> "Прямая ссылка на Шаг 5: Напишите регистрацию")

Создайте `__init__.py` — этот файл связывает схемы с обработчиками:

```python
"""Calculator plugin — registration."""

import logging

from . import schemas, tools

logger = logging.getLogger(__name__)

# Track tool usage via hooks
_call_log = []

def _on_post_tool_call(tool_name, args, result, task_id, **kwargs):
    """Hook: runs after every tool call (not just ours)."""
    _call_log.append({"tool": tool_name, "session": task_id})
    if len(_call_log) > 100:
        _call_log.pop(0)
    logger.debug("Tool called: %s (session %s)", tool_name, task_id)


def register(ctx):
    """Wire schemas to handlers and register hooks."""
    ctx.register_tool(name="calculate",    toolset="calculator",
                      schema=schemas.CALCULATE,    handler=tools.calculate)
    ctx.register_tool(name="unit_convert", toolset="calculator",
                      schema=schemas.UNIT_CONVERT, handler=tools.unit_convert)

    # This hook fires for ALL tool calls, not just ours
    ctx.register_hook("post_tool_call", _on_post_tool_call)
```

**Что делает `register()`:**

* Вызывается ровно один раз при запуске
* `ctx.register_tool()` помещает ваш инструмент в реестр — модель видит его немедленно
* `ctx.register_hook()` подписывается на события жизненного цикла
* `ctx.register_cli_command()` регистрирует CLI-подкоманду (например, `hermes my-plugin <subcommand>`)
* `ctx.register_command()` регистрирует внутрисессионную слеш-команду (например, `/myplugin <args>` в CLI / чате шлюза) — см. [Register slash commands](<#register-slash-commands>) ниже
* `ctx.dispatch_tool(name, arguments)` — вызывает любой другой инструмент (встроенный или из другого плагина) с контекстом родительского агента (одобрения, учетные данные, task_id), автоматически подключаемым. Полезно из обработчиков слеш-команд, которым нужно вызвать `terminal`, `read_file` или любой другой инструмент так, как если бы его вызвала модель напрямую.
* Если эта функция упадёт, плагин будет отключён, но Hermes продолжит работу

**Пример `dispatch_tool` — слеш-команда, запускающая инструмент:**

```python
def handle_scan(ctx, argstr):
    """Implement /scan by invoking the terminal tool through the registry."""
    result = ctx.dispatch_tool("terminal", {"command": f"find . -name '{argstr}'"})
    return result  # returned to the caller's chat UI

def register(ctx):
    ctx.register_command("scan", handle_scan, help="Find files matching a glob")
```

Вызванный инструмент проходит через обычные конвейеры одобрения, редактирования и бюджета — это полноценный вызов инструмента, а не обходной путь.

## Шаг 6: Протестируйте[​](<#step-6-test-it> "Прямая ссылка на Шаг 6: Протестируйте")

Запустите Hermes:

```bash
hermes
```

Вы должны увидеть `calculator: calculate, unit_convert` в списке инструментов баннера.

Попробуйте эти запросы:

```
What's 2 to the power of 16?
Convert 100 fahrenheit to celsius
What's the square root of 2 times pi?
How many gigabytes is 1.5 terabytes?
```

Проверьте статус плагина:

```
/plugins
```

Вывод:

```
Plugins (1):
  ✓ calculator v1.0.0 (2 tools, 1 hooks)
```

## Финальная структура плагина[​](<#your-plugins-final-structure> "Прямая ссылка на Финальная структура плагина")

```
~/.hermes/plugins/calculator/
├── plugin.yaml      # «Я calculator, я предоставляю инструменты и хуки»
├── __init__.py      # Связка: схемы → обработчики, регистрация хуков
├── schemas.py       # Что читает LLM (описания + спецификации параметров)
└── tools.py         # Что выполняется (функции calculate, unit_convert)
```

Четыре файла с чётким разделением:

* **Манифест** объявляет, что такое плагин
* **Схемы** описывают инструменты для LLM
* **Обработчики** реализуют фактическую логику
* **Регистрация** соединяет всё вместе

## Что ещё могут делать плагины?[​](<#what-else-can-plugins-do> "Прямая ссылка на Что ещё могут делать плагины?")

### Поставлять файлы данных[​](<#ship-data-files> "Прямая ссылка на Поставлять файлы данных")

Поместите любые файлы в директорию плагина и читайте их во время импорта:

```python
# In tools.py or __init__.py
from pathlib import Path

_PLUGIN_DIR = Path(__file__).parent
_DATA_FILE = _PLUGIN_DIR / "data" / "languages.yaml"

with open(_DATA_FILE) as f:
    _DATA = yaml.safe_load(f)
```

### Встраивать скиллы[​](<#bundle-skills> "Прямая ссылка на Встраивать скиллы")

Плагины могут поставлять файлы скиллов, которые агент загружает через `skill_view("plugin:skill")`. Зарегистрируйте их в вашем `__init__.py`:

```
~/.hermes/plugins/my-plugin/
├── __init__.py
├── plugin.yaml
└── skills/
    ├── my-workflow/
    │   └── SKILL.md
    └── my-checklist/
        └── SKILL.md
```

```python
from pathlib import Path

def register(ctx):
    skills_dir = Path(__file__).parent / "skills"
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)
```

Теперь агент может загружать ваши скиллы по их именам с пространством имён:

```
skill_view("my-plugin:my-workflow")   # → версия плагина
skill_view("my-workflow")              # → встроенная версия (без изменений)
```

**Ключевые свойства:**

* Скиллы плагина **только для чтения** — они не попадают в `~/.hermes/skills/` и не могут быть изменены через `skill_manage`.
* Скиллы плагина **не** перечисляются в индексе `<available_skills>` системного промпта — они загружаются явно по выбору.
* Обычные имена скиллов не затрагиваются — пространство имён предотвращает коллизии со встроенными скиллами.
* Когда агент загружает скилл плагина, в начало добавляется баннер контекста пакета со списком соседних скиллов из того же плагина.

Устаревший паттерн

Старый паттерн `shutil.copy2` (копирование скилла в `~/.hermes/skills/`) всё ещё работает, но создаёт риск коллизии имён со встроенными скиллами. Для новых плагинов предпочтительнее `ctx.register_skill()`.

### Ограничение по переменным окружения[​](<#gate-on-environment-variables> "Прямая ссылка на Ограничение по переменным окружения")

Если вашему плагину нужен API-ключ:

```yaml
# plugin.yaml — simple format (backwards-compatible)
requires_env:
  - WEATHER_API_KEY
```

Если `WEATHER_API_KEY` не установлена, плагин отключается с понятным сообщением. Ни падений, ни ошибок в агенте — просто «Plugin weather disabled (missing: WEATHER_API_KEY)».

Когда пользователи запускают `hermes plugins install`, их **интерактивно запрашивают** ввести недостающие переменные `requires_env`. Значения автоматически сохраняются в `.env`.

Для улучшенного опыта установки используйте расширенный формат с описаниями и ссылками для регистрации:

```yaml
# plugin.yaml — rich format
requires_env:
  - name: WEATHER_API_KEY
    description: "API key for OpenWeather"
    url: "https://openweathermap.org/api"
    secret: true
```

| Поле | Обязательное | Описание |
|---|---|---|
| `name` | Да | Имя переменной окружения |
| `description` | Нет | Показывается пользователю при запросе на установку |
| `url` | Нет | Где получить учётные данные |
| `secret` | Нет | Если `true`, ввод скрывается (как поле пароля) |

Оба формата можно смешивать в одном списке. Уже установленные переменные пропускаются молча.

### Условная доступность инструментов[​](<#conditional-tool-availability> "Прямая ссылка на Условная доступность инструментов")

Для инструментов, зависящих от опциональных библиотек:

```python
ctx.register_tool(
    name="my_tool",
    schema={...},
    handler=my_handler,
    check_fn=lambda: _has_optional_lib(),  # False = tool hidden from model
)
```

### Регистрация нескольких хуков[​](<#register-multiple-hooks> "Прямая ссылка на Регистрация нескольких хуков")

```python
def register(ctx):
    ctx.register_hook("pre_tool_call", before_any_tool)
    ctx.register_hook("post_tool_call", after_any_tool)
    ctx.register_hook("pre_llm_call", inject_memory)
    ctx.register_hook("on_session_start", on_new_session)
    ctx.register_hook("on_session_end", on_session_end)
```

### Справочник хуков[​](<#hook-reference> "Прямая ссылка на Справочник хуков")

Каждый хук полностью документирован в **[Event Hooks reference](</docs/user-guide/features/hooks#plugin-hooks>)** — сигнатуры колбэков, таблицы параметров, когда именно срабатывает и примеры. Вот сводка:

| Хук | Срабатывает когда | Сигнатура колбэка | Возвращает |
|---|---|---|---|
| [`pre_tool_call`](</docs/user-guide/features/hooks#pre_tool_call>) | Перед выполнением любого инструмента | `tool_name: str, args: dict, task_id: str` | игнорируется |
| [`post_tool_call`](</docs/user-guide/features/hooks#post_tool_call>) | После возврата любого инструмента | `tool_name: str, args: dict, result: str, task_id: str, duration_ms: int` | игнорируется |
| [`pre_llm_call`](</docs/user-guide/features/hooks#pre_llm_call>) | Один раз за ход, перед циклом вызова инструментов | `session_id: str, user_message: str, conversation_history: list, is_first_turn: bool, model: str, platform: str` | [внедрение контекста](<#pre_llm_call-context-injection>) |
| [`post_llm_call`](</docs/user-guide/features/hooks#post_llm_call>) | Один раз за ход, после цикла вызова инструментов (только успешные ходы) | `session_id: str, user_message: str, assistant_response: str, conversation_history: list, model: str, platform: str` | игнорируется |
| [`on_session_start`](</docs/user-guide/features/hooks#on_session_start>) | Создана новая сессия (только первый ход) | `session_id: str, model: str, platform: str` | игнорируется |
| [`on_session_end`](</docs/user-guide/features/hooks#on_session_end>) | Конец каждого вызова `run_conversation` + завершение CLI | `session_id: str, completed: bool, interrupted: bool, model: str, platform: str` | игнорируется |
| [`on_session_finalize`](</docs/user-guide/features/hooks#on_session_finalize>) | CLI/шлюз завершает активную сессию | `session_id: str \| None, platform: str` | игнорируется |
| [`on_session_reset`](</docs/user-guide/features/hooks#on_session_reset>) | Шлюз заменяет ключ сессии (`/new`, `/reset`) | `session_id: str, platform: str` | игнорируется |

Большинство хуков — это наблюдатели типа «запустил и забыл» — их возвращаемые значения игнорируются. Исключение — `pre_llm_call`, который может внедрять контекст в разговор.

Все колбэки должны принимать `**kwargs` для обратной совместимости. Если колбэк хука падает, это логируется и пропускается. Другие хуки и агент продолжают нормально работать.

### Внедрение контекста в `pre_llm_call`[​](<#pre_llm_call-context-injection> "Прямая ссылка на pre_llm_call-context-injection")

Это единственный хук, чьё возвращаемое значение имеет значение. Когда колбэк `pre_llm_call` возвращает словарь с ключом `"context"` (или простую строку), Hermes внедряет этот текст в **текущее пользовательское сообщение**. Это механизм для плагинов памяти, RAG-интеграций, гардрейлов и любых плагинов, которым нужно предоставить модели дополнительный контекст.

#### Формат возврата[​](<#return-format> "Прямая ссылка на Формат возврата")

```python
# Dict with context key
return {"context": "Recalled memories:\n- User prefers dark mode\n- Last project: hermes-agent"}

# Plain string (equivalent to the dict form above)
return "Recalled memories:\n- User prefers dark mode"

# Return None or don't return → no injection (observer-only)
return None
```

Любой не-None, непустой возврат с ключом `"context"` (или простая непустая строка) собирается и добавляется к пользовательскому сообщению текущего хода.

#### Как работает внедрение[​](<#how-injection-works> "Прямая ссылка на Как работает внедрение")

Внедрённый контекст добавляется к **пользовательскому сообщению**, а не к системному промпту. Это осознанный дизайнерский выбор:

* **Сохранение кэша промпта** — системный промпт остаётся идентичным между ходами. Anthropic и OpenRouter кэшируют префикс системного промпта, поэтому его стабильность экономит 75%+ входных токенов в многоходовых разговорах. Если бы плагины изменяли системный промпт, каждый ход приводил бы к промаху кэша.
* **Эфемерность** — внедрение происходит только в момент API-вызова. Исходное пользовательское сообщение в истории разговора никогда не изменяется, и ничего не сохраняется в базу данных сессии.
* **Системный промпт — территория Hermes** — он содержит модельно-специфичные инструкции, правила enforcement инструментов, инструкции по личности и кэшированное содержимое скиллов. Плагины добавляют контекст рядом с вводом пользователя, а не изменяя основные инструкции агента.

#### Пример: Плагин памяти[​](<#example-memory-recall-plugin> "Прямая ссылка на Пример: Плагин памяти")

```python
"""Memory plugin — recalls relevant context from a vector store."""

import httpx

MEMORY_API = "https://your-memory-api.example.com"

def recall_context(session_id, user_message, is_first_turn, **kwargs):
    """Called before each LLM turn. Returns recalled memories."""
    try:
        resp = httpx.post(f"{MEMORY_API}/recall", json={
            "session_id": session_id,
            "query": user_message,
        }, timeout=3)
        memories = resp.json().get("results", [])
        if not memories:
            return None  # nothing to inject

        text = "Recalled context from previous sessions:\n"
        text += "\n".join(f"- {m['text']}" for m in memories)
        return {"context": text}
    except Exception:
        return None  # fail silently, don't break the agent

def register(ctx):
    ctx.register_hook("pre_llm_call", recall_context)
```

#### Пример: Плагин гардрейлов[​](<#example-guardrails-plugin> "Прямая ссылка на Пример: Плагин гардрейлов")

```python
"""Guardrails plugin — enforces content policies."""

POLICY = """You MUST follow these content policies for this session:
- Never generate code that accesses the filesystem outside the working directory
- Always warn before executing destructive operations
- Refuse requests involving personal data extraction"""

def inject_guardrails(**kwargs):
    """Injects policy text into every turn."""
    return {"context": POLICY}

def register(ctx):
    ctx.register_hook("pre_llm_call", inject_guardrails)
```

#### Пример: Хук-наблюдатель (без внедрения)[​](<#example-observer-only-hook-no-injection> "Прямая ссылка на Пример: Хук-наблюдатель (без внедрения)")

```python
"""Analytics plugin — tracks turn metadata without injecting context."""

import logging
logger = logging.getLogger(__name__)

def log_turn(session_id, user_message, model, is_first_turn, **kwargs):
    """Fires before each LLM call. Returns None — no context injected."""
    logger.info("Turn: session=%s model=%s first=%s msg_len=%d",
                session_id, model, is_first_turn, len(user_message or ""))
    # No return → no injection

def register(ctx):
    ctx.register_hook("pre_llm_call", log_turn)
```

#### Несколько плагинов, возвращающих контекст[​](<#multiple-plugins-returning-context> "Прямая ссылка на Несколько плагинов, возвращающих контекст")

Когда несколько плагинов возвращают контекст из `pre_llm_call`, их выводы объединяются с двойными переводами строк и добавляются к пользовательскому сообщению вместе. Порядок соответствует порядку обнаружения плагинов (по алфавиту имён директорий плагинов).

### Регистрация CLI-команд[​](<#register-cli-commands> "Прямая ссылка на Регистрация CLI-команд")

Плагины могут добавлять собственное дерево подкоманд `hermes <plugin>`:

```python
def _my_command(args):
    """Handler for hermes my-plugin <subcommand>."""
    sub = getattr(args, "my_command", None)
    if sub == "status":
        print("All good!")
    elif sub == "config":
        print("Current config: ...")
    else:
        print("Usage: hermes my-plugin <status|config>")

def _setup_argparse(subparser):
    """Build the argparse tree for hermes my-plugin."""
    subs = subparser.add_subparsers(dest="my_command")
    subs.add_parser("status", help="Show plugin status")
    subs.add_parser("config", help="Show plugin config")
    subparser.set_defaults(func=_my_command)

def register(ctx):
    ctx.register_tool(...)
    ctx.register_cli_command(
        name="my-plugin",
        help="Manage my plugin",
        setup_fn=_setup_argparse,
        handler_fn=_my_command,
    )
```

После регистрации пользователи могут выполнять `hermes my-plugin status`, `hermes my-plugin config` и т.д.

**Плагины провайдеров памяти** используют подход на основе соглашений: добавьте функцию `register_cli(subparser)` в файл `cli.py` вашего плагина. Система обнаружения плагинов памяти находит её автоматически — вызов `ctx.register_cli_command()` не требуется. Подробности см. в [Memory Provider Plugin guide](</docs/developer-guide/memory-provider-plugin#adding-cli-commands>).

**Ограничение по активному провайдеру:** CLI-команды плагинов памяти отображаются только когда их провайдер является активным `memory.provider` в конфиге. Если пользователь не настроил ваш провайдер, ваши CLI-команды не будут засорять вывод справки.

### Регистрация слеш-команд[​](<#register-slash-commands> "Прямая ссылка на Регистрация слеш-команд")

Плагины могут регистрировать внутрисессионные слеш-команды — команды, которые пользователи вводят во время разговора (например, `/lcm status` или `/ping`). Они работают как в CLI, так и в шлюзах (Telegram, Discord и т.д.).

```python
def _handle_status(raw_args: str) -> str:
    """Handler for /mystatus — called with everything after the command name."""
    if raw_args.strip() == "help":
        return "Usage: /mystatus [help|check]"
    return "Plugin status: all systems nominal"

def register(ctx):
    ctx.register_command(
        "mystatus",
        handler=_handle_status,
        description="Show plugin status",
    )
```

После регистрации пользователи могут ввести `/mystatus` в любой сессии. Команда появляется в автодополнении, выводе `/help` и меню Telegram-бота.

**Сигнатура:** `ctx.register_command(name: str, handler: Callable, description: str = "")`

| Параметр | Тип | Описание |
|---|---|---|
| `name` | `str` | Имя команды без ведущего слеша (например, `"lcm"`, `"mystatus"`) |
| `handler` | `Callable[[str], str \| None]` | Вызывается с сырой строкой аргументов. Может быть `async`. |
| `description` | `str` | Показывается в `/help`, автодополнении и меню Telegram-бота |

**Ключевые отличия от `register_cli_command()`:**

| | `register_command()` | `register_cli_command()` |
|---|---|---|
| Вызов как | `/name` в сессии | `hermes name` в терминале |
| Где работает | CLI-сессии, Telegram, Discord и т.д. | Только терминал |
| Обработчик получает | Сырую строку аргументов | argparse `Namespace` |
| Сценарий | Диагностика, статус, быстрые действия | Сложные деревья подкоманд, мастера настройки |

**Защита от конфликтов:** Если плагин пытается зарегистрировать имя, конфликтующее со встроенной командой (`help`, `model`, `new` и т.д.), регистрация молча отклоняется с предупреждением в логе. Встроенные команды всегда имеют приоритет.

**Асинхронные обработчики:** Диспетчер шлюза автоматически определяет и ожидает асинхронные обработчики, поэтому вы можете использовать как синхронные, так и асинхронные функции:

```python
async def _handle_check(raw_args: str) -> str:
    result = await some_async_operation()
    return f"Check result: {result}"

def register(ctx):
    ctx.register_command("check", handler=_handle_check, description="Run async check")
```

### Диспетчеризация инструментов из слеш-команд[​](<#dispatch-tools-from-slash-commands> "Прямая ссылка на Диспетчеризация инструментов из слеш-команд")

Обработчики слеш-команд, которым нужно оркестрировать инструменты (запустить под-агента через `delegate_task`, вызвать `file_edit` и т.д.), должны использовать `ctx.dispatch_tool()` вместо обращения к внутренностям фреймворка. Контекст родительского агента (подсказки рабочей области, спиннер, наследование модели) подключается автоматически.

```python
def register(ctx):
    def _handle_deliver(raw_args: str):
        result = ctx.dispatch_tool(
            "delegate_task",
            {
                "goal": raw_args,
                "toolsets": ["terminal", "file", "web"],
            },
        )
        return result

    ctx.register_command(
        "deliver",
        handler=_handle_deliver,
        description="Delegate a goal to a subagent",
    )
```

**Сигнатура:** `ctx.dispatch_tool(name: str, args: dict, *, parent_agent=None) -> str`

| Параметр | Тип | Описание |
|---|---|---|
| `name` | `str` | Имя инструмента, зарегистрированное в реестре (например, `"delegate_task"`, `"file_edit"`) |
| `args` | `dict` | Аргументы инструмента, той же формы, которую отправила бы модель |
| `parent_agent` | `Agent \| None` | Опциональное переопределение. Если опущено, разрешается из текущего CLI-агента (или корректно деградирует в режиме шлюза) |

**Поведение во время выполнения:**

* **CLI-режим:** `parent_agent` разрешается из активного CLI-агента, так что подсказки рабочей области, спиннер и выбор модели наследуются как ожидается.
* **Режим шлюза:** CLI-агента нет, поэтому инструменты корректно деградируют — рабочая область читается из `TERMINAL_CWD`, спиннер не показывается.
* **Явное переопределение:** Если вызывающий передаёт `parent_agent=` явно, оно соблюдается и не перезаписывается.

Это публичный, стабильный интерфейс для диспетчеризации инструментов из команд плагинов. Плагины не должны обращаться к `ctx._cli_ref.agent` или другим приватным состояниям.

> **Совет**
> Это руководство охватывает **общие плагины** (инструменты, хуки, слеш-команды, CLI-команды). Разделы ниже описывают шаблон создания для каждого специализированного типа плагина; каждый ссылается на своё полное руководство для справки по полям и примерам.

## Специализированные типы плагинов[​](<#specialized-plugin-types> "Прямая ссылка на Специализированные типы плагинов")

Hermes имеет пять специализированных типов плагинов помимо общей поверхности. Каждый поставляется как директория в `plugins/<category>/<name>/` (встроенный) или `~/.hermes/plugins/<category>/<name>/` (пользовательский). Контракт различается по категории — выберите нужную, затем прочитайте её полное руководство.

### Плагины провайдеров моделей — добавьте LLM бэкенд[​](<#model-provider-plugins--add-an-llm-backend> "Прямая ссылка на Плагины провайдеров моделей — добавьте LLM бэкенд")

Поместите профиль в `plugins/model-providers/<name>/`:

```python
# plugins/model-providers/acme/__init__.py
from providers import register_provider
from providers.base import ProviderProfile

register_provider(ProviderProfile(
    name="acme",
    aliases=("acme-inference",),
    display_name="Acme Inference",
    env_vars=("ACME_API_KEY", "ACME_BASE_URL"),
    base_url="https://api.acme.example.com/v1",
    auth_type="api_key",
    default_aux_model="acme-small-fast",
    fallback_models=("acme-large-v3", "acme-medium-v3"),
))
```

```yaml
# plugins/model-providers/acme/plugin.yaml
name: acme-provider
kind: model-provider
version: 1.0.0
description: Acme Inference — OpenAI-compatible direct API
```

Лениво обнаруживается при первом вызове `get_provider_profile()` или `list_providers()` — `auth.py`, `config.py`, `doctor.py`, `models.py`, `runtime_provider.py` и транспорт chat_completions автоматически подключаются к нему. Пользовательские плагины переопределяют встроенные по имени.

**Полное руководство:** [Model Provider Plugins](</docs/developer-guide/model-provider-plugin>) — справочник полей, переопределяемые хуки (`prepare_messages`, `build_extra_body`, `build_api_kwargs_extras`, `fetch_models`), выбор `api_mode`, типы аутентификации, тестирование.

### Платформенные плагины — добавьте канал шлюза[​](<#platform-plugins--add-a-gateway-channel> "Прямая ссылка на Платформенные плагины — добавьте канал шлюза")

Поместите адаптер в `plugins/platforms/<name>/`:

```python
# plugins/platforms/myplatform/adapter.py
from gateway.platforms.base import BasePlatformAdapter

class MyPlatformAdapter(BasePlatformAdapter):
    async def connect(self): ...
    async def send(self, chat_id, text): ...
    async def disconnect(self): ...

def check_requirements():
    import os
    return bool(os.environ.get("MYPLATFORM_TOKEN"))

def register(ctx):
    ctx.register_platform(
        name="myplatform",
        label="MyPlatform",
        adapter_factory=lambda cfg: MyPlatformAdapter(cfg),
        check_fn=check_requirements,
        required_env=["MYPLATFORM_TOKEN"],
        emoji="💬",
        platform_hint="You are chatting via MyPlatform. Keep responses concise.",
    )
```

```yaml
# plugins/platforms/myplatform/plugin.yaml
name: myplatform-platform
kind: platform
version: 1.0.0
description: MyPlatform gateway adapter
requires_env: [MYPLATFORM_TOKEN]
```

**Полное руководство:** [Adding Platform Adapters](</docs/developer-guide/adding-platform-adapters>) — полный контракт `BasePlatformAdapter`, маршрутизация сообщений, ограничение по аутентификации, интеграция с мастером настройки. Смотрите `plugins/platforms/irc/` для рабочего примера только на stdlib.

### Плагины провайдеров памяти — добавьте кросc-сессионный бэкенд знаний[​](<#memory-provider-plugins--add-a-cross-session-knowledge-backend> "Прямая ссылка на Плагины провайдеров памяти — добавьте кросc-сессионный бэкенд знаний")

Поместите реализацию `MemoryProvider` в `plugins/memory/<name>/`:

```python
# plugins/memory/my-memory/__init__.py
from agent.memory_provider import MemoryProvider

class MyMemoryProvider(MemoryProvider):
    @property
    def name(self) -> str:
        return "my-memory"

    def is_available(self) -> bool:
        import os
        return bool(os.environ.get("MY_MEMORY_API_KEY"))

    def initialize(self, session_id: str, **kwargs) -> None:
        self._session_id = session_id

    def sync_turn(self, user_message, assistant_response, **kwargs) -> None:
        ...

    def prefetch(self, query: str, **kwargs) -> str | None:
        ...

def register(ctx):
    ctx.register_memory_provider(MyMemoryProvider())
```

Провайдеры памяти — это одиночный выбор: только один активен в данный момент, выбирается через `memory.provider` в `config.yaml`.

**Полное руководство:** [Memory Provider Plugins](</docs/developer-guide/memory-provider-plugin>) — полный ABC `MemoryProvider`, контракт потоков, изоляция профилей, регистрация CLI-команд через `cli.py`.

### Плагины движков контекста — замените компрессор контекста[​](<#context-engine-plugins--replace-the-context-compressor> "Прямая ссылка на Плагины движков контекста — замените компрессор контекста")

```python
# plugins/context_engine/my-engine/__init__.py
from agent.context_engine import ContextEngine

class MyContextEngine(ContextEngine):
    @property
    def name(self) -> str:
        return "my-engine"

    def should_compress(self, messages, model) -> bool: ...
    def compress(self, messages, model) -> list[dict]: ...

def register(ctx):
    ctx.register_context_engine(MyContextEngine())
```

Движки контекста — это одиночный выбор: выбираются через `context.engine` в `config.yaml`.

**Полное руководство:** [Context Engine Plugins](</docs/developer-guide/context-engine-plugin>).

### Бэкенды генерации изображений[​](<#image-generation-backends> "Прямая ссылка на Бэкенды генерации изображений")

Поместите провайдера в `plugins/image_gen/<name>/`:

```python
# plugins/image_gen/my-imggen/__init__.py
from agent.image_gen_provider import ImageGenProvider

class MyImageGenProvider(ImageGenProvider):
    @property
    def name(self) -> str:
        return "my-imggen"

    def is_available(self) -> bool: ...
    def generate(self, prompt: str, **kwargs) -> str: ...   # returns image path

def register(ctx):
    ctx.register_image_gen_provider(MyImageGenProvider())
```

```yaml
# plugins/image_gen/my-imggen/plugin.yaml
name: my-imggen
kind: backend
version: 1.0.0
description: Custom image generation backend
```

**Полное руководство:** [Image Generation Provider Plugins](</docs/developer-guide/image-gen-provider-plugin>) — полный ABC `ImageGenProvider`, метаданные `list_models()` / `get_setup_schema()`, хелперы `success_response()`/`error_response()`, вывод в base64 vs URL, пользовательские переопределения, pip-дистрибуция.

**Примеры для справки:** `plugins/image_gen/openai/` (DALL-E / GPT-Image через OpenAI SDK), `plugins/image_gen/openai-codex/`, `plugins/image_gen/xai/` (Grok image gen).

## Не-Python поверхности расширения[​](<#non-python-extension-surfaces> "Прямая ссылка на Не-Python поверхности расширения")

Hermes также принимает расширения, которые вообще не являются Python-плагинами. Они показаны в [Pluggable interfaces table](</docs/user-guide/features/plugins#pluggable-interfaces--where-to-go-for-each>); разделы ниже кратко описывают каждый стиль создания.

### MCP-серверы — регистрация внешних инструментов[​](<#mcp-servers--register-external-tools> "Прямая ссылка на MCP-серверы — регистрация внешних инструментов")

Серверы Model Context Protocol (MCP) регистрируют свои собственные инструменты в Hermes без какого-либо Python-плагина. Объявите их в `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    timeout: 120

  linear:
    url: "https://mcp.linear.app/sse"
    auth:
      type: "oauth"
```

Hermes подключается к каждому серверу при запуске, получает список его инструментов и регистрирует их вместе со встроенными. LLM видит их точно так же, как любой другой инструмент. **Полное руководство:** [MCP](</docs/user-guide/features/mcp>).

### Хуки событий шлюза — срабатывают на события жизненного цикла[​](<#gateway-event-hooks--fire-on-lifecycle-events> "Прямая ссылка на Хуки событий шлюза — срабатывают на события жизненного цикла")

Поместите манифест + обработчик в `~/.hermes/hooks/<name>/`:

```yaml
# ~/.hermes/hooks/long-task-alert/HOOK.yaml
name: long-task-alert
description: Send a push notification when a long task finishes
events:
  - agent:end
```

```python
# ~/.hermes/hooks/long-task-alert/handler.py
async def handle(event_type: str, context: dict) -> None:
    if context.get("duration_seconds", 0) > 120:
        # send notification …
        pass
```

События включают `gateway:startup`, `session:start`, `session:end`, `session:reset`, `agent:start`, `agent:step`, `agent:end` и wildcard `command:*`. Ошибки в хуках перехватываются и логируются — они никогда не блокируют основной конвейер.

**Полное руководство:** [Gateway Event Hooks](</docs/user-guide/features/hooks#gateway-event-hooks>).

### Shell-хуки — выполнить shell-команду при вызове инструмента[​](<#shell-hooks--run-a-shell-command-on-tool-calls> "Прямая ссылка на Shell-хуки — выполнить shell-команду при вызове инструмента")

Если вы просто хотите запустить скрипт при срабатывании инструмента (уведомления, аудит-логи, десктопные оповещения, автоформаттеры), используйте shell-хуки в `config.yaml` — Python не требуется:

```yaml
hooks:
  - event: post_tool_call
    command: "notify-send 'Tool ran: {tool_name}'"
    when:
      tools: [terminal, patch, write_file]
```

Поддерживает все те же события, что и Python-хуки плагинов (`pre_tool_call`, `post_tool_call`, `pre_llm_call`, `post_llm_call`, `on_session_start`, `on_session_end`, `pre_gateway_dispatch`) плюс структурированный JSON-вывод для блокирующих решений `pre_tool_call`.

**Полное руководство:** [Shell Hooks](</docs/user-guide/features/hooks#shell-hooks>).

### Источники скиллов — добавьте пользовательский реестр скиллов[​](<#skill-sources--add-a-custom-skill-registry> "Прямая ссылка на Источники скиллов — добавьте пользовательский реестр скиллов")

Если вы поддерживаете GitHub-репозиторий скиллов (или хотите получать скиллы из сообщественного индекса помимо встроенных источников), добавьте его как **tap**:

```
hermes skills tap add myorg/skills-repo
hermes skills search my-workflow --source myorg/skills-repo
hermes skills install myorg/skills-repo/my-workflow
```

Публикация собственного tap — это просто GitHub-репозиторий с директориями `skills/<skill-name>/SKILL.md` — не нужен ни сервер, ни регистрация.

**Полные руководства:** [Skills Hub](</docs/user-guide/features/skills#skills-hub>) · [Publishing a custom tap](</docs/user-guide/features/skills#publishing-a-custom-skill-tap>) (структура репозитория, минимальный пример, нестандартные пути, уровни доверия).

### TTS / STT через шаблоны команд[​](<#tts--stt-via-command-templates> "Прямая ссылка на TTS / STT через шаблоны команд")

Любой CLI, который читает/пишет аудио или текст, можно подключить через `config.yaml` — без Python-кода:

```yaml
tts:
  provider: voxcpm
  providers:
    voxcpm:
      type: command
      command: "voxcpm --ref ~/voice.wav --text-file {input_path} --out {output_path}"
      output_format: mp3
      voice_compatible: true
```

Для STT укажите `HERMES_LOCAL_STT_COMMAND` в виде shell-шаблона. Поддерживаемые плейсхолдеры: `{input_path}`, `{output_path}`, `{format}`, `{voice}`, `{model}`, `{speed}` (TTS); `{input_path}`, `{output_dir}`, `{language}`, `{model}` (STT). Любой CLI, работающий с путями, автоматически становится плагином.

**Полные руководства:** [TTS custom command providers](</docs/user-guide/features/tts#custom-command-providers>) · [STT](</docs/user-guide/features/tts#voice-message-transcription-stt>).

## Распространение через pip[​](<#distribute-via-pip> "Прямая ссылка на Распространение через pip")

Для публичного распространения плагинов добавьте точку входа в ваш Python-пакет:

```toml
# pyproject.toml
[project.entry-points."hermes_agent.plugins"]
my-plugin = "my_plugin_package"
```

```
pip install hermes-plugin-calculator
# Plugin auto-discovered on next hermes startup
```

## Распространение для NixOS[​](<#distribute-for-nixos> "Прямая ссылка на Распространение для NixOS")

Пользователи NixOS могут установить ваш плагин декларативно, если вы предоставите `pyproject.toml` с точками входа:

**Плагины с точками входа** (рекомендуется для распространения):

```nix
# User's configuration.nix
services.hermes-agent.extraPythonPackages = [
  (pkgs.python312Packages.buildPythonPackage {
    pname = "my-plugin";
    version = "1.0.0";
    src = pkgs.fetchFromGitHub {
      owner = "you";
      repo = "hermes-my-plugin";
      rev = "v1.0.0";
      hash = "sha256-...";  # nix-prefetch-url --unpack
    };
    format = "pyproject";
    build-system = [ pkgs.python312Packages.setuptools ];
  })
];
```

**Директорийные плагины** (без `pyproject.toml`):

```nix
services.hermes-agent.extraPlugins = [
  (pkgs.fetchFromGitHub {
    owner = "you";
    repo = "hermes-my-plugin";
    rev = "v1.0.0";
    hash = "sha256-...";
  })
];
```

См. [Nix Setup guide](</docs/getting-started/nix-setup#plugins>) для полной документации, включая использование overlay и проверку коллизий.

## Частые ошибки[​](<#common-mistakes> "Прямая ссылка на Частые ошибки")

**Обработчик не возвращает JSON-строку:**

```python
# Wrong — returns a dict
def handler(args, **kwargs):
    return {"result": 42}

# Right — returns a JSON string
def handler(args, **kwargs):
    return json.dumps({"result": 42})
```

**Отсутствует `**kwargs` в сигнатуре обработчика:**

```python
# Wrong — will break if Hermes passes extra context
def handler(args):
    ...

# Right
def handler(args, **kwargs):
    ...
```

**Обработчик выбрасывает исключения:**

```python
# Wrong — exception propagates, tool call fails
def handler(args, **kwargs):
    result = 1 / int(args["value"])  # ZeroDivisionError!
    return json.dumps({"result": result})

# Right — catch and return error JSON
def handler(args, **kwargs):
    try:
        result = 1 / int(args.get("value", 0))
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})
```

**Слишком расплывчатое описание схемы:**

```python
# Bad — model doesn't know when to use it
"description": "Does stuff"

# Good — model knows exactly when and how
"description": "Evaluate a mathematical expression. Use for arithmetic, trig, logarithms. Supports: +, -, *, /, **, sqrt, sin, cos, log, pi, e."
```

* [Что вы создадите](<#what-youre-building>)
* [Шаг 1: Создайте директорию плагина](<#step-1-create-the-plugin-directory>)
* [Шаг 2: Напишите манифест](<#step-2-write-the-manifest>)
* [Шаг 3: Напишите схемы инструментов](<#step-3-write-the-tool-schemas>)
* [Шаг 4: Напишите обработчики инструментов](<#step-4-write-the-tool-handlers>)
* [Шаг 5: Напишите регистрацию](<#step-5-write-the-registration>)
* [Шаг 6: Протестируйте](<#step-6-test-it>)
* [Финальная структура плагина](<#your-plugins-final-structure>)
* [Что ещё могут делать плагины?](<#what-else-can-plugins-do>)
  * [Поставлять файлы данных](<#ship-data-files>)
  * [Встраивать скиллы](<#bundle-skills>)
  * [Ограничение по переменным окружения](<#gate-on-environment-variables>)
  * [Условная доступность инструментов](<#conditional-tool-availability>)
  * [Регистрация нескольких хуков](<#register-multiple-hooks>)
  * [Справочник хуков](<#hook-reference>)
  * [Внедрение контекста в `pre_llm_call`](<#pre_llm_call-context-injection>)
  * [Регистрация CLI-команд](<#register-cli-commands>)
  * [Регистрация слеш-команд](<#register-slash-commands>)
  * [Диспетчеризация инструментов из слеш-команд](<#dispatch-tools-from-slash-commands>)
* [Специализированные типы плагинов](<#specialized-plugin-types>)
  * [Плагины провайдеров моделей — добавьте LLM бэкенд](<#model-provider-plugins--add-an-llm-backend>)
  * [Платформенные плагины — добавьте канал шлюза](<#platform-plugins--add-a-gateway-channel>)
  * [Плагины провайдеров памяти — добавьте кросc-сессионный бэкенд знаний](<#memory-provider-plugins--add-a-cross-session-knowledge-backend>)
  * [Плагины движков контекста — замените компрессор контекста](<#context-engine-plugins--replace-the-context-compressor>)
  * [Бэкенды генерации изображений](<#image-generation-backends>)
* [Не-Python поверхности расширения](<#non-python-extension-surfaces>)
  * [MCP-серверы — регистрация внешних инструментов](<#mcp-servers--register-external-tools>)
  * [Хуки событий шлюза — срабатывают на события жизненного цикла](<#gateway-event-hooks--fire-on-lifecycle-events>)
  * [Shell-хуки — выполнить shell-команду при вызове инструмента](<#shell-hooks--run-a-shell-command-on-tool-calls>)
  * [Источники скиллов — добавьте пользовательский реестр скиллов](<#skill-sources--add-a-custom-skill-registry>)
  * [TTS / STT через шаблоны команд](<#tts--stt-via-command-templates>)
* [Распространение через pip](<#distribute-via-pip>)
* [Распространение для NixOS](<#distribute-for-nixos>)
* [Частые ошибки](<#common-mistakes>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin -->
