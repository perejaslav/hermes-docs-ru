On this page
Дайте Hermes телефонные возможности без изменений в ядре инструментов. Предоставьте и сохраните номер Twilio, отправляйте и получайте SMS/MMS, совершайте прямые звонки, а также делайте исходящие AI-звонки через Bland.ai или Vapi.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")

|---|---  
|Source| Опциональный — установка: `hermes skills install official/productivity/telephony`  
|Path| `optional-skills/productivity/telephony`  
|Version| `1.0.0`  
|Author| Nous Research  
|License| MIT  
|Tags| `telephony`, `phone`, `sms`, `mms`, `voice`, `twilio`, `bland.ai`, `vapi`, `calling`, `texting`  
|Related skills| [`maps`](</docs/user-guide/skills/bundled/productivity/productivity-maps>), [`google-workspace`](</docs/user-guide/skills/bundled/productivity/productivity-google-workspace>), [`agentmail`](</docs/user-guide/skills/optional/email/email-agentmail>)  

## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")

info
Ниже приведено полное определение скилла, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда скилл активен.

# Telephony — Номера, Звонки и Тексты без Изменений в Ядре Инструментов

Этот опциональный скилл даёт Hermes практические телефонные возможности, оставляя телефонию вне основного списка инструментов.
В комплекте идёт вспомогательный скрипт `scripts/telephony.py`, который умеет:
  * сохранять учётные данные провайдера в `~/.hermes/.env`
  * искать и покупать телефонный номер Twilio
  * запоминать приобретённый номер для последующих сессий
  * отправлять SMS/MMS с приобретённого номера
  * опрашивать входящие SMS для этого номера без необходимости в webhook-сервере
  * совершать прямые Twilio-звонки с использованием TwiML `<Say>` или `<Play>`
  * импортировать приобретённый номер Twilio в Vapi
  * совершать исходящие AI-звонки через Bland.ai или Vapi


## Что решает этот скилл[​](<#what-this-solves> "Direct link to What this solves")

Этот скилл предназначен для покрытия практических телефонных задач, которые действительно нужны пользователям:
  * исходящие звонки
  * отправка текстовых сообщений
  * владение переиспользуемым номером агента
  * проверка сообщений, поступающих на этот номер позже
  * сохранение этого номера и связанных ID между сессиями
  * удобная для будущего использования телефонная идентификация для опроса входящих SMS и других автоматизаций


Он **не** превращает Hermes в шлюз для входящих звонков в реальном времени. Входящие SMS обрабатываются путём опроса Twilio REST API. Этого достаточно для многих сценариев, включая уведомления и получение некоторых одноразовых кодов, без необходимости добавления инфраструктуры webhook'ов в ядро.

## Правила безопасности — обязательны[​](<#safety-rules--mandatory> "Direct link to Safety rules — mandatory")

  1. Всегда подтверждайте перед совершением звонка или отправкой текста.
  2. Никогда не набирайте экстренные номера.
  3. Никогда не используйте телефонию для преследования, спама, выдачи себя за другого или любых незаконных действий.
  4. Относитесь к сторонним телефонным номерам как к чувствительным операционным данным:
     * не сохраняйте их в память Hermes
     * не включайте их в документы скилла, сводки или заметки, если пользователь явно этого не запросил
  5. Можно сохранять **принадлежащий агенту номер Twilio**, так как это часть конфигурации пользователя.
  6. VoIP-номера **не гарантируют** работу со всеми сторонними 2FA-сервисами. Используйте с осторожностью и чётко объясняйте пользователю ожидания.


## Дерево решений — какой сервис использовать?[​](<#decision-tree--which-service-to-use> "Direct link to Decision tree — which service to use?")

Используйте эту логику вместо жёстко заданной маршрутизации провайдеров:

### 1) «Я хочу, чтобы у Hermes был собственный настоящий телефонный номер»[​](<#1-i-want-hermes-to-own-a-real-phone-number> "Direct link to 1) \"I want Hermes to own a real phone number\"")

Используйте **Twilio**.
Почему:
  * самый простой путь к покупке и сохранению номера
  * лучшая поддержка SMS/MMS
  * наиболее простой сценарий опроса входящих SMS
  * самый чистый путь к будущим входящим webhook'ам или обработке звонков


Варианты использования:
  * получать тексты позже
  * отправлять оповещения о развёртывании / cron-уведомления
  * поддерживать переиспользуемую телефонную идентификацию для агента
  * экспериментировать с телефонными сценариями аутентификации в будущем


### 2) «Мне нужен только самый простой исходящий AI-звонок прямо сейчас»[​](<#2-i-only-need-the-easiest-outbound-ai-phone-call-right-now> "Direct link to 2) \"I only need the easiest outbound AI phone call right now\"")

Используйте **Bland.ai**.
Почему:
  * самая быстрая настройка
  * один API-ключ
  * не нужно сначала покупать/импортировать номер самостоятельно


Компромисс:
  * менее гибкий
  * качество голоса приемлемое, но не лучшее


### 3) «Я хочу лучшее качество разговорного AI-голоса»[​](<#3-i-want-the-best-conversational-ai-voice-quality> "Direct link to 3) \"I want the best conversational AI voice quality\"")

Используйте **Twilio + Vapi**.
Почему:
  * Twilio даёт вам собственный номер
  * Vapi обеспечивает лучшее качество разговорных AI-звонков и большую гибкость в выборе голосов и моделей


Рекомендуемый порядок действий:
  1. Купить/сохранить номер Twilio
  2. Импортировать его в Vapi
  3. Сохранить возвращённый `VAPI_PHONE_NUMBER_ID`
  4. Использовать `ai-call --provider vapi`


### 4) «Я хочу позвонить с кастомным предварительно записанным голосовым сообщением»[​](<#4-i-want-to-call-with-a-custom-prerecorded-voice-message> "Direct link to 4) \"I want to call with a custom prerecorded voice message\"")

Используйте **прямой Twilio-звонок** с публичным URL аудио.
Почему:
  * самый простой способ воспроизвести кастомный MP3
  * хорошо сочетается с Hermes `text_to_speech` и публичным файловым хостингом или туннелем


## Файлы и постоянное состояние[​](<#files-and-persistent-state> "Direct link to Files and persistent state")

Скилл сохраняет состояние телефонии в двух местах:

### `~/.hermes/.env`[​](<#hermesenv> "Direct link to hermesenv")

Используется для долгоживущих учётных данных провайдера и ID принадлежащих номеров, например:
  * `TWILIO_ACCOUNT_SID`
  * `TWILIO_AUTH_TOKEN`
  * `TWILIO_PHONE_NUMBER`
  * `TWILIO_PHONE_NUMBER_SID`
  * `BLAND_API_KEY`
  * `VAPI_API_KEY`
  * `VAPI_PHONE_NUMBER_ID`
  * `PHONE_PROVIDER` (провайдер AI-звонков: bland или vapi)


### `~/.hermes/telephony_state.json`[​](<#hermestelephony_statejson> "Direct link to hermestelephony_statejson")

Используется для состояния, специфичного для скилла, которое должно сохраняться между сессиями, например:
  * запомненный номер Twilio / SID по умолчанию
  * запомненный ID телефонного номера Vapi
  * последний SID/дата входящего сообщения для контрольных точек опроса входящих


Это означает:
  * при следующей загрузке скилла `diagnose` сможет показать, какой номер уже настроен
  * `twilio-inbox --since-last --mark-seen` может продолжить с предыдущей контрольной точки


## Поиск вспомогательного скрипта[​](<#locate-the-helper-script> "Direct link to Locate the helper script")

После установки скилла найдите скрипт следующим образом:

[code] 
    SCRIPT="$(find ~/.hermes/skills -path '*/telephony/scripts/telephony.py' -print -quit)"  
    
[/code]

Если `SCRIPT` пуст, скилл ещё не установлен.

## Установка[​](<#install> "Direct link to Install")

Это официальный опциональный скилл, поэтому установите его из Skills Hub:

[code] 
    hermes skills search telephony  
    hermes skills install official/productivity/telephony  
    
[/code]

## Настройка провайдеров[​](<#provider-setup> "Direct link to Provider setup")

### Twilio — собственный номер, SMS/MMS, прямые звонки, опрос входящих SMS[​](<#twilio--owned-number-smsmms-direct-calls-inbound-sms-polling> "Direct link to Twilio — owned number, SMS/MMS, direct calls, inbound SMS polling")

Зарегистрируйтесь на:
  * <https://www.twilio.com/try-twilio>


Затем сохраните учётные данные в Hermes:

[code] 
    python3 "$SCRIPT" save-twilio ACXXXXXXXXXXXXXXXXXXXXXXXXXXXX your_auth_token_here  
    
[/code]

Поиск доступных номеров:

[code] 
    python3 "$SCRIPT" twilio-search --country US --area-code 702 --limit 5  
    
[/code]

Купить и запомнить номер:

[code] 
    python3 "$SCRIPT" twilio-buy "+17025551234" --save-env  
    
[/code]

Список принадлежащих номеров:

[code] 
    python3 "$SCRIPT" twilio-owned  
    
[/code]

Установить один из них как номер по умолчанию позже:

[code] 
    python3 "$SCRIPT" twilio-set-default "+17025551234" --save-env  
    # или  
    python3 "$SCRIPT" twilio-set-default PNXXXXXXXXXXXXXXXXXXXXXXXXXXXX --save-env  
    
[/code]

### Bland.ai — самый простой исходящий AI-звонок[​](<#blandai--easiest-outbound-ai-calling> "Direct link to Bland.ai — easiest outbound AI calling")

Зарегистрируйтесь на:
  * <https://app.bland.ai>


Сохраните конфигурацию:

[code] 
    python3 "$SCRIPT" save-bland your_bland_api_key --voice mason  
    
[/code]

### Vapi — лучшее качество разговорного голоса[​](<#vapi--better-conversational-voice-quality> "Direct link to Vapi — better conversational voice quality")

Зарегистрируйтесь на:
  * <https://dashboard.vapi.ai>


Сначала сохраните API-ключ:

[code] 
    python3 "$SCRIPT" save-vapi your_vapi_api_key  
    
[/code]

Импортируйте ваш номер Twilio в Vapi и сохраните возвращённый ID телефонного номера:

[code] 
    python3 "$SCRIPT" vapi-import-twilio --save-env  
    
[/code]

Если вы уже знаете ID телефонного номера Vapi, сохраните его напрямую:

[code] 
    python3 "$SCRIPT" save-vapi your_vapi_api_key --phone-number-id vapi_phone_number_id_here  
    
[/code]

## Диагностика текущего состояния[​](<#diagnose-current-state> "Direct link to Diagnose current state")

В любой момент можно проверить, что скилл уже знает:

[code] 
    python3 "$SCRIPT" diagnose  
    
[/code]

Используйте это в первую очередь при возобновлении работы в последующей сессии.

## Типовые сценарии[​](<#common-workflows> "Direct link to Common workflows")

### A. Купить номер агента и продолжать использовать его позже[​](<#a-buy-an-agent-number-and-keep-using-it-later> "Direct link to A. Buy an agent number and keep using it later")

  1. Сохраните учётные данные Twilio:


[code] 
    python3 "$SCRIPT" save-twilio AC... auth_token_here  
    
[/code]

  2. Найдите номер:


[code] 
    python3 "$SCRIPT" twilio-search --country US --area-code 702 --limit 10  
    
[/code]

  3. Купите его и сохраните в `~/.hermes/.env` + состояние:


[code] 
    python3 "$SCRIPT" twilio-buy "+17025551234" --save-env  
    
[/code]

  4. В следующей сессии выполните:


[code] 
    python3 "$SCRIPT" diagnose  
    
[/code]

Это покажет запомненный номер по умолчанию и состояние контрольной точки входящих сообщений.

### B. Отправить текст с номера агента[​](<#b-send-a-text-from-the-agent-number> "Direct link to B. Send a text from the agent number")

[code] 
    python3 "$SCRIPT" twilio-send-sms "+15551230000" "Your deployment completed successfully."  
    
[/code]

С медиа:

[code] 
    python3 "$SCRIPT" twilio-send-sms "+15551230000" "Here is the chart." --media-url "https://example.com/chart.png"  
    
[/code]

### C. Проверить входящие тексты позже без webhook-сервера[​](<#c-check-inbound-texts-later-with-no-webhook-server> "Direct link to C. Check inbound texts later with no webhook server")

Опрос входящих для номера Twilio по умолчанию:

[code] 
    python3 "$SCRIPT" twilio-inbox --limit 20  
    
[/code]

Показать только сообщения, поступившие после последней контрольной точки, и сдвинуть контрольную точку после прочтения:

[code] 
    python3 "$SCRIPT" twilio-inbox --since-last --mark-seen  
    
[/code]

Это основной ответ на вопрос «как мне получить доступ к сообщениям, приходящим на номер, при следующей загрузке скилла?»

### D. Совершить прямой Twilio-звонок со встроенным TTS[​](<#d-make-a-direct-twilio-call-with-built-in-tts> "Direct link to D. Make a direct Twilio call with built-in TTS")

[code] 
    python3 "$SCRIPT" twilio-call "+15551230000" --message "Hello! This is Hermes calling with your status update." --voice Polly.Joanna  
    
[/code]

### E. Звонок с предварительно записанным / кастомным голосовым сообщением[​](<#e-call-with-a-prerecorded--custom-voice-message> "Direct link to E. Call with a prerecorded / custom voice message")

Это основной путь для повторного использования существующей поддержки `text_to_speech` в Hermes.
Используйте это когда:
  * вы хотите, чтобы звонок использовал настроенный голос TTS Hermes, а не Twilio `<Say>`
  * вам нужна однонаправленная голосовая доставка (брифинг, оповещение, шутка, напоминание, обновление статуса)
  * вам **не нужен** живой разговорный телефонный звонок


Сгенерируйте или разместите аудио отдельно, затем:

[code] 
    python3 "$SCRIPT" twilio-call "+155****0000" --audio-url "https://example.com/briefing.mp3"  
    
[/code]

Рекомендуемый процесс Hermes TTS -> Twilio Play:
  1. Сгенерируйте аудио с помощью Hermes `text_to_speech`.
  2. Сделайте полученный MP3 общедоступным по URL.
  3. Совершите Twilio-звонок с `--audio-url`.


Пример процесса агента:
  * Попросите Hermes создать аудиосообщение с помощью `text_to_speech`
  * При необходимости опубликуйте файл через временный статический хостинг / туннель / URL объектного хранилища
  * Используйте `twilio-call --audio-url ...` для доставки по телефону


Хорошие варианты хостинга для MP3:
  * временный публичный URL объектного/файлового хранилища
  * короткоживущий туннель к локальному статическому файловому серверу
  * любой существующий HTTPS URL, который телефонный провайдер может загрузить напрямую


Важное замечание:
  * TTS Hermes отлично подходит для предварительно записанных исходящих сообщений
  * Bland/Vapi лучше подходят для **живых разговорных AI-звонков**, так как они сами управляют аудиостеком телефонии в реальном времени
  * STT/TTS Hermes сам по себе здесь не используется как движок полноценного телефонного разговора; для этого потребовалась бы гораздо более тяжёлая интеграция streaming/webhook, чем этот скилл пытается внедрить


### F. Навигация по телефонному дереву / IVR с прямым Twilio-звонком[​](<#f-navigate-a-phone-tree--ivr-with-twilio-direct-calling> "Direct link to F. Navigate a phone tree / IVR with Twilio direct calling")

Если после соединения нужно нажать цифры, используйте `--send-digits`. Twilio интерпретирует `w` как короткую паузу.

[code] 
    python3 "$SCRIPT" twilio-call "+18005551234" --message "Connecting to billing now." --send-digits "ww1w2w3"  
    
[/code]

Это полезно для перехода к определённой ветке меню перед передачей человеку или доставкой короткого статусного сообщения.

### G. Исходящий AI-звонок с Bland.ai[​](<#g-outbound-ai-phone-call-with-blandai> "Direct link to G. Outbound AI phone call with Bland.ai")

[code] 
    python3 "$SCRIPT" ai-call "+15551230000" "Call the dental office, ask for a cleaning appointment on Tuesday afternoon, and if they do not have Tuesday availability, ask for Wednesday or Thursday instead." --provider bland --voice mason --max-duration 3  
    
[/code]

Проверить статус:

[code] 
    python3 "$SCRIPT" ai-status <call_id> --provider bland  
    
[/code]

Задать Bland аналитические вопросы после завершения:

[code] 
    python3 "$SCRIPT" ai-status <call_id> --provider bland --analyze "Was the appointment confirmed?,What date and time?,Any special instructions?"  
    
[/code]

### H. Исходящий AI-звонок с Vapi c вашего номера[​](<#h-outbound-ai-phone-call-with-vapi-on-your-owned-number> "Direct link to H. Outbound AI phone call with Vapi on your owned number")

  1. Импортируйте ваш номер Twilio в Vapi:


[code] 
    python3 "$SCRIPT" vapi-import-twilio --save-env  
    
[/code]

  2. Совершите звонок:


[code] 
    python3 "$SCRIPT" ai-call "+15551230000" "You are calling to make a dinner reservation for two at 7:30 PM. If that is unavailable, ask for the nearest time between 6:30 and 8:30 PM." --provider vapi --max-duration 4  
    
[/code]

  3. Проверьте результат:


[code] 
    python3 "$SCRIPT" ai-status <call_id> --provider vapi  
    
[/code]

## Рекомендуемая процедура агента[​](<#suggested-agent-procedure> "Direct link to Suggested agent procedure")

Когда пользователь запрашивает звонок или текст:
  1. Определите, какой путь соответствует запросу, с помощью дерева решений.
  2. Запустите `diagnose`, если состояние конфигурации неясно.
  3. Соберите полные детали задачи.
  4. Подтвердите с пользователем перед набором номера или отправкой текста.
  5. Используйте правильную команду.
  6. При необходимости опросите результаты.
  7. Опишите результат, не сохраняя сторонние номера в память Hermes.


## Что этот скилл всё ещё не делает[​](<#what-this-skill-still-does-not-do> "Direct link to What this skill still does not do")

  * приём входящих звонков в реальном времени
  * прямая отправка SMS на основе webhook'ов в цикл агента
  * гарантированная поддержка произвольных сторонних 2FA-провайдеров


Для этого потребовалось бы больше инфраструктуры, чем может предоставить чистый опциональный скилл.

## Подводные камни[​](<#pitfalls> "Direct link to Pitfalls")

  * Пробные аккаунты Twilio и региональные правила могут ограничивать, кому можно звонить/писать.
  * Некоторые сервисы отклоняют VoIP-номера для 2FA.
  * `twilio-inbox` опрашивает REST API; это не мгновенная push-доставка.
  * Исходящие звонки Vapi по-прежнему зависят от наличия действительного импортированного номера.
  * Bland — самый простой, но не всегда самый качественный по звучанию.
  * Не храните произвольные сторонние телефонные номера в памяти Hermes.


## Контрольный список проверки[​](<#verification-checklist> "Direct link to Verification checklist")

После настройки вы должны уметь делать всё следующее с помощью этого скилла:
  1. `diagnose` показывает готовность провайдера и запомненное состояние
  2. поиск и покупка номера Twilio
  3. сохранение этого номера в `~/.hermes/.env`
  4. отправка SMS с принадлежащего номера
  5. опрос входящих текстов для принадлежащего номера позже
  6. совершение прямого Twilio-звонка
  7. совершение AI-звонка через Bland или Vapi


## Ссылки[​](<#references> "Direct link to References")

  * Twilio phone numbers: <https://www.twilio.com/docs/phone-numbers/api>
  * Twilio messaging: <https://www.twilio.com/docs/messaging/api/message-resource>
  * Twilio voice: <https://www.twilio.com/docs/voice/api/call-resource>
  * Vapi docs: <https://docs.vapi.ai/>
  * Bland.ai: <https://app.bland.ai/>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [What this solves](<#what-this-solves>)
  * [Safety rules — mandatory](<#safety-rules--mandatory>)
  * [Decision tree — which service to use?](<#decision-tree--which-service-to-use>)
    * [1) "I want Hermes to own a real phone number"](<#1-i-want-hermes-to-own-a-real-phone-number>)
    * [2) "I only need the easiest outbound AI phone call right now"](<#2-i-only-need-the-easiest-outbound-ai-phone-call-right-now>)
    * [3) "I want the best conversational AI voice quality"](<#3-i-want-the-best-conversational-ai-voice-quality>)
    * [4) "I want to call with a custom prerecorded voice message"](<#4-i-want-to-call-with-a-custom-prerecorded-voice-message>)
  * [Files and persistent state](<#files-and-persistent-state>)
    * [`~/.hermes/.env`](<#hermesenv>)
    * [`~/.hermes/telephony_state.json`](<#hermestelephony_statejson>)
  * [Locate the helper script](<#locate-the-helper-script>)
  * [Install](<#install>)
  * [Provider setup](<#provider-setup>)
    * [Twilio — owned number, SMS/MMS, direct calls, inbound SMS polling](<#twilio--owned-number-smsmms-direct-calls-inbound-sms-polling>)
    * [Bland.ai — easiest outbound AI calling](<#blandai--easiest-outbound-ai-calling>)
    * [Vapi — better conversational voice quality](<#vapi--better-conversational-voice-quality>)
  * [Diagnose current state](<#diagnose-current-state>)
  * [Common workflows](<#common-workflows>)
    * [A. Buy an agent number and keep using it later](<#a-buy-an-agent-number-and-keep-using-it-later>)
    * [B. Send a text from the agent number](<#b-send-a-text-from-the-agent-number>)
    * [C. Check inbound texts later with no webhook server](<#c-check-inbound-texts-later-with-no-webhook-server>)
    * [D. Make a direct Twilio call with built-in TTS](<#d-make-a-direct-twilio-call-with-built-in-tts>)
    * [E. Call with a prerecorded / custom voice message](<#e-call-with-a-prerecorded--custom-voice-message>)
    * [F. Navigate a phone tree / IVR with Twilio direct calling](<#f-navigate-a-phone-tree--ivr-with-twilio-direct-calling>)
    * [G. Outbound AI phone call with Bland.ai](<#g-outbound-ai-phone-call-with-blandai>)
    * [H. Outbound AI phone call with Vapi on your owned number](<#h-outbound-ai-phone-call-with-vapi-on-your-owned-number>)
  * [Suggested agent procedure](<#suggested-agent-procedure>)
  * [What this skill still does not do](<#what-this-skill-still-does-not-do>)
  * [Pitfalls](<#pitfalls>)
  * [Verification checklist](<#verification-checklist>)
  * [References](<#references>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-telephony -->
