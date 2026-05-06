On this page
Проиндексируйте кодовую базу с помощью GitNexus и предоставьте интерактивный граф знаний через веб-интерфейс + туннель Cloudflare.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Опциональный — установка: `hermes skills install official/research/gitnexus-explorer`
|Path| `optional-skills/research/gitnexus-explorer`
|Version| `1.0.0`
|Author| Hermes Agent + Teknium
|License| MIT
|Tags| `gitnexus`, `code-intelligence`, `knowledge-graph`, `visualization`
|Related skills| [`native-mcp`](</docs/user-guide/skills/bundled/mcp/mcp-native-mcp>), [`codebase-inspection`](</docs/user-guide/skills/bundled/github/github-codebase-inspection>)
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Далее приведено полное описание навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# GitNexus Explorer
Проиндексируйте любую кодовую базу в граф знаний и запустите интерактивный веб-интерфейс для изучения символов, цепочек вызовов, кластеров и потоков выполнения. Туннелирование через Cloudflare для удалённого доступа.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь хочет визуально изучить архитектуру кодовой базы
  * Пользователь запрашивает граф знаний / граф зависимостей репозитория
  * Пользователь хочет поделиться интерактивным обозревателем кодовой базы с кем-либо


## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * **Node.js** (v18+) — требуется для GitNexus и прокси
  * **git** — репозиторий должен содержать директорию `.git`
  * **cloudflared** — для туннелирования (автоустанавливается в ~/.local/bin, если отсутствует)


## Size Warning[​](<#size-warning> "Direct link to Size Warning")
Веб-интерфейс отображает все узлы в браузере. Репозитории до ~5000 файлов работают хорошо. Крупные репозитории (30 000+ узлов) будут работать медленно или могут вызвать крах вкладки браузера. Инструменты CLI/MCP работают при любом масштабе — ограничение касается только веб-визуализации.
## Steps[​](<#steps> "Direct link to Steps")
### 1\\. Клонирование и сборка GitNexus (однократная настройка)[​](<#1-clone-and-build-gitnexus-one-time-setup> "Direct link to 1. Clone and Build GitNexus \\(one-time setup\\)")
[code] 
    GITNEXUS_DIR="${GITNEXUS_DIR:-$HOME/.local/share/gitnexus}"
    
    if [ ! -d "$GITNEXUS_DIR/gitnexus-web/dist" ]; then
      git clone https://github.com/abhigyanpatwari/GitNexus.git "$GITNEXUS_DIR"
      cd "$GITNEXUS_DIR/gitnexus-shared" && npm install && npm run build
      cd "$GITNEXUS_DIR/gitnexus-web" && npm install
    fi
    
[/code]
### 2\\. Патч веб-интерфейса для удалённого доступа[​](<#2-patch-the-web-ui-for-remote-access> "Direct link to 2. Patch the Web UI for Remote Access")
Веб-интерфейс по умолчанию использует `localhost:4747` для API-вызовов. Измените его на same-origin, чтобы он работал через туннель/прокси:
**Файл:`$GITNEXUS_DIR/gitnexus-web/src/config/ui-constants.ts`** Измените:
[code] 
    export const DEFAULT_BACKEND_URL = 'http://localhost:4747';
    
[/code]
На:
[code] 
    export const DEFAULT_BACKEND_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost' ? window.location.origin : 'http://localhost:4747';
    
[/code]
**Файл:`$GITNEXUS_DIR/gitnexus-web/vite.config.ts`** Добавьте `allowedHosts: true` внутрь блока `server: { }` (только если запускаете dev-режим вместо production-сборки):
[code] 
    server: {
        allowedHosts: true,
        // ... existing config
    },
    
[/code]
Затем соберите production-бандл:
[code] 
    cd "$GITNEXUS_DIR/gitnexus-web" && npx vite build
    
[/code]
### 3\\. Индексация целевого репозитория[​](<#3-index-the-target-repo> "Direct link to 3. Index the Target Repo")
[code] 
    cd /path/to/target-repo
    npx gitnexus analyze --skip-agents-md
    rm -rf .claude/    # удалить артефакты Claude Code
    
[/code]
Добавьте `--embeddings` для семантического поиска (медленнее — минуты вместо секунд).
Индекс хранится в `.gitnexus/` внутри репозитория (автоматически добавлен в .gitignore).
### 4\\. Создание прокси-скрипта[​](<#4-create-the-proxy-script> "Direct link to 4. Create the Proxy Script")
Запишите это в файл (например, `$GITNEXUS_DIR/proxy.mjs`). Он раздаёт production-версию веб-интерфейса и проксирует `/api/*` на бэкенд GitNexus — один Origin, никаких проблем с CORS, не требует sudo или nginx.
[code] 
    import http from 'node:http';
    import fs from 'node:fs';
    import path from 'node:path';
    
    const API_PORT = parseInt(process.env.API_PORT || '4747');
    const DIST_DIR = process.argv[2] || './dist';
    const PORT = parseInt(process.argv[3] || '8888');
    
    const MIME = {
      '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css',
      '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml',
      '.ico': 'image/x-icon', '.woff2': 'font/woff2', '.woff': 'font/woff',
      '.wasm': 'application/wasm',
    };
    
    function proxyToApi(req, res) {
      const opts = {
        hostname: '127.0.0.1', port: API_PORT,
        path: req.url, method: req.method, headers: req.headers,
      };
      const proxy = http.request(opts, (upstream) => {
        res.writeHead(upstream.statusCode, upstream.headers);
        upstream.pipe(res, { end: true });
      });
      proxy.on('error', () => { res.writeHead(502); res.end('Backend unavailable'); });
      req.pipe(proxy, { end: true });
    }
    
    function serveStatic(req, res) {
      let filePath = path.join(DIST_DIR, req.url === '/' ? 'index.html' : req.url.split('?')[0]);
      if (!fs.existsSync(filePath)) filePath = path.join(DIST_DIR, 'index.html');
      const ext = path.extname(filePath);
      const mime = MIME[ext] || 'application/octet-stream';
      try {
        const data = fs.readFileSync(filePath);
        res.writeHead(200, { 'Content-Type': mime, 'Cache-Control': 'public, max-age=3600' });
        res.end(data);
      } catch { res.writeHead(404); res.end('Not found'); }
    }
    
    http.createServer((req, res) => {
      if (req.url.startsWith('/api')) proxyToApi(req, res);
      else serveStatic(req, res);
    }).listen(PORT, () => console.log(`GitNexus proxy on http://localhost:${PORT}`));
    
[/code]
### 5\\. Запуск сервисов[​](<#5-start-the-services> "Direct link to 5. Start the Services")
[code] 
    # Терминал 1: API-бэкенд GitNexus
    npx gitnexus serve &
    
    # Терминал 2: Прокси (веб-интерфейс + API на одном порту)
    node "$GITNEXUS_DIR/proxy.mjs" "$GITNEXUS_DIR/gitnexus-web/dist" 8888 &
    
[/code]
Проверка: `curl -s http://localhost:8888/api/repos` должен вернуть проиндексированный репозиторий(и).
### 6\\. Туннель с Cloudflare (опционально — для удалённого доступа)[​](<#6-tunnel-with-cloudflare-optional--for-remote-access> "Direct link to 6. Tunnel with Cloudflare \\(optional — for remote access\\)")
[code] 
    # Установка cloudflared при необходимости (без sudo)
    if ! command -v cloudflared &>/dev/null; then
      mkdir -p ~/.local/bin
      curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
        -o ~/.local/bin/cloudflared
      chmod +x ~/.local/bin/cloudflared
      export PATH="$HOME/.local/bin:$PATH"
    fi
    
    # Запуск туннеля (--config /dev/null позволяет избежать конфликтов с существующими именованными туннелями)
    cloudflared tunnel --config /dev/null --url http://localhost:8888 --no-autoupdate --protocol http2
    
[/code]
URL туннеля (например, `https://random-words.trycloudflare.com`) выводится в stderr. Поделитесь им — любой, у кого есть ссылка, сможет исследовать граф.
### 7\\. Очистка[​](<#7-cleanup> "Direct link to 7. Cleanup")
[code] 
    # Остановка сервисов
    pkill -f "gitnexus serve"
    pkill -f "proxy.mjs"
    pkill -f cloudflared
    
    # Удаление индекса из целевого репозитория
    cd /path/to/target-repo
    npx gitnexus clean
    rm -rf .claude/
    
[/code]
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * **`--config /dev/null` обязателен для cloudflared**, если у пользователя есть существующая конфигурация именованного туннеля в `~/.cloudflared/config.yml`. Без этого параметра catch-all правило ingress в конфигурации будет возвращать 404 для всех запросов быстрых туннелей.
  * **Production-сборка обязательна для туннелирования.** Dev-сервер Vite по умолчанию блокирует хосты, отличные от localhost (`allowedHosts`). Production-сборка + Node-прокси полностью решают эту проблему.
  * **Веб-интерфейс НЕ создаёт `.claude/` или `CLAUDE.md`.** Их создаёт `npx gitnexus analyze`. Используйте `--skip-agents-md` для подавления markdown-файлов, затем `rm -rf .claude/` для остального. Это интеграции с Claude Code, которые не нужны пользователям hermes-agent.
  * **Ограничение памяти браузера.** Веб-интерфейс загружает весь граф в память браузера. Репозитории с 5k+ файлами могут тормозить. 30k+ файлов, скорее всего, приведут к краху вкладки.
  * **Embeddings опциональны.** `--embeddings` включает семантический поиск, но занимает минуты на крупных репозиториях. Пропустите для быстрого ознакомления; добавьте, если хотите запросы на естественном языке через панель AI-чата.
  * **Несколько репозиториев.** `gitnexus serve` обслуживает ВСЕ проиндексированные репозитории. Проиндексируйте несколько репозиториев, запустите serve один раз, и веб-интерфейс позволит переключаться между ними.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Prerequisites](<#prerequisites>)
  * [Size Warning](<#size-warning>)
  * [Steps](<#steps>)
    * [1\\. Clone and Build GitNexus (однократная настройка)](<#1-clone-and-build-gitnexus-one-time-setup>)
    * [2\\. Patch the Web UI for Remote Access](<#2-patch-the-web-ui-for-remote-access>)
    * [3\\. Index the Target Repo](<#3-index-the-target-repo>)
    * [4\\. Create the Proxy Script](<#4-create-the-proxy-script>)
    * [5\\. Start the Services](<#5-start-the-services>)
    * [6\\. Tunnel with Cloudflare (опционально — для удалённого доступа)](<#6-tunnel-with-cloudflare-optional--for-remote-access>)
    * [7\\. Cleanup](<#7-cleanup>)
  * [Pitfalls](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-gitnexus-explorer -->
