On this page
Himalaya CLI: работа с email через IMAP/SMTP из терминала.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Встроенный (устанавливается по умолчанию)
|Path| `skills/email/himalaya`
|Version| `1.1.0`
|Author| community
|License| MIT
|Tags| `Email`, `IMAP`, `SMTP`, `CLI`, `Communication`
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Далее приведено полное описание навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Himalaya Email CLI
Himalaya — это CLI-почтовый клиент, позволяющий управлять электронной почтой из терминала через бэкенды IMAP, SMTP, Notmuch или Sendmail.
## References[​](<#references> "Direct link to References")
  * `references/configuration.md` (настройка конфигурационного файла + аутентификация IMAP/SMTP)
  * `references/message-composition.md` (синтаксис MML для составления писем)


## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  1. Установленный Himalaya CLI (`himalaya --version` для проверки)
  2. Конфигурационный файл `~/.config/himalaya/config.toml`
  3. Настроенные учётные данные IMAP/SMTP (пароль хранится безопасно)


### Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Готовый бинарник (Linux/macOS — рекомендуется)
    curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh
    
    # macOS через Homebrew
    brew install himalaya
    
    # Или через cargo (любая платформа с Rust)
    cargo install himalaya --locked
    
[/code]
## Configuration Setup[​](<#configuration-setup> "Direct link to Configuration Setup")
Запустите интерактивный мастер для настройки учётной записи:
[code] 
    himalaya account configure
    
[/code]
Или создайте `~/.config/himalaya/config.toml` вручную:
[code] 
    [accounts.personal]
    email = "you@example.com"
    display-name = "Your Name"
    default = true
    
    backend.type = "imap"
    backend.host = "imap.example.com"
    backend.port = 993
    backend.encryption.type = "tls"
    backend.login = "you@example.com"
    backend.auth.type = "password"
    backend.auth.cmd = "pass show email/imap"  # или используйте keyring
    
    message.send.backend.type = "smtp"
    message.send.backend.host = "smtp.example.com"
    message.send.backend.port = 587
    message.send.backend.encryption.type = "start-tls"
    message.send.backend.login = "you@example.com"
    message.send.backend.auth.type = "password"
    message.send.backend.auth.cmd = "pass show email/smtp"
    
    # Псевдонимы папок (синтаксис himalaya v1.2.0+). Обязательны, когда
    # имена папок на сервере не совпадают с каноническими именами himalaya
    # (inbox/sent/drafts/trash). Gmail — типичный пример — см.
    # `references/configuration.md` для маппинга `[Gmail]/Sent Mail`.
    folder.aliases.inbox = "INBOX"
    folder.aliases.sent = "Sent"
    folder.aliases.drafts = "Drafts"
    folder.aliases.trash = "Trash"
    
[/code]
> **Внимание по поводу синтаксиса псевдонимов.** В документации до v1.2.0 использовался подраздел `[accounts.NAME.folder.alias]` (единственное число `alias`). Начиная с v1.2.0 эта форма молча игнорируется — TOML парсится нормально, но резолвер псевдонимов её не читает, поэтому каждый запрос проваливается к каноническому имени. На Gmail это означает, что сохранение в Sent _не удаётся_ после успешной SMTP-отправки, и `himalaya message send` завершается с ненулевым кодом. Любой вызывающий код (агент, скрипт, пользователь), который повторяет попытку при таком коде возврата, перезапустит всю отправку — включая SMTP — создавая дублирующие письма получателям. Всегда используйте `folder.aliases.X` (множественное число, dotted-ключи, непосредственно в `[accounts.NAME]`).
## Hermes Integration Notes[​](<#hermes-integration-notes> "Direct link to Hermes Integration Notes")
  * **Чтение, просмотр списка, поиск, перемещение, удаление** — всё работает напрямую через инструмент терминала
  * **Составление/ответ/пересылка** — рекомендуется передача через pipe (`cat << EOF | himalaya template send`) для надёжности. Интерактивный режим `$EDITOR` работает с `pty=true` + background + процесс, но требует знания редактора и его команд
  * Используйте `--output json` для структурированного вывода, который легче разбирать программно
  * Мастер `himalaya account configure` требует интерактивного ввода — используйте PTY-режим: `terminal(command="himalaya account configure", pty=true)`


## Common Operations[​](<#common-operations> "Direct link to Common Operations")
### List Folders[​](<#list-folders> "Direct link to List Folders")
[code] 
    himalaya folder list
    
[/code]
### List Emails[​](<#list-emails> "Direct link to List Emails")
Список писем во входящих (INBOX, по умолчанию):
[code] 
    himalaya envelope list
    
[/code]
Список писем в определённой папке:
[code] 
    himalaya envelope list --folder "Sent"
    
[/code]
Список с постраничной навигацией:
[code] 
    himalaya envelope list --page 1 --page-size 20
    
[/code]
### Search Emails[​](<#search-emails> "Direct link to Search Emails")
[code] 
    himalaya envelope list from john@example.com subject meeting
    
[/code]
### Read an Email[​](<#read-an-email> "Direct link to Read an Email")
Чтение письма по ID (показывает обычный текст):
[code] 
    himalaya message read 42
    
[/code]
Экспорт сырого MIME:
[code] 
    himalaya message export 42 --full
    
[/code]
### Reply to an Email[​](<#reply-to-an-email> "Direct link to Reply to an Email")
Чтобы ответить неинтерактивно из Hermes, прочитайте исходное сообщение, составьте ответ и передайте через pipe:
[code] 
    # Получить шаблон ответа, отредактировать и отправить
    himalaya template reply 42 | sed 's/^$/\nYour reply text here\n/' | himalaya template send
    
[/code]
Или соберите ответ вручную:
[code] 
    cat << 'EOF' | himalaya template send
    From: you@example.com
    To: sender@example.com
    Subject: Re: Original Subject
    In-Reply-To: <original-message-id>
    
    Your reply here.
    EOF
    
[/code]
Ответ всем (интерактивно — требуется $EDITOR, лучше используйте подход с шаблоном выше):
[code] 
    himalaya message reply 42 --all
    
[/code]
### Forward an Email[​](<#forward-an-email> "Direct link to Forward an Email")
[code] 
    # Получить шаблон пересылки и передать с изменениями через pipe
    himalaya template forward 42 | sed 's/^To:.*/To: newrecipient@example.com/' | himalaya template send
    
[/code]
### Write a New Email[​](<#write-a-new-email> "Direct link to Write a New Email")
**Неинтерактивно (используйте это из Hermes)** — передайте сообщение через stdin:
[code] 
    cat << 'EOF' | himalaya template send
    From: you@example.com
    To: recipient@example.com
    Subject: Test Message
    
    Hello from Himalaya!
    EOF
    
[/code]
Или с флагами заголовков:
[code] 
    himalaya message write -H "To:recipient@example.com" -H "Subject:Test" "Message body here"
    
[/code]
Примечание: `himalaya message write` без передачи через pipe открывает `$EDITOR`. Это работает с `pty=true` + background-режимом, но передача через pipe проще и надёжнее.
### Move/Copy Emails[​](<#movecopy-emails> "Direct link to Move/Copy Emails")
Переместить в папку:
[code] 
    himalaya message move 42 "Archive"
    
[/code]
Скопировать в папку:
[code] 
    himalaya message copy 42 "Important"
    
[/code]
### Delete an Email[​](<#delete-an-email> "Direct link to Delete an Email")
[code] 
    himalaya message delete 42
    
[/code]
### Manage Flags[​](<#manage-flags> "Direct link to Manage Flags")
Добавить флаг:
[code] 
    himalaya flag add 42 --flag seen
    
[/code]
Удалить флаг:
[code] 
    himalaya flag remove 42 --flag seen
    
[/code]
## Multiple Accounts[​](<#multiple-accounts> "Direct link to Multiple Accounts")
Список учётных записей:
[code] 
    himalaya account list
    
[/code]
Использовать определённую учётную запись:
[code] 
    himalaya --account work envelope list
    
[/code]
## Attachments[​](<#attachments> "Direct link to Attachments")
Сохранить вложения из сообщения:
[code] 
    himalaya attachment download 42
    
[/code]
Сохранить в определённую директорию:
[code] 
    himalaya attachment download 42 --dir ~/Downloads
    
[/code]
## Output Formats[​](<#output-formats> "Direct link to Output Formats")
Большинство команд поддерживают `--output` для структурированного вывода:
[code] 
    himalaya envelope list --output json
    himalaya envelope list --output plain
    
[/code]
## Debugging[​](<#debugging> "Direct link to Debugging")
Включить отладочное логирование:
[code] 
    RUST_LOG=debug himalaya envelope list
    
[/code]
Полная трассировка с backtrace:
[code] 
    RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
    
[/code]
## Tips[​](<#tips> "Direct link to Tips")
  * Используйте `himalaya --help` или `himalaya <command> --help` для подробной справки.
  * Идентификаторы сообщений привязаны к текущей папке; повторно запрашивайте список после смены папки.
  * Для составления форматированных писем с вложениями используйте синтаксис MML (см. `references/message-composition.md`).
  * Храните пароли безопасно с помощью `pass`, системной связки ключей или команды, которая выводит пароль.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [References](<#references>)
  * [Prerequisites](<#prerequisites>)
    * [Installation](<#installation>)
  * [Configuration Setup](<#configuration-setup>)
  * [Hermes Integration Notes](<#hermes-integration-notes>)
  * [Common Operations](<#common-operations>)
    * [List Folders](<#list-folders>)
    * [List Emails](<#list-emails>)
    * [Search Emails](<#search-emails>)
    * [Read an Email](<#read-an-email>)
    * [Reply to an Email](<#reply-to-an-email>)
    * [Forward an Email](<#forward-an-email>)
    * [Write a New Email](<#write-a-new-email>)
    * [Move/Copy Emails](<#movecopy-emails>)
    * [Delete an Email](<#delete-an-email>)
    * [Manage Flags](<#manage-flags>)
  * [Multiple Accounts](<#multiple-accounts>)
  * [Attachments](<#attachments>)
  * [Output Formats](<#output-formats>)
  * [Debugging](<#debugging>)
  * [Tips](<#tips>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/email/email-himalaya -->
