На этой странице

Управляйте контейнерами, образами, томами, сетями и стеками Docker Compose — операции жизненного цикла, отладка, очистка и оптимизация Dockerfile.

## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")

|
|---|---
|Источник| Опциональный — установка: `hermes skills install official/devops/docker-management`
|Путь| `optional-skills/devops/docker-management`
|Версия| `1.0.0`
|Автор| sprmn24
|Лицензия| MIT
|Теги| `docker`, `containers`, `devops`, `infrastructure`, `compose`, `images`, `volumes`, `networks`, `debugging`

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")

info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.

# Docker Management

Управляйте контейнерами, образами, томами, сетями и стеками Docker Compose с помощью стандартных команд Docker CLI. Не требует дополнительных зависимостей, кроме самого Docker.

## Когда использовать[​](<#when-to-use> "Direct link to When to Use")

* Запуск, остановка, перезапуск, удаление или просмотр контейнеров
* Сборка, загрузка (pull), публикация (push), тегирование или очистка образов Docker
* Работа с Docker Compose (многосервисные стеки)
* Управление томами или сетями
* Отладка аварийно завершающегося контейнера или анализ логов
* Проверка использования диска Docker или освобождение места
* Рецензирование или оптимизация Dockerfile

## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")

* Установленный и запущенный Docker Engine
* Пользователь добавлен в группу `docker` (или используйте `sudo`)
* Docker Compose v2 (входит в состав современных установок Docker)

Быстрая проверка:

[code]
    docker --version && docker compose version

[/code]

## Краткий справочник[​](<#quick-reference> "Direct link to Quick Reference")

Задача| Команда
---|---
Запуск контейнера (в фоне)| `docker run -d --name NAME IMAGE`
Остановка + удаление| `docker stop NAME && docker rm NAME`
Просмотр логов (в реальном времени)| `docker logs --tail 50 -f NAME`
Вход в контейнер| `docker exec -it NAME /bin/sh`
Список всех контейнеров| `docker ps -a`
Сборка образа| `docker build -t TAG .`
Compose up| `docker compose up -d`
Compose down| `docker compose down`
Использование диска| `docker system df`
Очистка «висячих» объектов| `docker image prune && docker container prune`

## Процедура[​](<#procedure> "Direct link to Procedure")

### 1\\. Определите область[​](<#1-identify-the-domain> "Direct link to 1. Identify the domain")

Выясните, к какой области относится запрос:

* **Жизненный цикл контейнера** → run, stop, start, restart, rm, pause/unpause
* **Взаимодействие с контейнером** → exec, cp, logs, inspect, stats
* **Управление образами** → build, pull, push, tag, rmi, save/load
* **Docker Compose** → up, down, ps, logs, exec, build, config
* **Тома и сети** → create, inspect, rm, prune, connect
* **Устранение неполадок** → анализ логов, коды выхода, проблемы с ресурсами

### 2\\. Операции с контейнерами[​](<#2-container-operations> "Direct link to 2. Container operations")

**Запуск нового контейнера:**

[code]
    # Фоновый сервис с пробросом портов
    docker run -d --name web -p 8080:80 nginx

    # С переменными окружения
    docker run -d -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=mydb --name db postgres:16

    # С постоянными данными (именованный том)
    docker run -d -v pgdata:/var/lib/postgresql/data --name db postgres:16

    # Для разработки (bind-монтирование исходного кода)
    docker run -d -v $(pwd)/src:/app/src -p 3000:3000 --name dev my-app

    # Интерактивная отладка (автоудаление при выходе)
    docker run -it --rm ubuntu:22.04 /bin/bash

    # С ограничениями ресурсов и политикой перезапуска
    docker run -d --memory=512m --cpus=1.5 --restart=unless-stopped --name app my-app

[/code]

Ключевые флаги: `-d` фон, `-it` интерактив+tty, `--rm` автоудаление, `-p` порт (хост:контейнер), `-e` переменная окружения, `-v` том, `--name` имя, `--restart` политика перезапуска.

**Управление запущенными контейнерами:**

[code]
    docker ps                        # запущенные контейнеры
    docker ps -a                     # все (включая остановленные)
    docker stop NAME                 # корректная остановка
    docker start NAME                # запуск остановленного контейнера
    docker restart NAME              # остановка + запуск
    docker rm NAME                   # удаление остановленного контейнера
    docker rm -f NAME                # принудительное удаление запущенного контейнера
    docker container prune           # удаление ВСЕХ остановленных контейнеров

[/code]

**Взаимодействие с контейнерами:**

[code]
    docker exec -it NAME /bin/sh          # доступ к оболочке (используйте /bin/bash если доступен)
    docker exec NAME env                   # просмотр переменных окружения
    docker exec -u root NAME apt update    # запуск от имени конкретного пользователя
    docker logs --tail 100 -f NAME         # последние 100 строк в реальном времени
    docker logs --since 2h NAME            # логи за последние 2 часа
    docker cp NAME:/path/file ./local      # копирование файла из контейнера
    docker cp ./file NAME:/path/           # копирование файла в контейнер
    docker inspect NAME                    # полная информация о контейнере (JSON)
    docker stats --no-stream               # снимок использования ресурсов
    docker top NAME                        # запущенные процессы

[/code]

### 3\\. Управление образами[​](<#3-image-management> "Direct link to 3. Image management")

[code]
    # Сборка
    docker build -t my-app:latest .
    docker build -t my-app:prod -f Dockerfile.prod .
    docker build --no-cache -t my-app .              # чистая пересборка
    DOCKER_BUILDKIT=1 docker build -t my-app .       # быстрее с BuildKit

    # Загрузка и публикация
    docker pull node:20-alpine
    docker login ghcr.io
    docker tag my-app:latest registry/my-app:v1.0
    docker push registry/my-app:v1.0

    # Просмотр
    docker images                          # список локальных образов
    docker history IMAGE                   # просмотр слоёв
    docker inspect IMAGE                   # полная информация

    # Очистка
    docker image prune                     # удаление «висячих» (без тегов) образов
    docker image prune -a                  # удаление ВСЕХ неиспользуемых образов (осторожно!)
    docker image prune -a --filter "until=168h"   # неиспользуемые образы старше 7 дней

[/code]

### 4\\. Docker Compose[​](<#4-docker-compose> "Direct link to 4. Docker Compose")

[code]
    # Запуск/остановка
    docker compose up -d                   # запуск всех сервисов в фоне
    docker compose up -d --build           # пересборка образов перед запуском
    docker compose down                    # остановка и удаление контейнеров
    docker compose down -v                 # также удаление томов (УНИЧТОЖАЕТ ДАННЫЕ)

    # Мониторинг
    docker compose ps                      # список сервисов
    docker compose logs -f api             # логи конкретного сервиса в реальном времени
    docker compose logs --tail 50          # последние 50 строк всех сервисов

    # Взаимодействие
    docker compose exec api /bin/sh        # вход в запущенный сервис
    docker compose run --rm api npm test   # разовая команда (новый контейнер)
    docker compose restart api             # перезапуск конкретного сервиса

    # Проверка
    docker compose config                  # проверка и просмотр итоговой конфигурации

[/code]

**Минимальный пример compose.yml:**

[code]
    services:
      api:
        build: .
        ports:
          - "3000:3000"
        environment:
          - DATABASE_URL=postgres://user:pass@db:5432/mydb
        depends_on:
          db:
            condition: service_healthy

      db:
        image: postgres:16-alpine
        environment:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: pass
          POSTGRES_DB: mydb
        volumes:
          - pgdata:/var/lib/postgresql/data
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U user"]
          interval: 10s
          timeout: 5s
          retries: 5

    volumes:
      pgdata:

[/code]

### 5\\. Тома и сети[​](<#5-volumes-and-networks> "Direct link to 5. Volumes and networks")

[code]
    # Тома
    docker volume ls                       # список томов
    docker volume create mydata            # создание именованного тома
    docker volume inspect mydata           # информация (точка монтирования и т.д.)
    docker volume rm mydata                # удаление (если не используется)
    docker volume prune                    # удаление неиспользуемых томов

    # Сети
    docker network ls                      # список сетей
    docker network create mynet            # создание bridge-сети
    docker network inspect mynet           # информация (подключенные контейнеры)
    docker network connect mynet NAME      # подключение контейнера к сети
    docker network disconnect mynet NAME   # отключение контейнера
    docker network rm mynet                # удаление сети
    docker network prune                   # удаление неиспользуемых сетей

[/code]

### 6\\. Использование диска и очистка[​](<#6-disk-usage-and-cleanup> "Direct link to 6. Disk usage and cleanup")

Всегда начинайте с диагностики перед очисткой:

[code]
    # Проверка использования пространства
    docker system df                       # сводка
    docker system df -v                    # детальный разбор

    # Целевая очистка (безопасно)
    docker container prune                 # остановленные контейнеры
    docker image prune                     # «висячие» образы
    docker volume prune                    # неиспользуемые тома
    docker network prune                   # неиспользуемые сети

    # Агрессивная очистка (сначала подтвердите с пользователем!)
    docker system prune                    # контейнеры + образы + сети
    docker system prune -a                 # также неиспользуемые образы
    docker system prune -a --volumes       # ВСЁ — включая именованные тома

[/code]

**Предупреждение:** Никогда не выполняйте `docker system prune -a --volumes` без подтверждения пользователя. Это удаляет именованные тома с потенциально важными данными.

## Типичные ошибки[​](<#pitfalls> "Direct link to Pitfalls")

Проблема| Причина| Исправление
---|---|---
Контейнер сразу завершается| Главный процесс завершился или упал| Проверьте `docker logs NAME`, попробуйте `docker run -it --entrypoint /bin/sh IMAGE`
«port is already allocated»| Другой процесс использует этот порт| `docker ps` или `lsof -i :PORT` чтобы найти его
«no space left on device»| Диск Docker переполнен| `docker system df`, затем целевая очистка (prune)
Не удаётся подключиться к контейнеру| Приложение слушает 127.0.0.1 внутри контейнера| Приложение должно слушать `0.0.0.0`, проверьте проброс `-p`
Отказано в доступе к тому (Permission denied)| Несовпадение UID/GID хоста и контейнера| Используйте `--user $(id -u):$(id -g)` или исправьте права
Сервисы Compose не могут связаться друг с другом| Неправильная сеть или имя сервиса| Сервисы используют имя сервиса как hostname, проверьте `docker compose config`
Кэш сборки не работает| Неправильный порядок слоёв в Dockerfile| Помещайте редко меняющиеся слои первыми (зависимости до исходного кода)
Слишком большой образ| Нет multi-stage сборки, нет .dockerignore| Используйте multi-stage сборки, добавьте `.dockerignore`

## Проверка[​](<#verification> "Direct link to Verification")

После любой операции с Docker проверьте результат:

* **Контейнер запущен?** → `docker ps` (проверьте статус «Up»)
* **Логи чистые?** → `docker logs --tail 20 NAME` (нет ошибок)
* **Порт доступен?** → `curl -s http://localhost:PORT` или `docker port NAME`
* **Образ собран?** → `docker images | grep TAG`
* **Стек Compose здоров?** → `docker compose ps` (все сервисы «running» или «healthy»)
* **Освободилось место?** → `docker system df` (сравните до и после)

## Советы по оптимизации Dockerfile[​](<#dockerfile-optimization-tips> "Direct link to Dockerfile Optimization Tips")

При просмотре или создании Dockerfile предлагайте следующие улучшения:

1. **Multi-stage сборки** — разделите среду сборки и выполнения, чтобы уменьшить итоговый размер образа
2. **Порядок слоёв** — размещайте зависимости до исходного кода, чтобы изменения не инвалидировали кэшированные слои
3. **Объединяйте команды RUN** — меньше слоёв, меньше образ
4. **Используйте .dockerignore** — исключите `node_modules`, `.git`, `__pycache__` и т.д.
5. **Фиксируйте версии базовых образов** — `node:20-alpine`, а не `node:latest`
6. **Запускайте не от root** — добавьте инструкцию `USER` для безопасности
7. **Используйте slim/alpine-образы** — `python:3.12-slim`, а не `python:3.12`

* [Метаданные навыка](<#skill-metadata>)
* [Справочник: полный SKILL.md](<#reference-full-skillmd>)
* [Когда использовать](<#when-to-use>)
* [Предварительные требования](<#prerequisites>)
* [Краткий справочник](<#quick-reference>)
* [Процедура](<#procedure>)
* [1\\. Определите область](<#1-identify-the-domain>)
* [2\\. Операции с контейнерами](<#2-container-operations>)
* [3\\. Управление образами](<#3-image-management>)
* [4\\. Docker Compose](<#4-docker-compose>)
* [5\\. Тома и сети](<#5-volumes-and-networks>)
* [6\\. Использование диска и очистка](<#6-disk-usage-and-cleanup>)
* [Типичные ошибки](<#pitfalls>)
* [Проверка](<#verification>)
* [Советы по оптимизации Dockerfile](<#dockerfile-optimization-tips>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/devops/devops-docker-management -->
