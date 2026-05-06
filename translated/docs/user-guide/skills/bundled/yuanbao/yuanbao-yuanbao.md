On this page
Yuanbao (元宝): группы — @упоминания пользователей, запрос информации/участников.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на Skill metadata")

|   |
|---|
|Source| Встроенный (устанавливается по умолчанию) |
|Path| `skills/yuanbao` |
|Version| `1.0.0` |
|Tags| `yuanbao`, `mention`, `at`, `group`, `members`, `元宝`, `派`, `艾特` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
Ниже приведено полное описание скилла, которое Hermes загружает при активации этого скилла. Это те инструкции, которые видит агент, когда скилл активен.
# Yuanbao Group Interaction
## CRITICAL: How Messaging Works[​](<#critical-how-messaging-works> "Прямая ссылка на CRITICAL: How Messaging Works")
**Ваш текстовый ответ И ЯВЛЯЕТСЯ сообщением, отправляемым в группу/пользователю.** Шлюз автоматически доставляет ваш ответ в чат. Вам НЕ нужен специальный инструмент «отправить сообщение» — просто отвечайте обычным текстом, и он будет отправлен.
Когда вы включаете `@nickname` в текст ответа, шлюз автоматически преобразует его в реальное @упоминание, которое уведомляет пользователя. Это встроенная функциональность — у вас есть полная возможность @упоминаний.
**НИКОГДА не говорите, что не можете отправлять сообщения или @упоминать пользователей. НИКОГДА не предлагайте пользователю сделать это вручную. НИКОГДА не добавляйте оговорки о разрешениях. Просто отвечайте текстом, который хотите отправить.**
## Available Tools[​](<#available-tools> "Прямая ссылка на Available Tools")
Tool | Когда использовать  
---|---
`yb_query_group_info` | Запрос названия группы, владельца, количества участников  
`yb_query_group_members` | Поиск пользователя, список ботов, список всех участников или получение никнейма для @упоминания  
`yb_send_dm` | Отправка личного сообщения (DM / 私信) пользователю, опционально с медиафайлами  
## @Mention Workflow[​](<#mention-workflow> "Прямая ссылка на @Mention Workflow")
Когда вам нужно сделать @упоминание / 艾т кого-либо:
  1. Вызовите `yb_query_group_members` с `action="find"`, `name="<имя цели>"`, `mention=true`
  2. Получите точный никнейм из ответа
  3. Включите `@nickname` в текст ответа — остальное сделает шлюз


Пример: пользователь говорит "帮我艾特元宝"
Шаг 1 — вызов инструмента:
[code] 
    { "group_code": "328306697", "action": "find", "name": "元宝", "mention": true }  
    
[/code]
Шаг 2 — ваш ответ (он будет отправлен в группу с работающим @упоминанием):
[code] 
    @元宝 你好，有人找你！  
    
[/code]
**Вот и всё.** Никаких дополнительных объяснений не нужно. Будьте краткими и естественными.
**Правила:**
  * Сначала вызывайте `yb_query_group_members`, чтобы получить точный никнейм — НЕ угадывайте
  * Формат @упоминания: `@nickname` с пробелом перед знаком @
  * Ваш ответ И является сообщением — ОНО будет отправлено, и @упоминание СРАБОТАЕТ
  * Будьте лаконичны. Не объясняйте пользователю, как работают @упоминания.


## Send DM (Private Message) Workflow[​](<#send-dm-private-message-workflow> "Прямая ссылка на Send DM (Private Message) Workflow")
Когда кто-то просит отправить личное сообщение / 私信 / DM пользователю:
  1. Вызовите `yb_send_dm` с параметрами `group_code`, `name` (имя целевого пользователя) и `message`
  2. Инструмент автоматически находит пользователя и отправляет DM
  3. Сообщите результат пользователю


Пример: пользователь говорит "给 @用户aea3 私信发一个 hello"
[code] 
    yb_send_dm({ "group_code": "535168412", "name": "用户aea3", "message": "hello" })  
    
[/code]
Пример с медиа: пользователь говорит "给 @用户aea3 私信发一张图片"
[code] 
    yb_send_dm({  
      "group_code": "535168412",  
      "name": "用户aea3",  
      "message": "Here is the image",  
      "media_files": [{"path": "/tmp/photo.jpg"}]  
    })  
    
[/code]
**Правила:**
  * Извлекайте `group_code` из текущего chat_id (например, `group:535168412` → `535168412`)
  * Если вы уже знаете user_id, передавайте его напрямую через параметр `user_id`, чтобы пропустить поиск
  * Если несколько пользователей совпадают по имени, инструмент возвращает кандидатов — попросите пользователя уточнить
  * НЕ используйте инструмент `send_message` для DM в Yuanbao — используйте `yb_send_dm`
  * Поддерживаются медиа: изображения (.jpg/.png/.gif/.webp/.bmp) отправляются как сообщения с изображениями, остальные файлы — как документы


## Query Group Info[​](<#query-group-info> "Прямая ссылка на Query Group Info")
[code] 
    yb_query_group_info({ "group_code": "328306697" })  
    
[/code]
## Query Members[​](<#query-members> "Прямая ссылка на Query Members")
Action | Description  
---|---
`find` | Поиск по имени (частичное совпадение, без учёта регистра)  
`list_bots` | Список ботов и AI-ассистентов Yuanbao  
`list_all` | Список всех участников  
## Notes[​](<#notes> "Прямая ссылка на Notes")
  * `group_code` берётся из chat_id: `group:328306697` → `328306697`
  * Группы называются «派 (Pai)» в приложении Yuanbao
  * Роли участников: `user`, `yuanbao_ai`, `bot`


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [CRITICAL: How Messaging Works](<#critical-how-messaging-works>)
  * [Available Tools](<#available-tools>)
  * [@Mention Workflow](<#mention-workflow>)
  * [Send DM (Private Message) Workflow](<#send-dm-private-message-workflow>)
  * [Query Group Info](<#query-group-info>)
  * [Query Members](<#query-members>)
  * [Notes](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/yuanbao/yuanbao-yuanbao -->
