On this page
Запрос данных блокчейна Solana с ценами в USD — балансы кошельков, портфели токенов со стоимостью, детали транзакций, NFT, обнаружение «китов» и статистика сети в реальном времени. Использует Solana RPC + CoinGecko. API-ключ не требуется.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   | 
|---|---  
|Source| Опциональный — установка: `hermes skills install official/blockchain/solana`  
|Path| `optional-skills/blockchain/solana`  
|Version| `0.2.0`  
|Author| Deniz Alagoz (gizdusum), доработано Hermes Agent  
|License| MIT  
|Tags| `Solana`, `Blockchain`, `Crypto`, `Web3`, `RPC`, `DeFi`, `NFT`  
## Reference: полный SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит в качестве инструкций, когда навык активен.
# Solana Blockchain Skill
Запрос данных блокчейна Solana с ценами в USD через CoinGecko. 8 команд: портфель кошелька, информация о токене, транзакции, активность, NFT, обнаружение «китов», статистика сети и поиск цен.
API-ключ не требуется. Использует только стандартную библиотеку Python (urllib, json, argparse).
* * *
## Когда использовать[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь запрашивает баланс кошелька Solana, активы или стоимость портфеля
  * Пользователь хочет просмотреть конкретную транзакцию по сигнатуре
  * Пользователь хочет получить метаданные SPL-токена, цену, эмиссию или крупнейших держателей
  * Пользователь хочет получить историю недавних транзакций для адреса
  * Пользователь хочет получить NFT, принадлежащие кошельку
  * Пользователь хочет найти крупные переводы SOL (обнаружение «китов»)
  * Пользователь хочет узнать состояние сети Solana, TPS, эпоху или цену SOL
  * Пользователь спрашивает «какая цена BONK/JUP/SOL?»


* * *
## Предварительные требования[​](<#prerequisites> "Direct link to Prerequisites")
Вспомогательный скрипт использует только стандартную библиотеку Python (urllib, json, argparse). Внешние пакеты не требуются.
Данные о ценах поступают из бесплатного API CoinGecko (ключ не нужен, ограничение ~10-30 запросов/мин). Для ускорения используйте флаг `--no-prices`.
* * *
## Краткая справка[​](<#quick-reference> "Direct link to Quick Reference")
RPC-эндпоинт (по умолчанию): <https://api.mainnet-beta.solana.com> Переопределение: export SOLANA_RPC_URL=<https://ваш-приватный-rpc.com>
Путь к вспомогательному скрипту: ~/.hermes/skills/blockchain/solana/scripts/solana_client.py
[code] 
    python3 solana_client.py wallet   <address> [--limit N] [--all] [--no-prices]  
    python3 solana_client.py tx       <signature>  
    python3 solana_client.py token    <mint_address>  
    python3 solana_client.py activity <address> [--limit N]  
    python3 solana_client.py nft      <address>  
    python3 solana_client.py whales   [--min-sol N]  
    python3 solana_client.py stats  
    python3 solana_client.py price    <mint_or_symbol>  
    
[/code]
* * *
## Процедура[​](<#procedure> "Direct link to Procedure")
### 0\. Проверка настройки[​](<#0-setup-check> "Direct link to 0. Setup Check")
[code] 
    python3 --version  
      
    # Опционально: установка приватного RPC для лучших лимитов  
    export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"  
      
    # Проверка подключения  
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py stats  
    
[/code]
### 1\. Портфель кошелька[​](<#1-wallet-portfolio> "Direct link to 1. Wallet Portfolio")
Получение баланса SOL, активов SPL-токенов со стоимостью в USD, количества NFT и общей стоимости портфеля. Токены отсортированы по стоимости, «пыль» отфильтрована, известные токены подписаны названиями (BONK, JUP, USDC и т.д.).
[code] 
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \  
      wallet 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM  
    
[/code]
Флаги:
  * `--limit N` — показать топ N токенов (по умолчанию: 20)
  * `--all` — показать все токены, без фильтрации «пыли», без лимита
  * `--no-prices` — пропустить запросы цен CoinGecko (быстрее, только RPC)


Результат включает: баланс SOL + стоимость в USD, список токенов с ценами, отсортированный по стоимости, количество «пылевых» токенов, сводка по NFT, общая стоимость портфеля в USD.
### 2\. Детали транзакции[​](<#2-transaction-details> "Direct link to 2. Transaction Details")
Просмотр полной транзакции по её base58-сигнатуре. Показывает изменения баланса в SOL и USD.
[code] 
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \  
      tx 5j7s8K...ваша_сигнатура_здесь  
    
[/code]
Результат: слот, временная метка, комиссия, статус, изменения баланса (SOL + USD), вызовы программ.
### 3\. Информация о токене[​](<#3-token-info> "Direct link to 3. Token Info")
Получение метаданных SPL-токена, текущей цены, рыночной капитализации, эмиссии, десятичных знаков, адресов минта/заморозки и топ-5 держателей.
[code] 
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \  
      token DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263  
    
[/code]
Результат: название, символ, десятичные знаки, эмиссия, цена, рыночная капитализация, топ-5 держателей с процентами.
### 4\. Недавняя активность[​](<#4-recent-activity> "Direct link to 4. Recent Activity")
Список недавних транзакций для адреса (по умолчанию: последние 10, макс: 25).
[code] 
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \  
      activity 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM --limit 25  
    
[/code]
### 5\. Портфель NFT[​](<#5-nft-portfolio> "Direct link to 5. NFT Portfolio")
Список NFT, принадлежащих кошельку (эвристика: SPL-токены с количеством=1, десятичными=0).
[code] 
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \  
      nft 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM  
    
[/code]
Примечание: Сжатые NFT (cNFT) не обнаруживаются данной эвристикой.
### 6\. Детектор «китов»[​](<#6-whale-detector> "Direct link to 6. Whale Detector")
Сканирование последнего блока на предмет крупных переводов SOL со стоимостью в USD.
[code] 
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \  
      whales --min-sol 500  
    
[/code]
Примечание: сканируется только последний блок — мгновенный снимок, не исторические данные.
### 7\. Статистика сети[​](<#7-network-stats> "Direct link to 7. Network Stats")
Состояние сети Solana в реальном времени: текущий слот, эпоха, TPS, эмиссия, версия валидатора, цена SOL и рыночная капитализация.
[code] 
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py stats  
    
[/code]
### 8\. Поиск цены[​](<#8-price-lookup> "Direct link to 8. Price Lookup")
Быстрая проверка цены любого токена по адресу минта или известному символу.
[code] 
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py price BONK  
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py price JUP  
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py price SOL  
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py price DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263  
    
[/code]
Известные символы: SOL, USDC, USDT, BONK, JUP, WETH, JTO, mSOL, stSOL, PYTH, HNT, RNDR, WEN, W, TNSR, DRIFT, bSOL, JLP, WIF, MEW, BOME, PENGU.
* * *
## Возможные проблемы[​](<#pitfalls> "Direct link to Pitfalls")
  * **Лимиты CoinGecko** — бесплатный тариф допускает ~10-30 запросов/мин. Поиск цен использует 1 запрос на токен. Для кошельков с большим количеством токенов цены могут быть получены не для всех. Используйте `--no-prices` для скорости.
  * **Лимиты публичного RPC** — публичный RPC основной сети Solana ограничивает запросы. Для продакшена установите SOLANA_RPC_URL на приватный эндпоинт (Helius, QuickNode, Triton).
  * **Обнаружение NFT — эвристическое** — количество=1 + десятичные=0. Сжатые NFT (cNFT) и Token-2022 NFT не будут отображаться.
  * **Детектор «китов» сканирует только последний блок** — не исторические данные. Результаты зависят от момента запроса.
  * **История транзакций** — публичный RPC хранит ~2 дня. Более старые транзакции могут быть недоступны.
  * **Названия токенов** — ~25 известных токенов подписаны названиями. Остальные показывают сокращённые адреса минтов. Используйте команду `token` для полной информации.
  * **Повтор при 429** — как RPC, так и CoinGecko повторяют запросы до 2 раз с экспоненциальной задержкой при ошибках лимита.


* * *
## Проверка[​](<#verification> "Direct link to Verification")
[code] 
    # Должен вывести текущий слот Solana, TPS и цену SOL  
    python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py stats  
    
[/code]
  * [Skill metadata](<#skill-metadata>)
  * [Reference: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Предварительные требования](<#prerequisites>)
  * [Краткая справка](<#quick-reference>)
  * [Процедура](<#procedure>)
    * [0\. Проверка настройки](<#0-setup-check>)
    * [1\. Портфель кошелька](<#1-wallet-portfolio>)
    * [2\. Детали транзакции](<#2-transaction-details>)
    * [3\. Информация о токене](<#3-token-info>)
    * [4\. Недавняя активность](<#4-recent-activity>)
    * [5\. Портфель NFT](<#5-nft-portfolio>)
    * [6\. Детектор «китов»](<#6-whale-detector>)
    * [7\. Статистика сети](<#7-network-stats>)
    * [8\. Поиск цены](<#8-price-lookup>)
  * [Возможные проблемы](<#pitfalls>)
  * [Проверка](<#verification>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/blockchain/blockchain-solana -->
