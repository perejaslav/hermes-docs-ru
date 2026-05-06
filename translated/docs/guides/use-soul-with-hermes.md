На этой странице
`SOUL.md` — это **основная идентичность** вашего экземпляра Hermes. Это первое, что находится в системном промпте — он определяет, кем является агент, как он говорит и чего избегает.
Если вы хотите, чтобы Hermes ощущался как один и тот же ассистент при каждом разговоре — или если вы хотите полностью заменить персону Hermes на свою собственную — это тот самый файл.
## Для чего нужен SOUL.md[​](<#what-soulmd-is-for> "Прямая ссылка на раздел «Для чего нужен SOUL.md»")
Используйте `SOUL.md` для:
  * тона
  * личности
  * стиля общения
  * степени прямоты или теплоты Hermes
  * того, чего Hermes должен стилистически избегать
  * того, как Hermes должен относиться к неопределённости, разногласиям и двусмысленности


Короче говоря:
  * `SOUL.md` — это о том, кто такой Hermes и как он говорит


## Для чего НЕ предназначен SOUL.md[​](<#what-soulmd-is-not-for> "Прямая ссылка на раздел «Для чего НЕ предназначен SOUL.md»")
Не используйте его для:
  * соглашений о коде, специфичных для репозитория
  * путей к файлам
  * команд
  * портов сервисов
  * заметок по архитектуре
  * инструкций по рабочему процессу проекта


Всё это должно быть в `AGENTS.md`.
Хорошее правило:
  * если это должно применяться везде — поместите в `SOUL.md`
  * если это относится только к одному проекту — поместите в `AGENTS.md`


## Где он находится[​](<#where-it-lives> "Прямая ссылка на раздел «Где он находится»")
Hermes теперь использует только глобальный SOUL-файл для текущего экземпляра:
[code] 
    ~/.hermes/SOUL.md  
    
[/code]
Если вы запускаете Hermes с пользовательской домашней директорией, она становится:
[code] 
    $HERMES_HOME/SOUL.md  
    
[/code]
## Поведение при первом запуске[​](<#first-run-behavior> "Прямая ссылка на раздел «Поведение при первом запуске»")
Hermes автоматически создаёт стартовый `SOUL.md`, если его ещё не существует.
Это означает, что большинство пользователей теперь начинают с реального файла, который можно сразу прочитать и отредактировать.
Важно:
  * если у вас уже есть `SOUL.md`, Hermes не перезаписывает его
  * если файл существует, но пуст, Hermes ничего из него не добавляет в промпт


## Как Hermes его использует[​](<#how-hermes-uses-it> "Прямая ссылка на раздел «Как Hermes его использует»")
Когда Hermes запускает сессию, он читает `SOUL.md` из `HERMES_HOME`, сканирует его на предмет паттернов промпт-инъекций, при необходимости усекает и использует как **идентичность агента** — слот №1 в системном промпте. Это означает, что SOUL.md полностью заменяет встроенный текст идентичности по умолчанию.
Если SOUL.md отсутствует, пуст или не может быть загружен, Hermes возвращается к встроенной идентичности по умолчанию.
Вокруг файла не добавляется никакого языка-обёртки. Важен сам контент — пишите так, как вы хотите, чтобы ваш агент думал и говорил.
## Хорошее первое редактирование[​](<#a-good-first-edit> "Прямая ссылка на раздел «Хорошее первое редактирование»")
Если вы ничего больше не сделаете, откройте файл и измените всего несколько строк, чтобы он стал похож на вас.
Например:
[code] 
    You are direct, calm, and technically precise.  
    Prefer substance over politeness theater.  
    Push back clearly when an idea is weak.  
    Keep answers compact unless deeper detail is useful.  
    
[/code]
Уже одно это может заметно изменить ощущение от Hermes.
## Примеры стилей[​](<#example-styles> "Прямая ссылка на раздел «Примеры стилей»")
### 1\. Прагматичный инженер[​](<#1-pragmatic-engineer> "Прямая ссылка на раздел «1. Прагматичный инженер»")
[code] 
    You are a pragmatic senior engineer.  
    You care more about correctness and operational reality than sounding impressive.  
      
    ## Style  
    - Be direct  
    - Be concise unless complexity requires depth  
    - Say when something is a bad idea  
    - Prefer practical tradeoffs over idealized abstractions  
      
    ## Avoid  
    - Sycophancy  
    - Hype language  
    - Overexplaining obvious things  
    
[/code]
### 2\. Исследовательский партнёр[​](<#2-research-partner> "Прямая ссылка на раздел «2. Исследовательский партнёр»")
[code] 
    You are a thoughtful research collaborator.  
    You are curious, honest about uncertainty, and excited by unusual ideas.  
      
    ## Style  
    - Explore possibilities without pretending certainty  
    - Distinguish speculation from evidence  
    - Ask clarifying questions when the idea space is underspecified  
    - Prefer conceptual depth over shallow completeness  
    
[/code]
### 3\. Учитель / Объясняющий[​](<#3-teacher--explainer> "Прямая ссылка на раздел «3. Учитель / Объясняющий»")
[code] 
    You are a patient technical teacher.  
    You care about understanding, not performance.  
      
    ## Style  
    - Explain clearly  
    - Use examples when they help  
    - Do not assume prior knowledge unless the user signals it  
    - Build from intuition to details  
    
[/code]
### 4\. Строгий рецензент[​](<#4-tough-reviewer> "Прямая ссылка на раздел «4. Строгий рецензент»")
[code] 
    You are a rigorous reviewer.  
    You are fair, but you do not soften important criticism.  
      
    ## Style  
    - Point out weak assumptions directly  
    - Prioritize correctness over harmony  
    - Be explicit about risks and tradeoffs  
    - Prefer blunt clarity to vague diplomacy  
    
[/code]
## Что делает SOUL.md сильным?[​](<#what-makes-a-strong-soulmd> "Прямая ссылка на раздел «Что делает SOUL.md сильным?»")
Сильный `SOUL.md` — это:
  * стабильный
  * широко применимый
  * конкретный по голосу
  * не перегруженный временными инструкциями


Слабый `SOUL.md` — это:
  * полный деталей проектов
  * противоречивый
  * пытающийся микроуправлять каждой формой ответа
  * в основном общие шаблоны вроде «будь полезным» и «будь понятным»


Hermes и так пытается быть полезным и понятным. `SOUL.md` должен добавлять настоящую личность и стиль, а не повторять очевидные умолчания.
## Рекомендуемая структура[​](<#suggested-structure> "Прямая ссылка на раздел «Рекомендуемая структура»")
Заголовки не обязательны, но они помогают.
Простая структура, которая хорошо работает:
[code] 
    # Identity  
    Who Hermes is.  
      
    # Style  
    How Hermes should sound.  
      
    # Avoid  
    What Hermes should not do.  
      
    # Defaults  
    How Hermes should behave when ambiguity appears.  
    
[/code]
## SOUL.md vs /personality[​](<#soulmd-vs-personality> "Прямая ссылка на раздел «SOUL.md vs /personality»")
Они дополняют друг друга.
Используйте `SOUL.md` для долгосрочной базовой настройки. Используйте `/personality` для временных переключений режимов.
Примеры:
  * ваш SOUL по умолчанию — прагматичный и прямой
  * затем для одной сессии вы используете `/personality teacher`
  * позже вы возвращаетесь обратно, не меняя ваш базовый голосовой файл


## SOUL.md vs AGENTS.md[​](<#soulmd-vs-agentsmd> "Прямая ссылка на раздел «SOUL.md vs AGENTS.md»")
Это самая распространённая ошибка.
### Поместите это в SOUL.md[​](<#put-this-in-soulmd> "Прямая ссылка на раздел «Поместите это в SOUL.md»")
  * «Будь прямолинейным.»
  * «Избегай хайпового языка.»
  * «Предпочитай короткие ответы, если глубина не помогает.»
  * «Возражай, когда пользователь не прав.»


### Поместите это в AGENTS.md[​](<#put-this-in-agentsmd> "Прямая ссылка на раздел «Поместите это в AGENTS.md»")
  * «Используй pytest, а не unittest.»
  * «Фронтенд находится в `frontend/`.»
  * «Никогда не редактируй миграции напрямую.»
  * «API работает на порту 8000.»


## Как редактировать[​](<#how-to-edit-it> "Прямая ссылка на раздел «Как редактировать»")
[code] 
    nano ~/.hermes/SOUL.md  
    
[/code]
или
[code] 
    vim ~/.hermes/SOUL.md  
    
[/code]
Затем перезапустите Hermes или начните новую сессию.
## Практический рабочий процесс[​](<#a-practical-workflow> "Прямая ссылка на раздел «Практический рабочий процесс»")
  1. Начните с созданного по умолчанию файла
  2. Удалите всё, что не соответствует голосу, который вы хотите
  3. Добавьте 4–8 строк, чётко определяющих тон и умолчания
  4. Поговорите с Hermes некоторое время
  5. Откорректируйте на основе того, что всё ещё кажется не так


Такой итеративный подход работает лучше, чем попытка спроектировать идеальную личность за один раз.
## Устранение неполадок[​](<#troubleshooting> "Прямая ссылка на раздел «Устранение неполадок»")
### Я отредактировал SOUL.md, но Hermes всё ещё звучит так же[​](<#i-edited-soulmd-but-hermes-still-sounds-the-same> "Прямая ссылка на раздел «Я отредактировал SOUL.md, но Hermes всё ещё звучит так же»")
Проверьте:
  * вы редактировали `~/.hermes/SOUL.md` или `$HERMES_HOME/SOUL.md`
  * а не какой-то локальный для репозитория `SOUL.md`
  * файл не пуст
  * сессия была перезапущена после редактирования
  * наложение `/personality` не переопределяет результат


### Hermes игнорирует части моего SOUL.md[​](<#hermes-is-ignoring-parts-of-my-soulmd> "Прямая ссылка на раздел «Hermes игнорирует части моего SOUL.md»")
Возможные причины:
  * инструкции с более высоким приоритетом переопределяют его
  * файл содержит противоречивые указания
  * файл слишком длинный и был усечён
  * часть текста напоминает контент для промпт-инъекций и может быть заблокирована или изменена сканером


### Мой SOUL.md стал слишком привязан к проекту[​](<#my-soulmd-became-too-project-specific> "Прямая ссылка на раздел «Мой SOUL.md стал слишком привязан к проекту»")
Перенесите проектные инструкции в `AGENTS.md` и оставьте `SOUL.md` сфокусированным на идентичности и стиле.
## Связанные документы[​](<#related-docs> "Прямая ссылка на раздел «Связанные документы»")
  * [Personality & SOUL.md](</docs/user-guide/features/personality>)
  * [Контекстные файлы](</docs/user-guide/features/context-files>)
  * [Конфигурация](</docs/user-guide/configuration>)
  * [Советы и лучшие практики](</docs/guides/tips>)


  * [Для чего нужен SOUL.md](<#what-soulmd-is-for>)
  * [Для чего НЕ предназначен SOUL.md](<#what-soulmd-is-not-for>)
  * [Где он находится](<#where-it-lives>)
  * [Поведение при первом запуске](<#first-run-behavior>)
  * [Как Hermes его использует](<#how-hermes-uses-it>)
  * [Хорошее первое редактирование](<#a-good-first-edit>)
  * [Примеры стилей](<#example-styles>)
    * [1\. Прагматичный инженер](<#1-pragmatic-engineer>)
    * [2\. Исследовательский партнёр](<#2-research-partner>)
    * [3\. Учитель / Объясняющий](<#3-teacher--explainer>)
    * [4\. Строгий рецензент](<#4-tough-reviewer>)
  * [Что делает SOUL.md сильным?](<#what-makes-a-strong-soulmd>)
  * [Рекомендуемая структура](<#suggested-structure>)
  * [SOUL.md vs /personality](<#soulmd-vs-personality>)
  * [SOUL.md vs AGENTS.md](<#soulmd-vs-agentsmd>)
    * [Поместите это в SOUL.md](<#put-this-in-soulmd>)
    * [Поместите это в AGENTS.md](<#put-this-in-agentsmd>)
  * [Как редактировать](<#how-to-edit-it>)
  * [Практический рабочий процесс](<#a-practical-workflow>)
  * [Устранение неполадок](<#troubleshooting>)
    * [Я отредактировал SOUL.md, но Hermes всё ещё звучит так же](<#i-edited-soulmd-but-hermes-still-sounds-the-same>)
    * [Hermes игнорирует части моего SOUL.md](<#hermes-is-ignoring-parts-of-my-soulmd>)
    * [Мой SOUL.md стал слишком привязан к проекту](<#my-soulmd-became-too-project-specific>)
  * [Связанные документы](<#related-docs>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes -->
