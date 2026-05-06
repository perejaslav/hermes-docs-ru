On this page
Планировщик тренировок в зале и трекер питания. Поиск 690+ упражнений по мышцам, оборудованию или категориям через wger. Просмотр макронутриентов и калорий для 380 000+ продуктов через USDA FoodData Central. Расчёт ИМТ, TDEE, максимума на одно повторение, распределения макронутриентов и процента жира в теле — чистый Python, без pip-установок. Создан для тех, кто стремится к росту мышц, худеет или просто пытается питаться лучше.
## Skill metadata[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")
|   |
|---|---|
|Source| Опциональный — установка: `hermes skills install official/health/fitness-nutrition` |
|Path| `optional-skills/health/fitness-nutrition` |
|Version| `1.0.0` |
|License| MIT |
|Tags| `health`, `fitness`, `nutrition`, `gym`, `workout`, `diet`, `exercise` |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Агент видит эти инструкции, когда навык активен.
# Fitness & Nutrition
Навык экспертного фитнес-тренера и спортивного диетолога. Два источника данных плюс офлайн-калькуляторы — всё, что нужно посетителю спортзала, в одном месте.
**Data sources (all free, no pip dependencies):**
  * **wger** (<https://wger.de/api/v2/>) — открытая база упражнений, 690+ упражнений с указанием мышц, оборудования и изображений. Публичным конечным точкам не требуется аутентификация.
  * **USDA FoodData Central** (<https://api.nal.usda.gov/fdc/v1/>) — правительственная база данных по питанию США, 380 000+ продуктов. `DEMO_KEY` работает сразу; бесплатная регистрация для более высоких лимитов.


**Offline calculators (pure stdlib Python):**
  * ИМТ, TDEE (Mifflin-St Jeor), максимум на одно повторение (Epley/Brzycki/Lombardi), распределение макронутриентов, процент жира в теле (метод ВМС США)


* * *
## When to Use[​](<#when-to-use> "Прямая ссылка на When to Use")
Активируйте этот навык, когда пользователь спрашивает о:
  * Упражнениях, тренировках, программах в зале, группах мышц, сплитах тренировок
  * Макронутриентах продуктов, калориях, содержании белка, планировании питания, подсчёте калорий
  * Составе тела: ИМТ, процент жира, TDEE, избыток/дефицит калорий
  * Оценке максимума на одно повторение, тренировочных процентах, прогрессивной перегрузке
  * Соотношении макронутриентов для сушки, набора массы или поддержания формы


* * *
## Procedure[​](<#procedure> "Прямая ссылка на Procedure")
### Exercise Lookup (wger API)[​](<#exercise-lookup-wger-api> "Прямая ссылка на Exercise Lookup (wger API)")
Все публичные конечные точки wger возвращают JSON и не требуют аутентификации. Всегда добавляйте `format=json` и `language=2` (английский) в запросы упражнений.
**Step 1 — Identify what the user wants:**
  * По мышцам → используйте `/api/v2/exercise/?muscles={id}&language=2&status=2&format=json`
  * По категории → используйте `/api/v2/exercise/?category={id}&language=2&status=2&format=json`
  * По оборудованию → используйте `/api/v2/exercise/?equipment={id}&language=2&status=2&format=json`
  * По названию → используйте `/api/v2/exercise/search/?term={query}&language=english&format=json`
  * Полные детали → используйте `/api/v2/exerciseinfo/{exercise_id}/?format=json`


**Step 2 — Reference IDs (so you don't need extra API calls):**
Категории упражнений:
ID| Категория  
---|---  
8| Arms (Руки)  
9| Legs (Ноги)  
10| Abs (Пресс)  
11| Chest (Грудь)  
12| Back (Спина)  
13| Shoulders (Плечи)  
14| Calves (Икры)  
15| Cardio (Кардио)  
Мышцы:
ID| Мышца| ID| Мышца  
---|---|---|---  
1| Biceps brachii (Двуглавая)| 2| Anterior deltoid (Передняя дельтовидная)  
3| Serratus anterior (Передняя зубчатая)| 4| Pectoralis major (Большая грудная)  
5| Obliquus externus (Наружная косая)| 6| Gastrocnemius (Икроножная)  
7| Rectus abdominis (Прямая живота)| 8| Gluteus maximus (Большая ягодичная)  
9| Trapezius (Трапециевидная)| 10| Quadriceps femoris (Четырёхглавая бедра)  
11| Biceps femoris (Двуглавая бедра)| 12| Latissimus dorsi (Широчайшая спины)  
13| Brachialis (Плечевая)| 14| Triceps brachii (Трёхглавая)  
15| Soleus (Камбаловидная)| |   
Оборудование:
ID| Оборудование  
---|---  
1| Barbell (Штанга)  
3| Dumbbell (Гантель)  
4| Gym mat (Коврик)  
5| Swiss Ball (Фитбол)  
6| Pull-up bar (Турник)  
7| none (bodyweight) (без оборудования / вес тела)  
8| Bench (Скамья)  
9| Incline bench (Наклонная скамья)  
10| Kettlebell (Гиря)  
**Step 3 — Fetch and present results:**
[code] 
    # Search exercises by name  
    QUERY="$1"  
    ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")  
    curl -s "https://wger.de/api/v2/exercise/search/?term=${ENCODED}&language=english&format=json" \
      | python3 -c "  
    import json,sys  
    data=json.load(sys.stdin)  
    for s in data.get('suggestions',[])[:10]:  
        d=s.get('data',{})  
        print(f\"  ID {d.get('id','?'):>4} | {d.get('name','N/A'):<35} | Category: {d.get('category','N/A')}\")  
    "  
    
[/code]
[code] 
    # Get full details for a specific exercise  
    EXERCISE_ID="$1"  
    curl -s "https://wger.de/api/v2/exerciseinfo/${EXERCISE_ID}/?format=json" \
      | python3 -c "  
    import json,sys,html,re  
    data=json.load(sys.stdin)  
    trans=[t for t in data.get('translations',[]) if t.get('language')==2]  
    t=trans[0] if trans else data.get('translations',[{}])[0]  
    desc=re.sub('<[^>]+>','',html.unescape(t.get('description','N/A')))  
    print(f\"Exercise  : {t.get('name','N/A')}\")  
    print(f\"Category  : {data.get('category',{}).get('name','N/A')}\")  
    print(f\"Primary   : {', '.join(m.get('name_en','') for m in data.get('muscles',[])) or 'N/A'}\")  
    print(f\"Secondary : {', '.join(m.get('name_en','') for m in data.get('muscles_secondary',[])) or 'none'}\")  
    print(f\"Equipment : {', '.join(e.get('name','') for e in data.get('equipment',[])) or 'bodyweight'}\")  
    print(f\"How to    : {desc[:500]}\")  
    imgs=data.get('images',[])  
    if imgs: print(f\"Image     : {imgs[0].get('image','')}\")  
    "  
    
[/code]
[code] 
    # List exercises filtering by muscle, category, or equipment  
    # Combine filters as needed: ?muscles=4&equipment=1&language=2&status=2  
    FILTER="$1"  # e.g. "muscles=4" or "category=11" or "equipment=3"  
    curl -s "https://wger.de/api/v2/exercise/?${FILTER}&language=2&status=2&limit=20&format=json" \
      | python3 -c "  
    import json,sys  
    data=json.load(sys.stdin)  
    print(f'Found {data.get(\"count\",0)} exercises.')  
    for ex in data.get('results',[]):  
        print(f\"  ID {ex['id']:>4} | muscles: {ex.get('muscles',[])} | equipment: {ex.get('equipment',[])}\")  
    "  
    
[/code]
### Nutrition Lookup (USDA FoodData Central)[​](<#nutrition-lookup-usda-fooddata-central> "Прямая ссылка на Nutrition Lookup (USDA FoodData Central)")
Использует переменную окружения `USDA_API_KEY`, если она установлена, иначе `DEMO_KEY`. DEMO_KEY = 30 запросов/час. Ключ бесплатной регистрации = 1 000 запросов/час.
[code] 
    # Search foods by name  
    FOOD="$1"  
    API_KEY="${USDA_API_KEY:-DEMO_KEY}"  
    ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$FOOD")  
    curl -s "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=${API_KEY}&query=${ENCODED}&pageSize=5&dataType=Foundation,SR%20Legacy" \
      | python3 -c "  
    import json,sys  
    data=json.load(sys.stdin)  
    foods=data.get('foods',[])  
    if not foods: print('No foods found.'); sys.exit()  
    for f in foods:  
        n={x['nutrientName']:x.get('value','?') for x in f.get('foodNutrients',[])}  
        cal=n.get('Energy','?'); prot=n.get('Protein','?')  
        fat=n.get('Total lipid (fat)','?'); carb=n.get('Carbohydrate, by difference','?')  
        print(f\"{f.get('description','N/A')}\")  
        print(f\"  Per 100g: {cal} kcal | {prot}g protein | {fat}g fat | {carb}g carbs\")  
        print(f\"  FDC ID: {f.get('fdcId','N/A')}\")  
        print()  
    "  
    
[/code]
[code] 
    # Detailed nutrient profile by FDC ID  
    FDC_ID="$1"  
    API_KEY="${USDA_API_KEY:-DEMO_KEY}"  
    curl -s "https://api.nal.usda.gov/fdc/v1/food/${FDC_ID}?api_key=${API_KEY}" \
      | python3 -c "  
    import json,sys  
    d=json.load(sys.stdin)  
    print(f\"Food: {d.get('description','N/A')}\")  
    print(f\"{'Nutrient':<40} {'Amount':>8} {'Unit'}\")  
    print('-'*56)  
    for x in sorted(d.get('foodNutrients',[]),key=lambda x:x.get('nutrient',{}).get('rank',9999)):  
        nut=x.get('nutrient',{}); amt=x.get('amount',0)  
        if amt and float(amt)>0:  
            print(f\"  {nut.get('name',''):<38} {amt:>8} {nut.get('unitName','')}\")  
    "  
    
[/code]
### Offline Calculators[​](<#offline-calculators> "Прямая ссылка на Offline Calculators")
Используйте вспомогательные скрипты в `scripts/` для пакетных операций или запускайте inline для одиночных расчётов:
  * `python3 scripts/body_calc.py bmi <weight_kg> <height_cm>`
  * `python3 scripts/body_calc.py tdee <weight_kg> <height_cm> <age> <M|F> <activity 1-5>`
  * `python3 scripts/body_calc.py 1rm <weight> <reps>`
  * `python3 scripts/body_calc.py macros <tdee_kcal> <cut|maintain|bulk>`
  * `python3 scripts/body_calc.py bodyfat <M|F> <neck_cm> <waist_cm> [hip_cm] <height_cm>`


См. `references/FORMULAS.md` для научного обоснования каждой формулы.
* * *
## Pitfalls[​](<#pitfalls> "Прямая ссылка на Pitfalls")
  * Конечная точка упражнений wger возвращает **все языки по умолчанию** — всегда добавляйте `language=2` для английского
  * wger включает **непроверенные пользовательские материалы** — добавляйте `status=2`, чтобы получать только утверждённые упражнения
  * USDA `DEMO_KEY` имеет лимит **30 запросов/час** — добавляйте `sleep 2` между пакетными запросами или получите бесплатный ключ
  * Данные USDA приведены **на 100 г** — напоминайте пользователям масштабировать до их реального размера порции
  * ИМТ не различает мышцы и жир — высокий ИМТ у мускулистых людей не обязательно указывает на проблемы со здоровьем
  * Формулы процента жира являются **приблизительными** (±3–5%) — рекомендуйте DEXA-сканирование для точности
  * Формулы 1RM теряют точность при более 10 повторений — используйте подходы по 3–5 повторений для наилучшей оценки
  * Конечная точка `exercise/search` wger использует `term`, а не `query` в качестве имени параметра


* * *
## Verification[​](<#verification> "Прямая ссылка на Verification")
После поиска упражнений: проверьте, что результаты включают названия упражнений, группы мышц и оборудование. После просмотра питания: проверьте, что макронутриенты на 100 г возвращаются с указанием ккал, белка, жиров, углеводов. После калькуляторов: проверьте outputs на адекватность (например, TDEE должен быть 1500–3500 для большинства взрослых).
* * *
## Quick Reference[​](<#quick-reference> "Прямая ссылка на Quick Reference")
Задача| Источник| Конечная точка  
---|---|---  
Поиск упражнений по названию| wger| `GET /api/v2/exercise/search/?term=&language=english`  
Детали упражнения| wger| `GET /api/v2/exerciseinfo/{id}/`  
Фильтр по мышцам| wger| `GET /api/v2/exercise/?muscles={id}&language=2&status=2`  
Фильтр по оборудованию| wger| `GET /api/v2/exercise/?equipment={id}&language=2&status=2`  
Список категорий| wger| `GET /api/v2/exercisecategory/`  
Список мышц| wger| `GET /api/v2/muscle/`  
Поиск продуктов| USDA| `GET /fdc/v1/foods/search?query=&dataType=Foundation,SR Legacy`  
Детали продукта| USDA| `GET /fdc/v1/food/{fdcId}`  
ИМТ / TDEE / 1RM / макронутриенты| офлайн| `python3 scripts/body_calc.py`  
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Procedure](<#procedure>)
    * [Exercise Lookup (wger API)](<#exercise-lookup-wger-api>)
    * [Nutrition Lookup (USDA FoodData Central)](<#nutrition-lookup-usda-fooddata-central>)
    * [Offline Calculators](<#offline-calculators>)
  * [Pitfalls](<#pitfalls>)
  * [Verification](<#verification>)
  * [Quick Reference](<#quick-reference>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/health/health-fitness-nutrition -->
