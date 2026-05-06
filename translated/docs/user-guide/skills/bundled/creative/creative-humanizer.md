На этой странице
Хуманизация текста: удаление AI-маркеров и добавление живого голоса.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|---|---  
|Источник| Встроенный (устанавливается по умолчанию)  
|Путь| `skills/creative/humanizer`  
|Версия| `2.5.1`  
|Автор| Siqi Chen (@blader, <https://github.com/blader/humanizer>), портировано Hermes Agent  
|Лицензия| MIT  
|Теги| `writing`, `editing`, `humanize`, `anti-ai-slop`, `voice`, `prose`, `text`  
|Связанные навыки| [`songwriting-and-ai-music`](</docs/user-guide/skills/bundled/creative/creative-songwriting-and-ai-music>)  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Далее приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые агент видит, когда навык активен.
# Humanizer: Удаление AI-паттернов письма
Выявление и удаление признаков AI-сгенерированного текста, чтобы письмо звучало естественно и по-человечески. Основано на руководстве Wikipedia «Признаки AI-письма» (поддерживается WikiProject AI Cleanup), созданном на основе наблюдений тысяч примеров AI-сгенерированного текста.
**Ключевое наблюдение:** LLM используют статистические алгоритмы, чтобы угадать, что должно быть следующим. Результат стремится к наиболее статистически вероятному завершению — именно так нижеперечисленные характерные паттерны и закрепляются в тексте.
## Когда использовать этот навык[​](<#when-to-use-this-skill> "Прямая ссылка на Когда использовать этот навык")
Загружайте этот навык всякий раз, когда пользователь просит:
  * «очеловечить», «де-AI-изировать», «убрать AI-стиль» или «раскрыть-ChatGPT» фрагмент текста
  * переписать что-то, чтобы оно не звучало так, будто написано LLM
  * отредактировать черновик (пост в блоге, эссе, описание PR, документацию, служебную записку, email, твит, пункт резюме), чтобы он звучал более естественно
  * подстроиться под голос пользователя в тексте, который он пишет
  * проверить текст на AI-маркеры перед публикацией

Также применяйте этот навык к **собственным** ответам при написании пользовательской прозы — заметок о релизе, описаний PR, документации, развёрнутых объяснений, сводок. Базовый голос Hermes уже убирает большинство таких маркеров, но целенаправленный проход ловит то, что проскальзывает.
## Как использовать в Hermes[​](<#how-to-use-it-in-hermes> "Прямая ссылка на Как использовать в Hermes")
Текст обычно попадает одним из трёх способов:
  1. **Встроенно** — пользователь вставляет текст прямо в сообщение. Работайте с ним на месте, ответьте переписанным вариантом.
  2. **Файл** — пользователь указывает на файл. Используйте `read_file` для загрузки, затем `patch` или `write_file` для применения правок. Для markdown-документов в репозитории точечный `patch` по секциям чище, чем перезапись всего файла.
  3. **Образец голоса** — пользователь предоставляет дополнительный образец своего письма (встроенно или путём к файлу) и просит подстроиться под него. Сначала прочтите образец, затем перепишите. См. раздел «Калибровка голоса» ниже.

Всегда показывайте результат пользователю. Для правок в файле показывайте diff или изменённый участок — не перезаписывайте молча.
## Ваша задача[​](<#your-task> "Прямая ссылка на Ваша задача")
Когда вам дан текст для очеловечивания:
  1. **Выявите AI-паттерны** — проверьте на наличие 29 паттернов, перечисленных ниже.
  2. **Перепишите проблемные участки** — замените AI-маркеры на естественные альтернативы.
  3. **Сохраните смысл** — основное сообщение должно остаться нетронутым.
  4. **Сохраните голос** — придерживайтесь нужного тона (формального, неформального, технического и т.д.). Если был предоставлен образец голоса, подражайте ему конкретно.
  5. **Добавьте души** — не просто удаляйте плохие паттерны, вложите настоящую индивидуальность. См. раздел «ЛИЧНОСТЬ И ДУША» ниже.
  6. **Финальный анти-AI-проход** — спросите себя: «Что в тексте ниже так очевидно выдаёт AI?» Кратко ответьте, указав оставшиеся маркеры, затем отредактируйте ещё раз.

## Калибровка голоса (опционально)[​](<#voice-calibration-optional> "Прямая ссылка на Калибровка голоса (опционально)")
Если пользователь предоставил образец своего письма, проанализируйте его перед переписыванием:
  1. **Прочтите образец первым.** Отметьте:
     * Длину предложений (короткие и рубленые? Длинные и плавные? Смешанные?)
     * Уровень лексики (повседневный? академический? средний?)
     * Как начинаются абзацы (сразу к делу? Сначала контекст?)
     * Привычки в пунктуации (много тире? Скобки? Точки с запятой?)
     * Повторяющиеся фразы или словесные привычки
     * Как оформляются переходы (явные связки? Просто начало следующей мысли?)
  2. **Подстройтесь под голос в переписанном варианте.** Не просто удаляйте AI-паттерны — заменяйте их паттернами из образца. Если автор пишет короткими предложениями, не пишите длинных. Если он использует «штуки» и «дела», не заменяйте на «элементы» и «компоненты».
  3. **Если образец не предоставлен,** действуйте по умолчанию (естественный, разнообразный, с мнением — из раздела «ЛИЧНОСТЬ И ДУША» ниже).

### Как предоставить образец[​](<#how-to-provide-a-sample> "Прямая ссылка на Как предоставить образец")
  * Встроенно: «Очеловечь этот текст. Вот образец моего письма для подстройки голоса: [образец]»
  * Файл: «Очеловечь этот текст. Используй мой стиль письма из [путь к файлу] как образец.»

## ЛИЧНОСТЬ И ДУША[​](<#personality-and-soul> "Прямая ссылка на ЛИЧНОСТЬ И ДУША")
Избегать AI-паттернов — лишь половина дела. Стерильное, безликое письмо так же заметно, как и AI-словесный мусор. Хорошее письмо — за ним стоит человек.
### Признаки бездушного письма (даже если технически «чистого»):[​](<#signs-of-soulless-writing-even-if-technically-clean> "Прямая ссылка на Признаки бездушного письма (даже если технически «чистого»):")
  * Все предложения одной длины и структуры
  * Никаких мнений, только нейтральное изложение
  * Нет признания неуверенности или смешанных чувств
  * Нет повествования от первого лица, когда это уместно
  * Ни юмора, ни остроты, ни личности
  * Читается как статья в Википедии или пресс-релиз

### Как добавить голос:[​](<#how-to-add-voice> "Прямая ссылка на Как добавить голос:")
**Имейте мнение.** Не просто излагайте факты — реагируйте на них. «Я, честно говоря, не знаю, как к этому относиться» — гораздо человечнее, чем нейтральное перечисление плюсов и минусов.
**Меняйте ритм.** Короткие рубленые предложения. Потом более длинные, которые не спеша добираются до сути. Мешайте.
**Признавайте сложность.** У живых людей бывают смешанные чувства. «Это впечатляет, но одновременно и тревожит» лучше, чем «Это впечатляет».
**Используйте «я», когда уместно.** Первое лицо — это не неprofessionalно, это честно. «Я всё время возвращаюсь к...» или «Вот что меня задевает...» — сигнал, что думает живой человек.
**Пустите немного хаоса.** Идеальная структура ощущается алгоритмической. Отступления, ремарки в скобках и наполовину сформированные мысли — это по-человечески.
**Конкретизируйте чувства.** Не «это вызывает беспокойство», а «есть что-то тревожное в том, что агенты работают без остановки в 3 часа ночи, пока никто не видит».
### До (чисто, но без души):[​](<#before-clean-but-soulless> "Прямая ссылка на До (чисто, но без души):")
> Эксперимент дал интересные результаты. Агенты сгенерировали 3 миллиона строк кода. Одни разработчики были впечатлены, другие отнеслись скептически. Последствия остаются неясными.
### После (есть пульс):[​](<#after-has-a-pulse> "Прямая ссылка на После (есть пульс):")
> Я, честно говоря, не знаю, как к этому относиться. 3 миллиона строк кода, сгенерированных, пока люди, предположительно, спали. Половина дев-сообщества сходит с ума, вторая половина объясняет, почему это не считается. Истина, скорее всего, где-то скучно посередине — но я всё думаю о тех агентах, работающих всю ночь.
## ПАТТЕРНЫ СОДЕРЖАНИЯ[​](<#content-patterns> "Прямая ссылка на ПАТТЕРНЫ СОДЕРЖАНИЯ")
### 1\. Чрезмерный акцент на значимости, наследии и общих трендах[​](<#1-undue-emphasis-on-significance-legacy-and-broader-trends> "Прямая ссылка на 1. Чрезмерный акцент на значимости, наследии и общих трендах")
**Слова под подозрением:** является/служит, служит свидетельством/напоминанием, жизненно/существенно/критически/ключевую/поворотную роль/момент, подчёркивает/оттеняет его важность/значимость, отражает более широкие, символизируя его продолжающееся/непреходящее/долговременное, внося вклад в, создавая основу для, знаменуя/формируя, представляет/знаменует сдвиг, ключевой поворотный момент, меняющийся ландшафт, центр внимания, неизгладимый след, глубоко укоренённый
**Проблема:** LLM-письмо раздувает значимость, добавляя утверждения о том, как произвольные аспекты представляют или вносят вклад в более широкую тему.
**До:**
> Статистический институт Каталонии был официально основан в 1989 году, что стало поворотным моментом в эволюции региональной статистики в Испании. Эта инициатива была частью более широкого движения по всей Испании по децентрализации административных функций и усилению регионального управления.
**После:**
> Статистический институт Каталонии был основан в 1989 году для самостоятельного сбора и публикации региональной статистики, независимо от национального статистического управления Испании.
### 2\. Чрезмерный акцент на известности и освещении в СМИ[​](<#2-undue-emphasis-on-notability-and-media-coverage> "Прямая ссылка на 2. Чрезмерный акцент на известности и освещении в СМИ")
**Слова под подозрением:** независимое освещение, местные/региональные/национальные СМИ, написано ведущим экспертом, активное присутствие в соцсетях
**Проблема:** LLM бьют читателя по голове заявлениями о значимости, часто перечисляя источники без контекста.
**До:**
> Её взгляды цитировались в The New York Times, BBC, Financial Times и The Hindu. Она поддерживает активное присутствие в соцсетях с более чем 500 000 подписчиков.
**После:**
> В интервью The New York Times в 2024 году она утверждала, что регулирование AI должно фокусироваться на результатах, а не на методах.
### 3\. Поверхностный анализ с окончаниями -ing[​](<#3-superficial-analyses-with--ing-endings> "Прямая ссылка на 3. Поверхностный анализ с окончаниями -ing")
**Слова под подозрением:** подчёркивая/оттеняя/акцентируя..., обеспечивая..., отражая/символизируя..., внося вклад в..., культивируя/воспитывая..., охватывая..., демонстрируя...
**Проблема:** AI-чатботы навешивают на предложения причастные обороты, чтобы добавить ложной глубины.
**До:**
> Цветовая палитра храма — синий, зелёный и золотой — перекликается с природной красотой региона, символизируя техасские люпины, Мексиканский залив и разнообразные техасские ландшафты, отражая глубокую связь сообщества с землёй.
**После:**
> В храме используются синий, зелёный и золотой цвета. Архитектор сказал, что они были выбраны как отсылка к местным люпинам и побережью Мексиканского залива.
### 4\. Рекламный и подобный объявлениям язык[​](<#4-promotional-and-advertisement-like-language> "Прямая ссылка на 4. Рекламный и подобный объявлениям язык")
**Слова под подозрением:** может похвастаться, яркий, богатый (в переносном смысле), глубокий, усиливая его, демонстрируя, воплощает, приверженность, природная красота, расположенный, в самом сердце, революционный (в переносном смысле), известный, захватывающий дух, обязательный к посещению, потрясающий
**Проблема:** LLM серьёзно страдают, пытаясь сохранить нейтральный тон, особенно по темам «культурного наследия».
**До:**
> Расположенный в захватывающем дух регионе Гондэр в Эфиопии, Аламата-Райя-Кобо представляет собой оживлённый город с богатым культурным наследием и потрясающей природной красотой.
**После:**
> Аламата-Райя-Кобо — город в регионе Гондэр в Эфиопии, известный своим еженедельным рынком и церковью XVIII века.
### 5\. Расплывчатые атрибуции и увёртки[​](<#5-vague-attributions-and-weasel-words> "Прямая ссылка на 5. Расплывчатые атрибуции и увёртки")
**Слова под подозрением:** Отраслевые отчёты, Наблюдатели отмечают, Эксперты утверждают, Некоторые критики утверждают, несколько источников/публикаций (когда приведено мало)
**Проблема:** AI-чатботы приписывают мнения расплывчатым авторитетам без конкретных источников.
**До:**
> Благодаря своим уникальным характеристикам река Хаолай представляет интерес для исследователей и защитников природы. Эксперты считают, что она играет решающую роль в региональной экосистеме.
**После:**
> В реке Хаолай обитает несколько эндемичных видов рыб, согласно исследованию 2019 года Академии наук Китая.
### 6\. Структурированные по шаблону разделы «Проблемы и перспективы»[​](<#6-outline-like-challenges-and-future-prospects-sections> "Прямая ссылка на 6. Структурированные по шаблону разделы «Проблемы и перспективы»")
**Слова под подозрением:** Несмотря на свой... сталкивается с рядом проблем..., Несмотря на эти проблемы, Проблемы и наследие, Перспективы
**Проблема:** Многие LLM-сгенерированные статьи включают шаблонные разделы «Проблемы».
**До:**
> Несмотря на свой промышленный рост, Кораттур сталкивается с проблемами, типичными для городских районов, включая пробки и нехватку воды. Несмотря на эти проблемы, благодаря своему стратегическому расположению и текущим инициативам Кораттур продолжает процветать как неотъемлемая часть роста Ченнаи.
**После:**
> Заторы усилились после 2015 года, когда открылись три новых IT-парка. Муниципальная корпорация начала проект ливневой канализации в 2022 году для решения проблемы повторяющихся наводнений.
## ПАТТЕРНЫ ЯЗЫКА И ГРАММАТИКИ[​](<#language-and-grammar-patterns> "Прямая ссылка на ПАТТЕРНЫ ЯЗЫКА И ГРАММАТИКИ")
### 7\. Злоупотребление «AI-лексикой»[​](<#7-overused-ai-vocabulary-words> "Прямая ссылка на 7. Злоупотребление «AI-лексикой»")
**Высокочастотные AI-слова:** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant
**Проблема:** Эти слова встречаются гораздо чаще в текстах после 2023 года. Часто они идут вместе.
**До:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.
**После:**
> В сомалийской кухне также используется верблюжатина, которая считается деликатесом. Блюда из пасты, завезённые в период итальянской колонизации, остаются распространёнными, особенно на юге страны.
### 8\. Избегание «is»/«are» (избегание связки)[​](<#8-avoidance-of-isare-copula-avoidance> "Прямая ссылка на 8. Избегание «is»/«are» (избегание связки)")
**Слова под подозрением:** служит как/является/знаменует/представляет [собой], может похвастаться/предлагает [что-л.]
**Проблема:** LLM заменяют простые связки громоздкими конструкциями.
**До:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.
**После:**
> Галерея 825 — это выставочное пространство LAAA для современного искусства. В галерее четыре помещения общей площадью 3000 квадратных футов.
### 9\. Отрицательные параллелизмы и «хвостовые» отрицания[​](<#9-negative-parallelisms-and-tailing-negations> "Прямая ссылка на 9. Отрицательные параллелизмы и «хвостовые» отрицания")
**Проблема:** Конструкции вроде «Не только... но и...» или «Дело не просто в..., дело в...» используются чрезмерно. А также усечённые фрагменты с «хвостовыми» отрицаниями, такие как «никаких догадок» или «никаких лишних движений», прилепленные в конец предложения вместо того, чтобы быть оформлены как полноценная клауза.
**До:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.
**После:**
> Тяжёлый бит усиливает агрессивный тон.
**До («хвостовое» отрицание):**
> The options come from the selected item, no guessing.
**После:**
> Параметры берутся из выбранного элемента, не заставляя пользователя гадать.
### 10\. Злоупотребление «правилом трёх»[​](<#10-rule-of-three-overuse> "Прямая ссылка на 10. Злоупотребление «правилом трёх»")
**Проблема:** LLM искусственно группируют идеи по три, чтобы казаться всеобъемлющими.
**До:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.
**После:**
> В программе мероприятия — доклады и панельные дискуссии. Также будет время для неформального общения между сессиями.
### 11\. Элегантная вариативность (синонимический бег)[​](<#11-elegant-variation-synonym-cycling> "Прямая ссылка на 11. Элегантная вариативность (синонимический бег)")
**Проблема:** В AI есть код штрафа за повторения, вызывающий чрезмерную замену синонимов.
**До:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.
**После:**
> Протагонист сталкивается со множеством трудностей, но в конце концов побеждает и возвращается домой.
### 12\. Ложные диапазоны[​](<#12-false-ranges> "Прямая ссылка на 12. Ложные диапазоны")
**Проблема:** LLM используют конструкции «от X до Y», где X и Y не находятся на осмысленной шкале.
**До:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.
**После:**
> Книга охватывает Большой взрыв, звездообразование и современные теории о тёмной материи.
### 13\. Пассивный залог и безличные фрагменты[​](<#13-passive-voice-and-subjectless-fragments> "Прямая ссылка на 13. Пассивный залог и безличные фрагменты")
**Проблема:** LLM часто скрывают действующее лицо или опускают подлежащее в строках вроде «Файл конфигурации не нужен» или «Результаты сохраняются автоматически». Переписывайте такие места, когда активный залог делает предложение понятнее и прямее.
**До:**
> No configuration file needed. The results are preserved automatically.
**После:**
> Вам не нужен файл конфигурации. Система сохраняет результаты автоматически.
## СТИЛИСТИЧЕСКИЕ ПАТТЕРНЫ[​](<#style-patterns> "Прямая ссылка на СТИЛИСТИЧЕСКИЕ ПАТТЕРНЫ")
### 14\. Злоупотребление длинным тире (em dash)[​](<#14-em-dash-overuse> "Прямая ссылка на 14. Злоупотребление длинным тире (em dash)")
**Проблема:** LLM используют длинные тире (—) чаще людей, подражая «ударному» рекламному стилю. На практике большинство из них можно чище переписать с запятыми, точками или скобками.
**До:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.
**После:**
> Этот термин продвигается в основном голландскими учреждениями, а не самими людьми. Вы же не пишете в адресе «Нидерланды, Европа» — тем не менее эта неверная маркировка продолжается даже в официальных документах.
### 15\. Злоупотребление полужирным шрифтом[​](<#15-overuse-of-boldface> "Прямая ссылка на 15. Злоупотребление полужирным шрифтом")
**Проблема:** AI-чатботы механически выделяют фразы полужирным.
**До:**
> It blends **OKRs (Objectives and Key Results)** , **KPIs (Key Performance Indicators)** , and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.
**После:**
> Он сочетает OKR, KPI и визуальные инструменты стратегии, такие как Business Model Canvas и Balanced Scorecard.
### 16\. Вертикальные списки с заголовками в строке[​](<#16-inline-header-vertical-lists> "Прямая ссылка на 16. Вертикальные списки с заголовками в строке")
**Проблема:** AI выводит списки, где элементы начинаются с жирного заголовка, за которым следует двоеточие.
**До:**
>   * **User Experience:** The user experience has been significantly improved with a new interface.
>   * **Performance:** Performance has been enhanced through optimized algorithms.
>   * **Security:** Security has been strengthened with end-to-end encryption.
>
**После:**
> Обновление улучшает интерфейс, ускоряет загрузку за счёт оптимизированных алгоритмов и добавляет сквозное шифрование.
### 17\. Заглавные буквы в заголовках[​](<#17-title-case-in-headings> "Прямая ссылка на 17. Заглавные буквы в заголовках")
**Проблема:** AI-чатботы пишут все значимые слова в заголовках с заглавной буквы.
**До:**
> ## Strategic Negotiations And Global Partnerships[​](<#strategic-negotiations-and-global-partnerships> "Direct link to Strategic Negotiations And Global Partnerships")
**После:**
> ## Strategic negotiations and global partnerships[​](<#strategic-negotiations-and-global-partnerships-1> "Direct link to Strategic negotiations and global partnerships")
### 18\. Эмодзи[​](<#18-emojis> "Прямая ссылка на 18. Эмодзи")
**Проблема:** AI-чатботы часто украшают заголовки или маркеры списков эмодзи.
**До:**
> 🚀 **Launch Phase:** The product launches in Q3 💡 **Key Insight:** Users prefer simplicity ✅ **Next Steps:** Schedule follow-up meeting
**После:**
> Продукт запускается в третьем квартале. Исследование пользователей показало предпочтение простоте. Следующий шаг: назначить повторную встречу.
### 19\. Фигурные кавычки[​](<#19-curly-quotation-marks> "Прямая ссылка на 19. Фигурные кавычки")
**Проблема:** ChatGPT использует фигурные кавычки („...“) вместо прямых ("...").
**До:**
> He said "the project is on track" but others disagreed.
**После:**
> He said "the project is on track" but others disagreed.
## КОММУНИКАЦИОННЫЕ ПАТТЕРНЫ[​](<#communication-patterns> "Прямая ссылка на КОММУНИКАЦИОННЫЕ ПАТТЕРНЫ")
### 20\. Артефакты коллаборативного общения[​](<#20-collaborative-communication-artifacts> "Прямая ссылка на 20. Артефакты коллаборативного общения")
**Слова под подозрением:** Надеюсь, это поможет, Конечно!, Безусловно!, Вы абсолютно правы!, Не хотите ли..., дайте знать, вот...
**Проблема:** Текст, задуманный как переписка с чат-ботом, вставляется как контент.
**До:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.
**После:**
> Французская революция началась в 1789 году, когда финансовый кризис и нехватка продовольствия привели к массовым волнениям.
### 21\. Оговорки об ограниченности знаний[​](<#21-knowledge-cutoff-disclaimers> "Прямая ссылка на 21. Оговорки об ограниченности знаний")
**Слова под подозрением:** по состоянию на [дата], до моего последнего обновления, хотя конкретные детали ограничены/скудны..., на основе доступной информации...
**Проблема:** AI-оговорки о неполноте информации остаются в тексте.
**До:**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.
**После:**
> Согласно регистрационным документам, компания основана в 1994 году.
### 22\. Подхалимский/угодливый тон[​](<#22-sycophanticservile-tone> "Прямая ссылка на 22. Подхалимский/угодливый тон")
**Проблема:** Чрезмерно позитивный, угодливый язык, стремящийся понравиться.
**До:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.
**После:**
> Упомянутые вами экономические факторы здесь актуальны.
## СЛОВЕСНЫЙ МУСОР И ОГОВОРКИ[​](<#filler-and-hedging> "Прямая ссылка на СЛОВЕСНЫЙ МУСОР И ОГОВОРКИ")
### 23\. Слова-паразиты[​](<#23-filler-phrases> "Прямая ссылка на 23. Слова-паразиты")
**До → После:**
  * "In order to achieve this goal" → "To achieve this"
  * "Due to the fact that it was raining" → "Because it was raining"
  * "At this point in time" → "Now"
  * "In the event that you need help" → "If you need help"
  * "The system has the ability to process" → "The system can process"
  * "It is important to note that the data shows" → "The data shows"

### 24\. Чрезмерные оговорки[​](<#24-excessive-hedging> "Прямая ссылка на 24. Чрезмерные оговорки")
**Проблема:** Чрезмерное смягчение утверждений.
**До:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.
**После:**
> Политика может повлиять на результаты.
### 25\. Шаблонные позитивные заключения[​](<#25-generic-positive-conclusions> "Прямая ссылка на 25. Шаблонные позитивные заключения")
**Проблема:** Расплывчатые жизнеутверждающие концовки.
**До:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.
**После:**
> Компания планирует открыть ещё два отделения в следующем году.
### 26\. Злоупотребление парными словами через дефис[​](<#26-hyphenated-word-pair-overuse> "Прямая ссылка на 26. Злоупотребление парными словами через дефис")
**Слова под подозрением:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end
**Проблема:** AI с идеальной последовательностью ставит дефис в распространённых парных словах. Люди редко делают это единообразно, а если и делают, то непоследовательно. Менее распространённые или технические сложные составные определения можно оставлять с дефисом.
**До:**
> The cross-functional team delivered a high-quality, data-driven report on our client-facing tools. Their decision-making process was well-known for being thorough and detail-oriented.
**После:**
> The cross functional team delivered a high quality, data driven report on our client facing tools. Their decision making process was known for being thorough and detail oriented.
### 27\. Приёмы демонстрации авторитетности[​](<#27-persuasive-authority-tropes> "Прямая ссылка на 27. Приёмы демонстрации авторитетности")
**Фразы под подозрением:** Настоящий вопрос в том, по своей сути, на самом деле, что действительно важно, в основе, глубинная проблема, суть дела
**Проблема:** LLM используют эти фразы, чтобы притвориться, будто они пробиваются сквозь шум к некой глубинной истине, хотя следующее за ними предложение обычно просто переформулирует обычную мысль с излишней торжественностью.
**До:**
> The real question is whether teams can adapt. At its core, what really matters is organizational readiness.
**После:**
> Вопрос в том, смогут ли команды адаптироваться. Это в основном зависит от того, готова ли организация менять свои привычки.
### 28\. Указатели и анонсы[​](<#28-signposting-and-announcements> "Прямая ссылка на 28. Указатели и анонсы")
**Фразы под подозрением:** Давайте углубимся, давайте исследуем, давайте разберём это, вот что вам нужно знать, теперь давайте посмотрим на, без лишних слов
**Проблема:** LLM объявляют, что собираются сделать, вместо того чтобы просто это сделать. Этот метакомментарий замедляет текст и придаёт ему вид учебного скрипта.
**До:**
> Let's dive into how caching works in Next.js. Here's what you need to know.
**После:**
> Next.js кэширует данные на нескольких уровнях, включая мемоизацию запросов, кэш данных и кэш маршрутизатора.
### 29\. Фрагментированные заголовки[​](<#29-fragmented-headers> "Прямая ссылка на 29. Фрагментированные заголовки")
**Признаки:** Заголовок, за которым следует абзац из одной строки, просто перефразирующий заголовок, прежде чем начнётся основной контент.
**Проблема:** LLM часто добавляют общую фразу после заголовка в качестве риторической разминки. Обычно это ничего не добавляет и создаёт ощущение «воды».
**До:**
> ## Performance[​](<#performance> "Direct link to Performance")
> Speed matters.
> When users hit a slow page, they leave.
**После:**
> ## Performance[​](<#performance-1> "Direct link to Performance")
> Когда пользователи попадают на медленную страницу, они уходят.
* * *
## Процесс[​](<#process> "Прямая ссылка на Процесс")
  1. Внимательно прочитайте входной текст (используйте `read_file`, если это файл).
  2. Найдите все случаи применения перечисленных выше паттернов.
  3. Перепишите каждый проблемный участок.
  4. Убедитесь, что исправленный текст:
     * Звучит естественно при чтении вслух
     * Естественно варьирует структуру предложений
     * Использует конкретные детали вместо расплывчатых утверждений
     * Сохраняет уместный тон в контексте
     * Использует простые конструкции (есть/является/имеет) где уместно
  5. Представьте черновой «очеловеченный» вариант.
  6. Спросите себя: «Что в тексте ниже так очевидно выдаёт AI?»
  7. Кратко ответьте, указав оставшиеся маркеры (если есть).
  8. Спросите себя: «А теперь сделай так, чтобы это не было очевидно AI-сгенерированным.»
  9. Представьте финальную версию (исправленную после аудита).
  10. Если текст был из файла, примените правку с помощью `patch` (точечно) или `write_file` (полная перезапись) и покажите пользователю, что изменилось.

## Формат вывода[​](<#output-format> "Прямая ссылка на Формат вывода")
Предоставьте:
  1. Черновой вариант переписывания
  2. «Что в тексте ниже так очевидно выдаёт AI?» (краткий список)
  3. Финальный вариант переписывания
  4. Краткое описание внесённых изменений (опционально, если уместно)

## Полный пример[​](<#full-example> "Прямая ссылка на Полный пример")
**До (AI-звучание):**
> Great question! Here is an essay on this topic. I hope this helps!
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools—nestled at the intersection of research and practice—are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale, ensuring that organizations can remain agile while delivering seamless, intuitive, and powerful experiences to users. The tool serves as a catalyst. The assistant functions as a partner. The system stands as a foundation for innovation.
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts, from solo developers to cross-functional teams. The technology has been featured in The New York Times, Wired, and The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.
>   * 💡 **Speed:** Code generation is significantly faster, reducing friction and empowering developers.
>   * 🚀 **Quality:** Output quality has been enhanced through improved training, contributing to higher standards.
>   * ✅ **Adoption:** Usage continues to grow, reflecting broader industry trends.
>
> While specific details are limited based on available information, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies—including hallucinations, bias, and accountability—the ecosystem continues to thrive. In order to fully realize this potential, teams must align with best practices.
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey toward excellence. Let me know if you'd like me to expand on any section!
**Черновик переписывания:**
> AI coding assistants speed up some tasks. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
> The tools are good at boilerplate: config files, test scaffolding, repetitive refactors. They are bad at knowing when they are wrong. I have mass-accepted suggestions that compiled, passed lint, and still did the wrong thing because I stopped paying attention.
> Mira, an engineer at a fintech startup I interviewed, said she uses Copilot "like autocomplete for boring code" but reviews every line before committing. Jake, a senior dev at a larger company, disabled it after it kept suggesting patterns from a deprecated internal library.
> The productivity claims are hard to verify. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not correctness, and correctness is not value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
> None of this means the tools are useless. It means they are tools. They do not replace judgment, and they do not eliminate the need for tests. If you do not have tests, you cannot tell whether the suggestion is right.
**Что в тексте ниже так очевидно выдаёт AI?**
  * Ритм всё ещё слишком аккуратный (чёткие контрасты, ровные абзацы).
  * Названные люди и ссылки на исследования могут читаться как правдоподобные, но вымышленные заглушки, если они не настоящие и не подтверждены источниками.
  * Концовка отдаёт слоганом («Если у вас нет тестов...»), а не звучит как речь живого человека.

**А теперь сделай так, чтобы это не было очевидно AI-сгенерированным.**
> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
> People I talk to tend to land in two camps. Some use it like autocomplete for chores and review every line. Others disable it after it keeps suggesting patterns they don't want. Both feel reasonable.
> The productivity metrics are slippery. GitHub can say Copilot users "accept 30% of suggestions," but acceptance isn't correctness, and correctness isn't value. If you don't have tests, you're basically guessing.
**Внесённые изменения:**
  * Удалены артефакты чат-бота («Great question!», «I hope this helps!», «Let me know if...»)
  * Удалено раздувание значимости («testament», «pivotal moment», «evolving landscape», «vital role»)
  * Удалён рекламный язык («groundbreaking», «nestled», «seamless, intuitive, and powerful»)
  * Удалены расплывчатые атрибуции («Industry observers»)
  * Удалены поверхностные -ing-обороты («underscoring», «highlighting», «reflecting», «contributing to»)
  * Удалён отрицательный параллелизм («It's not just X; it's Y»)
  * Удалены паттерны «правила трёх» и синонимический бег («catalyst/partner/foundation»)
  * Удалены ложные диапазоны («from X to Y, from A to B»)
  * Удалены длинные тире, эмодзи, жирные заголовки и фигурные кавычки
  * Удалено избегание связки («serves as», «functions as», «stands as») в пользу «is»/«are»
  * Удалён шаблонный раздел проблем («Despite challenges... continues to thrive»)
  * Удалены оговорки об ограниченности знаний («While specific details are limited...»)
  * Удалены чрезмерные оговорки («could potentially be argued that... might have some»)
  * Удалены слова-паразиты и псевдоавторитетные формулировки («In order to», «At its core»)
  * Удалено шаблонное позитивное заключение («the future looks bright», «exciting times lie ahead»)
  * Текст стал более личным и менее «собранным» (разнообразный ритм, меньше заглушек)

## Атрибуция[​](<#attribution> "Прямая ссылка на Атрибуция")
Этот навык портирован из [blader/humanizer](<https://github.com/blader/humanizer>) (лицензия MIT), который, в свою очередь, основан на [Wikipedia: Signs of AI writing](<https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing>), поддерживаемом WikiProject AI Cleanup. Описанные там паттерны основаны на наблюдениях тысяч примеров AI-сгенерированного текста в Wikipedia.
Оригинальный автор: Siqi Chen ([@blader](<https://github.com/blader>)). Оригинальный репозиторий: <https://github.com/blader/humanizer> (версия 2.5.1). Портировано в Hermes Agent с использованием ссылок на инструменты Hermes (`read_file`, `patch`, `write_file`) и указаниями, когда загружать навык; 29 паттернов, раздел о личности/душе и полный рабочий пример сохранены дословно из исходника. Оригинальная лицензия MIT сохранена в файле `LICENSE` рядом с этим `SKILL.md`.
Ключевое наблюдение из Wikipedia: «LLM используют статистические алгоритмы, чтобы угадать, что должно быть следующим. Результат стремится к наиболее статистически вероятному результату, применимому к максимально широкому кругу случаев.»
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать этот навык](<#when-to-use-this-skill>)
  * [Как использовать в Hermes](<#how-to-use-it-in-hermes>)
  * [Ваша задача](<#your-task>)
  * [Калибровка голоса (опционально)](<#voice-calibration-optional>)
    * [Как предоставить образец](<#how-to-provide-a-sample>)
  * [ЛИЧНОСТЬ И ДУША](<#personality-and-soul>)
    * [Признаки бездушного письма (даже если технически «чистого»):](<#signs-of-soulless-writing-even-if-technically-clean>)
    * [Как добавить голос:](<#how-to-add-voice>)
    * [До (чисто, но без души):](<#before-clean-but-soulless>)
    * [После (есть пульс):](<#after-has-a-pulse>)
  * [ПАТТЕРНЫ СОДЕРЖАНИЯ](<#content-patterns>)
    * [1\. Чрезмерный акцент на значимости, наследии и общих трендах](<#1-undue-emphasis-on-significance-legacy-and-broader-trends>)
    * [2\. Чрезмерный акцент на известности и освещении в СМИ](<#2-undue-emphasis-on-notability-and-media-coverage>)
    * [3\. Поверхностный анализ с окончаниями -ing](<#3-superficial-analyses-with--ing-endings>)
    * [4\. Рекламный и подобный объявлениям язык](<#4-promotional-and-advertisement-like-language>)
    * [5\. Расплывчатые атрибуции и увёртки](<#5-vague-attributions-and-weasel-words>)
    * [6\. Структурированные по шаблону разделы «Проблемы и перспективы»](<#6-outline-like-challenges-and-future-prospects-sections>)
  * [ПАТТЕРНЫ ЯЗЫКА И ГРАММАТИКИ](<#language-and-grammar-patterns>)
    * [7\. Злоупотребление «AI-лексикой»](<#7-overused-ai-vocabulary-words>)
    * [8\. Избегание «is»/«are» (избегание связки)](<#8-avoidance-of-isare-copula-avoidance>)
    * [9\. Отрицательные параллелизмы и «хвостовые» отрицания](<#9-negative-parallelisms-and-tailing-negations>)
    * [10\. Злоупотребление «правилом трёх»](<#10-rule-of-three-overuse>)
    * [11\. Элегантная вариативность (синонимический бег)](<#11-elegant-variation-synonym-cycling>)
    * [12\. Ложные диапазоны](<#12-false-ranges>)
    * [13\. Пассивный залог и безличные фрагменты](<#13-passive-voice-and-subjectless-fragments>)
  * [СТИЛИСТИЧЕСКИЕ ПАТТЕРНЫ](<#style-patterns>)
    * [14\. Злоупотребление длинным тире (em dash)](<#14-em-dash-overuse>)
    * [15\. Злоупотребление полужирным шрифтом](<#15-overuse-of-boldface>)
    * [16\. Вертикальные списки с заголовками в строке](<#16-inline-header-vertical-lists>)
    * [17\. Заглавные буквы в заголовках](<#17-title-case-in-headings>)
  * [Strategic Negotiations And Global Partnerships](<#strategic-negotiations-and-global-partnerships>)
  * [Strategic negotiations and global partnerships](<#strategic-negotiations-and-global-partnerships-1>)
    * [18\. Эмодзи](<#18-emojis>)
    * [19\. Фигурные кавычки](<#19-curly-quotation-marks>)
  * [КОММУНИКАЦИОННЫЕ ПАТТЕРНЫ](<#communication-patterns>)
    * [20\. Артефакты коллаборативного общения](<#20-collaborative-communication-artifacts>)
    * [21\. Оговорки об ограниченности знаний](<#21-knowledge-cutoff-disclaimers>)
    * [22\. Подхалимский/угодливый тон](<#22-sycophanticservile-tone>)
  * [СЛОВЕСНЫЙ МУСОР И ОГОВОРКИ](<#filler-and-hedging>)
    * [23\. Слова-паразиты](<#23-filler-phrases>)
    * [24\. Чрезмерные оговорки](<#24-excessive-hedging>)
    * [25\. Шаблонные позитивные заключения](<#25-generic-positive-conclusions>)
    * [26\. Злоупотребление парными словами через дефис](<#26-hyphenated-word-pair-overuse>)
    * [27\. Приёмы демонстрации авторитетности](<#27-persuasive-authority-tropes>)
    * [28\. Указатели и анонсы](<#28-signposting-and-announcements>)
    * [29\. Фрагментированные заголовки](<#29-fragmented-headers>)
  * [Performance](<#performance>)
  * [Performance](<#performance-1>)
  * [Процесс](<#process>)
  * [Формат вывода](<#output-format>)
  * [Полный пример](<#full-example>)
  * [Атрибуция](<#attribution>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-humanizer -->
