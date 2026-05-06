На этой странице
Shopify Admin и Storefront GraphQL API через curl. Товары, заказы, клиенты, складские остатки, метаполя.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   |
|---  |
|Источник| Опционально — установка: `hermes skills install official/productivity/shopify`  |
|Путь| `optional-skills/productivity/shopify`  |
|Версия| `1.0.0`  |
|Автор| community  |
|Лицензия| MIT  |
|Теги| `Shopify`, `E-commerce`, `Commerce`, `API`, `GraphQL`  |
|Связанные навыки| [`airtable`](</docs/user-guide/skills/bundled/productivity/productivity-airtable>), [`xurl`](</docs/user-guide/skills/bundled/social-media/social-media-xurl>)  |
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Shopify — Admin и Storefront GraphQL API
Работайте с магазинами Shopify напрямую через `curl`: список товаров, управление складскими остатками, получение заказов, обновление клиентов, чтение метаполей. Никакого SDK, никаких фреймворков для приложений — только GraphQL-эндпоинт и токен доступа кастомного приложения.
REST Admin API является устаревшим начиная с 2024-04 и получает только исправления безопасности. **Используйте GraphQL Admin** для всей административной работы. Используйте **Storefront GraphQL** для публичных read-only запросов (товары, коллекции, корзина).
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
  1. В админке Shopify: **Settings → Apps and sales channels → Develop apps → Create an app**.
  2. Нажмите **Configure Admin API scopes**, выберите необходимые разрешения (примеры ниже), сохраните.
  3. **Install app** — токен Admin API показывается ОДИН раз. Скопируйте его немедленно — Shopify больше никогда его не покажет. Токены начинаются с `shpat_`.
  4. Сохраните в `~/.hermes/.env`:
[code] SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxx  
         SHOPIFY_STORE_DOMAIN=my-store.myshopify.com  
         SHOPIFY_API_VERSION=2026-01  
         
[/code]


> **Внимание:** Начиная с 1 января 2026 года новые «устаревшие кастомные приложения», созданные в админке Shopify, больше не доступны. Для новых установок используйте **Dev Dashboard** (`shopify.dev/docs/apps/build/dev-dashboard`). Существующие приложения, созданные через админку, продолжат работу. Если у пользователя в магазине нет существующего кастомного приложения и дата после 2026-01-01, направьте его в Dev Dashboard вместо процедуры через админку.
Распространённые области доступа по задачам:
  * Товары / коллекции: `read_products`, `write_products`
  * Складские остатки: `read_inventory`, `write_inventory`, `read_locations`
  * Заказы: `read_orders`, `write_orders` (30 последних без `read_all_orders`)
  * Клиенты: `read_customers`, `write_customers`
  * Черновики заказов: `read_draft_orders`, `write_draft_orders`
  * Выполнения: `read_fulfillments`, `write_fulfillments`
  * Метаполя / метаобъекты: покрываются соответствующими разрешениями ресурсов

## Основы API[​](<#api-basics> "Прямая ссылка на Основы API")
  * **Эндпоинт:** `https://$SHOPIFY_STORE_DOMAIN/admin/api/$SHOPIFY_API_VERSION/graphql.json`
  * **Заголовок авторизации:** `X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN` (НЕ `Authorization: Bearer`)
  * **Метод:** всегда `POST`, всегда `Content-Type: application/json`, тело запроса — `{"query": "...", "variables": {...}}`
  * **HTTP 200 не означает успех.** GraphQL возвращает ошибки в массиве `errors` верхнего уровня и в по-полях `userErrors`. Всегда проверяйте оба.
  * **ID — это GID-строки:** `gid://shopify/Product/10079467700516`, `gid://shopify/Variant/...`, `gid://shopify/Order/...`. Передавайте их как есть — не удаляйте префикс.
  * **Лимит запросов:** рассчитывается через стоимость запроса (дырявое ведро). Каждый ответ содержит `extensions.cost` с полями `requestedQueryCost`, `actualQueryCost`, `throttleStatus.{currentlyAvailable, maximumAvailable, restoreRate}`. Снижайте нагрузку, когда `currentlyAvailable` падает ниже стоимости следующего запроса. Стандартные магазины = корзина на 100 баллов, восстановление 50/с; Plus = 1000/100.

Базовый шаблон curl (многоразовый):
[code] 
    shop_gql() {  
      local query="$1"  
      local variables="${2:-{}}"  
      curl -sS -X POST \  
        "https://${SHOPIFY_STORE_DOMAIN}/admin/api/${SHOPIFY_API_VERSION:-2026-01}/graphql.json" \  
        -H "Content-Type: application/json" \  
        -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \  
        --data "$(jq -nc --arg q "$query" --argjson v "$variables" '{query: $q, variables: $v}')"  
    }  
    
[/code]
Пропускайте через `jq` для читаемого вывода. `-sS` сохраняет видимость ошибок, но скрывает индикатор прогресса.
## Обнаружение[​](<#discovery> "Прямая ссылка на Обнаружение")
### Информация о магазине + текущая версия API[​](<#shop-info--current-api-version> "Прямая ссылка на Информация о магазине + текущая версия API")
[code] 
    shop_gql '{ shop { name myshopifyDomain primaryDomain { url } currencyCode plan { displayName } } }' | jq  
    
[/code]
### Список всех поддерживаемых версий API[​](<#list-all-supported-api-versions> "Прямая ссылка на Список всех поддерживаемых версий API")
[code] 
    shop_gql '{ publicApiVersions { handle supported } }' | jq '.data.publicApiVersions[] | select(.supported)'  
    
[/code]
## Товары[​](<#products> "Прямая ссылка на Товары")
### Поиск товаров (первые 20 по запросу)[​](<#search-products-first-20-matching-query> "Прямая ссылка на Поиск товаров (первые 20 по запросу)")
[code] 
    shop_gql '  
    query($q: String!) {  
      products(first: 20, query: $q) {  
        edges { node { id title handle status totalInventory variants(first: 5) { edges { node { id sku price inventoryQuantity } } } } }  
        pageInfo { hasNextPage endCursor }  
      }  
    }' '{"q":"hoodie status:active"}' | jq  
    
[/code]
Синтаксис запросов поддерживает `title:`, `sku:`, `vendor:`, `product_type:`, `status:active`, `tag:`, `created_at:>2025-01-01`. Полная грамматика: <https://shopify.dev/docs/api/usage/search-syntax>
### Пагинация товаров (курсор)[​](<#paginate-products-cursor> "Прямая ссылка на Пагинация товаров (курсор)")
[code] 
    shop_gql '  
    query($cursor: String) {  
      products(first: 100, after: $cursor) {  
        edges { cursor node { id handle } }  
        pageInfo { hasNextPage endCursor }  
      }  
    }' '{"cursor":null}'  
    # subsequent calls: pass the previous endCursor  
    
[/code]
### Получить товар с вариантами и метаполями[​](<#get-a-product-with-variants--metafields> "Прямая ссылка на Получить товар с вариантами и метаполями")
[code] 
    shop_gql '  
    query($id: ID!) {  
      product(id: $id) {  
        id title handle descriptionHtml tags status  
        variants(first: 20) { edges { node { id sku price compareAtPrice inventoryQuantity selectedOptions { name value } } } }  
        metafields(first: 20) { edges { node { namespace key type value } } }  
      }  
    }' '{"id":"gid://shopify/Product/10079467700516"}' | jq  
    
[/code]
### Создать товар с одним вариантом[​](<#create-a-product-with-one-variant> "Прямая ссылка на Создать товар с одним вариантом")
[code] 
    shop_gql '  
    mutation($input: ProductCreateInput!) {  
      productCreate(product: $input) {  
        product { id handle }  
        userErrors { field message }  
      }  
    }' '{"input":{"title":"Test Hoodie","status":"DRAFT","vendor":"Hermes","productType":"Apparel","tags":["test"]}}'  
    
[/code]
В последних версиях у вариантов есть собственные мутации:
[code] 
    # Add variants after creating the product  
    shop_gql '  
    mutation($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {  
      productVariantsBulkCreate(productId: $productId, variants: $variants) {  
        productVariants { id sku price }  
        userErrors { field message }  
      }  
    }' '{"productId":"gid://shopify/Product/...","variants":[{"optionValues":[{"optionName":"Size","name":"M"}],"price":"49.00","inventoryItem":{"sku":"HD-M","tracked":true}}]}'  
    
[/code]
### Обновить цену / SKU[​](<#update-price--sku> "Прямая ссылка на Обновить цену / SKU")
[code] 
    shop_gql '  
    mutation($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {  
      productVariantsBulkUpdate(productId: $productId, variants: $variants) {  
        productVariants { id sku price }  
        userErrors { field message }  
      }  
    }' '{"productId":"gid://shopify/Product/...","variants":[{"id":"gid://shopify/ProductVariant/...","price":"55.00"}]}'  
    
[/code]
## Заказы[​](<#orders> "Прямая ссылка на Заказы")
### Список последних заказов (последние 30 по умолчанию без `read_all_orders`)[​](<#list-recent-orders-last-30-by-default-without-read_all_orders> "Прямая ссылка на Список последних заказов (последние 30 по умолчанию без `read_all_orders`)")
[code] 
    shop_gql '  
    {  
      orders(first: 20, reverse: true, query: "financial_status:paid") {  
        edges { node {  
          id name createdAt displayFinancialStatus displayFulfillmentStatus  
          totalPriceSet { shopMoney { amount currencyCode } }  
          customer { id displayName email }  
          lineItems(first: 10) { edges { node { title quantity sku } } }  
        } }  
      }  
    }' | jq  
    
[/code]
Полезные фильтры запросов заказов: `financial_status:paid|pending|refunded`, `fulfillment_status:unfulfilled|fulfilled`, `created_at:>2025-01-01`, `tag:gift`, `email:foo@example.com`.
### Получить отдельный заказ с адресом доставки[​](<#fetch-a-single-order-with-shipping-address> "Прямая ссылка на Получить отдельный заказ с адресом доставки")
[code] 
    shop_gql '  
    query($id: ID!) {  
      order(id: $id) {  
        id name email  
        shippingAddress { name address1 address2 city province country zip phone }  
        lineItems(first: 50) { edges { node { title quantity variant { sku } originalUnitPriceSet { shopMoney { amount currencyCode } } } } }  
        transactions { id kind status amountSet { shopMoney { amount currencyCode } } }  
      }  
    }' '{"id":"gid://shopify/Order/...."}' | jq  
    
[/code]
## Клиенты[​](<#customers> "Прямая ссылка на Клиенты")
[code] 
    # Search  
    shop_gql '  
    {  
      customers(first: 10, query: "email:*@example.com") {  
        edges { node { id email displayName numberOfOrders amountSpent { amount currencyCode } } }  
      }  
    }'  
      
    # Create  
    shop_gql '  
    mutation($input: CustomerInput!) {  
      customerCreate(input: $input) {  
        customer { id email }  
        userErrors { field message }  
      }  
    }' '{"input":{"email":"test@example.com","firstName":"Test","lastName":"User","tags":["api-created"]}}'  
    
[/code]
## Складские остатки[​](<#inventory> "Прямая ссылка на Складские остатки")
Остатки хранятся в **складских единицах (inventory items)**, привязанных к вариантам, количество отслеживается по **локациям**.
[code] 
    # Get inventory for a variant across all locations  
    shop_gql '  
    query($id: ID!) {  
      productVariant(id: $id) {  
        id sku  
        inventoryItem {  
          id tracked  
          inventoryLevels(first: 10) {  
            edges { node { location { id name } quantities(names: ["available","on_hand","committed"]) { name quantity } } }  
          }  
        }  
      }  
    }' '{"id":"gid://shopify/ProductVariant/..."}'  
    
[/code]
Корректировка запасов (дельта) — через `inventoryAdjustQuantities`:
[code] 
    shop_gql '  
    mutation($input: InventoryAdjustQuantitiesInput!) {  
      inventoryAdjustQuantities(input: $input) {  
        inventoryAdjustmentGroup { reason changes { name delta } }  
        userErrors { field message }  
      }  
    }' '{  
      "input": {  
        "reason": "correction",  
        "name": "available",  
        "changes": [{"delta": 5, "inventoryItemId": "gid://shopify/InventoryItem/...", "locationId": "gid://shopify/Location/..."}]  
      }  
    }'  
    
[/code]
Установка абсолютного количества (не дельта) — `inventorySetQuantities`:
[code] 
    shop_gql '  
    mutation($input: InventorySetQuantitiesInput!) {  
      inventorySetQuantities(input: $input) {  
        inventoryAdjustmentGroup { id }  
        userErrors { field message }  
      }  
    }' '{"input":{"reason":"correction","name":"available","ignoreCompareQuantity":true,"quantities":[{"inventoryItemId":"gid://shopify/InventoryItem/...","locationId":"gid://shopify/Location/...","quantity":100}]}}'  
    
[/code]
## Метаполя и метаобъекты[​](<#metafields--metaobjects> "Прямая ссылка на Метаполя и метаобъекты")
Метаполя присоединяют пользовательские данные к ресурсам (товары, клиенты, заказы, магазин).
[code] 
    # Read  
    shop_gql '  
    query($id: ID!) {  
      product(id: $id) {  
        metafields(first: 10, namespace: "custom") {  
          edges { node { key type value } }  
        }  
      }  
    }' '{"id":"gid://shopify/Product/..."}'  
      
    # Write (works for any owner type)  
    shop_gql '  
    mutation($metafields: [MetafieldsSetInput!]!) {  
      metafieldsSet(metafields: $metafields) {  
        metafields { id key namespace }  
        userErrors { field message code }  
      }  
    }' '{"metafields":[{"ownerId":"gid://shopify/Product/...","namespace":"custom","key":"care_instructions","type":"multi_line_text_field","value":"Wash cold. Tumble dry low."}]}'  
    
[/code]
## Storefront API (публичный, только чтение)[​](<#storefront-api-public-read-only> "Прямая ссылка на Storefront API (публичный, только чтение)")
Другой эндпоинт, другой токен, используется для публичных приложений и headless-установок на основе Hydrogen. Заголовки отличаются:
  * **Эндпоинт:** `https://$SHOPIFY_STORE_DOMAIN/api/$SHOPIFY_API_VERSION/graphql.json`
  * **Заголовок авторизации (публичный):** `X-Shopify-Storefront-Access-Token: <public token>` — можно встраивать в браузер
  * **Заголовок авторизации (приватный):** `Shopify-Storefront-Private-Token: <private token>` — только для сервера

[code] 
    curl -sS -X POST \  
      "https://${SHOPIFY_STORE_DOMAIN}/api/${SHOPIFY_API_VERSION:-2026-01}/graphql.json" \  
      -H "Content-Type: application/json" \  
      -H "X-Shopify-Storefront-Access-Token: ${SHOPIFY_STOREFRONT_TOKEN}" \  
      -d '{"query":"{ shop { name } products(first: 5) { edges { node { id title handle } } } }"}' | jq  
    
[/code]
## Массовые операции[​](<#bulk-operations> "Прямая ссылка на Массовые операции")
Для выгрузок, превышающих лимиты запросов (полный каталог товаров, все заказы за год):
[code] 
    # 1. Start bulk query  
    shop_gql '  
    mutation {  
      bulkOperationRunQuery(query: """  
        { products { edges { node { id title handle variants { edges { node { sku price } } } } } } }  
      """) {  
        bulkOperation { id status }  
        userErrors { field message }  
      }  
    }'  
      
    # 2. Poll status  
    shop_gql '{ currentBulkOperation { id status errorCode objectCount fileSize url partialDataUrl } }'  
      
    # 3. When status=COMPLETED, download the JSONL file  
    curl -sS "$URL" > products.jsonl  
    
[/code]
Каждая строка JSONL — это узел, а вложенные связи выводятся отдельными строками с `__parentId`. При необходимости можно собрать структуру на стороне клиента.
## Вебхуки[​](<#webhooks> "Прямая ссылка на Вебхуки")
Подпишитесь на события, чтобы не опрашивать API вручную:
[code] 
    shop_gql '  
    mutation($topic: WebhookSubscriptionTopic!, $sub: WebhookSubscriptionInput!) {  
      webhookSubscriptionCreate(topic: $topic, webhookSubscription: $sub) {  
        webhookSubscription { id topic endpoint { __typename ... on WebhookHttpEndpoint { callbackUrl } } }  
        userErrors { field message }  
      }  
    }' '{"topic":"ORDERS_CREATE","sub":{"callbackUrl":"https://example.com/webhook","format":"JSON"}}'  
    
[/code]
Проверяйте входящие вебхуки по HMAC, используя секрет приложения (не токен доступа):
[code] 
    echo -n "$REQUEST_BODY" | openssl dgst -sha256 -hmac "$APP_SECRET" -binary | base64  
    # Compare to X-Shopify-Hmac-Sha256 header  
    
[/code]
## Подводные камни[​](<#pitfalls> "Прямая ссылка на Подводные камни")
  * **REST-эндпоинты всё ещё существуют, но заморожены.** Не пишите новые интеграции против `/admin/api/.../products.json`. Используйте GraphQL.
  * **Проверка формата токена.** Admin-токены начинаются с `shpat_`. Storefront-публичные токены — с `shpua_`. Если у вас есть токен и неправильный заголовок, каждый запрос будет возвращать 401 без полезного тела ошибки.
  * **403 с валидным токеном = недостаточно прав.** Shopify возвращает `{"errors":[{"message":"Access denied for ..."}]}`. Перенастройте разрешения Admin API в приложении, затем переустановите его для генерации нового токена.
  * **Пустой `userErrors` ≠ успех.** Также проверяйте, что `data.<mutation>.<resource>` не null. Некоторые сбои не заполняют ни то, ни другое — проверяйте весь ответ.
  * **GID против числового ID.** Устаревший REST возвращал числовые ID; GraphQL требует полные GID-строки. Для конвертации: `gid://shopify/Product/<numeric>`.
  * **Неожиданный лимит запросов.** Один запрос `products(first: 250)` с глубокой вложенностью может стоить 1000+ баллов и мгновенно вызвать троттлинг в магазине со стандартным планом. Начинайте с малого, читайте `extensions.cost`, подстраивайтесь.
  * **Порядок пагинации.** `products(first: N, reverse: true)` сортирует по `id DESC`, а не по `created_at`. Используйте `sortKey: CREATED_AT, reverse: true` для сортировки «сначала новые».
  * **`read_all_orders` для исторических данных.** Без него `orders(...)` неявно ограничивается окном в 60 дней. Вы не получите ошибку — просто меньше результатов, чем ожидалось. Для продавцов Shopify Plus с большим количеством заказов запросите эту область через настройки защищённых данных приложения.
  * **Валюты — это строки.** Суммы возвращаются как `"49.00"`, а не `49.0`. Не применяйте `jq tonumber` вслепую, если вам важны нули после запятой.
  * **Мультивалютные Money-поля** содержат `shopMoney` (валюта магазина) И `presentmentMoney` (валюта клиента). Выберите один вариант последовательно.

## Безопасность[​](<#safety> "Прямая ссылка на Безопасность")
Мутации в Shopify реальны — они создают товары, списывают средства, отменяют заказы, оформляют отправки. Перед выполнением `productDelete`, `orderCancel`, `refundCreate` или любой массовой мутации: чётко объясните, какое изменение будет сделано, в каком магазине, и подтвердите с пользователем. Отдельной тестовой копии рабочих данных не существует, если у пользователя нет отдельного dev-магазина.
  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
  * [Основы API](<#api-basics>)
  * [Обнаружение](<#discovery>)
    * [Информация о магазине + текущая версия API](<#shop-info--current-api-version>)
    * [Список всех поддерживаемых версий API](<#list-all-supported-api-versions>)
  * [Товары](<#products>)
    * [Поиск товаров (первые 20 по запросу)](<#search-products-first-20-matching-query>)
    * [Пагинация товаров (курсор)](<#paginate-products-cursor>)
    * [Получить товар с вариантами и метаполями](<#get-a-product-with-variants--metafields>)
    * [Создать товар с одним вариантом](<#create-a-product-with-one-variant>)
    * [Обновить цену / SKU](<#update-price--sku>)
  * [Заказы](<#orders>)
    * [Список последних заказов (последние 30 по умолчанию без `read_all_orders`)](<#list-recent-orders-last-30-by-default-without-read_all_orders>)
    * [Получить отдельный заказ с адресом доставки](<#fetch-a-single-order-with-shipping-address>)
  * [Клиенты](<#customers>)
  * [Складские остатки](<#inventory>)
  * [Метаполя и метаобъекты](<#metafields--metaobjects>)
  * [Storefront API (публичный, только чтение)](<#storefront-api-public-read-only>)
  * [Массовые операции](<#bulk-operations>)
  * [Вебхуки](<#webhooks>)
  * [Подводные камни](<#pitfalls>)
  * [Безопасность](<#safety>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-shopify -->
