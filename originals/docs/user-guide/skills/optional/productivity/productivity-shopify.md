On this page
Shopify Admin & Storefront GraphQL APIs via curl. Products, orders, customers, inventory, metafields.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/productivity/shopify`  
Path| `optional-skills/productivity/shopify`  
Version| `1.0.0`  
Author| community  
License| MIT  
Tags| `Shopify`, `E-commerce`, `Commerce`, `API`, `GraphQL`  
Related skills| [`airtable`](</docs/user-guide/skills/bundled/productivity/productivity-airtable>), [`xurl`](</docs/user-guide/skills/bundled/social-media/social-media-xurl>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Shopify — Admin & Storefront GraphQL APIs
Work with Shopify stores directly through `curl`: list products, manage inventory, pull orders, update customers, read metafields. No SDK, no app framework — just the GraphQL endpoint and a custom-app access token.
The REST Admin API is legacy since 2024-04 and only receives security fixes. **Use GraphQL Admin** for all admin work. Use **Storefront GraphQL** for read-only customer-facing queries (products, collections, cart).
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  1. In Shopify admin: **Settings → Apps and sales channels → Develop apps → Create an app**.
  2. Click **Configure Admin API scopes** , select what you need (examples below), save.
  3. **Install app** → the Admin API access token appears ONCE. Copy it immediately — Shopify will never show it again. Tokens start with `shpat_`.
  4. Save to `~/.hermes/.env`:
[code] SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxx  
         SHOPIFY_STORE_DOMAIN=my-store.myshopify.com  
         SHOPIFY_API_VERSION=2026-01  
         
[/code]


> **Heads up:** As of January 1, 2026, new "legacy custom apps" created in the Shopify admin are gone. New setups should use the **Dev Dashboard** (`shopify.dev/docs/apps/build/dev-dashboard`). Existing admin-created apps keep working. If the user's shop has no existing custom app and it's after 2026-01-01, direct them to Dev Dashboard instead of the admin flow.
Common scopes by task:
  * Products / collections: `read_products`, `write_products`
  * Inventory: `read_inventory`, `write_inventory`, `read_locations`
  * Orders: `read_orders`, `write_orders` (30 most recent without `read_all_orders`)
  * Customers: `read_customers`, `write_customers`
  * Draft orders: `read_draft_orders`, `write_draft_orders`
  * Fulfillments: `read_fulfillments`, `write_fulfillments`
  * Metafields / metaobjects: covered by the matching resource scopes


## API Basics[​](<#api-basics> "Direct link to API Basics")
  * **Endpoint:** `https://$SHOPIFY_STORE_DOMAIN/admin/api/$SHOPIFY_API_VERSION/graphql.json`
  * **Auth header:** `X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN` (NOT `Authorization: Bearer`)
  * **Method:** always `POST`, always `Content-Type: application/json`, body is `{"query": "...", "variables": {...}}`
  * **HTTP 200 does not mean success.** GraphQL returns errors in a top-level `errors` array and per-field `userErrors`. Always check both.
  * **IDs are GID strings:** `gid://shopify/Product/10079467700516`, `gid://shopify/Variant/...`, `gid://shopify/Order/...`. Pass these verbatim — don't strip the prefix.
  * **Rate limit:** calculated via query cost (leaky bucket). Each response has `extensions.cost` with `requestedQueryCost`, `actualQueryCost`, `throttleStatus.{currentlyAvailable, maximumAvailable, restoreRate}`. Back off when `currentlyAvailable` drops below your next query's cost. Standard shops = 100 points bucket, 50/s restore; Plus = 1000/100.


Base curl pattern (reusable):
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
Pipe through `jq` for readable output. `-sS` keeps errors visible but hides the progress bar.
## Discovery[​](<#discovery> "Direct link to Discovery")
### Shop info + current API version[​](<#shop-info--current-api-version> "Direct link to Shop info + current API version")
[code] 
    shop_gql '{ shop { name myshopifyDomain primaryDomain { url } currencyCode plan { displayName } } }' | jq  
    
[/code]
### List all supported API versions[​](<#list-all-supported-api-versions> "Direct link to List all supported API versions")
[code] 
    shop_gql '{ publicApiVersions { handle supported } }' | jq '.data.publicApiVersions[] | select(.supported)'  
    
[/code]
## Products[​](<#products> "Direct link to Products")
### Search products (first 20 matching query)[​](<#search-products-first-20-matching-query> "Direct link to Search products \(first 20 matching query\)")
[code] 
    shop_gql '  
    query($q: String!) {  
      products(first: 20, query: $q) {  
        edges { node { id title handle status totalInventory variants(first: 5) { edges { node { id sku price inventoryQuantity } } } } }  
        pageInfo { hasNextPage endCursor }  
      }  
    }' '{"q":"hoodie status:active"}' | jq  
    
[/code]
Query syntax supports `title:`, `sku:`, `vendor:`, `product_type:`, `status:active`, `tag:`, `created_at:>2025-01-01`. Full grammar: <https://shopify.dev/docs/api/usage/search-syntax>
### Paginate products (cursor)[​](<#paginate-products-cursor> "Direct link to Paginate products \(cursor\)")
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
### Get a product with variants + metafields[​](<#get-a-product-with-variants--metafields> "Direct link to Get a product with variants + metafields")
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
### Create a product with one variant[​](<#create-a-product-with-one-variant> "Direct link to Create a product with one variant")
[code] 
    shop_gql '  
    mutation($input: ProductCreateInput!) {  
      productCreate(product: $input) {  
        product { id handle }  
        userErrors { field message }  
      }  
    }' '{"input":{"title":"Test Hoodie","status":"DRAFT","vendor":"Hermes","productType":"Apparel","tags":["test"]}}'  
    
[/code]
Variants now have their own mutations in recent versions:
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
### Update price / SKU[​](<#update-price--sku> "Direct link to Update price / SKU")
[code] 
    shop_gql '  
    mutation($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {  
      productVariantsBulkUpdate(productId: $productId, variants: $variants) {  
        productVariants { id sku price }  
        userErrors { field message }  
      }  
    }' '{"productId":"gid://shopify/Product/...","variants":[{"id":"gid://shopify/ProductVariant/...","price":"55.00"}]}'  
    
[/code]
## Orders[​](<#orders> "Direct link to Orders")
### List recent orders (last 30 by default without `read_all_orders`)[​](<#list-recent-orders-last-30-by-default-without-read_all_orders> "Direct link to list-recent-orders-last-30-by-default-without-read_all_orders")
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
Useful order query filters: `financial_status:paid|pending|refunded`, `fulfillment_status:unfulfilled|fulfilled`, `created_at:>2025-01-01`, `tag:gift`, `email:foo@example.com`.
### Fetch a single order with shipping address[​](<#fetch-a-single-order-with-shipping-address> "Direct link to Fetch a single order with shipping address")
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
## Customers[​](<#customers> "Direct link to Customers")
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
## Inventory[​](<#inventory> "Direct link to Inventory")
Inventory lives on **inventory items** tied to variants, quantities tracked per **location**.
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
Adjust stock (delta) — uses `inventoryAdjustQuantities`:
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
Set absolute stock (not delta) — `inventorySetQuantities`:
[code] 
    shop_gql '  
    mutation($input: InventorySetQuantitiesInput!) {  
      inventorySetQuantities(input: $input) {  
        inventoryAdjustmentGroup { id }  
        userErrors { field message }  
      }  
    }' '{"input":{"reason":"correction","name":"available","ignoreCompareQuantity":true,"quantities":[{"inventoryItemId":"gid://shopify/InventoryItem/...","locationId":"gid://shopify/Location/...","quantity":100}]}}'  
    
[/code]
## Metafields & Metaobjects[​](<#metafields--metaobjects> "Direct link to Metafields & Metaobjects")
Metafields attach custom data to resources (products, customers, orders, shop).
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
## Storefront API (public read-only)[​](<#storefront-api-public-read-only> "Direct link to Storefront API \(public read-only\)")
Different endpoint, different token, used for customer-facing apps/hydrogen-style headless setups. Headers differ:
  * **Endpoint:** `https://$SHOPIFY_STORE_DOMAIN/api/$SHOPIFY_API_VERSION/graphql.json`
  * **Auth header (public):** `X-Shopify-Storefront-Access-Token: <public token>` — embeddable in browser
  * **Auth header (private):** `Shopify-Storefront-Private-Token: <private token>` — server-only


[code] 
    curl -sS -X POST \  
      "https://${SHOPIFY_STORE_DOMAIN}/api/${SHOPIFY_API_VERSION:-2026-01}/graphql.json" \  
      -H "Content-Type: application/json" \  
      -H "X-Shopify-Storefront-Access-Token: ${SHOPIFY_STOREFRONT_TOKEN}" \  
      -d '{"query":"{ shop { name } products(first: 5) { edges { node { id title handle } } } }"}' | jq  
    
[/code]
## Bulk Operations[​](<#bulk-operations> "Direct link to Bulk Operations")
For dumps larger than rate limits allow (full product catalog, all orders for a year):
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
Each JSONL line is a node, and nested connections are emitted as separate lines with `__parentId`. Reassemble client-side if needed.
## Webhooks[​](<#webhooks> "Direct link to Webhooks")
Subscribe to events so you don't have to poll:
[code] 
    shop_gql '  
    mutation($topic: WebhookSubscriptionTopic!, $sub: WebhookSubscriptionInput!) {  
      webhookSubscriptionCreate(topic: $topic, webhookSubscription: $sub) {  
        webhookSubscription { id topic endpoint { __typename ... on WebhookHttpEndpoint { callbackUrl } } }  
        userErrors { field message }  
      }  
    }' '{"topic":"ORDERS_CREATE","sub":{"callbackUrl":"https://example.com/webhook","format":"JSON"}}'  
    
[/code]
Verify incoming webhook HMAC using the app's client secret (not the access token):
[code] 
    echo -n "$REQUEST_BODY" | openssl dgst -sha256 -hmac "$APP_SECRET" -binary | base64  
    # Compare to X-Shopify-Hmac-Sha256 header  
    
[/code]
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * **REST endpoints still exist but are frozen.** Don't write new integrations against `/admin/api/.../products.json`. Use GraphQL.
  * **Token format check.** Admin tokens start with `shpat_`. Storefront public tokens with `shpua_`. If you have one and the wrong header, every request returns 401 without a useful error body.
  * **403 with a valid token = missing scope.** Shopify returns `{"errors":[{"message":"Access denied for ..."}]}`. Re-configure Admin API scopes on the app, then reinstall to regenerate the token.
  * **`userErrors` is empty != success.** Also check `data.<mutation>.<resource>` is non-null. Some failures populate neither — inspect the whole response.
  * **GID vs numeric ID.** Legacy REST gave numeric IDs; GraphQL wants full GID strings. To convert: `gid://shopify/Product/<numeric>`.
  * **Rate limit surprise.** A single `products(first: 250)` with deep nesting can cost 1000+ points and throttle immediately on a standard-plan shop. Start narrow, read `extensions.cost`, adjust.
  * **Pagination order.** `products(first: N, reverse: true)` sorts by `id DESC`, not `created_at`. Use `sortKey: CREATED_AT, reverse: true` for "newest first."
  * **`read_all_orders` for historical data.** Without it, `orders(...)` silently caps at the 60-day window. You won't get an error, just fewer results than expected. For Shopify Plus merchants with many orders, request this scope via the app's protected-data settings.
  * **Currencies are strings.** Amounts come back as `"49.00"` not `49.0`. Don't `jq tonumber` blindly if you care about zero-padding.
  * **Multi-currency Money fields** have `shopMoney` (store's currency) AND `presentmentMoney` (customer's). Pick one consistently.


## Safety[​](<#safety> "Direct link to Safety")
Mutations in Shopify are real — they create products, charge refunds, cancel orders, ship fulfillments. Before running `productDelete`, `orderCancel`, `refundCreate`, or any bulk mutation: state clearly what the change is, on which shop, and confirm with the user. There is no staging clone of production data unless the user has a separate dev store.
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Prerequisites](<#prerequisites>)
  * [API Basics](<#api-basics>)
  * [Discovery](<#discovery>)
    * [Shop info + current API version](<#shop-info--current-api-version>)
    * [List all supported API versions](<#list-all-supported-api-versions>)
  * [Products](<#products>)
    * [Search products (first 20 matching query)](<#search-products-first-20-matching-query>)
    * [Paginate products (cursor)](<#paginate-products-cursor>)
    * [Get a product with variants + metafields](<#get-a-product-with-variants--metafields>)
    * [Create a product with one variant](<#create-a-product-with-one-variant>)
    * [Update price / SKU](<#update-price--sku>)
  * [Orders](<#orders>)
    * [List recent orders (last 30 by default without `read_all_orders`)](<#list-recent-orders-last-30-by-default-without-read_all_orders>)
    * [Fetch a single order with shipping address](<#fetch-a-single-order-with-shipping-address>)
  * [Customers](<#customers>)
  * [Inventory](<#inventory>)
  * [Metafields & Metaobjects](<#metafields--metaobjects>)
  * [Storefront API (public read-only)](<#storefront-api-public-read-only>)
  * [Bulk Operations](<#bulk-operations>)
  * [Webhooks](<#webhooks>)
  * [Pitfalls](<#pitfalls>)
  * [Safety](<#safety>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-shopify -->
