On this page
Делегирование задач по кодингу OpenAI Codex CLI (фичи, PR).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default) |
|Path| `skills/autonomous-ai-agents/codex` |
|Version| `1.0.0` |
|Author| Hermes Agent |
|License| MIT |
|Tags| `Coding-Agent`, `Codex`, `OpenAI`, `Code-Review`, `Refactoring` |
|Related skills| [`claude-code`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code>), [`hermes-agent`](</docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent>) |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Codex CLI
Делегируй задачи по кодингу [Codex](<https://github.com/openai/codex>) через терминал Hermes. Codex — это автономный агент-кодировщик от OpenAI в виде CLI.
## When to use[​](<#when-to-use> "Direct link to When to use")
  * Создание функционала
  * Рефакторинг
  * Ревью PR
  * Пакетное исправление ошибок


Требуются CLI codex и git-репозиторий.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * Codex установлен: `npm install -g @openai/codex`
  * Аутентификация OpenAI настроена: либо `OPENAI_API_KEY`, либо учётные данные OAuth Codex из процесса входа в Codex CLI
  * **Должен запускаться внутри git-репозитория** — Codex отказывается работать вне его
  * Используй `pty=true` в вызовах terminal — Codex — интерактивное терминальное приложение


Для самого Hermes `model.provider: openai-codex` использует управляемый Hermes OAuth Codex из `~/.hermes/auth.json` после `hermes auth add openai-codex`. Для автономного Codex CLI действующая OAuth-сессия CLI может находиться в `~/.codex/auth.json`; не считай отсутствие `OPENAI_API_KEY` само по себе доказательством отсутствия аутентификации Codex.
## One-Shot Tasks[​](<#one-shot-tasks> "Direct link to One-Shot Tasks")
[code] 
    terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)  
    
[/code]
Для временной работы (Codex нужен git-репозиторий):
[code] 
    terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)  
    
[/code]
## Background Mode (Long Tasks)[​](<#background-mode-long-tasks> "Direct link to Background Mode \(Long Tasks\)")
[code] 
    # Запустить в фоне с PTY  
    terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)  
    # Возвращает session_id  
      
    # Мониторинг прогресса  
    process(action="poll", session_id="<id>")  
    process(action="log", session_id="<id>")  
      
    # Отправить ввод, если Codex задаёт вопрос  
    process(action="submit", session_id="<id>", data="yes")  
      
    # Завершить при необходимости  
    process(action="kill", session_id="<id>")  
    
[/code]
## Key Flags[​](<#key-flags> "Direct link to Key Flags")
Flag| Effect  
---|---  
`exec "prompt"`| Одноразовое выполнение, завершается по готовности  
`--full-auto`| Песочница, но авто-одобрение изменений файлов в рабочей области  
`--yolo`| Без песочницы и одобрений (самый быстрый, самый опасный)  
## PR Reviews[​](<#pr-reviews> "Direct link to PR Reviews")
Клонировать во временную директорию для безопасного ревью:
[code] 
    terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)  
    
[/code]
## Parallel Issue Fixing with Worktrees[​](<#parallel-issue-fixing-with-worktrees> "Direct link to Parallel Issue Fixing with Worktrees")
[code] 
    # Создать worktree  
    terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")  
    terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")  
      
    # Запустить Codex в каждом  
    terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)  
    terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)  
      
    # Мониторинг  
    process(action="list")  
      
    # После завершения, запушить и создать PR  
    terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")  
    terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")  
      
    # Очистка  
    terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")  
    
[/code]
## Batch PR Reviews[​](<#batch-pr-reviews> "Direct link to Batch PR Reviews")
[code] 
    # Получить все PR-ссылки  
    terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")  
      
    # Проверить несколько PR параллельно  
    terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)  
    terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)  
      
    # Опубликовать результаты  
    terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")  
    
[/code]
## Rules[​](<#rules> "Direct link to Rules")
  1. **Всегда используй`pty=true`** — Codex — интерактивное терминальное приложение и зависает без PTY
  2. **Требуется git-репозиторий** — Codex не работает вне git-директории. Используй `mktemp -d && git init` для временной работы
  3. **Используй`exec` для одноразовых задач** — `codex exec "prompt"` запускается и чисто завершается
  4. **`--full-auto` для разработки** — авто-одобрение изменений в песочнице
  5. **Фон для долгих задач** — используй `background=true` и мониторь с помощью `process`
  6. **Не вмешивайся** — мониторь с помощью `poll`/`log`, будь терпелив с длительными задачами
  7. **Параллельность допустима** — запускай несколько процессов Codex одновременно для пакетной работы


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use](<#when-to-use>)
  * [Prerequisites](<#prerequisites>)
  * [One-Shot Tasks](<#one-shot-tasks>)
  * [Background Mode (Long Tasks)](<#background-mode-long-tasks>)
  * [Key Flags](<#key-flags>)
  * [PR Reviews](<#pr-reviews>)
  * [Parallel Issue Fixing with Worktrees](<#parallel-issue-fixing-with-worktrees>)
  * [Batch PR Reviews](<#batch-pr-reviews>)
  * [Rules](<#rules>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex -->
