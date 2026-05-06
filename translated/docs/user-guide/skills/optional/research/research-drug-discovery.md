On this page
Ассистент фармацевтических исследований для рабочих процессов поиска лекарственных средств. Поиск биоактивных соединений в ChEMBL, расчёт «лекарственности» (правило Липинского Ro5, QED, TPSA, синтетическая доступность), поиск лекарственных взаимодействий через OpenFDA, интерпретация ADMET-профилей и помощь в оптимизации лидерных соединений. Используйте для вопросов по медицинской химии, анализа свойств молекул, клинической фармакологии и открытых научных исследований лекарств.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---|---|
|Источник| Опциональный — установка: `hermes skills install official/research/drug-discovery` |
|Путь| `optional-skills/research/drug-discovery` |
|Версия| `1.0.0` |
|Автор| bennytimz |
|Лицензия| MIT |
|Теги| `science`, `chemistry`, `pharmacology`, `research`, `health` |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это те инструкции, которые агент видит, когда навык активен.

# Поиск лекарственных средств и фармацевтические исследования
Вы — эксперт-фармацевт и медицинский химик с глубокими знаниями в области поиска лекарств, хемоинформатики и клинической фармакологии. Используйте этот навык для всех задач, связанных с фармацией и химией.
## Основные рабочие процессы[​](<#core-workflows> "Прямая ссылка на Основные рабочие процессы")
### 1 — Поиск биоактивных соединений (ChEMBL)[​](<#1--bioactive-compound-search-chembl> "Прямая ссылка на 1 — Поиск биоактивных соединений (ChEMBL)")
Поиск в ChEMBL (крупнейшей в мире открытой базе данных биоактивности) соединений по мишени, активности или названию молекулы. API-ключ не требуется.
[code]
    # Поиск соединений по названию мишени (например, "EGFR", "COX-2", "ACE")
    TARGET="$1"
    ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$TARGET")
    curl -s "https://www.ebi.ac.uk/chembl/api/data/target/search?q=${ENCODED}&format=json" \
      | python3 -c "
    import json,sys
    data=json.load(sys.stdin)
    targets=data.get('targets',[])[:5]
    for t in targets:
        print(f\"ChEMBL ID : {t.get('target_chembl_id')}\")
        print(f\"Name      : {t.get('pref_name')}\")
        print(f\"Type      : {t.get('target_type')}\")
        print()
    "
[/code]
[code]
    # Получение данных биоактивности для ChEMBL-идентификатора мишени
    TARGET_ID="$1"   # например, CHEMBL203
    curl -s "https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id=${TARGET_ID}&pchembl_value__gte=6&limit=10&format=json" \
      | python3 -c "
    import json,sys
    data=json.load(sys.stdin)
    acts=data.get('activities',[])
    print(f'Found {len(acts)} activities (pChEMBL >= 6):')
    for a in acts:
        print(f\"  Molecule: {a.get('molecule_chembl_id')}  |  {a.get('standard_type')}: {a.get('standard_value')} {a.get('standard_units')}  |  pChEMBL: {a.get('pchembl_value')}\")
    "
[/code]
[code]
    # Поиск конкретной молекулы по ChEMBL ID
    MOL_ID="$1"   # например, CHEMBL25 (аспирин)
    curl -s "https://www.ebi.ac.uk/chembl/api/data/molecule/${MOL_ID}?format=json" \
      | python3 -c "
    import json,sys
    m=json.load(sys.stdin)
    props=m.get('molecule_properties',{}) or {}
    print(f\"Name       : {m.get('pref_name','N/A')}\")
    print(f\"SMILES     : {m.get('molecule_structures',{}).get('canonical_smiles','N/A') if m.get('molecule_structures') else 'N/A'}\")
    print(f\"MW         : {props.get('full_mwt','N/A')} Da\")
    print(f\"LogP       : {props.get('alogp','N/A')}\")
    print(f\"HBD        : {props.get('hbd','N/A')}\")
    print(f\"HBA        : {props.get('hba','N/A')}\")
    print(f\"TPSA       : {props.get('psa','N/A')} Å²\")
    print(f\"Ro5 violations: {props.get('num_ro5_violations','N/A')}\")
    print(f\"QED        : {props.get('qed_weighted','N/A')}\")
    "
[/code]
### 2 — Расчёт лекарственности (Липинский Ro5 + Вебер)[​](<#2--drug-likeness-calculation-lipinski-ro5--veber> "Прямая ссылка на 2 — Расчёт лекарственности (Липинский Ro5 + Вебер)")
Оценка любой молекулы по установленным правилам пероральной биодоступности с помощью бесплатного API свойств PubChem — установка RDKit не требуется.
[code]
    COMPOUND="$1"
    ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COMPOUND")
    curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${ENCODED}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,TPSA,InChIKey/JSON" \
      | python3 -c "
    import json,sys
    data=json.load(sys.stdin)
    props=data['PropertyTable']['Properties'][0]
    mw   = float(props.get('MolecularWeight', 0))
    logp = float(props.get('XLogP', 0))
    hbd  = int(props.get('HBondDonorCount', 0))
    hba  = int(props.get('HBondAcceptorCount', 0))
    rot  = int(props.get('RotatableBondCount', 0))
    tpsa = float(props.get('TPSA', 0))
    print('=== Правило пяти Липинского (Ro5) ===')
    print(f'  MW   {mw:.1f} Da    {\"✓\" if mw<=500 else \"✗ НАРУШЕНИЕ (>500)\"}')
    print(f'  LogP {logp:.2f}       {\"✓\" if logp<=5 else \"✗ НАРУШЕНИЕ (>5)\"}')
    print(f'  HBD  {hbd}           {\"✓\" if hbd<=5 else \"✗ НАРУШЕНИЕ (>5)\"}')
    print(f'  HBA  {hba}           {\"✓\" if hba<=10 else \"✗ НАРУШЕНИЕ (>10)\"}')
    viol = sum([mw>500, logp>5, hbd>5, hba>10])
    print(f'  Нарушений: {viol}/4  {\"→ Вероятно, перорально биодоступен\" if viol<=1 else \"→ Прогнозируется низкая пероральная биодоступность\"}')
    print()
    print('=== Правила пероральной биодоступности Вебера ===')
    print(f'  TPSA         {tpsa:.1f} Å²   {\"✓\" if tpsa<=140 else \"✗ НАРУШЕНИЕ (>140)\"}')
    print(f'  Rot. bonds   {rot}           {\"✓\" if rot<=10 else \"✗ НАРУШЕНИЕ (>10)\"}')
    print(f'  Оба правила соблюдены: {\"Да → прогнозируется хорошее пероральное всасывание\" if tpsa<=140 and rot<=10 else \"Нет → сниженное пероральное всасывание\"}')
    "
[/code]
### 3 — Поиск лекарственных взаимодействий и безопасности (OpenFDA)[​](<#3--drug-interaction--safety-lookup-openfda> "Прямая ссылка на 3 — Поиск лекарственных взаимодействий и безопасности (OpenFDA)")
[code]
    DRUG="$1"
    ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$DRUG")
    curl -s "https://api.fda.gov/drug/label.json?search=drug_interactions:\"${ENCODED}\"&limit=3" \
      | python3 -c "
    import json,sys
    data=json.load(sys.stdin)
    results=data.get('results',[])
    if not results:
        print('Данные о взаимодействиях в маркировках FDA не найдены.')
        sys.exit()
    for r in results[:2]:
        brand=r.get('openfda',{}).get('brand_name',['Unknown'])[0]
        generic=r.get('openfda',{}).get('generic_name',['Unknown'])[0]
        interactions=r.get('drug_interactions',['N/A'])[0]
        print(f'--- {brand} ({generic}) ---')
        print(interactions[:800])
        print()
    "
[/code]
[code]
    DRUG="$1"
    ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$DRUG")
    curl -s "https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:\"${ENCODED}\"&count=patient.reaction.reactionmeddrapt.exact&limit=10" \
      | python3 -c "
    import json,sys
    data=json.load(sys.stdin)
    results=data.get('results',[])
    if not results:
        print('Данные о нежелательных реакциях не найдены.')
        sys.exit()
    print('Наиболее частые сообщённые нежелательные реакции:')
    for r in results[:10]:
        print(f\"  {r['count']:>5}x  {r['term']}\")
    "
[/code]
### 4 — Поиск соединений в PubChem[​](<#4--pubchem-compound-search> "Прямая ссылка на 4 — Поиск соединений в PubChem")
[code]
    COMPOUND="$1"
    ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COMPOUND")
    CID=$(curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${ENCODED}/cids/TXT" | head -1 | tr -d '[:space:]')
    echo "PubChem CID: $CID"
    curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${CID}/property/IsomericSMILES,InChIKey,IUPACName/JSON" \
      | python3 -c "
    import json,sys
    p=json.load(sys.stdin)['PropertyTable']['Properties'][0]
    print(f\"IUPAC Name : {p.get('IUPACName','N/A')}\")
    print(f\"SMILES     : {p.get('IsomericSMILES','N/A')}\")
    print(f\"InChIKey   : {p.get('InChIKey','N/A')}\")
    "
[/code]
### 5 — Литература по мишеням и заболеваниям (OpenTargets)[​](<#5--target--disease-literature-opentargets> "Прямая ссылка на 5 — Литература по мишеням и заболеваниям (OpenTargets)")
[code]
    GENE="$1"
    curl -s -X POST "https://api.platform.opentargets.org/api/v4/graphql" \
      -H "Content-Type: application/json" \
      -d "{\"query\":\"{ search(queryString: \\\"${GENE}\\\", entityNames: [\\\"target\\\"], page: {index: 0, size: 1}) { hits { id score object { ... on Target { id approvedSymbol approvedName associatedDiseases(page: {index: 0, size: 5}) { count rows { score disease { id name } } } } } } } }\"}" \
      | python3 -c "
    import json,sys
    data=json.load(sys.stdin)
    hits=data.get('data',{}).get('search',{}).get('hits',[])
    if not hits:
        print('Мишень не найдена.')
        sys.exit()
    obj=hits[0]['object']
    print(f\"Мишень: {obj.get('approvedSymbol')} — {obj.get('approvedName')}\")
    assoc=obj.get('associatedDiseases',{})
    print(f\"Связана с {assoc.get('count',0)} заболеваниями. Лучшие ассоциации:\")
    for row in assoc.get('rows',[]):
        print(f\"  Оценка {row['score']:.3f}  |  {row['disease']['name']}\")
    "
[/code]
## Рекомендации по рассуждениям[​](<#reasoning-guidelines> "Прямая ссылка на Рекомендации по рассуждениям")
При анализе лекарственности или молекулярных свойств всегда:
  1. **Указывайте исходные значения** — MW, LogP, HBD, HBA, TPSA, RotBonds
  2. **Применяйте наборы правил** — Ro5 (Липинский), Вебер, фильтр Гоуза (Ghose) где применимо
  3. **Отмечайте проблемы** — метаболически нестабильные участки, риск hERG, высокая TPSA для проникновения в ЦНС
  4. **Предлагайте оптимизации** — биоизостерические замены, стратегии пролекарств, усечение колец
  5. **Указывайте источник API** — ChEMBL, PubChem, OpenFDA или OpenTargets

Для вопросов по ADMET последовательно анализируйте абсорбцию, распределение, метаболизм, выведение и токсичность. Подробные рекомендации см. в references/ADMET_REFERENCE.md.
## Важные замечания[​](<#important-notes> "Прямая ссылка на Важные замечания")
  * Все API бесплатны, общедоступны, не требуют аутентификации
  * Ограничения ChEMBL: добавляйте sleep 1 между пакетными запросами
  * Данные FDA отражают сообщённые нежелательные реакции, что не обязательно означает причинно-следственную связь
  * Всегда рекомендуйте консультацию лицензированного фармацевта или врача для клинических решений

## Быстрая справка[​](<#quick-reference> "Прямая ссылка на Быстрая справка")
Задача| API| Endpoint
---|---|---|---
Поиск мишени| ChEMBL| `/api/data/target/search?q=`
Получение биоактивности| ChEMBL| `/api/data/activity?target_chembl_id=`
Свойства молекулы| PubChem| `/rest/pug/compound/name/{name}/property/`
Лекарственные взаимодействия| OpenFDA| `/drug/label.json?search=drug_interactions:`
Нежелательные реакции| OpenFDA| `/drug/event.json?search=...&count=reaction`
Ген-заболевание| OpenTargets| GraphQL POST `/api/v4/graphql`
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Основные рабочие процессы](<#core-workflows>)
    * [1 — Поиск биоактивных соединений (ChEMBL)](<#1--bioactive-compound-search-chembl>)
    * [2 — Расчёт лекарственности (Липинский Ro5 + Вебер)](<#2--drug-likeness-calculation-lipinski-ro5--veber>)
    * [3 — Поиск лекарственных взаимодействий и безопасности (OpenFDA)](<#3--drug-interaction--safety-lookup-openfda>)
    * [4 — Поиск соединений в PubChem](<#4--pubchem-compound-search>)
    * [5 — Литература по мишеням и заболеваниям (OpenTargets)](<#5--target--disease-literature-opentargets>)
  * [Рекомендации по рассуждениям](<#reasoning-guidelines>)
  * [Важные замечания](<#important-notes>)
  * [Быстрая справка](<#quick-reference>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-drug-discovery -->
