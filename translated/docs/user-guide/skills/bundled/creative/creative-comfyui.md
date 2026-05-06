On this page
Генерируй изображения, видео и аудио с ComfyUI — установка, запуск, управление узлами/моделями, запуск воркфлоу с инъекцией параметров. Использует официальный comfy-cli для жизненного цикла и прямой REST/WebSocket API для выполнения.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default) |
|Path| `skills/creative/comfyui` |
|Version| `5.0.0` |
|Author| ['kshitijk4poor', 'alt-glitch'] |
|License| MIT |
|Platforms| macos, linux, windows |
|Tags| `comfyui`, `image-generation`, `stable-diffusion`, `flux`, `sd3`, `wan-video`, `hunyuan-video`, `creative`, `generative-ai`, `video-generation` |
|Related skills| [`stable-diffusion-image-generation`](</docs/user-guide/skills/optional/mlops/mlops-stable-diffusion>), `image_gen` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# ComfyUI
Генерируй изображения, видео, аудио и 3D-контент через ComfyUI, используя официальный `comfy-cli` для установки/жизненного цикла и прямой REST/WebSocket API для выполнения воркфлоу.
## Что в этом скилле[​](<#whats-in-this-skill> "Direct link to What's in this skill")
**Справочная документация (`references/`):**
  * `official-cli.md` — каждая команда `comfy ...` с флагами
  * `rest-api.md` — REST + WebSocket эндпоинты (локальные + облачные), схемы payload
  * `workflow-format.md` — JSON в формате API, общие типы узлов, маппинг параметров


**Скрипты (`scripts/`):**
Script| Purpose  
---|---  
`_common.py`| Общие HTTP, облачная маршрутизация, каталоги узлов (не запускать напрямую)  
`hardware_check.py`| Проверка GPU/VRAM/диска → рекомендация Локально или Comfy Cloud  
`comfyui_setup.sh`| Проверка железа + comfy-cli + установка ComfyUI + запуск + верификация  
`extract_schema.py`| Чтение воркфлоу → список управляемых параметров + зависимости моделей  
`check_deps.py`| Проверка воркфлоу на запущенном сервере → список отсутствующих узлов/моделей  
`auto_fix_deps.py`| Запуск check_deps затем `comfy node install` / `comfy model download`  
`run_workflow.py`| Инъекция параметров, отправка, мониторинг, скачивание результатов (HTTP или WS)  
`run_batch.py`| Отправка воркфлоу N раз с прогонами, параллельно до вашего тарифа  
`ws_monitor.py`| Просмотрщик WebSocket в реальном времени для выполняющихся задач (живой прогресс)  
`health_check.py`| Запуск чеклиста верификации — comfy-cli + сервер + модели + smoke-тест  
`fetch_logs.py`| Извлечение traceback / статусных сообщений для заданного prompt_id  
**Примеры воркфлоу (`workflows/`):** SD 1.5, SDXL, Flux Dev, SDXL img2img, SDXL inpaint, ESRGAN upscale, AnimateDiff video, Wan T2V. См. `workflows/README.md`.
## Когда использовать[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь просит сгенерировать изображения с Stable Diffusion, SDXL, Flux, SD3 и т.д.
  * Пользователь хочет запустить конкретный файл воркфлоу ComfyUI
  * Пользователь хочет выстроить цепочку генеративных шагов (txt2img → upscale → face restore)
  * Пользователю нужны ControlNet, inpainting, img2img или другие продвинутые пайплайны
  * Пользователь просит управлять очередью ComfyUI, проверять модели или устанавливать пользовательские узлы
  * Пользователь хочет генерацию видео/аудио/3D через AnimateDiff, Hunyuan, Wan, AudioCraft и т.д.


## Архитектура: Два слоя[​](<#architecture-two-layers> "Direct link to Architecture: Two Layers")
[code] 
    ┌─────────────────────────────────────────────────────┐  
    │ Layer 1: comfy-cli (official lifecycle tool)        │  
    │   Setup, server lifecycle, custom nodes, models     │  
    │   → comfy install / launch / stop / node / model    │  
    └─────────────────────────┬───────────────────────────┘  
                              │  
    ┌─────────────────────────▼───────────────────────────┐  
    │ Layer 2: REST/WebSocket API + skill scripts         │  
    │   Workflow execution, param injection, monitoring   │  
    │   POST /api/prompt, GET /api/view, WS /ws           │  
    │   → run_workflow.py, run_batch.py, ws_monitor.py    │  
    └─────────────────────────────────────────────────────┘  
    
[/code]
**Почему два слоя?** Официальный CLI отлично подходит для установки и управления сервером, но имеет минимальную поддержку выполнения воркфлоу. REST/WS API заполняет этот пробел — скрипты обрабатывают инъекцию параметров, мониторинг выполнения и скачивание результатов, чего CLI не делает.
## Быстрый старт[​](<#quick-start> "Direct link to Quick Start")
### Определение окружения[​](<#detect-environment> "Direct link to Detect environment")
[code] 
    # What's available?  
    command -v comfy >/dev/null 2>&1 && echo "comfy-cli: installed"  
    curl -s http://127.0.0.1:8188/system_stats 2>/dev/null && echo "server: running"  
      
    # Can this machine run ComfyUI locally? (GPU/VRAM/disk check)  
    python3 scripts/hardware_check.py  
    
[/code]
Если ничего не установлено, смотри **Setup & Onboarding** ниже — но сначала всегда запускай проверку железа.
### Однострочная проверка здоровья[​](<#one-line-health-check> "Direct link to One-line health check")
[code] 
    python3 scripts/health_check.py  
    # → JSON: comfy_cli on PATH? server reachable? at least one checkpoint? smoke-test passes?  
    
[/code]
## Основной воркфлоу[​](<#core-workflow> "Direct link to Core Workflow")
### Шаг 1: Получи JSON воркфлоу в формате API[​](<#step-1-get-a-workflow-json-in-api-format> "Direct link to Step 1: Get a workflow JSON in API format")
Воркфлоу должны быть в формате API (каждый узел имеет `class_type`). Они берутся из:
  * Веб-интерфейс ComfyUI → **Workflow → Export (API)** (новый UI) или старая кнопка "Save (API Format)" (старый UI)
  * Директории `workflows/` этого скилла (готовые к запуску примеры)
  * Загрузок сообщества (civitai, Reddit, Discord) — обычно в редакторском формате, нужно загрузить в ComfyUI и реэкспортировать


Редакторский формат (верхнеуровневые массивы `nodes` и `links`) **нельзя напрямую выполнять**. Скрипты определяют это и сообщают, что нужно реэкспортировать.
### Шаг 2: Посмотри, что можно контролировать[​](<#step-2-see-whats-controllable> "Direct link to Step 2: See what's controllable")
[code] 
    python3 scripts/extract_schema.py workflow_api.json --summary-only  
    # → {"parameter_count": 12, "has_negative_prompt": true, "has_seed": true, ...}  
      
    python3 scripts/extract_schema.py workflow_api.json  
    # → full schema with parameters, model deps, embedding refs  
    
[/code]
### Шаг 3: Запусти с параметрами[​](<#step-3-run-with-parameters> "Direct link to Step 3: Run with parameters")
[code] 
    # Local (defaults to http://127.0.0.1:8188)  
    python3 scripts/run_workflow.py \  
      --workflow workflow_api.json \  
      --args '{"prompt": "a beautiful sunset over mountains", "seed": -1, "steps": 30}' \  
      --output-dir ./outputs  
      
    # Cloud (export API key once; uses correct /api routing automatically)  
    export COMFY_CLOUD_API_KEY="comfyui-..."  
    python3 scripts/run_workflow.py \  
      --workflow workflow_api.json \  
      --args '{"prompt": "..."}' \  
      --host https://cloud.comfy.org \  
      --output-dir ./outputs  
      
    # Real-time progress via WebSocket (requires `pip install websocket-client`)  
    python3 scripts/run_workflow.py \  
      --workflow flux_dev.json \  
      --args '{"prompt": "..."}' \  
      --ws  
      
    # img2img / inpaint: pass --input-image to upload + reference automatically  
    python3 scripts/run_workflow.py \  
      --workflow sdxl_img2img.json \  
      --input-image image=./photo.png \  
      --args '{"prompt": "make it watercolor", "denoise": 0.6}'  
      
    # Batch / sweep: 8 random seeds, parallel up to cloud tier limit  
    python3 scripts/run_batch.py \  
      --workflow sdxl.json \  
      --args '{"prompt": "abstract"}' \  
      --count 8 --randomize-seed --parallel 3 \  
      --output-dir ./outputs/batch  
    
[/code]
`-1` для `seed` (или его пропуск с `--randomize-seed`) генерирует новый случайный seed для каждого запуска.
### Шаг 4: Представь результаты[​](<#step-4-present-results> "Direct link to Step 4: Present results")
Скрипты выводят JSON в stdout, описывающий каждый выходной файл:
[code] 
    {  
      "status": "success",  
      "prompt_id": "abc-123",  
      "outputs": [  
        {"file": "./outputs/sdxl_00001_.png", "node_id": "9",  
         "type": "image", "filename": "sdxl_00001_.png"}  
      ]  
    }  
    
[/code]
## Decision Tree[​](<#decision-tree> "Direct link to Decision Tree")
User says| Tool| Command  
---|---|---|---  
**Lifecycle (use comfy-cli)**| |  
"install ComfyUI"| comfy-cli| `bash scripts/comfyui_setup.sh`  
"start ComfyUI"| comfy-cli| `comfy launch --background`  
"stop ComfyUI"| comfy-cli| `comfy stop`  
"install X node"| comfy-cli| `comfy node install <name>`  
"download X model"| comfy-cli| `comfy model download --url <url> --relative-path models/checkpoints`  
"list installed models"| comfy-cli| `comfy model list`  
"list installed nodes"| comfy-cli| `comfy node show installed`  
**Execution (use scripts)**| |  
"is everything ready?"| script| `health_check.py` (optionally with `--workflow X --smoke-test`)  
"what can I change in this workflow?"| script| `extract_schema.py W.json`  
"check if W's deps are met"| script| `check_deps.py W.json`  
"fix missing deps"| script| `auto_fix_deps.py W.json`  
"generate an image"| script| `run_workflow.py --workflow W --args '{...}'`  
"use this image" (img2img)| script| `run_workflow.py --input-image image=./x.png ...`  
"8 variations with random seeds"| script| `run_batch.py --count 8 --randomize-seed ...`  
"show me live progress"| script| `ws_monitor.py --prompt-id <id>`  
"fetch the error from job X"| script| `fetch_logs.py <prompt_id>`  
**Direct REST**| |  
"what's in the queue?"| REST| `curl http://HOST:8188/queue` (local) or `--host https://cloud.comfy.org`  
"cancel that"| REST| `curl -X POST http://HOST:8188/interrupt`  
"free GPU memory"| REST| `curl -X POST http://HOST:8188/free`  
## Setup & Onboarding[​](<#setup--onboarding> "Direct link to Setup & Onboarding")
Когда пользователь просит настроить ComfyUI, **ПЕРВОЕ, что нужно сделать — спросить, хочет ли он Comfy Cloud (размещённый, нулевая установка, API-ключ) или Локально (установка ComfyUI на свою машину)**. Не начинай выполнять команды установки или проверки железа, пока они не ответят.
**Официальная документация:** <https://docs.comfy.org/installation> **CLI docs:** <https://docs.comfy.org/comfy-cli/getting-started> **Cloud docs:** <https://docs.comfy.org/get_started/cloud> **Cloud API:** <https://docs.comfy.org/development/cloud/overview>
### Шаг 0: Спроси Локально vs Облако (ВСЕГДА ПЕРВЫМ)[​](<#step-0-ask-local-vs-cloud-always-first> "Direct link to Step 0: Ask Local vs Cloud (ALWAYS FIRST)")
Предлагаемый скрипт:
> «Вы хотите запускать ComfyUI локально на своей машине или использовать Comfy Cloud?
>   * **Comfy Cloud** — размещён на GPU RTX 6000 Pro, все популярные модели предустановлены, нулевая настройка. Требует API-ключ (платная подписка для фактического запуска воркфлоу; бесплатный тариф только для чтения). Лучший выбор, если у вас нет подходящего GPU.
>   * **Локально** — бесплатно, но ваша машина ДОЛЖНА соответствовать аппаратным требованиям:
>     * NVIDIA GPU с **≥6 ГБ VRAM** (≥8 ГБ для SDXL, ≥12 ГБ для Flux/видео), ИЛИ
>     * AMD GPU с поддержкой ROCm (Linux), ИЛИ
>     * Apple Silicon Mac (M1+) с **≥16 ГБ unified memory** (рекомендуется ≥32 ГБ).
>     * Intel Mac и машины без GPU НЕ будут работать — используйте Cloud.
> 
> Что вы предпочитаете?»
Маршрутизация:
  * **Cloud** → перейти к **Path A**.
  * **Локально** → сначала запустить проверку железа, затем выбрать путь из Paths B–E на основе результата.
  * **Не уверен** → запустить проверку железа и позволить результату решить.


### Шаг 1: Проверка железа (ТОЛЬКО если пользователь выбрал локально)[​](<#step-1-verify-hardware-only-if-user-chose-local> "Direct link to Step 1: Verify Hardware (ONLY if user chose local)")
[code] 
    python3 scripts/hardware_check.py --json  
    # Optional: also probe `torch` for actual CUDA/MPS:  
    python3 scripts/hardware_check.py --json --check-pytorch  
    
[/code]
Verdict| Meaning| Action  
---|---|---|---  
`ok`| ≥8 ГБ VRAM (дискретный) ИЛИ ≥32 ГБ unified (Apple Silicon)| Локальная установка — используй `comfy_cli_flag` из отчёта  
`marginal`| SD1.5 работает; SDXL тяжело; Flux/видео маловероятно| Локально нормально для лёгких воркфлоу, иначе **Path A (Cloud)**  
`cloud`| Нет подходящего GPU, <6 ГБ VRAM, <16 ГБ Apple unified, Intel Mac, Rosetta Python| **Переключиться на Cloud** если пользователь явно не настаивает на локальном  
Скрипт также сообщает `wsl: true` (WSL2 с NVIDIA passthrough) и `rosetta: true` (x86_64 Python на Apple Silicon — нужно переустановить как ARM64).
Если вердикт `cloud`, но пользователь хочет локально, не продолжай молча. Покажи массив `notes` дословно и спроси, хотят ли они (a) переключиться на Cloud или (b) форсировать локальную установку (будет OOM или непригодно медленно на современных моделях).
### Выбор пути установки[​](<#choosing-an-installation-path> "Direct link to Choosing an Installation Path")
Сначала используй проверку железа. Таблица ниже — запасной вариант, когда пользователь уже сообщил своё железо:
Situation| Recommended Path  
---|---  
`verdict: cloud` from hardware check| **Path A: Comfy Cloud**  
Нет GPU / хочу попробовать без обязательств| **Path A: Comfy Cloud**  
Windows + NVIDIA + нетехнический| **Path B: ComfyUI Desktop**  
Windows + NVIDIA + технический| **Path C: Portable** или **Path D: comfy-cli**  
Linux + любой GPU| **Path D: comfy-cli** (проще всего)  
macOS + Apple Silicon| **Path B: Desktop** или **Path D: comfy-cli**  
Headless / сервер / CI / агенты| **Path D: comfy-cli**  
Для полностью автоматического пути (проверка железа → установка → запуск → верификация):
[code] 
    bash scripts/comfyui_setup.sh  
    # Or with overrides:  
    bash scripts/comfyui_setup.sh --m-series --port=8190 --workspace=/data/comfy  
    
[/code]
Он запускает `hardware_check.py` внутри, отказывается устанавливать локально при вердикте `cloud` (если не передан `--force-cloud-override`), выбирает правильный флаг `comfy-cli`, и предпочитает `pipx`/`uvx` глобальному `pip`, чтобы не засорять системный Python.
* * *
### Path A: Comfy Cloud (без локальной установки)[​](<#path-a-comfy-cloud-no-local-install> "Direct link to Path A: Comfy Cloud (No Local Install)")
Для пользователей без подходящего GPU или кто хочет нулевую настройку. Размещён на RTX 6000 Pro.
**Документация:** <https://docs.comfy.org/get_started/cloud>
  1. Зарегистрируйтесь на <https://comfy.org/cloud>
  2. Сгенерируйте API-ключ на <https://platform.comfy.org/login>
  3. Установите ключ:
[code] export COMFY_CLOUD_API_KEY="comfyui-xxxxxxxxxxxx"
         
[/code]
  4. Запускайте воркфлоу:
[code] python3 scripts/run_workflow.py \  
           --workflow workflows/flux_dev_txt2img.json \  
           --args '{"prompt": "..."}' \  
           --host https://cloud.comfy.org \  
           --output-dir ./outputs  
         
[/code]


**Цены:** <https://www.comfy.org/cloud/pricing> **Одновременные задачи:** Free/Standard 1, Creator 3, Pro 5. Бесплатный тариф **не может запускать воркфлоу через API** — только просмотр моделей. Требуется платная подписка для `/api/prompt`, `/api/upload/*`, `/api/view` и т.д.
* * *
### Path B: ComfyUI Desktop (Windows / macOS)[​](<#path-b-comfyui-desktop-windows--macos> "Direct link to Path B: ComfyUI Desktop (Windows / macOS)")
Установщик в один клик для нетехнических пользователей. Сейчас в бета-версии.
**Документация:** <https://docs.comfy.org/installation/desktop>
  * **Windows (NVIDIA):** <https://download.comfy.org/windows/nsis/x64>
  * **macOS (Apple Silicon):** <https://comfy.org>


Linux **не поддерживается** для Desktop — используйте Path D.
* * *
### Path C: ComfyUI Portable (только Windows)[​](<#path-c-comfyui-portable-windows-only> "Direct link to Path C: ComfyUI Portable (Windows Only)")
**Документация:** <https://docs.comfy.org/installation/comfyui_portable_windows>
Скачайте с <https://github.com/comfyanonymous/ComfyUI/releases>, распакуйте, запустите `run_nvidia_gpu.bat`. Обновление через `update/update_comfyui_stable.bat`.
* * *
### Path D: comfy-cli (все платформы — рекомендуется для агентов)[​](<#path-d-comfy-cli-all-platforms--recommended-for-agents> "Direct link to Path D: comfy-cli (All Platforms — Recommended for Agents)")
Официальный CLI — лучший путь для headless/автоматизированных установок.
**Документация:** <https://docs.comfy.org/comfy-cli/getting-started>
#### Установка comfy-cli[​](<#install-comfy-cli> "Direct link to Install comfy-cli")
[code] 
    # Recommended:  
    pipx install comfy-cli  
    # Or use uvx without installing:  
    uvx --from comfy-cli comfy --help  
    # Or (if pipx/uvx unavailable):  
    pip install --user comfy-cli  
    
[/code]
Отключение аналитики без интерактива:
[code] 
    comfy --skip-prompt tracking disable  
    
[/code]
#### Установка ComfyUI[​](<#install-comfyui> "Direct link to Install ComfyUI")
[code] 
    comfy --skip-prompt install --nvidia              # NVIDIA (CUDA)  
    comfy --skip-prompt install --amd                 # AMD (ROCm, Linux)  
    comfy --skip-prompt install --m-series            # Apple Silicon (MPS)  
    comfy --skip-prompt install --cpu                 # CPU only (slow)  
    comfy --skip-prompt install --nvidia --fast-deps  # uv-based dep resolution  
    
[/code]
Расположение по умолчанию: `~/comfy/ComfyUI` (Linux), `~/Documents/comfy/ComfyUI` (macOS/Win). Переопределите через `comfy --workspace /custom/path install`.
#### Запуск / проверка[​](<#launch--verify> "Direct link to Launch / verify")
[code] 
    comfy launch --background                       # background daemon on :8188  
    comfy launch -- --listen 0.0.0.0 --port 8190    # LAN-accessible custom port  
    curl -s http://127.0.0.1:8188/system_stats      # health check  
    
[/code]
* * *
### Path E: Ручная установка (продвинутая / неподдерживаемое железо)[​](<#path-e-manual-install-advanced--unsupported-hardware> "Direct link to Path E: Manual Install (Advanced / Unsupported Hardware)")
Для Ascend NPU, Cambricon MLU, Intel Arc и другого неподдерживаемого железа.
**Документация:** <https://docs.comfy.org/installation/manual_install>
[code] 
    git clone https://github.com/comfyanonymous/ComfyUI.git  
    cd ComfyUI  
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130  
    pip install -r requirements.txt  
    python main.py  
    
[/code]
* * *
### После установки: Загрузка моделей[​](<#post-install-download-models> "Direct link to Post-Install: Download Models")
[code] 
    # SDXL (general purpose, ~6.5 GB)  
    comfy model download \  
      --url "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" \  
      --relative-path models/checkpoints  
      
    # SD 1.5 (lighter, ~4 GB, good for 6 GB cards)  
    comfy model download \  
      --url "https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors" \  
      --relative-path models/checkpoints  
      
    # Flux Dev fp8 (smaller variant, ~12 GB)  
    comfy model download \  
      --url "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors" \  
      --relative-path models/checkpoints  
      
    # CivitAI (set token first):  
    comfy model download \  
      --url "https://civitai.com/api/download/models/128713" \  
      --relative-path models/checkpoints \  
      --set-civitai-api-token "YOUR_TOKEN"  
    
[/code]
Список установленных: `comfy model list`.
### После установки: Установка пользовательских узлов[​](<#post-install-install-custom-nodes> "Direct link to Post-Install: Install Custom Nodes")
[code] 
    comfy node install comfyui-impact-pack             # popular utility pack  
    comfy node install comfyui-animatediff-evolved     # video generation  
    comfy node install comfyui-controlnet-aux          # ControlNet preprocessors  
    comfy node install comfyui-essentials              # common helpers  
    comfy node update all  
    comfy node install-deps --workflow=workflow.json   # install everything a workflow needs  
    
[/code]
### После установки: Верификация[​](<#post-install-verify> "Direct link to Post-Install: Verify")
[code] 
    python3 scripts/health_check.py  
    # → comfy_cli on PATH? server reachable? checkpoints? smoke test?  
      
    python3 scripts/check_deps.py my_workflow.json  
    # → are this workflow's nodes/models/embeddings installed?  
      
    python3 scripts/run_workflow.py \  
      --workflow workflows/sd15_txt2img.json \  
      --args '{"prompt": "test", "steps": 4}' \  
      --output-dir ./test-outputs  
    
[/code]
## Загрузка изображений (img2img / Inpainting)[​](<#image-upload-img2img--inpainting> "Direct link to Image Upload (img2img / Inpainting)")
Самый простой способ — использовать `--input-image` с `run_workflow.py`:
[code] 
    python3 scripts/run_workflow.py \  
      --workflow workflows/sdxl_img2img.json \  
      --input-image image=./photo.png \  
      --args '{"prompt": "make it cyberpunk", "denoise": 0.6}'  
    
[/code]
Флаг загружает `photo.png`, затем внедряет его серверное имя файла в параметр схемы с именем `image`. Для inpainting передайте оба:
[code] 
    python3 scripts/run_workflow.py \  
      --workflow workflows/sdxl_inpaint.json \  
      --input-image image=./photo.png \  
      --input-image mask_image=./mask.png \  
      --args '{"prompt": "fill with flowers"}'  
    
[/code]
Ручная загрузка через REST:
[code] 
    curl -X POST "http://127.0.0.1:8188/upload/image" \  
      -F "image=@photo.png" -F "type=input" -F "overwrite=true"  
    # Returns: {"name": "photo.png", "subfolder": "", "type": "input"}  
      
    # Cloud equivalent:  
    curl -X POST "https://cloud.comfy.org/api/upload/image" \  
      -H "X-API-Key: $COMFY_CLOUD_API_KEY" \  
      -F "image=@photo.png" -F "type=input" -F "overwrite=true"  
    
[/code]
## Особенности облака[​](<#cloud-specifics> "Direct link to Cloud Specifics")
  * **Базовый URL:** `https://cloud.comfy.org`
  * **Аутентификация:** заголовок `X-API-Key` (или `?token=KEY` для WebSocket)
  * **API-ключ:** установите `$COMFY_CLOUD_API_KEY` один раз, и скрипты подхватят его автоматически
  * **Скачивание результатов:** `/api/view` возвращает 302 на подписанный URL; скрипты следуют за ним и удаляют `X-API-Key` перед запросом к бэкенду хранилища (не допускайте утечки API-ключа в S3/CloudFront)
  * **Отличия эндпоинтов от локального ComfyUI:**
    * `/api/object_info`, `/api/queue`, `/api/userdata` — **403 на бесплатном тарифе** ; только платный.
    * `/history` переименован в `/history_v2` в облаке (скрипты маршрутизируют автоматически).
    * `/models/<folder>` переименован в `/experiment/models/<folder>` в облаке (скрипты маршрутизируют автоматически).
    * `clientId` в WebSocket в настоящее время игнорируется — все соединения одного пользователя получают одинаковую трансляцию. Фильтруйте по `prompt_id` на стороне клиента.
    * `subfolder` принимается при загрузке, но игнорируется — в облаке плоское пространство имён.
  * **Одновременные задачи:** Free/Standard: 1, Creator: 3, Pro: 5. Дополнительные задачи встают в очередь автоматически. Используйте `run_batch.py --parallel N` для насыщения вашего тарифа.


## Управление очередью и системой[​](<#queue--system-management> "Direct link to Queue & System Management")
[code] 
    # Local  
    curl -s http://127.0.0.1:8188/queue | python3 -m json.tool  
    curl -X POST http://127.0.0.1:8188/queue -d '{"clear": true}'    # cancel pending  
    curl -X POST http://127.0.0.1:8188/interrupt                      # cancel running  
    curl -X POST http://127.0.0.1:8188/free \  
      -H "Content-Type: application/json" \  
      -d '{"unload_models": true, "free_memory": true}'  
      
    # Cloud — same paths under /api/, plus:  
    python3 scripts/fetch_logs.py --tail-queue --host https://cloud.comfy.org  
    
[/code]
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  1. **Требуется формат API** — каждый скрипт и эндпоинт `/api/prompt` ожидают JSON воркфлоу в формате API. Скрипты обнаруживают редакторский формат (верхнеуровневые массивы `nodes` и `links`) и сообщают о необходимости реэкспорта через "Workflow → Export (API)" (новый UI) или "Save (API Format)" (старый UI).
  2. **Сервер должен быть запущен** — всё выполнение требует работающего сервера. `comfy launch --background` запускает его. Проверьте через `curl http://127.0.0.1:8188/system_stats`.
  3. **Имена моделей точны** — чувствительны к регистру, включают расширение файла. `check_deps.py` выполняет нечёткое сопоставление (с/без расширения и префикса папки), но сам воркфлоу должен использовать каноническое имя. Используйте `comfy model list` для просмотра установленного.
  4. **Отсутствуют пользовательские узлы** — "class_type not found" означает, что необходимый узел не установлен. `check_deps.py` сообщает, какой пакет установить; `auto_fix_deps.py` выполняет установку за вас.
  5. **Рабочая директория** — `comfy-cli` автоматически определяет рабочую область ComfyUI. Если команды не работают с "no workspace found", используйте `comfy --workspace /path/to/ComfyUI <command>` или `comfy set-default /path/to/ComfyUI`.
  6. **Ограничения бесплатного облачного API** — `/api/prompt`, `/api/view`, `/api/upload/*`, `/api/object_info` возвращают 403 на бесплатных аккаунтах. `health_check.py` и `check_deps.py` обрабатывают это корректно и выводят понятное сообщение.
  7. **Тайм-аут для видео/аудио воркфлоу** — автоматически определяется, когда выходной узел — `VHS_VideoCombine`, `SaveVideo` и т.д.; значение по умолчанию увеличивается с 300 с до 900 с. Явно переопределите через `--timeout 1800`.
  8. **Path traversal в именах выходных файлов** — имена файлов от сервера пропускаются через `safe_path_join`, чтобы отклонить всё, что выходит за пределы `--output-dir`. Оставляйте эту защиту включённой — воркфлоу с пользовательскими узлами сохранения могут создавать произвольные пути.
  9. **JSON воркфлоу — это произвольный код** — пользовательские узлы выполняют Python, поэтому отправка неизвестного воркфлоу имеет такой же уровень доверия, как `eval`. Проверяйте воркфлоу из ненадёжных источников перед запуском.
  10. **Авто-рандомизация seed** — передайте `seed: -1` в `--args` (или используйте `--randomize-seed` и опустите seed), чтобы получить новый seed для каждого запуска. Фактический seed выводится в stderr.
  11. **Приглашение`tracking`** — первый запуск `comfy` может запросить аналитику. Используйте `comfy --skip-prompt tracking disable`, чтобы пропустить без интерактива. `comfyui_setup.sh` делает это за вас.


## Verification Checklist[​](<#verification-checklist> "Direct link to Verification Checklist")
Используйте `python3 scripts/health_check.py` для выполнения всего списка сразу. Вручную:
  * Вердикт `hardware_check.py` — `ok` ИЛИ пользователь явно выбрал Comfy Cloud
  * `comfy --version` работает (или `uvx --from comfy-cli comfy --help`)
  * `curl http://HOST:PORT/system_stats` возвращает JSON
  * `comfy model list` показывает хотя бы одну контрольную точку (локально) ИЛИ `/api/experiment/models/checkpoints` возвращает модели (облако)
  * JSON воркфлоу в формате API
  * `check_deps.py` сообщает `is_ready: true` (или только `node_check_skipped` на бесплатном облачном тарифе)
  * Тестовый запуск с маленьким воркфлоу завершается; результаты попадают в `--output-dir`


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Что в этом скилле](<#whats-in-this-skill>)
  * [Когда использовать](<#when-to-use>)
  * [Архитектура: Два слоя](<#architecture-two-layers>)
  * [Быстрый старт](<#quick-start>)
    * [Определение окружения](<#detect-environment>)
    * [Однострочная проверка здоровья](<#one-line-health-check>)
  * [Основной воркфлоу](<#core-workflow>)
    * [Шаг 1: Получи JSON воркфлоу в формате API](<#step-1-get-a-workflow-json-in-api-format>)
    * [Шаг 2: Посмотри, что можно контролировать](<#step-2-see-whats-controllable>)
    * [Шаг 3: Запусти с параметрами](<#step-3-run-with-parameters>)
    * [Шаг 4: Представь результаты](<#step-4-present-results>)
  * [Decision Tree](<#decision-tree>)
  * [Setup & Onboarding](<#setup--onboarding>)
    * [Шаг 0: Спроси Локально vs Облако (ВСЕГДА ПЕРВЫМ)](<#step-0-ask-local-vs-cloud-always-first>)
    * [Шаг 1: Проверка железа (ТОЛЬКО если пользователь выбрал локально)](<#step-1-verify-hardware-only-if-user-chose-local>)
    * [Выбор пути установки](<#choosing-an-installation-path>)
    * [Path A: Comfy Cloud (без локальной установки)](<#path-a-comfy-cloud-no-local-install>)
    * [Path B: ComfyUI Desktop (Windows / macOS)](<#path-b-comfyui-desktop-windows--macos>)
    * [Path C: ComfyUI Portable (только Windows)](<#path-c-comfyui-portable-windows-only>)
    * [Path D: comfy-cli (все платформы — рекомендуется для агентов)](<#path-d-comfy-cli-all-platforms--recommended-for-agents>)
    * [Path E: Ручная установка (продвинутая / неподдерживаемое железо)](<#path-e-manual-install-advanced--unsupported-hardware>)
    * [После установки: Загрузка моделей](<#post-install-download-models>)
    * [После установки: Установка пользовательских узлов](<#post-install-install-custom-nodes>)
    * [После установки: Верификация](<#post-install-verify>)
  * [Загрузка изображений (img2img / Inpainting)](<#image-upload-img2img--inpainting>)
  * [Особенности облака](<#cloud-specifics>)
  * [Управление очередью и системой](<#queue--system-management>)
  * [Pitfalls](<#pitfalls>)
  * [Verification Checklist](<#verification-checklist>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-comfyui -->
