On this page
Веб-скрапинг с Scrapling — HTTP-загрузка, скрытная автоматизация браузера, обход Cloudflare и паутинный обход через CLI и Python.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |   |
|---|---|
|Источник| Опциональный — установка: `hermes skills install official/research/scrapling`  |
|Путь| `optional-skills/research/scrapling`  |
|Версия| `1.0.0`  |
|Автор| FEUAZUR  |
|Лицензия| MIT  |
|Теги| `Web Scraping`, `Browser`, `Cloudflare`, `Stealth`, `Crawling`, `Spider`  |
|Связанные навыки| [`duckduckgo-search`](</docs/user-guide/skills/optional/research/research-duckduckgo-search>), [`domain-intel`](</docs/user-guide/skills/optional/research/research-domain-intel>)  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# Scrapling
[Scrapling](<https://github.com/D4Vinci/Scrapling>) — это фреймворк для веб-скрапинга с обходом антибот-систем, скрытной автоматизацией браузера и паутинным фреймворком. Он предоставляет три стратегии загрузки (HTTP, динамический JS, скрытный/Cloudflare) и полноценный CLI.
**Данный навык предназначен только для образовательных и исследовательских целей.** Пользователи обязаны соблюдать местные/международные законы о сборе данных и уважать Условия использования веб-сайтов.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Парсинг статических HTML-страниц (быстрее, чем инструменты с браузером)
  * Парсинг страниц с JS-рендерингом, требующих реального браузера
  * Обход Cloudflare Turnstile или систем обнаружения ботов
  * Обход нескольких страниц с помощью паука (spider)
  * Когда встроенный инструмент `web_extract` не возвращает нужные данные


## Installation[​](<#installation> "Direct link to Installation")
[code] 
    pip install "scrapling[all]"  
    scrapling install  
    
[/code]
Минимальная установка (только HTTP, без браузера):
[code] 
    pip install scrapling  
    
[/code]
Только с автоматизацией браузера:
[code] 
    pip install "scrapling[fetchers]"  
    scrapling install  
    
[/code]
## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
Подход| Класс| Когда использовать  
|---|---|---  
HTTP| `Fetcher` / `FetcherSession`| Статические страницы, API, быстрые массовые запросы  
Динамический| `DynamicFetcher` / `DynamicSession`| Контент с JS-рендерингом, SPA  
Скрытный| `StealthyFetcher` / `StealthySession`| Cloudflare, сайты с защитой от ботов  
Паук| `Spider`| Многостраничный обход с переходом по ссылкам  
## CLI Usage[​](<#cli-usage> "Direct link to CLI Usage")
### Extract Static Page[​](<#extract-static-page> "Direct link to Extract Static Page")
[code] 
    scrapling extract get 'https://example.com' output.md  
    
[/code]
С CSS-селектором и эмуляцией браузера:
[code] 
    scrapling extract get 'https://example.com' output.md \  
      --css-selector '.content' \  
      --impersonate 'chrome'  
    
[/code]
### Extract JS-Rendered Page[​](<#extract-js-rendered-page> "Direct link to Extract JS-Rendered Page")
[code] 
    scrapling extract fetch 'https://example.com' output.md \  
      --css-selector '.dynamic-content' \  
      --disable-resources \  
      --network-idle  
    
[/code]
### Extract Cloudflare-Protected Page[​](<#extract-cloudflare-protected-page> "Direct link to Extract Cloudflare-Protected Page")
[code] 
    scrapling extract stealthy-fetch 'https://protected-site.com' output.html \  
      --solve-cloudflare \  
      --block-webrtc \  
      --hide-canvas  
    
[/code]
### POST Request[​](<#post-request> "Direct link to POST Request")
[code] 
    scrapling extract post 'https://example.com/api' output.json \  
      --json '{"query": "search term"}'  
    
[/code]
### Output Formats[​](<#output-formats> "Direct link to Output Formats")
Формат вывода определяется расширением файла:
  * `.html` — сырой HTML
  * `.md` — конвертировано в Markdown
  * `.txt` — обычный текст
  * `.json` / `.jsonl` — JSON


## Python: HTTP Scraping[​](<#python-http-scraping> "Direct link to Python: HTTP Scraping")
### Single Request[​](<#single-request> "Direct link to Single Request")
[code] 
    from scrapling.fetchers import Fetcher  
      
    page = Fetcher.get('https://quotes.toscrape.com/')  
    quotes = page.css('.quote .text::text').getall()  
    for q in quotes:  
        print(q)  
    
[/code]
### Session (Persistent Cookies)[​](<#session-persistent-cookies> "Direct link to Session (Persistent Cookies)")
[code] 
    from scrapling.fetchers import FetcherSession  
      
    with FetcherSession(impersonate='chrome') as session:  
        page = session.get('https://example.com/', stealthy_headers=True)  
        links = page.css('a::attr(href)').getall()  
        for link in links[:5]:  
            sub = session.get(link)  
            print(sub.css('h1::text').get())  
    
[/code]
### POST / PUT / DELETE[​](<#post--put--delete> "Direct link to POST / PUT / DELETE")
[code] 
    page = Fetcher.post('https://api.example.com/data', json={"key": "value"})  
    page = Fetcher.put('https://api.example.com/item/1', data={"name": "updated"})  
    page = Fetcher.delete('https://api.example.com/item/1')  
    
[/code]
### With Proxy[​](<#with-proxy> "Direct link to With Proxy")
[code] 
    page = Fetcher.get('https://example.com', proxy='http://user:pass@proxy:8080')  
    
[/code]
## Python: Dynamic Pages (JS-Rendered)[​](<#python-dynamic-pages-js-rendered> "Direct link to Python: Dynamic Pages (JS-Rendered)")
Для страниц, требующих выполнения JavaScript (SPA, ленивая загрузка контента):
[code] 
    from scrapling.fetchers import DynamicFetcher  
      
    page = DynamicFetcher.fetch('https://example.com', headless=True)  
    data = page.css('.js-loaded-content::text').getall()  
    
[/code]
### Wait for Specific Element[​](<#wait-for-specific-element> "Direct link to Wait for Specific Element")
[code] 
    page = DynamicFetcher.fetch(  
        'https://example.com',  
        wait_selector=('.results', 'visible'),  
        network_idle=True,  
    )  
    
[/code]
### Disable Resources for Speed[​](<#disable-resources-for-speed> "Direct link to Disable Resources for Speed")
Блокирует шрифты, изображения, медиа, таблицы стилей (~на 25% быстрее):
[code] 
    from scrapling.fetchers import DynamicSession  
      
    with DynamicSession(headless=True, disable_resources=True, network_idle=True) as session:  
        page = session.fetch('https://example.com')  
        items = page.css('.item::text').getall()  
    
[/code]
### Custom Page Automation[​](<#custom-page-automation> "Direct link to Custom Page Automation")
[code] 
    from playwright.sync_api import Page  
    from scrapling.fetchers import DynamicFetcher  
      
    def scroll_and_click(page: Page):  
        page.mouse.wheel(0, 3000)  
        page.wait_for_timeout(1000)  
        page.click('button.load-more')  
        page.wait_for_selector('.extra-results')  
      
    page = DynamicFetcher.fetch('https://example.com', page_action=scroll_and_click)  
    results = page.css('.extra-results .item::text').getall()  
    
[/code]
## Python: Stealth Mode (Anti-Bot Bypass)[​](<#python-stealth-mode-anti-bot-bypass> "Direct link to Python: Stealth Mode (Anti-Bot Bypass)")
Для сайтов под защитой Cloudflare или с активной проверкой отпечатков:
[code] 
    from scrapling.fetchers import StealthyFetcher  
      
    page = StealthyFetcher.fetch(  
        'https://protected-site.com',  
        headless=True,  
        solve_cloudflare=True,  
        block_webrtc=True,  
        hide_canvas=True,  
    )  
    content = page.css('.protected-content::text').getall()  
    
[/code]
### Stealth Session[​](<#stealth-session> "Direct link to Stealth Session")
[code] 
    from scrapling.fetchers import StealthySession  
      
    with StealthySession(headless=True, solve_cloudflare=True) as session:  
        page1 = session.fetch('https://protected-site.com/page1')  
        page2 = session.fetch('https://protected-site.com/page2')  
    
[/code]
## Element Selection[​](<#element-selection> "Direct link to Element Selection")
Все загрузчики возвращают объект `Selector` со следующими методами:
### CSS Selectors[​](<#css-selectors> "Direct link to CSS Selectors")
[code] 
    page.css('h1::text').get()              # Текст первого h1  
    page.css('a::attr(href)').getall()      # Все href ссылок  
    page.css('.quote .text::text').getall() # Вложенный выбор  
    
[/code]
### XPath[​](<#xpath> "Direct link to XPath")
[code] 
    page.xpath('//div[@class="content"]/text()').getall()  
    page.xpath('//a/@href').getall()  
    
[/code]
### Find Methods[​](<#find-methods> "Direct link to Find Methods")
[code] 
    page.find_all('div', class_='quote')       # По тегу + атрибуту  
    page.find_by_text('Read more', tag='a')    # По текстовому содержимому  
    page.find_by_regex(r'\$\d+\.\d{2}')        # По регулярному выражению  
    
[/code]
### Similar Elements[​](<#similar-elements> "Direct link to Similar Elements")
Поиск элементов со схожей структурой (полезно для списков товаров и т.д.):
[code] 
    first_product = page.css('.product')[0]  
    all_similar = first_product.find_similar()  
    
[/code]
### Navigation[​](<#navigation> "Direct link to Navigation")
[code] 
    el = page.css('.target')[0]  
    el.parent                # Родительский элемент  
    el.children              # Дочерние элементы  
    el.next_sibling          # Следующий соседний элемент  
    el.prev_sibling          # Предыдущий соседний элемент  
    
[/code]
## Python: Spider Framework[​](<#python-spider-framework> "Direct link to Python: Spider Framework")
Для многостраничного обхода с переходом по ссылкам:
[code] 
    from scrapling.spiders import Spider, Request, Response  
      
    class QuotesSpider(Spider):  
        name = "quotes"  
        start_urls = ["https://quotes.toscrape.com/"]  
        concurrent_requests = 10  
        download_delay = 1  
      
        async def parse(self, response: Response):  
            for quote in response.css('.quote'):  
                yield {  
                    "text": quote.css('.text::text').get(),  
                    "author": quote.css('.author::text').get(),  
                    "tags": quote.css('.tag::text').getall(),  
                }  
      
            next_page = response.css('.next a::attr(href)').get()  
            if next_page:  
                yield response.follow(next_page)  
      
    result = QuotesSpider().start()  
    print(f"Scraped {len(result.items)} quotes")  
    result.items.to_json("quotes.json")  
    
[/code]
### Multi-Session Spider[​](<#multi-session-spider> "Direct link to Multi-Session Spider")
Маршрутизация запросов к разным типам загрузчиков:
[code] 
    from scrapling.fetchers import FetcherSession, AsyncStealthySession  
      
    class SmartSpider(Spider):  
        name = "smart"  
        start_urls = ["https://example.com/"]  
      
        def configure_sessions(self, manager):  
            manager.add("fast", FetcherSession(impersonate="chrome"))  
            manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)  
      
        async def parse(self, response: Response):  
            for link in response.css('a::attr(href)').getall():  
                if "protected" in link:  
                    yield Request(link, sid="stealth")  
                else:  
                    yield Request(link, sid="fast", callback=self.parse)  
    
[/code]
### Pause/Resume Crawling[​](<#pauseresume-crawling> "Direct link to Pause/Resume Crawling")
[code] 
    spider = QuotesSpider(crawldir="./crawl_checkpoint")  
    spider.start()  # Ctrl+C для паузы, повторный запуск для продолжения с контрольной точки  
    
[/code]
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * **Требуется установка браузера**: выполните `scrapling install` после pip install — без этого `DynamicFetcher` и `StealthyFetcher` не будут работать
  * **Тайм-ауты**: у DynamicFetcher/StealthyFetcher тайм-аут в **миллисекундах** (по умолчанию 30000), у Fetcher — в **секундах**
  * **Обход Cloudflare**: `solve_cloudflare=True` добавляет 5-15 секунд к времени загрузки — включайте только при необходимости
  * **Использование ресурсов**: StealthyFetcher запускает реальный браузер — ограничивайте параллельное использование
  * **Юридические аспекты**: всегда проверяйте robots.txt и Условия использования сайта перед скрапингом. Данная библиотека предназначена для образовательных и исследовательских целей
  * **Версия Python**: требуется Python 3.10+


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Installation](<#installation>)
  * [Quick Reference](<#quick-reference>)
  * [CLI Usage](<#cli-usage>)
    * [Extract Static Page](<#extract-static-page>)
    * [Extract JS-Rendered Page](<#extract-js-rendered-page>)
    * [Extract Cloudflare-Protected Page](<#extract-cloudflare-protected-page>)
    * [POST Request](<#post-request>)
    * [Output Formats](<#output-formats>)
  * [Python: HTTP Scraping](<#python-http-scraping>)
    * [Single Request](<#single-request>)
    * [Session (Persistent Cookies)](<#session-persistent-cookies>)
    * [POST / PUT / DELETE](<#post--put--delete>)
    * [With Proxy](<#with-proxy>)
  * [Python: Dynamic Pages (JS-Rendered)](<#python-dynamic-pages-js-rendered>)
    * [Wait for Specific Element](<#wait-for-specific-element>)
    * [Disable Resources for Speed](<#disable-resources-for-speed>)
    * [Custom Page Automation](<#custom-page-automation>)
  * [Python: Stealth Mode (Anti-Bot Bypass)](<#python-stealth-mode-anti-bot-bypass>)
    * [Stealth Session](<#stealth-session>)
  * [Element Selection](<#element-selection>)
    * [CSS Selectors](<#css-selectors>)
    * [XPath](<#xpath>)
    * [Find Methods](<#find-methods>)
    * [Similar Elements](<#similar-elements>)
    * [Navigation](<#navigation>)
  * [Python: Spider Framework](<#python-spider-framework>)
    * [Multi-Session Spider](<#multi-session-spider>)
    * [Pause/Resume Crawling](<#pauseresume-crawling>)
  * [Pitfalls](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-scrapling -->
