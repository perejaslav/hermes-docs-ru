На этой странице
Создание, тестирование и отладка RL-окружений Hermes Agent для обучения Atropos. Описывает интерфейс HermesAgentBaseEnv, функции награды, интеграцию с циклом агента, оценку с инструментами, логирование wandb и три режима CLI (serve/process/evaluate). Используйте при создании, рецензировании или исправлении RL-окружений в репозитории hermes-agent.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Опционально — установка: `hermes skills install official/mlops/hermes-atropos-environments`  |
|Путь| `optional-skills/mlops/hermes-atropos-environments`  |
|Версия| `1.1.0`  |
|Автор| Hermes Agent  |
|Лицензия| MIT  |
|Теги| `atropos`, `rl`, `environments`, `training`, `reinforcement-learning`, `reward-functions`  |
|Связанные навыки| [`axolotl`](</docs/user-guide/skills/bundled/mlops/mlops-training-axolotl>), [`fine-tuning-with-trl`](</docs/user-guide/skills/bundled/mlops/mlops-training-trl-fine-tuning>), `lm-evaluation-harness`  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Это инструкции, которые агент видит, когда навык активен.
# Hermes Agent Atropos Окружения
Руководство по созданию RL-окружений в репозитории hermes-agent, которые интегрируются с фреймворком обучения Atropos.
## Обзор архитектуры[​](<#architecture-overview> "Прямая ссылка на Обзор архитектуры")
[code] 
    Atropos BaseEnv (atroposlib/envs/base.py)  
        └── HermesAgentBaseEnv (environments/hermes_base_env.py)  
                ├── Управляет оркестрацией цикла агента  
                ├── Управляет разрешением инструментов для группы  
                ├── Управляет ToolContext для верификации наград  
                └── ВАШЕ ОКРУЖЕНИЕ (environments/your_env.py)  
                        Реализует только: setup, get_next_item, format_prompt,  
                                        compute_reward, evaluate, wandb_log  
    
[/code]
Окружения Hermes особенны тем, что они запускают **многоходовой цикл агента с вызовом инструментов** — а не просто одноходовые завершения. Базовое окружение управляет циклом; вы реализуете задачу и оценку.
## Расположение файлов[​](<#file-locations> "Прямая ссылка на Расположение файлов")
Файл| Назначение  
---|---
`environments/hermes_base_env.py`| Базовый класс с циклом агента + разрешением инструментов  
`environments/agent_loop.py`| `HermesAgentLoop` + dataclass `AgentResult`  
`environments/tool_context.py`| `ToolContext` для верификации наград  
`environments/tool_call_parsers.py`| Парсеры вызовов инструментов фазы 2 (hermes, mistral и т.д.)  
`environments/your_env.py`| Реализация вашего окружения  
## Настройка инференса — сначала спросите пользователя[​](<#inference-setup--ask-the-user-first> "Прямая ссылка на Настройка инференса — сначала спросите пользователя")
**ВАЖНО:** Перед запуском любой команды тестирования, оценки или генерации данных всегда спрашивайте пользователя, как он хочет настроить инференс. НЕ предполагайте OpenRouter или какую-либо конкретную конечную точку. Предложите эти варианты:
  1. **OpenRouter** — Спросите, какую модель они хотят использовать (например, `anthropic/claude-sonnet-4.5`, `google/gemini-2.5-pro`, `meta-llama/llama-3.3-70b-instruct` и т.д.). Требуется `OPENROUTER_API_KEY` в окружении.
  2. **Собственная конечная точка VLLM** — Спросите базовый URL (например, `http://localhost:8000/v1`) и имя модели. Установите `--openai.server_type vllm`.
  3. **Другой API, совместимый с OpenAI** — Спросите базовый URL, имя модели и при необходимости API-ключ. Установите `--openai.server_type openai` и `--openai.health_check false`.
  4. **Локальный сервер обучения Atropos** — Для режима `serve` с живым циклом обучения. По умолчанию `http://localhost:8000/v1`.


После того как пользователь сообщит свою настройку, используйте эти значения во всех командах CLI в рамках сессии. Пример подсказки:
> "Перед запуском этого, как вы хотите настроить инференс?
>   1. OpenRouter (укажите предпочтительную модель, например claude-sonnet-4.5)
>   2. Собственная конечная точка VLLM (дайте URL и имя модели)
>   3. Другой API, совместимый с OpenAI (дайте URL, модель и данные аутентификации)
>   4. Локальный сервер обучения Atropos (режим serve)"
> 

>
### Ключевые флаги по провайдеру:[​](<#key-flags-by-provider> "Прямая ссылка на Ключевые флаги по провайдеру:")
Провайдер| `--openai.server_type`| `--openai.health_check`| `--openai.api_key`  
---|---|---|---  
OpenRouter| `openai`| `false`| `$OPENROUTER_API_KEY`  
VLLM (собственный)| `vllm`| (по умолчанию)| (не требуется)  
Другой OpenAI-совместимый| `openai`| `false`| При необходимости  
Локальный Atropos| (по умолчанию)| (по умолчанию)| (не требуется)  
## Обязательные методы[​](<#required-methods> "Прямая ссылка на Обязательные методы")
### 1\\. `setup()` — Загрузка набора данных и инициализация состояния[​](<#1-setup--load-dataset-and-initialize-state> "Прямая ссылка на 1-setup--load-dataset-and-initialize-state")
[code] 
    async def setup(self) -> None:  
        """Вызывается один раз при запуске. Загружает наборы данных, инициализирует состояние."""  
        # Попробовать HuggingFace, при ошибке — встроенные образцы  
        try:  
            from datasets import load_dataset  
            ds = load_dataset("your/dataset", split="test")  
            self._items = [...]  
        except Exception:  
            self._items = BUILTIN_SAMPLES  
      
        # Всегда разделять на train/eval  
        random.shuffle(self._items)  
        eval_size = max(20, int(len(self._items) * 0.1))  
        self._eval_items = self._items[:eval_size]  
        self._items = self._items[eval_size:]  
    
[/code]
### 2\\. `get_next_item()` — Возврат следующего элемента обучения[​](<#2-get_next_item--return-next-training-item> "Прямая ссылка на 2-get_next_item--return-next-training-item")
[code] 
    async def get_next_item(self) -> dict:  
        """Возвращает следующий элемент, циклически проходя по набору данных."""  
        item = self._items[self._index % len(self._items)]  
        self._index += 1  
        return item  
    
[/code]
### 3\\. `format_prompt(item)` — Преобразование элемента в сообщение пользователя[​](<#3-format_promptitem--convert-item-to-user-message> "Прямая ссылка на 3-format_promptitem--convert-item-to-user-message")
[code] 
    def format_prompt(self, item: dict) -> str:  
        """Преобразует элемент набора данных в промпт для пользователя."""  
        return f"Исследуйте этот вопрос: {item['question']}"  
    
[/code]
### 4\\. `compute_reward(item, result, ctx)` — Оценка прогона[​](<#4-compute_rewarditem-result-ctx--score-the-rollout> "Прямая ссылка на 4-compute_rewarditem-result-ctx--score-the-rollout")
**ВАЖНО**: `result` — это `AgentResult`, НЕ словарь. У него есть следующие атрибуты:
  * `result.messages` — Список словарей сообщений (формат OpenAI)
  * `result.turns_used` — Количество выполненных вызовов LLM
  * `result.finished_naturally` — True, если модель остановилась самостоятельно
  * `result.tool_errors` — Список объектов ToolError


**AgentResult НЕ имеет**: `final_response`, `tool_calls`, `tools_used`. Их нужно извлекать из `result.messages`:
[code] 
    async def compute_reward(self, item, result: AgentResult, ctx: ToolContext) -> float:  
        # Извлечение финального ответа (последнее сообщение assistant с контентом)  
        final_response = ""  
        tools_used = []  
        for msg in reversed(result.messages):  
            if msg.get("role") == "assistant" and msg.get("content") and not final_response:  
                final_response = msg["content"]  
            if msg.get("role") == "assistant" and msg.get("tool_calls"):  
                for tc in msg["tool_calls"]:  
                    fn = tc.get("function", {}) if isinstance(tc, dict) else {}  
                    name = fn.get("name", "")  
                    if name:  
                        tools_used.append(name)  
      
        # Оценка через LLM-судью, эвристику или ToolContext  
        correctness = await self._llm_judge(item, final_response)  
        return correctness  
    
[/code]
`ctx` (ToolContext) предоставляет доступ к терминалу/файлам в песочнице агента для верификации:
[code] 
    # Запуск тестов в песочнице агента  
    result = ctx.terminal("pytest /workspace/test.py")  
    return 1.0 if result["exit_code"] == 0 else 0.0  
    
[/code]
### 5\\. `evaluate()` — Периодическая оценка с полным циклом агента[​](<#5-evaluate--periodic-evaluation-with-full-agent-loop> "Прямая ссылка на 5-evaluate--periodic-evaluation-with-full-agent-loop")
**ОБЯЗАТЕЛЬНО** используйте полный цикл агента с инструментами, а не одноходовой chat_completion. Весь смысл окружений hermes-agent в агентской оценке:
[code] 
    async def evaluate(self, *args, **kwargs) -> None:  
        import time, uuid  
        from environments.agent_loop import HermesAgentLoop  
        from environments.tool_context import ToolContext  
      
        start_time = time.time()  
        tools, valid_names = self._resolve_tools_for_group()  
        samples = []  
      
        for item in self._eval_items[:self.config.eval_size]:  
            task_id = str(uuid.uuid4())  
            messages = []  
            if self.config.system_prompt:  
                messages.append({"role": "system", "content": self.config.system_prompt})  
            messages.append({"role": "user", "content": self.format_prompt(item)})  
      
            agent = HermesAgentLoop(  
                server=self.server,  
                tool_schemas=tools,  
                valid_tool_names=valid_names,  
                max_turns=self.config.max_agent_turns,  
                task_id=task_id,  
                temperature=0.0,  # Детерминированно для оценки  
                max_tokens=self.config.max_token_length,  
                extra_body=self.config.extra_body,  
            )  
            result = await agent.run(messages)  
      
            ctx = ToolContext(task_id)  
            try:  
                reward = await self.compute_reward(item, result, ctx)  
            finally:  
                ctx.cleanup()  
      
            samples.append({"prompt": ..., "response": ..., "reward": reward})  
      
        eval_metrics = {"eval/mean_reward": ...}  
        await self.evaluate_log(metrics=eval_metrics, samples=samples,  
                                start_time=start_time, end_time=time.time())  
    
[/code]
### 6\\. `wandb_log()` — Кастомное логирование метрик[​](<#6-wandb_log--custom-metrics-logging> "Прямая ссылка на 6-wandb_log--custom-metrics-logging")
Всегда вызывайте `super().wandb_log()` в конце:
[code] 
    async def wandb_log(self, wandb_metrics=None):  
        if wandb_metrics is None:  
            wandb_metrics = {}  
        if self._reward_buffer:  
            n = len(self._reward_buffer)  
            wandb_metrics["train/mean_reward"] = sum(self._reward_buffer) / n  
            self._reward_buffer.clear()  
        await super().wandb_log(wandb_metrics)  # ОБЯЗАТЕЛЬНО вызвать super  
    
[/code]
**Ловушка**: `compute_reward` добавляет данные в буфер метрик. Во время оценки это загрязняет метрики обучения. Откатывайте записи буфера, добавленные во время оценки.
## Класс конфигурации[​](<#config-class> "Прямая ссылка на Класс конфигурации")
Всегда создавайте кастомный подкласс конфигурации с Pydantic Field-дескрипторами. Ключевые наследуемые поля, которые можно настраивать: `enabled_toolsets`, `max_agent_turns`, `agent_temperature`, `system_prompt`, `terminal_backend`, `group_size`, `steps_per_eval`, `total_steps`.
## config_init() — Конфигурация по умолчанию[​](<#config_init--default-configuration> "Прямая ссылка на config_init() — Конфигурация по умолчанию")
Classmethod, возвращающий `(YourEnvConfig, [APIServerConfig(...)])`. Установите server_type в "openai" для OpenRouter/внешних API. Загружайте API-ключ из переменной окружения.
## Три режима CLI[​](<#three-cli-modes> "Прямая ссылка на Три режима CLI")
[code] 
    # SERVE — Полный цикл обучения (подключается к API-серверу Atropos)  
    python environments/my_env.py serve --openai.base_url http://localhost:8000/v1  
      
    # PROCESS — Офлайн-генерация данных (сохраняет JSONL)  
    python environments/my_env.py process --env.total_steps 10 --env.group_size 1 \  
        --env.use_wandb false --env.data_path_to_save_groups output.jsonl \  
        --openai.base_url "<USER_BASE_URL>" \  
        --openai.model_name "<USER_MODEL>" \  
        --openai.server_type <USER_SERVER_TYPE> --openai.health_check false  
      
    # EVALUATE — Автономная оценка (запускает только setup + evaluate)  
    python environments/my_env.py evaluate --env.eval_size 20 \  
        --env.data_dir_to_save_evals /tmp/eval_results \  
        --openai.base_url "<USER_BASE_URL>" \  
        --openai.model_name "<USER_MODEL>" \  
        --openai.server_type <USER_SERVER_TYPE> --openai.health_check false  
    
[/code]
Приоритет конфигурации: аргументы CLI > YAML-файл > значения по умолчанию config_init().
## Частые ловушки[​](<#common-pitfalls> "Прямая ссылка на Частые ловушки")
  1. **У AgentResult есть .messages, а не .final_response** — Извлекайте финальный ответ, проходя по reversed(result.messages) в поисках последнего сообщения assistant с контентом.
  2. **evaluate() должен использовать HermesAgentLoop, а не chat_completion** — У одноходового chat_completion нет инструментов. Весь смысл бенчмарков hermes-agent в агентской оценке с использованием инструментов.
  3. **Не вызывайте _llm_judge дважды** — Если compute_reward уже вызывает его, извлекайте оценку из буфера вместо отдельного вызова судьи в evaluate().
  4. **Оценка загрязняет буферы обучения** — compute_reward добавляет данные в буфер метрик. Во время оценки откатывайте записи буфера, чтобы метрики обучения оставались чистыми.
  5. **Всегда устанавливайте health_check=false для OpenRouter** — У OpenRouter нет эндпоинта /health.
  6. **Устанавливайте data_dir_to_save_evals в режиме evaluate** — Без этого результаты не сохраняются.
  7. **Переменная класса default_toolsets vs поле конфигурации enabled_toolsets** — Переменная класса — это подсказка; поле конфигурации — то, что на самом деле управляет разрешением инструментов.
  8. **Парсинг вызовов инструментов в сообщениях** — Вызовы инструментов — это словари с `{"function": {"name": ..., "arguments": ...}}`. Всегда проверяйте `isinstance(tc, dict)`.
  9. **ToolContext.cleanup()** — Всегда вызывайте в блоке finally для освобождения ресурсов песочницы.
  10. **server_type должен быть \"openai\" для внешних API** — Без этого Atropos предполагает локальный сервер VLLM.
  11. **Всегда спрашивайте пользователя о настройке инференса** — Никогда не зашивайте и не предполагайте конкретного провайдера/модели. Смотрите раздел «Настройка инференса» выше.


## Шаблоны функций награды[​](<#reward-function-patterns> "Прямая ссылка на Шаблоны функций награды")
### LLM-судья (для задач с открытым ответом)[​](<#llm-judge-for-open-ended-tasks> "Прямая ссылка на LLM-судья (для задач с открытым ответом)")
Используйте `self.server.chat_completion()` с промптом для оценки. Парсите JSON-ответ для получения числовой оценки. Всегда включайте эвристический запасной вариант (пересечение ключевых слов) на случай сбоя вызова судьи.
### Бинарная верификация (для задач с кодом/терминалом)[​](<#binary-verification-for-codeterminal-tasks> "Прямая ссылка на Бинарная верификация (для задач с кодом/терминалом)")
Используйте `ctx.terminal("pytest test.py -q")` для запуска тестов в песочнице агента. Возвращайте 1.0 при успехе, 0.0 при неудаче.
### Мульти-сигнал (комбинация нескольких показателей)[​](<#multi-signal-combine-multiple-indicators> "Прямая ссылка на Мульти-сигнал (комбинация нескольких показателей)")
Взвешивайте правильность (0.6) + использование инструментов (0.2) + эффективность (0.2) + опциональные бонусы. Ограничьте до [0, 1].
## Тестирование вашего окружения[​](<#testing-your-environment> "Прямая ссылка на Тестирование вашего окружения")
  1. **Тест импорта**: `python -c "from environments.my_env import MyEnv; print('OK')"`
  2. **Спросите пользователя о настройке инференса** (см. раздел «Настройка инференса» выше)
  3. **Режим Process** (1 элемент): Проверьте, что JSONL-вывод содержит валидные токены, маски, оценки
  4. **Режим Evaluate**: Проверьте, что полный цикл агента работает с инструментами, метрики логируются корректно
  5. **Проверьте диапазон наград**: Оценки должны быть в [0, 1], не все одинаковые


## Минимальный чек-лист реализации[​](<#minimum-implementation-checklist> "Прямая ссылка на Минимальный чек-лист реализации")
[code] 
    class MyEnv(HermesAgentBaseEnv):  
        name = "my-env"  
        env_config_cls = MyEnvConfig  
      
        @classmethod  
        def config_init(cls): ...          # Конфигурация сервера и окружения по умолчанию  
        async def setup(self): ...         # Загрузка набора данных + разделение train/eval  
        async def get_next_item(self): ... # Циклический проход по элементам обучения  
        def format_prompt(self, item): ... # Элемент → строка сообщения пользователя  
        async def compute_reward(self, item, result, ctx): ...  # Оценка прогона  
        async def evaluate(self, *args, **kwargs): ...  # Оценка с полным циклом агента  
        async def wandb_log(self, metrics=None): ...    # Кастомные метрики + super()  
      
    if __name__ == "__main__":  
        MyEnv.cli()  
    
[/code]
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Обзор архитектуры](<#architecture-overview>)
  * [Расположение файлов](<#file-locations>)
  * [Настройка инференса — сначала спросите пользователя](<#inference-setup--ask-the-user-first>)
    * [Ключевые флаги по провайдеру:](<#key-flags-by-provider>)
  * [Обязательные методы](<#required-methods>)
    * [1\\. `setup()` — Загрузка набора данных и инициализация состояния](<#1-setup--load-dataset-and-initialize-state>)
    * [2\\. `get_next_item()` — Возврат следующего элемента обучения](<#2-get_next_item--return-next-training-item>)
    * [3\\. `format_prompt(item)` — Преобразование элемента в сообщение пользователя](<#3-format_promptitem--convert-item-to-user-message>)
    * [4\\. `compute_reward(item, result, ctx)` — Оценка прогона](<#4-compute_rewarditem-result-ctx--score-the-rollout>)
    * [5\\. `evaluate()` — Периодическая оценка с полным циклом агента](<#5-evaluate--periodic-evaluation-with-full-agent-loop>)
    * [6\\. `wandb_log()` — Кастомное логирование метрик](<#6-wandb_log--custom-metrics-logging>)
  * [Класс конфигурации](<#config-class>)
  * [config_init() — Конфигурация по умолчанию](<#config_init--default-configuration>)
  * [Три режима CLI](<#three-cli-modes>)
  * [Частые ловушки](<#common-pitfalls>)
  * [Шаблоны функций награды](<#reward-function-patterns>)
    * [LLM-судья (для задач с открытым ответом)](<#llm-judge-for-open-ended-tasks>)
    * [Бинарная верификация (для задач с кодом/терминалом)](<#binary-verification-for-codeterminal-tasks>)
    * [Мульти-сигнал (комбинация нескольких показателей)](<#multi-signal-combine-multiple-indicators>)
  * [Тестирование вашего окружения](<#testing-your-environment>)
  * [Минимальный чек-лист реализации](<#minimum-implementation-checklist>)



