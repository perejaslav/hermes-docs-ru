On this page
Это проверенный путь для запуска Hermes Agent непосредственно на Android-телефоне через [Termux](<https://termux.dev/>).
Он предоставляет работающий локальный CLI на телефоне, а также основные дополнительные возможности, которые, как известно, чисто устанавливаются на Android.
## Что поддерживается в проверенном пути?[​](<#what-is-supported-in-the-tested-path> "Прямая ссылка на Что поддерживается в проверенном пути?")
Проверенный комплект Termux устанавливает:
 * CLI Hermes
 * поддержку cron
 * поддержку PTY/фоновых терминалов
 * поддержку Telegram-шлюза (ручной / фоновые запуски best-effort)
 * поддержку MCP
 * поддержку памяти Honcho
 * поддержку ACP

Конкретно, это соответствует:
[code] 
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
## Что пока не входит в проверенный путь?[​](<#what-is-not-part-of-the-tested-path-yet> "Прямая ссылка на Что пока не входит в проверенный путь?")
Некоторые функции всё ещё требуют зависимостей в стиле настольных/серверных систем, которые не опубликованы для Android или не были проверены на телефонах:
 * `.[all]` не поддерживается на Android сегодня
 * расширение `voice` блокируется `faster-whisper -> ctranslate2`, а `ctranslate2` не публикует Android-колёса
 * автоматическая загрузка браузера / Playwright пропускается в установщике Termux
 * изоляция терминала на основе Docker недоступна внутри Termux
 * Android может приостанавливать фоновые задания Termux, поэтому устойчивость шлюза работает по принципу best-effort, а не как обычный управляемый сервис

Это не мешает Hermes хорошо работать в качестве нативного телефонного CLI-агента — просто рекомендуемая мобильная установка намеренно уже, чем установка на настольном компьютере/сервере.
* * *
## Вариант 1: Установка одной командой[​](<#option-1-one-line-installer> "Прямая ссылка на Вариант 1: Установка одной командой")
Hermes теперь содержит установщик с поддержкой Termux:
[code] 
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash  
    
[/code]
В Termux установщик автоматически:
 * использует `pkg` для системных пакетов
 * создаёт виртуальное окружение с помощью `python -m venv`
 * устанавливает `.[termux]` через `pip`
 * создаёт ссылку `hermes` в `$PREFIX/bin`, чтобы она оставалась в вашем PATH Termux
 * пропускает непроверенную загрузку браузера / WhatsApp

Если вам нужны явные команды или необходимо отладить неудачную установку, используйте ручной путь ниже.
* * *
## Вариант 2: Ручная установка (полностью явная)[​](<#option-2-manual-install-fully-explicit> "Прямая ссылка на Вариант 2: Ручная установка (полностью явная)")
### 1\\. Обновление Termux и установка системных пакетов[​](<#1-update-termux-and-install-system-packages> "Прямая ссылка на 1. Обновление Termux и установка системных пакетов")
[code] 
    pkg update  
    pkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ffmpeg  
    
[/code]
Зачем эти пакеты?
 * `python` — среда выполнения + поддержка виртуального окружения
 * `git` — клонирование/обновление репозитория
 * `clang`, `rust`, `make`, `pkg-config`, `libffi`, `openssl` — необходимы для сборки некоторых Python-зависимостей на Android
 * `nodejs` — опциональная среда выполнения Node для экспериментов за пределами проверенного основного пути
 * `ripgrep` — быстрый поиск по файлам
 * `ffmpeg` — конвертация медиа / TTS

### 2\\. Клонирование Hermes[​](<#2-clone-hermes> "Прямая ссылка на 2. Клонирование Hermes")
[code] 
    git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git  
    cd hermes-agent  
    
[/code]
Если вы уже клонировали без подмодулей:
[code] 
    git submodule update --init --recursive  
    
[/code]
### 3\\. Создание виртуального окружения[​](<#3-create-a-virtual-environment> "Прямая ссылка на 3. Создание виртуального окружения")
[code] 
    python -m venv venv  
    source venv/bin/activate  
    export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"  
    python -m pip install --upgrade pip setuptools wheel  
    
[/code]
`ANDROID_API_LEVEL` важен для пакетов на основе Rust / maturin, таких как `jiter`.
### 4\\. Установка проверенного комплекта Termux[​](<#4-install-the-tested-termux-bundle> "Прямая ссылка на 4. Установка проверенного комплекта Termux")
[code] 
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
Если вам нужен только минимальный основной агент, это также работает:
[code] 
    python -m pip install -e '.' -c constraints-termux.txt  
    
[/code]
### 5\\. Добавление `hermes` в PATH Termux[​](<#5-put-hermes-on-your-termux-path> "Прямая ссылка на 5. Добавление `hermes` в PATH Termux")
[code] 
    ln -sf "$PWD/venv/bin/hermes" "$PREFIX/bin/hermes"  
    
[/code]
`$PREFIX/bin` уже находится в PATH в Termux, поэтому команда `hermes` будет доступна в новых оболочках без повторной активации виртуального окружения каждый раз.
### 6\\. Проверка установки[​](<#6-verify-the-install> "Прямая ссылка на 6. Проверка установки")
[code] 
    hermes version  
    hermes doctor  
    
[/code]
### 7\\. Запуск Hermes[​](<#7-start-hermes> "Прямая ссылка на 7. Запуск Hermes")
[code] 
    hermes  
    
[/code]
* * *
## Рекомендуемая дальнейшая настройка[​](<#recommended-follow-up-setup> "Прямая ссылка на Рекомендуемая дальнейшая настройка")
### Настройка модели[​](<#configure-a-model> "Прямая ссылка на Настройка модели")
[code] 
    hermes model  
    
[/code]
Или укажите ключи напрямую в `~/.hermes/.env`.
### Повторный запуск полного интерактивного мастера настройки[​](<#re-run-the-full-interactive-setup-wizard-later> "Прямая ссылка на Повторный запуск полного интерактивного мастера настройки")
[code] 
    hermes setup  
    
[/code]
### Установка опциональных Node-зависимостей вручную[​](<#install-optional-node-dependencies-manually> "Прямая ссылка на Установка опциональных Node-зависимостей вручную")
Проверенный путь Termux намеренно пропускает загрузку Node/браузера. Если вы хотите поэкспериментировать с инструментарием браузера позже:
[code] 
    pkg install nodejs-lts  
    npm install  
    
[/code]
Инструмент браузера автоматически включает директории Termux (`/data/data/com.termux/files/usr/bin`) в свой поиск PATH, поэтому `agent-browser` и `npx` обнаруживаются без дополнительной настройки PATH.
Относитесь к инструментам браузера / WhatsApp на Android как к экспериментальным, пока не будет указано иное.
* * *
## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на Устранение неполадок")
### `No solution found` при установке `.[all]`[​](<#no-solution-found-when-installing-all> "Прямая ссылка на `No solution found` при установке `.[all]`")
Вместо этого используйте проверенный комплект Termux:
[code] 
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
Проблема в настоящее время в расширении `voice`:
 * `voice` подтягивает `faster-whisper`
 * `faster-whisper` зависит от `ctranslate2`
 * `ctranslate2` не публикует Android-колёса

### `uv pip install` не работает на Android[​](<#uv-pip-install-fails-on-android> "Прямая ссылка на `uv pip install` не работает на Android")
Используйте путь Termux со стандартным venv + `pip`:
[code] 
    python -m venv venv  
    source venv/bin/activate  
    export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"  
    python -m pip install --upgrade pip setuptools wheel  
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
### `jiter` / `maturin` сообщает об ошибке `ANDROID_API_LEVEL`[​](<#jiter--maturin-complains-about-android_api_level> "Прямая ссылка на `jiter` / `maturin` сообщает об ошибке `ANDROID_API_LEVEL`")
Установите уровень API явно перед установкой:
[code] 
    export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"  
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
### `hermes doctor` сообщает, что ripgrep или Node отсутствуют[​](<#hermes-doctor-says-ripgrep-or-node-is-missing> "Прямая ссылка на `hermes doctor` сообщает, что ripgrep или Node отсутствуют")
Установите их с помощью пакетов Termux:
[code] 
    pkg install ripgrep nodejs  
    
[/code]
### Ошибки сборки при установке Python-пакетов[​](<#build-failures-while-installing-python-packages> "Прямая ссылка на Ошибки сборки при установке Python-пакетов")
Убедитесь, что инструментарий сборки установлен:
[code] 
    pkg install clang rust make pkg-config libffi openssl  
    
[/code]
Затем повторите попытку:
[code] 
    python -m pip install -e '.[termux]' -c constraints-termux.txt  
    
[/code]
* * *
## Известные ограничения на телефонах[​](<#known-limitations-on-phones> "Прямая ссылка на Известные ограничения на телефонах")
 * Docker-бэкенд недоступен
 * локальное распознавание голоса через `faster-whisper` недоступно в проверенном пути
 * настройка автоматизации браузера намеренно пропускается установщиком
 * некоторые опциональные расширения могут работать, но только `.[termux]` в настоящее время задокументирован как проверенный комплект для Android

Если вы столкнулись с новой проблемой, специфичной для Android, пожалуйста, откройте GitHub issue с:
 * версией вашего Android
 * `termux-info`
 * `python --version`
 * `hermes doctor`
 * точной командой установки и полным выводом ошибки

 * [Что поддерживается в проверенном пути?](<#what-is-supported-in-the-tested-path>)
 * [Что пока не входит в проверенный путь?](<#what-is-not-part-of-the-tested-path-yet>)
 * [Вариант 1: Установка одной командой](<#option-1-one-line-installer>)
 * [Вариант 2: Ручная установка (полностью явная)](<#option-2-manual-install-fully-explicit>)
   * [1\\. Обновление Termux и установка системных пакетов](<#1-update-termux-and-install-system-packages>)
   * [2\\. Клонирование Hermes](<#2-clone-hermes>)
   * [3\\. Создание виртуального окружения](<#3-create-a-virtual-environment>)
   * [4\\. Установка проверенного комплекта Termux](<#4-install-the-tested-termux-bundle>)
   * [5\\. Добавление `hermes` в PATH Termux](<#5-put-hermes-on-your-termux-path>)
   * [6\\. Проверка установки](<#6-verify-the-install>)
   * [7\\. Запуск Hermes](<#7-start-hermes>)
 * [Рекомендуемая дальнейшая настройка](<#recommended-follow-up-setup>)
   * [Настройка модели](<#configure-a-model>)
   * [Повторный запуск полного интерактивного мастера настройки](<#re-run-the-full-interactive-setup-wizard-later>)
   * [Установка опциональных Node-зависимостей вручную](<#install-optional-node-dependencies-manually>)
 * [Устранение неполадок](<#troubleshooting>)
   * [`No solution found` при установке `.[all]`](<#no-solution-found-when-installing-all>)
   * [`uv pip install` не работает на Android](<#uv-pip-install-fails-on-android>)
   * [`jiter` / `maturin` сообщает об ошибке `ANDROID_API_LEVEL`](<#jiter--maturin-complains-about-android_api_level>)
   * [`hermes doctor` сообщает, что ripgrep или Node отсутствуют](<#hermes-doctor-says-ripgrep-or-node-is-missing>)
   * [Ошибки сборки при установке Python-пакетов](<#build-failures-while-installing-python-packages>)
 * [Известные ограничения на телефонах](<#known-limitations-on-phones>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/getting-started/termux -->
