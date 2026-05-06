On this page
Используйте CLI-инструмент mcporter для просмотра, настройки, аутентификации и вызова MCP-серверов/инструментов напрямую (через HTTP или stdio), включая ad-hoc серверы, редактирование конфигурации и генерацию CLI/типов.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на Skill metadata")

|   |
|---|
|Source| Опционально — установка: `hermes skills install official/mcp/mcporter` |
|Path| `optional-skills/mcp/mcporter` |
|Version| `1.0.0` |
|Author| community |
|License| MIT |
|Tags| `MCP`, `Tools`, `API`, `Integrations`, `Interop` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
Ниже приведено полное описание скилла, которое Hermes загружает при активации этого скилла. Это те инструкции, которые видит агент, когда скилл активен.
# mcporter
Используйте `mcporter` для обнаружения, вызова и управления серверами и инструментами [MCP (Model Context Protocol)](<https://modelcontextprotocol.io/>) прямо из терминала.
## Prerequisites[​](<#prerequisites> "Прямая ссылка на Prerequisites")
Требуется Node.js:
[code] 
    # Установка не требуется (запуск через npx)  
    npx mcporter list  
      
    # Или глобальная установка  
    npm install -g mcporter  
    
[/code]
## Quick Start[​](<#quick-start> "Прямая ссылка на Quick Start")
[code] 
    # Список MCP-серверов, уже настроенных на этой машине  
    mcporter list  
      
    # Список инструментов конкретного сервера с описанием схемы  
    mcporter list <server> --schema  
      
    # Вызов инструмента  
    mcporter call <server.tool> key=value  
    
[/code]
## Discovering MCP Servers[​](<#discovering-mcp-servers> "Прямая ссылка на Discovering MCP Servers")
mcporter автоматически обнаруживает серверы, настроенные другими MCP-клиентами (Claude Desktop, Cursor и т.д.) на этой машине. Чтобы найти новые серверы, просмотрите реестры вроде [mcpfinder.dev](<https://mcpfinder.dev>) или [mcp.so](<https://mcp.so>), затем подключитесь ad-hoc:
[code] 
    # Подключение к любому MCP-серверу по URL (без конфигурации)  
    mcporter list --http-url https://some-mcp-server.com --name my_server  
      
    # Или запуск stdio-сервера на лету  
    mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs  
    
[/code]
## Calling Tools[​](<#calling-tools> "Прямая ссылка на Calling Tools")
[code] 
    # Синтаксис key=value  
    mcporter call linear.list_issues team=ENG limit:5  
      
    # Синтаксис функций  
    mcporter call "linear.create_issue(title: \"Bug fix needed\")"  
      
    # Ad-hoc HTTP-сервер (без конфигурации)  
    mcporter call https://api.example.com/mcp.fetch url=https://example.com  
      
    # Ad-hoc stdio-сервер  
    mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com  
      
    # JSON-полезная нагрузка  
    mcporter call <server.tool> --args '{"limit": 5}'  
      
    # Машиночитаемый вывод (рекомендуется для Hermes)  
    mcporter call <server.tool> key=value --output json  
    
[/code]
## Auth and Config[​](<#auth-and-config> "Прямая ссылка на Auth and Config")
[code] 
    # OAuth-логин для сервера  
    mcporter auth <server | url> [--reset]  
      
    # Управление конфигурацией  
    mcporter config list  
    mcporter config get <key>  
    mcporter config add <server>  
    mcporter config remove <server>  
    mcporter config import <path>  
    
[/code]
Расположение файла конфигурации: `./config/mcporter.json` (переопределяется через `--config`).
## Daemon[​](<#daemon> "Прямая ссылка на Daemon")
Для постоянных подключений к серверам:
[code] 
    mcporter daemon start  
    mcporter daemon status  
    mcporter daemon stop  
    mcporter daemon restart  
    
[/code]
## Code Generation[​](<#code-generation> "Прямая ссылка на Code Generation")
[code] 
    # Генерация CLI-обёртки для MCP-сервера  
    mcporter generate-cli --server <name>  
    mcporter generate-cli --command <url>  
      
    # Просмотр сгенерированного CLI  
    mcporter inspect-cli <path> [--json]  
      
    # Генерация TypeScript-типов/клиента  
    mcporter emit-ts <server> --mode client  
    mcporter emit-ts <server> --mode types  
    
[/code]
## Notes[​](<#notes> "Прямая ссылка на Notes")
  * Используйте `--output json` для структурированного вывода, который проще парсить
  * Ad-hoc серверы (HTTP URL или команда `--stdio`) работают без какой-либо конфигурации — удобно для разовых вызовов
  * OAuth-аутентификация может потребовать интерактивного взаимодействия с браузером — при необходимости используйте `terminal(command="mcporter auth <server>", pty=true)`


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [Quick Start](<#quick-start>)
  * [Discovering MCP Servers](<#discovering-mcp-servers>)
  * [Calling Tools](<#calling-tools>)
  * [Auth and Config](<#auth-and-config>)
  * [Daemon](<#daemon>)
  * [Code Generation](<#code-generation>)
  * [Notes](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mcp/mcp-mcporter -->
