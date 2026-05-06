On this page
Система флеш-карточек с интервальными повторениями. Создавайте карточки из фактов или текста, общайтесь с флеш-карточками через ответы свободным текстом с оценкой агента, генерируйте викторины из транскриптов YouTube, просматривайте карточки по расписанию, экспортируйте и импортируйте колоды в CSV.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |   |
|---|---|
|Source| Опционально — установка `hermes skills install official/productivity/memento-flashcards` |
|Path| `optional-skills/productivity/memento-flashcards` |
|Version| `1.0.0` |
|Author| Memento AI |
|License| MIT |
|Platforms| macos, linux |
|Tags| `Education`, `Flashcards`, `Spaced Repetition`, `Learning`, `Quiz`, `YouTube` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
> [!info]
> Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Именно эти инструкции видит агент, когда навык активен.

# Memento Flashcards — Spaced-Repetition Flashcard Skill
## Overview[​](<#overview> "Direct link to Overview")
Memento предоставляет локальную файловую систему флеш-карточек с интервальными повторениями. Пользователи могут общаться со своими флеш-карточками, отвечая свободным текстом, а агент оценивает ответ перед планированием следующего повторения. Используйте навык, когда пользователь хочет:
  * **Запомнить факт** — превратить любое утверждение в карточку Вопрос/Ответ
  * **Учиться с интервальными повторениями** — просматривать карточки с адаптивными интервалами и оценкой ответов агентом
  * **Пройти викторину по видео YouTube** — получить транскрипт и сгенерировать викторину из 5 вопросов
  * **Управлять колодами** — организовывать карточки в коллекции, экспортировать/импортировать CSV

Все данные карточек хранятся в одном JSON-файле. Внешние API-ключи не требуются — вы (агент) генерируете содержимое флеш-карточек и вопросы викторин напрямую.
Стиль ответа пользователю в Memento Flashcards:
  * Используйте только обычный текст. Не используйте Markdown-форматирование в ответах пользователю.
  * Делайте отзывы и комментарии к викторинам краткими и нейтральными. Избегайте лишних похвал, подбадриваний или длинных объяснений.

## When to Use[​](<#when-to-use> "Direct link to When to Use")
Используйте этот навык, когда пользователь хочет:
  * Сохранять факты как флеш-карточки для последующего повторения
  * Просматривать карточки с интервальными повторениями
  * Сгенерировать викторину из транскрипта видео YouTube
  * Импортировать, экспортировать, просматривать или удалять данные флеш-карточек

Не используйте этот навык для общих вопросов и ответов, помощи с кодом или задач, не связанных с памятью.
## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
| Намерение пользователя | Действие |
|---|---|
| «Запомни, что X» / «сохрани это как флеш-карточку» | Сгенерировать карточку В/О, вызвать `memento_cards.py add` |
| Пользователь отправляет факт, не упоминая флеш-карточки | Спросить «Хотите сохранить это как флеш-карточку Memento?» — создавать только после подтверждения |
| «Создай флеш-карточку» | Спросить В, О, коллекцию; вызвать `memento_cards.py add` |
| «Покажи мои карточки» | Вызвать `memento_cards.py due`, показывать карточки по одной |
| «Проведи викторину по [YouTube URL]» | Вызвать `youtube_quiz.py fetch VIDEO_ID`, сгенерировать 5 вопросов, вызвать `memento_cards.py add-quiz` |
| «Экспортируй мои карточки» | Вызвать `memento_cards.py export --output PATH` |
| «Импортируй карточки из CSV» | Вызвать `memento_cards.py import --file PATH --collection NAME` |
| «Покажи мою статистику» | Вызвать `memento_cards.py stats` |
| «Удали карточку» | Вызвать `memento_cards.py delete --id ID` |
| «Удали коллекцию» | Вызвать `memento_cards.py delete-collection --collection NAME` |
## Card Storage[​](<#card-storage> "Direct link to Card Storage")
Карточки хранятся в JSON-файле по пути:
```bash
~/.hermes/skills/productivity/memento-flashcards/data/cards.json
```
**Никогда не редактируйте этот файл напрямую.** Всегда используйте подкоманды `memento_cards.py`. Скрипт обрабатывает атомарные записи (запись во временный файл, затем переименование) для предотвращения повреждений.
Файл создаётся автоматически при первом использовании.
## Procedure[​](<#procedure> "Direct link to Procedure")
### Creating Cards from Facts[​](<#creating-cards-from-facts> "Direct link to Creating Cards from Facts")
### Activation Rules[​](<#activation-rules> "Direct link to Activation Rules")
Не каждое фактическое утверждение должно стать флеш-карточкой. Используйте трёхуровневую проверку:
  1. **Явное намерение** — пользователь упоминает «memento», «флеш-карточка», «запомни это», «сохрани эту карточку», «добавь карточку» или аналогичные фразы, явно запрашивающие флеш-карточку → **создайте карточку напрямую**, подтверждение не требуется.
  2. **Неявное намерение** — пользователь отправляет фактическое утверждение без упоминания флеш-карточек (например, «Скорость света — 299 792 км/с») → **сначала спросите**: «Хотите сохранить это как флеш-карточку Memento?» Создавайте карточку только после подтверждения пользователя.
  3. **Нет намерения** — сообщение является задачей по программированию, вопросом, инструкцией, обычным разговором или чем-то, что явно не является фактом для запоминания → **НЕ активируйте этот навык**. Пусть другие навыки или поведение по умолчанию обработают запрос.

Когда активация подтверждена (уровень 1 напрямую, уровень 2 после подтверждения), создайте флеш-карточку:
**Шаг 1:** Превратите утверждение в пару Вопрос/Ответ. Используйте этот формат внутри:
```text
Turn the factual statement into a front-back pair.
Return exactly two lines:
Q: <question text>
A: <answer text>

Statement: "{statement}"
```
Правила:
  * Вопрос должен проверять запоминание ключевого факта
  * Ответ должен быть кратким и прямым

**Шаг 2:** Вызовите скрипт для сохранения карточки:
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py add \
  --question "What year did World War 2 end?" \
  --answer "1945" \
  --collection "History"
```
Если пользователь не указал коллекцию, используйте `"General"` по умолчанию.
Скрипт выводит JSON с подтверждением созданной карточки.
### Manual Card Creation[​](<#manual-card-creation> "Direct link to Manual Card Creation")
Когда пользователь явно просит создать флеш-карточку, спросите у него:
  1. Вопрос (лицевая сторона карточки)
  2. Ответ (обратная сторона карточки)
  3. Название коллекции (опционально — по умолчанию `"General"`)

Затем вызовите `memento_cards.py add`, как показано выше.
### Reviewing Due Cards[​](<#reviewing-due-cards> "Direct link to Reviewing Due Cards")
Когда пользователь хочет повторить, получите все карточки, подлежащие повторению:
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due
```
Это возвращает JSON-массив карточек, где `next_review_at <= now`. Если нужен фильтр по коллекции:
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due --collection "History"
```
**Процесс повторения (оценка свободного текста):**
Ниже приведён пример ТОЧНОГО шаблона взаимодействия, которому вы должны следовать. Пользователь отвечает, вы оцениваете, сообщаете правильный ответ, затем оцениваете карточку.
**Пример взаимодействия:**
> **Агент:** В каком году пала Берлинская стена?
> **Пользователь:** 1991
> **Агент:** Почти. Берлинская стена пала в 1989. Следующее повторение — завтра. _(агент вызывает: memento_cards.py rate --id ABC --rating hard --user-answer "1991")_
> Следующий вопрос: Кто был первым человеком, ступившим на Луну?
**Правила:**
  1. Показывайте только вопрос. Ждите ответа пользователя.
  2. Получив ответ, сравните его с ожидаемым ответом и оцените:
     * **correct** — пользователь правильно назвал ключевой факт (даже если сформулировал иначе)
     * **partial** — правильное направление, но не хватает ключевой детали
     * **incorrect** — неправильно или не по теме
  3. **Вы ОБЯЗАНЫ сообщить пользователю правильный ответ и результат.** Будьте краткими, используйте обычный текст. Формат:
     * correct: «Верно. Ответ: {answer}. Следующее повторение через 7 дней.»
     * partial: «Почти. Ответ: {answer}. {что он упустил}. Следующее повторение через 3 дня.»
     * incorrect: «Не совсем. Ответ: {answer}. Следующее повторение завтра.»
  4. Затем вызовите команду оценки: correct→easy, partial→good, incorrect→hard.
  5. Затем покажите следующий вопрос.

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py rate \
  --id CARD_ID --rating easy --user-answer "what the user said"
```
**Никогда не пропускайте шаг 3.** Пользователь всегда должен видеть правильный ответ и обратную связь, прежде чем вы продолжите.
Если карточек для повторения нет, сообщите пользователю: «Сейчас нет карточек для повторения. Загляните позже!»
**Отмена повторения:** В любой момент пользователь может сказать «убрать эту карточку», чтобы навсегда удалить её из повторений. Используйте `--rating retire` для этого.
### Spaced Repetition Algorithm[​](<#spaced-repetition-algorithm> "Direct link to Spaced Repetition Algorithm")
Оценка определяет следующий интервал повторения:
| Оценка | Интервал | ease_streak | Изменение статуса |
|---|---|---|---|
| **hard** | +1 день | сброс на 0 | остаётся learning |
| **good** | +3 дня | сброс на 0 | остаётся learning |
| **easy** | +7 дней | +1 | если ease_streak >= 3 → retired |
| **retire** | навсегда | сброс на 0 | → retired |
  * **learning** : карточка активно в ротации
  * **retired** : карточка не будет появляться в повторениях (пользователь её освоил или вручную убрал)
  * Три последовательных оценки «easy» автоматически отправляют карточку в retired

### YouTube Quiz Generation[​](<#youtube-quiz-generation> "Direct link to YouTube Quiz Generation")
Когда пользователь отправляет URL YouTube и хочет викторину:
**Шаг 1:** Извлеките ID видео из URL (например, `dQw4w9WgXcQ` из `https://www.youtube.com/watch?v=dQw4w9WgXcQ`).
**Шаг 2:** Получите транскрипт:
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/youtube_quiz.py fetch VIDEO_ID
```
Это возвращает `{"title": "...", "transcript": "..."}` или ошибку.
Если скрипт сообщает `missing_dependency`, скажите пользователю установить зависимость:
```bash
pip install youtube-transcript-api
```
**Шаг 3:** Сгенерируйте 5 вопросов для викторины из транскрипта. Используйте следующие правила:
```text
You are creating a 5-question quiz for a podcast episode.
Return ONLY a JSON array with exactly 5 objects.
Each object must contain keys 'question' and 'answer'.

Selection criteria:
- Prioritize important, surprising, or foundational facts.
- Skip filler, obvious details, and facts that require heavy context.
- Never return true/false questions.
- Never ask only for a date.

Question rules:
- Each question must test exactly one discrete fact.
- Use clear, unambiguous wording.
- Prefer What, Who, How many, Which.
- Avoid open-ended Describe or Explain prompts.

Answer rules:
- Each answer must be under 240 characters.
- Lead with the answer itself, not preamble.
- Add only minimal clarifying detail if needed.
```
Используйте первые 15 000 символов транскрипта как контекст. Сгенерируйте вопросы самостоятельно (вы — LLM).
**Шаг 4:** Проверьте, что вывод является валидным JSON с ровно 5 элементами, каждый из которых имеет непустые строки `question` и `answer`. Если проверка не пройдена, повторите попытку один раз.
**Шаг 5:** Сохраните карточки викторины:
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py add-quiz \
  --video-id "VIDEO_ID" \
  --questions '[{"question":"...","answer":"..."},...]' \
  --collection "Quiz - Episode Title"
```
Скрипт дедуплицирует по `video_id` — если карточки для этого видео уже существуют, он пропускает создание и сообщает о существующих карточках.
**Шаг 6:** Представляйте вопросы по одному, используя тот же процесс оценки свободного текста:
  1. Покажите «Вопрос 1/5: ...» и ждите ответа пользователя. Никогда не включайте ответ или подсказку о его раскрытии.
  2. Ждите, пока пользователь ответит своими словами
  3. Оцените ответ, используя промпт для оценки (см. раздел «Просмотр карточек по расписанию»)
  4. **ВАЖНО: Вы ОБЯЗАНЫ ответить пользователю с обратной связью, прежде чем делать что-либо ещё.** Покажите оценку, правильный ответ и когда карточка будет в следующий раз к повторению. Не переходите молча к следующему вопросу. Будьте краткими, используйте обычный текст. Пример: «Не совсем. Ответ: {answer}. Следующее повторение завтра.»
  5. **После показа обратной связи** вызовите команду оценки, а затем покажите следующий вопрос в том же сообщении:

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py rate \
  --id CARD_ID --rating easy --user-answer "what the user said"
```
  6. Повторяйте. Каждый ответ ОБЯЗАТЕЛЬНО должен получать видимую обратную связь перед следующим вопросом.

### Export/Import CSV[​](<#exportimport-csv> "Direct link to Export/Import CSV")
**Экспорт:**
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py export \
  --output ~/flashcards.csv
```
Создаёт CSV с 3 столбцами: `question,answer,collection` (без строки заголовка).
**Импорт:**
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py import \
  --file ~/flashcards.csv \
  --collection "Imported"
```
Читает CSV со столбцами: question, answer и опционально collection (столбец 3). Если столбец collection отсутствует, используется аргумент `--collection`.
### Statistics[​](<#statistics> "Direct link to Statistics")
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py stats
```
Возвращает JSON с:
  * `total`: общее количество карточек
  * `learning`: карточки в активной ротации
  * `retired`: освоенные карточки
  * `due_now`: карточки, ожидающие повторения прямо сейчас
  * `collections`: разбивка по названиям коллекций

## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * **Никогда не редактируйте `cards.json` напрямую** — всегда используйте подкоманды скрипта, чтобы избежать повреждений
  * **Сбои транскрипции** — некоторые видео YouTube не имеют английского транскрипта или транскрипты отключены; сообщите пользователю и предложите другое видео
  * **Опциональная зависимость** — `youtube_quiz.py` требует `youtube-transcript-api`; если отсутствует, скажите пользователю выполнить `pip install youtube-transcript-api`
  * **Большие импорты** — импорт CSV с тысячами строк работает нормально, но вывод JSON может быть объёмным; суммируйте результат для пользователя
  * **Извлечение ID видео** — поддерживаются оба формата URL: `youtube.com/watch?v=ID` и `youtu.be/ID`

## Verification[​](<#verification> "Direct link to Verification")
Проверьте вспомогательные скрипты напрямую:
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py stats
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py add --question "Capital of France?" --answer "Paris" --collection "General"
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due
```
Если вы тестируете из репозитория, выполните:
```bash
pytest tests/skills/test_memento_cards.py tests/skills/test_youtube_quiz.py -q
```
Проверка на уровне агента:
  * Начните повторение и убедитесь, что обратная связь — обычный текст, краткая и всегда включает правильный ответ перед следующей карточкой
  * Запустите викторину по YouTube и убедитесь, что каждый ответ получает видимую обратную связь перед следующим вопросом

  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Overview](<#overview>)
  * [When to Use](<#when-to-use>)
  * [Quick Reference](<#quick-reference>)
  * [Card Storage](<#card-storage>)
  * [Procedure](<#procedure>)
    * [Creating Cards from Facts](<#creating-cards-from-facts>)
    * [Activation Rules](<#activation-rules>)
    * [Manual Card Creation](<#manual-card-creation>)
    * [Reviewing Due Cards](<#reviewing-due-cards>)
    * [Spaced Repetition Algorithm](<#spaced-repetition-algorithm>)
    * [YouTube Quiz Generation](<#youtube-quiz-generation>)
    * [Export/Import CSV](<#exportimport-csv>)
    * [Statistics](<#statistics>)
  * [Pitfalls](<#pitfalls>)
  * [Verification](<#verification>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-memento-flashcards -->
