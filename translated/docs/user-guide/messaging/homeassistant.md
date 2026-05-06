На этой странице

Hermes Agent интегрируется с [Home Assistant](<https://www.home-assistant.io/>) двумя способами:

1. **Шлюзовая платформа (Gateway)** — подписывается на изменения состояний в реальном времени через WebSocket и реагирует на события
2. **Инструменты умного дома** — четыре инструмента, вызываемых LLM, для запросов и управления устройствами через REST API

## Настройка[​](<#setup> "Прямая ссылка на Настройка")

### 1\. Создайте долгоживущий токен доступа[​](<#1-create-a-long-lived-access-token> "Прямая ссылка на 1. Создайте долгоживущий токен доступа")

1. Откройте ваш экземпляр Home Assistant
2. Перейдите в **Профиль** (нажмите на ваше имя на боковой панели)
3. Прокрутите до раздела **Долгоживущие токены доступа (Long-Lived Access Tokens)**
4. Нажмите **Создать токен (Create Token)** , дайте ему имя, например "Hermes Agent"
5. Скопируйте токен

### 2\. Настройте переменные окружения[​](<#2-configure-environment-variables> "Прямая ссылка на 2. Настройте переменные окружения")

[code]

    # Добавьте в ~/.hermes/.env  
      
    # Обязательно: ваш долгоживущий токен доступа  
    HASS_TOKEN=your-long-lived-access-token  
      
    # Опционально: URL Home Assistant (по умолчанию: http://homeassistant.local:8123)  
    HASS_URL=http://192.168.1.100:8123  
    
[/code]

info

Набор инструментов `homeassistant` автоматически включается, когда задан `HASS_TOKEN`. Шлюзовая платформа и инструменты управления устройствами активируются по одному токену.

### 3\. Запустите шлюз[​](<#3-start-the-gateway> "Прямая ссылка на 3. Запустите шлюз")

[code]

    hermes gateway  
    
[/code]

Home Assistant появится как подключённая платформа вместе с другими платформами обмена сообщениями (Telegram, Discord и т.д.).

## Доступные инструменты[​](<#available-tools> "Прямая ссылка на Доступные инструменты")

Hermes Agent регистрирует четыре инструмента для управления умным домом:

### `ha_list_entities`[​](<#ha_list_entities> "Прямая ссылка на ha_list_entities")

Получение списка сущностей Home Assistant, опционально с фильтрацией по домену или зоне.

**Параметры:**

- `domain` _(опционально)_ — Фильтр по домену сущности: `light`, `switch`, `climate`, `sensor`, `binary_sensor`, `cover`, `fan`, `media_player` и др.
- `area` _(опционально)_ — Фильтр по названию зоны/комнаты (сопоставляется с понятными именами): `living room`, `kitchen`, `bedroom` и др.

**Пример:**

[code]

    List all lights in the living room  
    
[/code]

Возвращает ID сущностей, состояния и понятные имена.

### `ha_get_state`[​](<#ha_get_state> "Прямая ссылка на ha_get_state")

Получение детального состояния одной сущности, включая все атрибуты (яркость, цвет, заданная температура, показания датчиков и т.д.).

**Параметры:**

- `entity_id` _(обязательно)_ — Сущность для запроса, например `light.living_room`, `climate.thermostat`, `sensor.temperature`

**Пример:**

[code]

    What's the current state of climate.thermostat?  
    
[/code]

Возвращает: состояние, все атрибуты, временные метки последнего изменения/обновления.

### `ha_list_services`[​](<#ha_list_services> "Прямая ссылка на ha_list_services")

Получение списка доступных сервисов (действий) для управления устройствами. Показывает, какие действия можно выполнять для каждого типа устройств и какие параметры они принимают.

**Параметры:**

- `domain` _(опционально)_ — Фильтр по домену, например `light`, `climate`, `switch`

**Пример:**

[code]

    What services are available for climate devices?  
    
[/code]

### `ha_call_service`[​](<#ha_call_service> "Прямая ссылка на ha_call_service")

Вызов сервиса Home Assistant для управления устройством.

**Параметры:**

- `domain` _(обязательно)_ — Домен сервиса: `light`, `switch`, `climate`, `cover`, `media_player`, `fan`, `scene`, `script`
- `service` _(обязательно)_ — Имя сервиса: `turn_on`, `turn_off`, `toggle`, `set_temperature`, `set_hvac_mode`, `open_cover`, `close_cover`, `set_volume_level`
- `entity_id` _(опционально)_ — Целевая сущность, например `light.living_room`
- `data` _(опционально)_ — Дополнительные параметры в виде JSON-объекта

**Примеры:**

[code]

    Turn on the living room lights  
    → ha_call_service(domain="light", service="turn_on", entity_id="light.living_room")  
    
[/code]

[code]

    Set the thermostat to 22 degrees in heat mode  
    → ha_call_service(domain="climate", service="set_temperature",  
        entity_id="climate.thermostat", data={"temperature": 22, "hvac_mode": "heat"})  
    
[/code]

[code]

    Set living room lights to blue at 50% brightness  
    → ha_call_service(domain="light", service="turn_on",  
        entity_id="light.living_room", data={"brightness": 128, "color_name": "blue"})  
    
[/code]

## Шлюзовая платформа: события в реальном времени[​](<#gateway-platform-real-time-events> "Прямая ссылка на Шлюзовая платформа: события в реальном времени")

Адаптер шлюза Home Assistant подключается через WebSocket и подписывается на события `state_changed`. Когда состояние устройства меняется и соответствует вашим фильтрам, оно пересылается агенту как сообщение.

### Фильтрация событий[​](<#event-filtering> "Прямая ссылка на Фильтрация событий")

Необходимая конфигурация

По умолчанию **никакие события не пересылаются**. Вы должны настроить хотя бы один из параметров `watch_domains`, `watch_entities` или `watch_all`, чтобы получать события. Без фильтров при запуске выводится предупреждение, и все изменения состояний молча игнорируются.

Настройте, какие события видит агент, в файле `~/.hermes/config.yaml` в разделе `extra` платформы Home Assistant:

[code]

    platforms:  
      homeassistant:  
        enabled: true  
        extra:  
          watch_domains:  
            - climate  
            - binary_sensor  
            - alarm_control_panel  
            - light  
          watch_entities:  
            - sensor.front_door_battery  
          ignore_entities:  
            - sensor.uptime  
            - sensor.cpu_usage  
            - sensor.memory_usage  
          cooldown_seconds: 30  
    
[/code]

Настройка| Значение по умолчанию| Описание  
---|---|---
`watch_domains`|  _(нет)_|  Следить только за доменами сущностей (например, `climate`, `light`, `binary_sensor`)  
`watch_entities`|  _(нет)_|  Следить только за указанными ID сущностей  
`watch_all`| `false`|  Установите `true`, чтобы получать **все** изменения состояний (не рекомендуется для большинства настроек)  
`ignore_entities`|  _(нет)_|  Всегда игнорировать эти сущности (применяется до фильтров по доменам/сущностям)  
`cooldown_seconds`| `30`|  Минимальное количество секунд между событиями для одной и той же сущности  

tip

Начните с небольшого набора доменов — `climate`, `binary_sensor` и `alarm_control_panel` покрывают большинство полезных автоматизаций. Добавляйте другие по мере необходимости. Используйте `ignore_entities` для подавления «шумных» датчиков, таких как температура CPU или счётчики времени работы.

### Форматирование событий[​](<#event-formatting> "Прямая ссылка на Форматирование событий")

Изменения состояний форматируются в читаемые сообщения в зависимости от домена:

Домен| Формат  
---|---
`climate`| «Режим HVAC изменён с 'off' на 'heat' (текущая: 21, целевая: 23)»  
`sensor`| «изменилось с 21°C на 22°C»  
`binary_sensor`| «сработал» / «сброшен»  
`light`, `switch`, `fan`| «включён» / «выключен»  
`alarm_control_panel`| «состояние сигнализации изменилось с 'armed_away' на 'triggered'»  
_(другие)_|  «изменилось с 'old' на 'new'»  

### Ответы агента[​](<#agent-responses> "Прямая ссылка на Ответы агента")

Исходящие сообщения от агента доставляются как **постоянные уведомления Home Assistant** (через `persistent_notification.create`). Они отображаются на панели уведомлений HA с заголовком «Hermes Agent».

### Управление подключением[​](<#connection-management> "Прямая ссылка на Управление подключением")

- **WebSocket** с 30-секундным heartbeat для событий в реальном времени
- **Автоматическое переподключение** с возрастающей задержкой: 5с → 10с → 30с → 60с
- **REST API** для исходящих уведомлений (отдельная сессия, чтобы избежать конфликтов с WebSocket)
- **Авторизация** — события HA всегда авторизованы (список разрешённых пользователей не требуется, так как `HASS_TOKEN` аутентифицирует подключение)

## Безопасность[​](<#security> "Прямая ссылка на Безопасность")

Инструменты Home Assistant применяют ограничения безопасности:

Заблокированные домены

Следующие домены сервисов **заблокированы** для предотвращения выполнения произвольного кода на хосте HA:

- `shell_command` — произвольные команды оболочки
- `command_line` — датчики/выключатели, выполняющие команды
- `python_script` — скриптовое выполнение Python
- `pyscript` — более широкая интеграция скриптов
- `hassio` — управление дополнениями, выключение/перезагрузка хоста
- `rest_command` — HTTP-запросы с сервера HA (вектор SSRF)

Попытка вызова сервисов из этих доменов возвращает ошибку.

ID сущностей проверяются по шаблону `^[a-z_][a-z0-9_]*\.[a-z0-9_]+$` для предотвращения инъекционных атак.

## Примеры автоматизаций[​](<#example-automations> "Прямая ссылка на Примеры автоматизаций")

### Утренняя рутина[​](<#morning-routine> "Прямая ссылка на Утренняя рутина")

[code]

    User: Start my morning routine  
      
    Agent:  
    1. ha_call_service(domain="light", service="turn_on",  
         entity_id="light.bedroom", data={"brightness": 128})  
    2. ha_call_service(domain="climate", service="set_temperature",  
         entity_id="climate.thermostat", data={"temperature": 22})  
    3. ha_call_service(domain="media_player", service="turn_on",  
         entity_id="media_player.kitchen_speaker")  
    
[/code]

### Проверка безопасности[​](<#security-check> "Прямая ссылка на Проверка безопасности")

[code]

    User: Is the house secure?  
      
    Agent:  
    1. ha_list_entities(domain="binary_sensor")  
         → checks door/window sensors  
    2. ha_get_state(entity_id="alarm_control_panel.home")  
         → checks alarm status  
    3. ha_list_entities(domain="lock")  
         → checks lock states  
    4. Reports: "All doors closed, alarm is armed_away, all locks engaged."  
    
[/code]

### Реактивная автоматизация (через события шлюза)[​](<#reactive-automation-via-gateway-events> "Прямая ссылка на Реактивная автоматизация (через события шлюза)")

Когда агент подключён как шлюзовая платформа, он может реагировать на события:

[code]

    [Home Assistant] Front Door: triggered (was cleared)  
      
    Agent automatically:  
    1. ha_get_state(entity_id="binary_sensor.front_door")  
    2. ha_call_service(domain="light", service="turn_on",  
         entity_id="light.hallway")  
    3. Sends notification: "Front door opened. Hallway lights turned on."  
    
[/code]

- [Настройка](<#setup>)
  - [1\. Создайте долгоживущий токен доступа](<#1-create-a-long-lived-access-token>)
  - [2\. Настройте переменные окружения](<#2-configure-environment-variables>)
  - [3\. Запустите шлюз](<#3-start-the-gateway>)
- [Доступные инструменты](<#available-tools>)
  - [`ha_list_entities`](<#ha_list_entities>)
  - [`ha_get_state`](<#ha_get_state>)
  - [`ha_list_services`](<#ha_list_services>)
  - [`ha_call_service`](<#ha_call_service>)
- [Шлюзовая платформа: события в реальном времени](<#gateway-platform-real-time-events>)
  - [Фильтрация событий](<#event-filtering>)
  - [Форматирование событий](<#event-formatting>)
  - [Ответы агента](<#agent-responses>)
  - [Управление подключением](<#connection-management>)
- [Безопасность](<#security>)
- [Примеры автоматизаций](<#example-automations>)
  - [Утренняя рутина](<#morning-routine>)
  - [Проверка безопасности](<#security-check>)
  - [Реактивная автоматизация (через события шлюза)](<#reactive-automation-via-gateway-events>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant -->
