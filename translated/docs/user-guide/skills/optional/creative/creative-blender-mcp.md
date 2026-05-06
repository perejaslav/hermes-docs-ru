На этой странице
Управляйте Blender напрямую из Hermes через сокетное соединение с аддоном blender-mcp. Создавайте 3D-объекты, материалы, анимации и выполняйте произвольный Python-код Blender (bpy). Используйте, когда пользователь хочет создать или изменить что-либо в Blender.

## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|   |   |
|---|---|
|Источник| Опциональный — установка через `hermes skills install official/creative/blender-mcp`  |
|Путь| `optional-skills/creative/blender-mcp`  |
|Версия| `1.0.0`  |
|Автор| alireza78a  |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")

> **info**
> Ниже приведено полное определение навыка, которое загружает Hermes при активации этого навыка. Это те инструкции, которые видит агент, когда навык активен.

# Blender MCP

Управляйте запущенным экземпляром Blender из Hermes через сокет на TCP-порту 9876.

## Настройка (однократно)[​](<#setup-one-time> "Прямая ссылка на Настройка (однократно)")

### 1. Установка аддона Blender[​](<#1-install-the-blender-addon> "Прямая ссылка на 1. Установка аддона Blender")

```bash
curl -sL https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py -o ~/Desktop/blender_mcp_addon.py
```

В Blender: Edit > Preferences > Add-ons > Install > выберите blender_mcp_addon.py. Включите "Interface: Blender MCP".

### 2. Запуск сокет-сервера в Blender[​](<#2-start-the-socket-server-in-blender> "Прямая ссылка на 2. Запуск сокет-сервера в Blender")

Нажмите N в окне просмотра Blender, чтобы открыть боковую панель. Найдите вкладку "BlenderMCP" и нажмите "Start Server".

### 3. Проверка соединения[​](<#3-verify-connection> "Прямая ссылка на 3. Проверка соединения")

```bash
nc -z -w2 localhost 9876 && echo "OPEN" || echo "CLOSED"
```

## Протокол[​](<#protocol> "Прямая ссылка на Протокол")

Простой UTF-8 JSON поверх TCP — без префикса длины.

**Отправка:** `{"type": "<command>", "params": {<kwargs>}}`

**Получение:** `{"status": "success", "result": <value>}` или `{"status": "error", "message": "<reason>"}`

## Доступные команды[​](<#available-commands> "Прямая ссылка на Доступные команды")

| type | params | Описание |
|---|---|---|
| execute_code | code (str) | Выполнить произвольный Python-код bpy |
| get_scene_info | (нет) | Список всех объектов в сцене |
| get_object_info | object_name (str) | Информация о конкретном объекте |
| get_viewport_screenshot | (нет) | Снимок текущего окна просмотра |

## Python-помощник[​](<#python-helper> "Прямая ссылка на Python-помощник")

Используйте этот код внутри вызовов execute_code:

```python
import socket, json

def blender_exec(code: str, host="localhost", port=9876, timeout=15):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.settimeout(timeout)
    payload = json.dumps({"type": "execute_code", "params": {"code": code}})
    s.sendall(payload.encode("utf-8"))
    buf = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
            try:
                json.loads(buf.decode("utf-8"))
                break
            except json.JSONDecodeError:
                continue
        except socket.timeout:
            break
    s.close()
    return json.loads(buf.decode("utf-8"))
```

## Типовые шаблоны bpy[​](<#common-bpy-patterns> "Прямая ссылка на Типовые шаблоны bpy")

### Очистка сцены[​](<#clear-scene> "Прямая ссылка на Очистка сцены")

```python
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
```

### Добавление mesh-объектов[​](<#add-mesh-objects> "Прямая ссылка на Добавление mesh-объектов")

```python
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
bpy.ops.mesh.primitive_cube_add(size=2, location=(3, 0, 0))
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=(-3, 0, 0))
```

### Создание и назначение материала[​](<#create-and-assign-material> "Прямая ссылка на Создание и назначение материала")

```python
mat = bpy.data.materials.new(name="MyMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (R, G, B, 1.0)
bsdf.inputs["Roughness"].default_value = 0.3
bsdf.inputs["Metallic"].default_value = 0.0
obj.data.materials.append(mat)
```

### Ключевая анимация[​](<#keyframe-animation> "Прямая ссылка на Ключевая анимация")

```python
obj.location = (0, 0, 0)
obj.keyframe_insert(data_path="location", frame=1)
obj.location = (0, 0, 3)
obj.keyframe_insert(data_path="location", frame=60)
```

### Рендеринг в файл[​](<#render-to-file> "Прямая ссылка на Рендеринг в файл")

```python
bpy.context.scene.render.filepath = "/tmp/render.png"
bpy.context.scene.render.engine = 'CYCLES'
bpy.ops.render.render(write_still=True)
```

## Подводные камни[​](<#pitfalls> "Прямая ссылка на Подводные камни")

* Перед запуском обязательно проверяйте, открыт ли сокет (`nc -z localhost 9876`)
* Сервер аддона необходимо запускать внутри Blender в каждой сессии (N-панель > BlenderMCP > Connect)
* Разбивайте сложные сцены на несколько небольших вызовов execute_code, чтобы избежать тайм-аутов
* Путь для сохранения рендера должен быть абсолютным (`/tmp/...`), а не относительным
* `shade_smooth()` требует, чтобы объект был выделен и находился в режиме объекта

* [Метаданные навыка](<#skill-metadata>)
* [Справочник: полный SKILL.md](<#reference-full-skillmd>)
* [Настройка (однократно)](<#setup-one-time>)
  * [1. Установка аддона Blender](<#1-install-the-blender-addon>)
  * [2. Запуск сокет-сервера в Blender](<#2-start-the-socket-server-in-blender>)
  * [3. Проверка соединения](<#3-verify-connection>)
* [Протокол](<#protocol>)
* [Доступные команды](<#available-commands>)
* [Python-помощник](<#python-helper>)
* [Типовые шаблоны bpy](<#common-bpy-patterns>)
  * [Очистка сцены](<#clear-scene>)
  * [Добавление mesh-объектов](<#add-mesh-objects>)
  * [Создание и назначение материала](<#create-and-assign-material>)
  * [Ключевая анимация](<#keyframe-animation>)
  * [Рендеринг в файл](<#render-to-file>)
* [Подводные камни](<#pitfalls>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/creative/creative-blender-mcp -->
