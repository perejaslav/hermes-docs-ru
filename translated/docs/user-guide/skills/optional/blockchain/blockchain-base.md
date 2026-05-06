На этой странице

Запрашивайте данные блокчейна Base (L2 Ethereum) с ценами в USD — балансы кошельков, информацию о токенах, детали транзакций, анализ газа, проверку контрактов, обнаружение крупных транзакций («китов») и статистику сети в реальном времени. Использует Base RPC + CoinGecko. API-ключ не требуется.

## Метаданные навыка[​](<#skill-metadata> "Direct link to Skill metadata")

|   |
|---|
| Источник | Опционально — установка: `hermes skills install official/blockchain/base` |
| Путь | `optional-skills/blockchain/base` |
| Версия | `0.1.0` |
| Автор | youssefea |
| Лицензия | MIT |
| Теги | `Base`, `Blockchain`, `Crypto`, `Web3`, `RPC`, `DeFi`, `EVM`, `L2`, `Ethereum` |

## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")

info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.

# Навык «Base Blockchain»

Запрашивайте данные блокчейна Base (L2 Ethereum) с ценами в USD через CoinGecko. 8 команд: портфель кошелька, информация о токене, транзакции, анализ газа, проверка контракта, обнаружение «китов», статистика сети и поиск цен.

API-ключ не требуется. Использует только стандартную библиотеку Python (urllib, json, argparse).

* * *

## Когда использовать[​](<#when-to-use> "Direct link to When to Use")

  * Пользователь запрашивает баланс кошелька Base, его токены или стоимость портфеля
  * Пользователь хочет проверить конкретную транзакцию по хешу
  * Пользователь хочет получить метаданные ERC-20 токена, цену, эмиссию или рыночную капитализацию
  * Пользователь хочет понять стоимость газа на Base и комиссии за данные L1
  * Пользователь хочет проверить контракт (определение типа ERC, разрешение прокси)
  * Пользователь хочет найти крупные переводы ETH (обнаружение «китов»)
  * Пользователь хочет узнать состояние сети Base, цену газа или цену ETH
  * Пользователь спрашивает «какая цена USDC/AERO/DEGEN/ETH?»

* * *

## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")

Вспомогательный скрипт использует только стандартную библиотеку Python (urllib, json, argparse). Внешние пакеты не требуются.

Данные о ценах поступают из бесплатного API CoinGecko (ключ не нужен, ограничение — ~10-30 запросов/мин). Для более быстрых запросов используйте флаг `--no-prices`.

* * *

## Краткая справка[​](<#quick-reference> "Direct link to Quick Reference")

RPC-эндпоинт (по умолчанию): https://mainnet.base.org
Переопределение: export BASE_RPC_URL=https://your-private-rpc.com

Путь к вспомогательному скрипту: ~/.hermes/skills/blockchain/base/scripts/base_client.py

[code] 
    python3 base_client.py wallet   <address> [--limit N] [--all] [--no-prices]  
    python3 base_client.py tx       <hash>  
    python3 base_client.py token    <contract_address>  
    python3 base_client.py gas  
    python3 base_client.py contract <address>  
    python3 base_client.py whales   [--min-eth N]  
    python3 base_client.py stats  
    python3 base_client.py price    <contract_address_or_symbol>  
    
[/code]

* * *

## Процедура[​](<#procedure> "Direct link to Procedure")

### 0\\. Проверка настройки[​](<#0-setup-check> "Direct link to 0. Setup Check")

[code] 
    python3 --version  
      
    # Опционально: установите приватный RPC для лучших лимитов  
    export BASE_RPC_URL="https://mainnet.base.org"  
      
    # Проверьте подключение  
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py stats  
    
[/code]

### 1\\. Портфель кошелька[​](<#1-wallet-portfolio> "Direct link to 1. Wallet Portfolio")

Получите баланс ETH и информацию о ERC-20 токенах со стоимостью в USD. Проверяет ~15 известных токенов Base (USDC, WETH, AERO, DEGEN и др.) через on-chain вызовы `balanceOf`. Токены отсортированы по стоимости, мелкие суммы отфильтрованы.

[code] 
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py \  
      wallet 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045  
    
[/code]

Флаги:

  * `--limit N` — показать топ N токенов (по умолчанию: 20)
  * `--all` — показать все токены, без фильтрации мелких сумм и лимита
  * `--no-prices` — пропустить запросы цен к CoinGecko (быстрее, только RPC)

Вывод включает: баланс ETH + стоимость в USD, список токенов с ценами, отсортированный по стоимости, количество отфильтрованных мелких сумм, общую стоимость портфеля в USD.

Примечание: проверяются только известные токены. Неизвестные ERC-20 не обнаруживаются. Используйте команду `token` с конкретным адресом контракта для любого токена.

### 2\\. Детали транзакции[​](<#2-transaction-details> "Direct link to 2. Transaction Details")

Проверьте полную транзакцию по её хешу. Показывает переведённую сумму ETH, использованный газ, комиссию в ETH/USD, статус и декодированные переводы ERC-20/ERC-721.

[code] 
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py \  
      tx 0xabc123...your_tx_hash_here  
    
[/code]

Вывод: хеш, блок, отправитель, получатель, сумма (ETH + USD), цена газа, использованный газ, комиссия, статус, адрес созданного контракта (если есть), переводы токенов.

### 3\\. Информация о токене[​](<#3-token-info> "Direct link to 3. Token Info")

Получите метаданные ERC-20 токена: название, символ, десятичные знаки, общую эмиссию, цену, рыночную капитализацию и размер кода контракта.

[code] 
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py \  
      token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913  
    
[/code]

Вывод: название, символ, десятичные знаки, общая эмиссия, цена, рыночная капитализация. Читает название/символ/десятичные знаки напрямую из контракта через eth_call.

### 4\\. Анализ газа[​](<#4-gas-analysis> "Direct link to 4. Gas Analysis")

Детальный анализ газа с оценкой стоимости для типичных операций. Показывает текущую цену газа, тренд базовой комиссии за 10 блоков, загрузку блоков и примерную стоимость переводов ETH, ERC-20 и свопов.

[code] 
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py gas  
    
[/code]

Вывод: текущая цена газа, базовая комиссия, загрузка блоков, тренд за 10 блоков, оценки стоимости в ETH и USD.

Примечание: Base — это L2, поэтому фактические затраты на транзакцию включают комиссию за публикацию данных L1, которая зависит от размера calldata и цен газа L1. Приведённые оценки касаются только выполнения на L2.

### 5\\. Проверка контракта[​](<#5-contract-inspection> "Direct link to 5. Contract Inspection")

Проверьте адрес: определите, является ли он EOA или контрактом, обнаружьте интерфейсы ERC-20/ERC-721/ERC-1155, получите адрес реализации прокси EIP-1967.

[code] 
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py \  
      contract 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913  
    
[/code]

Вывод: is_contract, размер кода, баланс ETH, обнаруженные интерфейсы (ERC-20, ERC-721, ERC-1155), метаданные ERC-20, адрес реализации прокси.

### 6\\. Обнаружение «китов»[​](<#6-whale-detector> "Direct link to 6. Whale Detector")

Сканирование последнего блока на предмет крупных переводов ETH со стоимостью в USD.

[code] 
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py \  
      whales --min-eth 1.0  
    
[/code]

Примечание: сканируется только последний блок — мгновенный снимок, не исторический. Порог по умолчанию — 1.0 ETH (ниже, чем у Solana, так как стоимость ETH выше).

### 7\\. Статистика сети[​](<#7-network-stats> "Direct link to 7. Network Stats")

Состояние сети Base в реальном времени: последний блок, идентификатор цепи, цена газа, базовая комиссия, загрузка блоков, количество транзакций и цена ETH.

[code] 
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py stats  
    
[/code]

### 8\\. Поиск цены[​](<#8-price-lookup> "Direct link to 8. Price Lookup")

Быстрая проверка цены любого токена по адресу контракта или известному символу.

[code] 
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py price ETH  
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py price USDC  
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py price AERO  
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py price DEGEN  
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py price 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913  
    
[/code]

Известные символы: ETH, WETH, USDC, cbETH, AERO, DEGEN, TOSHI, BRETT, WELL, wstETH, rETH, cbBTC.

* * *

## Возможные проблемы[​](<#pitfalls> "Direct link to Pitfalls")

  * **Лимиты CoinGecko** — бесплатный тариф позволяет ~10-30 запросов/мин. Поиск цен использует 1 запрос на токен. Используйте `--no-prices` для ускорения.
  * **Лимиты публичного RPC** — публичный RPC Base ограничивает запросы. Для промышленного использования установите BASE_RPC_URL на приватный эндпоинт (Alchemy, QuickNode, Infura).
  * **Кошелёк показывает только известные токены** — в отличие от Solana, в EVM-цепочках нет встроенного RPC-метода «получить все токены». Команда wallet проверяет ~15 популярных токенов Base через `balanceOf`. Неизвестные ERC-20 не отображаются. Используйте команду `token` для конкретного контракта.
  * **Названия токенов читаются из контракта** — если контракт не реализует `name()` или `symbol()`, эти поля могут быть пустыми. Для известных токенов предусмотрены жёстко заданные названия как запасной вариант.
  * **Оценки газа только для L2** — стоимость транзакций Base включает комиссию за публикацию данных L1 (зависит от размера calldata и цен газа L1). Команда gas оценивает только стоимость выполнения на L2.
  * **Детектор «китов» сканирует только последний блок** — не исторически. Результаты зависят от момента запроса. Порог по умолчанию — 1.0 ETH.
  * **Обнаружение прокси** — определяются только прокси EIP-1967. Другие паттерны прокси (EIP-1167 минимальный прокси, пользовательские слоты хранения) не проверяются.
  * **Повтор при 429** — как RPC, так и CoinGecko выполняют до 2 повторных попыток с экспоненциальной задержкой при ошибках лимита запросов.

* * *

## Проверка[​](<#verification> "Direct link to Verification")

[code] 
    # Должен вывести идентификатор цепи Base (8453), последний блок, цену газа и цену ETH  
    python3 ~/.hermes/skills/blockchain/base/scripts/base_client.py stats  
    
[/code]

  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Предварительные требования](<#prerequisites>)
  * [Краткая справка](<#quick-reference>)
  * [Процедура](<#procedure>)
    * [0\\. Проверка настройки](<#0-setup-check>)
    * [1\\. Портфель кошелька](<#1-wallet-portfolio>)
    * [2\\. Детали транзакции](<#2-transaction-details>)
    * [3\\. Информация о токене](<#3-token-info>)
    * [4\\. Анализ газа](<#4-gas-analysis>)
    * [5\\. Проверка контракта](<#5-contract-inspection>)
    * [6\\. Обнаружение «китов»](<#6-whale-detector>)
    * [7\\. Статистика сети](<#7-network-stats>)
    * [8\\. Поиск цены](<#8-price-lookup>)
  * [Возможные проблемы](<#pitfalls>)
  * [Проверка](<#verification>)

<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/blockchain/blockchain-base -->
