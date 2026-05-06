On this page
Поиск имени пользователя OSINT в 400+ социальных сетях. Найдите аккаунты в социальных сетях по имени пользователя.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Optional — установка с `hermes skills install official/security/sherlock`  |
|Path| `optional-skills/security/sherlock`  |
|Version| `1.0.0`  |
|Author| unmodeled-tyler  |
|License| MIT  |
|Tags| `osint`, `security`, `username`, `social-media`, `reconnaissance`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит в качестве инструкций, когда навык активен.
# Sherlock OSINT Username Search
Найдите аккаунты в социальных сетях по имени пользователя в 400+ социальных сетях с помощью [Sherlock Project](<https://github.com/sherlock-project/sherlock>).
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь просит найти аккаунты, связанные с именем пользователя
  * Пользователь хочет проверить доступность имени пользователя на разных платформах
  * Пользователь проводит OSINT или разведывательное исследование
  * Пользователь спрашивает «где зарегистрировано это имя пользователя?» или подобное


## Requirements[​](<#requirements> "Direct link to Requirements")
  * Установленный Sherlock CLI: `pipx install sherlock-project` или `pip install sherlock-project`
  * Альтернативно: доступен Docker (`docker run -it --rm sherlock/sherlock`)
  * Сетевой доступ для запросов к социальным платформам


## Procedure[​](<#procedure> "Direct link to Procedure")
### 1\\. Check if Sherlock is Installed[​](<#1-check-if-sherlock-is-installed> "Direct link to 1. Check if Sherlock is Installed")
**Прежде чем делать что-либо ещё**, убедитесь, что sherlock доступен:
[code] 
    sherlock --version  
    
[/code]
Если команда не выполняется:
  * Предложите установку: `pipx install sherlock-project` (рекомендуется) или `pip install sherlock-project`
  * **НЕ** пробуйте несколько методов установки — выберите один и продолжайте
  * Если установка не удалась, сообщите пользователю и остановитесь


### 2\\. Extract Username[​](<#2-extract-username> "Direct link to 2. Extract Username")
**Извлеките имя пользователя непосредственно из сообщения пользователя, если оно явно указано.**
Примеры, когда **НЕ** следует уточнять:
  * «Найди аккаунты для nasa» → имя пользователя `nasa`
  * «Поищи johndoe123» → имя пользователя `johndoe123`
  * «Проверь, существует ли alice в социальных сетях» → имя пользователя `alice`
  * «Найди пользователя bob в социальных сетях» → имя пользователя `bob`


**Используйте уточнение только если:**
  * Упомянуто несколько возможных имён пользователей («поищи alice или bob»)
  * Неоднозначная формулировка («найди моё имя пользователя» без уточнения)
  * Имя пользователя не упомянуто вообще («сделай OSINT-поиск»)


При извлечении берите **точное** имя пользователя, как указано — сохраняйте регистр, цифры, подчёркивания и т.д.
### 3\\. Build Command[​](<#3-build-command> "Direct link to 3. Build Command")
**Команда по умолчанию** (используйте эту, если пользователь не запросил иное):
[code] 
    sherlock --print-found --no-color "<username>" --timeout 90  
    
[/code]
**Опциональные флаги** (добавляйте только если пользователь явно запросил):
  * `--nsfw` — Включить NSFW-сайты (только если пользователь просит)
  * `--tor` — Маршрутизация через Tor (только если пользователь просит анонимность)


**НЕ спрашивайте о настройках через уточнение** — просто запускайте поиск по умолчанию. Пользователи могут запросить определённые опции при необходимости.
### 4\\. Execute Search[​](<#4-execute-search> "Direct link to 4. Execute Search")
Запустите через инструмент `terminal`. Команда обычно занимает 30–120 секунд в зависимости от сетевых условий и количества сайтов.
**Пример вызова terminal:**
[code] 
    {  
      "command": "sherlock --print-found --no-color \"target_username\"",  
      "timeout": 180  
    }  
    
[/code]
### 5\\. Parse and Present Results[​](<#5-parse-and-present-results> "Direct link to 5. Parse and Present Results")
Sherlock выводит найденные аккаунты в простом формате. Разберите вывод и представьте:
  1. **Строка итога:** «Найдено X аккаунтов для имени пользователя 'Y'»
  2. **Категоризированные ссылки:** Сгруппируйте по типу платформы, если это полезно (социальные, профессиональные, форумы и т.д.)
  3. **Расположение выходного файла:** Sherlock сохраняет результаты в `<username>.txt` по умолчанию


**Пример разбора вывода:**
[code] 
    [+] Instagram: https://instagram.com/username  
    [+] Twitter: https://twitter.com/username  
    [+] GitHub: https://github.com/username  
    
[/code]
Представляйте результаты в виде кликабельных ссылок, когда это возможно.
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
### No Results Found[​](<#no-results-found> "Direct link to No Results Found")
Если Sherlock не находит аккаунтов, это часто корректно — имя пользователя может не быть зарегистрировано на проверенных платформах. Предложите:
  * Проверить написание/вариант
  * Попробовать похожие имена с подстановочным знаком `?`: `sherlock "user?name"`
  * У пользователя могут быть настройки приватности или удалённые аккаунты


### Timeout Issues[​](<#timeout-issues> "Direct link to Timeout Issues")
Некоторые сайты медленные или блокируют автоматические запросы. Используйте `--timeout 120` для увеличения времени ожидания или `--site` для ограничения области поиска.
### Tor Configuration[​](<#tor-configuration> "Direct link to Tor Configuration")
`--tor` требует запущенного демона Tor. Если пользователь хочет анонимность, но Tor недоступен, предложите:
  * Установить службу Tor
  * Использовать `--proxy` с альтернативным прокси


### False Positives[​](<#false-positives> "Direct link to False Positives")
Некоторые сайты всегда возвращают «найдено» из-за структуры их ответов. Перепроверяйте неожиданные результаты вручную.
### Rate Limiting[​](<#rate-limiting> "Direct link to Rate Limiting")
Агрессивный поиск может вызвать ограничение частоты запросов. Для массового поиска имён пользователей добавляйте задержки между вызовами или используйте `--local` с кэшированными данными.
## Installation[​](<#installation> "Direct link to Installation")
### pipx (recommended)[​](<#pipx-recommended> "Direct link to pipx \\(recommended\\)")
[code] 
    pipx install sherlock-project  
    
[/code]
### pip[​](<#pip> "Direct link to pip")
[code] 
    pip install sherlock-project  
    
[/code]
### Docker[​](<#docker> "Direct link to Docker")
[code] 
    docker pull sherlock/sherlock  
    docker run -it --rm sherlock/sherlock <username>  
    
[/code]
### Linux packages[​](<#linux-packages> "Direct link to Linux packages")
Доступно на Debian 13+, Ubuntu 22.10+, Homebrew, Kali, BlackArch.
## Ethical Use[​](<#ethical-use> "Direct link to Ethical Use")
Этот инструмент предназначен только для законных OSINT- и исследовательских целей. Напомните пользователям:
  * Искать только те имена пользователей, которыми они владеют или на расследование которых имеют разрешение
  * Соблюдать условия обслуживания платформ
  * Не использовать для преследования, сталкинга или незаконной деятельности
  * Учитывать последствия для конфиденциальности перед публикацией результатов


## Verification[​](<#verification> "Direct link to Verification")
После запуска sherlock проверьте:
  1. Вывод содержит список найденных сайтов с URL
  2. Файл `<username>.txt` создан (вывод по умолчанию) при использовании файлового вывода
  3. Если использовался `--print-found`, вывод должен содержать только строки `[+]` для совпадений


## Example Interaction[​](<#example-interaction> "Direct link to Example Interaction")
**Пользователь:** «Можешь проверить, существует ли имя пользователя 'johndoe123' в социальных сетях?»
**Действия агента:**
  1. Проверить `sherlock --version` (убедиться, что установлен)
  2. Имя пользователя предоставлено — действовать напрямую
  3. Запустить: `sherlock --print-found --no-color "johndoe123" --timeout 90`
  4. Разобрать вывод и представить ссылки


**Формат ответа:**
> Найдено 12 аккаунтов для имени пользователя 'johndoe123':
> • <https://twitter.com/johndoe123> • <https://github.com/johndoe123> • <https://instagram.com/johndoe123> • [... дополнительные ссылки]
> Результаты сохранены в: johndoe123.txt
* * *
**Пользователь:** «Найди имя пользователя 'alice', включая NSFW-сайты»
**Действия агента:**
  1. Проверить, установлен ли sherlock
  2. Имя пользователя и флаг NSFW предоставлены
  3. Запустить: `sherlock --print-found --no-color --nsfw "alice" --timeout 90`
  4. Представить результаты


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Requirements](<#requirements>)
  * [Procedure](<#procedure>)
    * [1\\. Check if Sherlock is Installed](<#1-check-if-sherlock-is-installed>)
    * [2\\. Extract Username](<#2-extract-username>)
    * [3\\. Build Command](<#3-build-command>)
    * [4\\. Execute Search](<#4-execute-search>)
    * [5\\. Parse and Present Results](<#5-parse-and-present-results>)
  * [Pitfalls](<#pitfalls>)
    * [No Results Found](<#no-results-found>)
    * [Timeout Issues](<#timeout-issues>)
    * [Tor Configuration](<#tor-configuration>)
    * [False Positives](<#false-positives>)
    * [Rate Limiting](<#rate-limiting>)
  * [Installation](<#installation>)
    * [pipx (recommended)](<#pipx-recommended>)
    * [pip](<#pip>)
    * [Docker](<#docker>)
    * [Linux packages](<#linux-packages>)
  * [Ethical Use](<#ethical-use>)
  * [Verification](<#verification>)
  * [Example Interaction](<#example-interaction>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/security/security-sherlock -->
