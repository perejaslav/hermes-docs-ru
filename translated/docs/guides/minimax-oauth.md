On this page
Hermes Agent поддерживает **MiniMax** через браузерный OAuth-логин, используя те же учётные данные, что и [портал MiniMax](<https://www.minimax.io>). Никаких API-ключей или кредитных карт не требуется — достаточно войти один раз, и Hermes автоматически будет обновлять вашу сессию.
Транспорт использует тот же адаптер `anthropic_messages` (MiniMax предоставляет совместимый с Anthropic Messages эндпоинт на `/anthropic`), поэтому все существующие функции вызова инструментов, стриминга и контекста работают без каких-либо изменений адаптера.
## Overview[​](<#overview> "Direct link to Overview")
Item| Value  
---|---  
Provider ID| `minimax-oauth`  
Display name| MiniMax (OAuth)  
Auth type| Browser OAuth (PKCE device-code flow)  
Transport| Anthropic Messages-compatible (`anthropic_messages`)  
Models| `MiniMax-M2.7`, `MiniMax-M2.7-highspeed`  
Global endpoint| `https://api.minimax.io/anthropic`  
China endpoint| `https://api.minimaxi.com/anthropic`  
Requires env var| No (`MINIMAX_API_KEY` **не** используется для этого провайдера)  
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * Python 3.9+
  * Установленный Hermes Agent
  * Аккаунт MiniMax на [minimax.io](<https://www.minimax.io>) (глобальный) или [minimaxi.com](<https://www.minimaxi.com>) (Китай)
  * Браузер на локальной машине (или используйте `--no-browser` для удалённых сессий)


## Quick Start[​](<#quick-start> "Direct link to Quick Start")
[code] 
    # Запустите выбор провайдера и модели  
    hermes model  
    # → Выберите "MiniMax (OAuth)" из списка провайдеров  
    # → Hermes откроет ваш браузер на странице авторизации MiniMax  
    # → Подтвердите доступ в браузере  
    # → Выберите модель (MiniMax-M2.7 или MiniMax-M2.7-highspeed)  
    # → Начинайте общение  
      
    hermes  
    
[/code]
После первого входа учётные данные сохраняются в `~/.hermes/auth.json` и автоматически обновляются перед каждой сессией.
## Logging In Manually[​](<#logging-in-manually> "Direct link to Logging In Manually")
Вы можете запустить логин, не проходя через выбор модели:
[code] 
    hermes auth add minimax-oauth  
    
[/code]
### China region[​](<#china-region> "Direct link to China region")
Если ваш аккаунт находится на китайской платформе (`minimaxi.com`), передайте флаг `--region cn`:
[code] 
    hermes auth add minimax-oauth --region cn  
    
[/code]
### Remote / headless sessions[​](<#remote--headless-sessions> "Direct link to Remote / headless sessions")
На серверах или в контейнерах, где нет браузера:
[code] 
    hermes auth add minimax-oauth --no-browser  
    
[/code]
Hermes выведет URL для верификации и код пользователя — откройте URL на любом устройстве и введите код, когда будет предложено.
## The OAuth Flow[​](<#the-oauth-flow> "Direct link to The OAuth Flow")
Hermes реализует PKCE device-code flow через OAuth-эндпоинты MiniMax:
  1. Hermes генерирует пару PKCE verifier / challenge и случайное значение state.
  2. Он отправляет POST-запрос на `{base_url}/oauth/code` с challenge и получает `user_code` и `verification_uri`.
  3. Ваш браузер открывает `verification_uri`. При необходимости введите `user_code`.
  4. Hermes опрашивает `{base_url}/oauth/token` до получения токена (или до истечения времени ожидания).
  5. Токены (`access_token`, `refresh_token`, срок действия) сохраняются в `~/.hermes/auth.json` под ключом `minimax-oauth`.


Обновление токена (стандартный OAuth-грант `refresh_token`) выполняется автоматически при каждом запуске сессии, если до истечения срока действия access-токена осталось менее 60 секунд.
## Checking Login Status[​](<#checking-login-status> "Direct link to Checking Login Status")
[code] 
    hermes doctor  
    
[/code]
Раздел `◆ Auth Providers` покажет:
[code] 
    ✓ MiniMax OAuth  (logged in, region=global)  
    
[/code]
или, если не авторизованы:
[code] 
    ⚠ MiniMax OAuth  (not logged in)  
    
[/code]
## Switching Models[​](<#switching-models> "Direct link to Switching Models")
[code] 
    hermes model  
    # → Выберите "MiniMax (OAuth)"  
    # → Выберите модель из списка  
    
[/code]
Или укажите модель напрямую:
[code] 
    hermes config set model MiniMax-M2.7  
    hermes config set provider minimax-oauth  
    
[/code]
## Configuration Reference[​](<#configuration-reference> "Direct link to Configuration Reference")
После входа в систему `~/.hermes/config.yaml` будет содержать записи, похожие на:
[code] 
    model:  
      default: MiniMax-M2.7  
      provider: minimax-oauth  
      base_url: https://api.minimax.io/anthropic  
    
[/code]
### `--region` flag[​](<#--region-flag> "Direct link to --region-flag")
Value| Portal| Inference endpoint  
---|---|---  
`global` (default)| `https://api.minimax.io`| `https://api.minimax.io/anthropic`  
`cn`| `https://api.minimaxi.com`| `https://api.minimaxi.com/anthropic`  
### Provider aliases[​](<#provider-aliases> "Direct link to Provider aliases")
Все следующие значения разрешаются в `minimax-oauth`:
[code] 
    hermes --provider minimax-oauth    # каноническое  
    hermes --provider minimax-portal   # псевдоним  
    hermes --provider minimax-global   # псевдоним  
    hermes --provider minimax_oauth    # псевдоним (с подчёркиванием)  
    
[/code]
## Environment Variables[​](<#environment-variables> "Direct link to Environment Variables")
Провайдер `minimax-oauth` **не** использует `MINIMAX_API_KEY` или `MINIMAX_BASE_URL`. Эти переменные предназначены только для провайдеров `minimax` и `minimax-cn`, работающих по API-ключу.
Variable| Effect  
---|---  
`MINIMAX_API_KEY`| Используется только провайдером `minimax` — игнорируется для `minimax-oauth`  
`MINIMAX_CN_API_KEY`| Используется только провайдером `minimax-cn` — игнорируется для `minimax-oauth`  
Чтобы принудительно использовать провайдер `minimax-oauth` во время выполнения:
[code] 
    HERMES_INFERENCE_PROVIDER=minimax-oauth hermes  
    
[/code]
## Models[​](<#models> "Direct link to Models")
Model| Best for  
---|---  
`MiniMax-M2.7`| Длинные контексты, сложный вызов инструментов  
`MiniMax-M2.7-highspeed`| Низкая задержка, лёгкие задачи, вспомогательные вызовы  
Обе модели поддерживают до 200 000 токенов контекста.
`MiniMax-M2.7-highspeed` также автоматически используется в качестве вспомогательной модели для задач зрения и делегирования, когда `minimax-oauth` является основным провайдером.
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### Token expired — not re-logging in automatically[​](<#token-expired--not-re-logging-in-automatically> "Direct link to Token expired — not re-logging in automatically")
Hermes обновляет токен при каждом запуске сессии, если до истечения его срока действия осталось менее 60 секунд. Если access-токен уже истёк (например, после длительного офлайн-периода), обновление происходит автоматически при следующем запросе. Если обновление не удаётся с ошибкой `refresh_token_reused` или `invalid_grant`, Hermes помечает сессию как требующую повторного входа.
**Решение:** снова выполните `hermes auth add minimax-oauth`, чтобы начать новый логин.
### Authorization timed out[​](<#authorization-timed-out> "Direct link to Authorization timed out")
Device-code flow имеет ограниченное время ожидания. Если вы не подтвердите вход вовремя, Hermes выдаст ошибку тайм-аута.
**Решение:** повторно выполните `hermes auth add minimax-oauth` (или `hermes model`). Процесс начнётся заново.
### State mismatch (possible CSRF)[​](<#state-mismatch-possible-csrf> "Direct link to State mismatch (possible CSRF)")
Hermes обнаружил, что значение `state`, возвращённое сервером авторизации, не соответствует тому, что было отправлено.
**Решение:** повторите вход. Если ошибка сохраняется, проверьте, не изменяет ли прокси или редирект OAuth-ответ.
### Logging in from a remote server[​](<#logging-in-from-a-remote-server> "Direct link to Logging in from a remote server")
Если `hermes` не может открыть окно браузера, используйте `--no-browser`:
[code] 
    hermes auth add minimax-oauth --no-browser  
    
[/code]
Hermes выведет URL и код. Откройте URL на любом устройстве и завершите процесс там.
### "Not logged into MiniMax OAuth" error at runtime[​](<#not-logged-into-minimax-oauth-error-at-runtime> "Direct link to \"Not logged into MiniMax OAuth\" error at runtime")
Хранилище аутентификации не содержит учётных данных для `minimax-oauth`. Вы ещё не вошли в систему, или файл с учётными данными был удалён.
**Решение:** выполните `hermes model` и выберите MiniMax (OAuth), или выполните `hermes auth add minimax-oauth`.
## Logging Out[​](<#logging-out> "Direct link to Logging Out")
Чтобы удалить сохранённые учётные данные MiniMax OAuth:
[code] 
    hermes auth remove minimax-oauth  
    
[/code]
## See Also[​](<#see-also> "Direct link to See Also")
  * [AI Providers reference](</docs/integrations/providers>)
  * [Environment Variables](</docs/reference/environment-variables>)
  * [Configuration](</docs/user-guide/configuration>)
  * [hermes doctor](</docs/reference/cli-commands>)


  * [Overview](<#overview>)
  * [Prerequisites](<#prerequisites>)
  * [Quick Start](<#quick-start>)
  * [Logging In Manually](<#logging-in-manually>)
    * [China region](<#china-region>)
    * [Remote / headless sessions](<#remote--headless-sessions>)
  * [The OAuth Flow](<#the-oauth-flow>)
  * [Checking Login Status](<#checking-login-status>)
  * [Switching Models](<#switching-models>)
  * [Configuration Reference](<#configuration-reference>)
    * [`--region` flag](<#--region-flag>)
    * [Provider aliases](<#provider-aliases>)
  * [Environment Variables](<#environment-variables>)
  * [Models](<#models>)
  * [Troubleshooting](<#troubleshooting>)
    * [Token expired — not re-logging in automatically](<#token-expired--not-re-logging-in-automatically>)
    * [Authorization timed out](<#authorization-timed-out>)
    * [State mismatch (possible CSRF)](<#state-mismatch-possible-csrf>)
    * [Logging in from a remote server](<#logging-in-from-a-remote-server>)
    * ["Not logged into MiniMax OAuth" error at runtime](<#not-logged-into-minimax-oauth-error-at-runtime>)
  * [Logging Out](<#logging-out>)
  * [See Also](<#see-also>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/minimax-oauth -->
