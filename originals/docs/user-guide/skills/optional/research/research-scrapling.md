On this page
Web scraping with Scrapling - HTTP fetching, stealth browser automation, Cloudflare bypass, and spider crawling via CLI and Python.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/research/scrapling`  
Path| `optional-skills/research/scrapling`  
Version| `1.0.0`  
Author| FEUAZUR  
License| MIT  
Tags| `Web Scraping`, `Browser`, `Cloudflare`, `Stealth`, `Crawling`, `Spider`  
Related skills| [`duckduckgo-search`](</docs/user-guide/skills/optional/research/research-duckduckgo-search>), [`domain-intel`](</docs/user-guide/skills/optional/research/research-domain-intel>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Scrapling
[Scrapling](<https://github.com/D4Vinci/Scrapling>) is a web scraping framework with anti-bot bypass, stealth browser automation, and a spider framework. It provides three fetching strategies (HTTP, dynamic JS, stealth/Cloudflare) and a full CLI.
**This skill is for educational and research purposes only.** Users must comply with local/international data scraping laws and respect website Terms of Service.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Scraping static HTML pages (faster than browser tools)
  * Scraping JS-rendered pages that need a real browser
  * Bypassing Cloudflare Turnstile or bot detection
  * Crawling multiple pages with a spider
  * When the built-in `web_extract` tool does not return the data you need


## Installation[​](<#installation> "Direct link to Installation")
[code] 
    pip install "scrapling[all]"  
    scrapling install  
    
[/code]
Minimal install (HTTP only, no browser):
[code] 
    pip install scrapling  
    
[/code]
With browser automation only:
[code] 
    pip install "scrapling[fetchers]"  
    scrapling install  
    
[/code]
## Quick Reference[​](<#quick-reference> "Direct link to Quick Reference")
Approach| Class| Use When  
---|---|---  
HTTP| `Fetcher` / `FetcherSession`| Static pages, APIs, fast bulk requests  
Dynamic| `DynamicFetcher` / `DynamicSession`| JS-rendered content, SPAs  
Stealth| `StealthyFetcher` / `StealthySession`| Cloudflare, anti-bot protected sites  
Spider| `Spider`| Multi-page crawling with link following  
## CLI Usage[​](<#cli-usage> "Direct link to CLI Usage")
### Extract Static Page[​](<#extract-static-page> "Direct link to Extract Static Page")
[code] 
    scrapling extract get 'https://example.com' output.md  
    
[/code]
With CSS selector and browser impersonation:
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
The output format is determined by the file extension:
  * `.html` \-- raw HTML
  * `.md` \-- converted to Markdown
  * `.txt` \-- plain text
  * `.json` / `.jsonl` \-- JSON


## Python: HTTP Scraping[​](<#python-http-scraping> "Direct link to Python: HTTP Scraping")
### Single Request[​](<#single-request> "Direct link to Single Request")
[code] 
    from scrapling.fetchers import Fetcher  
      
    page = Fetcher.get('https://quotes.toscrape.com/')  
    quotes = page.css('.quote .text::text').getall()  
    for q in quotes:  
        print(q)  
    
[/code]
### Session (Persistent Cookies)[​](<#session-persistent-cookies> "Direct link to Session \(Persistent Cookies\)")
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
## Python: Dynamic Pages (JS-Rendered)[​](<#python-dynamic-pages-js-rendered> "Direct link to Python: Dynamic Pages \(JS-Rendered\)")
For pages that require JavaScript execution (SPAs, lazy-loaded content):
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
Blocks fonts, images, media, stylesheets (~25% faster):
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
## Python: Stealth Mode (Anti-Bot Bypass)[​](<#python-stealth-mode-anti-bot-bypass> "Direct link to Python: Stealth Mode \(Anti-Bot Bypass\)")
For Cloudflare-protected or heavily fingerprinted sites:
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
All fetchers return a `Selector` object with these methods:
### CSS Selectors[​](<#css-selectors> "Direct link to CSS Selectors")
[code] 
    page.css('h1::text').get()              # First h1 text  
    page.css('a::attr(href)').getall()      # All link hrefs  
    page.css('.quote .text::text').getall() # Nested selection  
    
[/code]
### XPath[​](<#xpath> "Direct link to XPath")
[code] 
    page.xpath('//div[@class="content"]/text()').getall()  
    page.xpath('//a/@href').getall()  
    
[/code]
### Find Methods[​](<#find-methods> "Direct link to Find Methods")
[code] 
    page.find_all('div', class_='quote')       # By tag + attribute  
    page.find_by_text('Read more', tag='a')    # By text content  
    page.find_by_regex(r'\$\d+\.\d{2}')       # By regex pattern  
    
[/code]
### Similar Elements[​](<#similar-elements> "Direct link to Similar Elements")
Find elements with similar structure (useful for product listings, etc.):
[code] 
    first_product = page.css('.product')[0]  
    all_similar = first_product.find_similar()  
    
[/code]
### Navigation[​](<#navigation> "Direct link to Navigation")
[code] 
    el = page.css('.target')[0]  
    el.parent                # Parent element  
    el.children              # Child elements  
    el.next_sibling          # Next sibling  
    el.prev_sibling          # Previous sibling  
    
[/code]
## Python: Spider Framework[​](<#python-spider-framework> "Direct link to Python: Spider Framework")
For multi-page crawling with link following:
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
Route requests to different fetcher types:
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
    spider.start()  # Ctrl+C to pause, re-run to resume from checkpoint  
    
[/code]
## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * **Browser install required** : run `scrapling install` after pip install -- without it, `DynamicFetcher` and `StealthyFetcher` will fail
  * **Timeouts** : DynamicFetcher/StealthyFetcher timeout is in **milliseconds** (default 30000), Fetcher timeout is in **seconds**
  * **Cloudflare bypass** : `solve_cloudflare=True` adds 5-15 seconds to fetch time -- only enable when needed
  * **Resource usage** : StealthyFetcher runs a real browser -- limit concurrent usage
  * **Legal** : always check robots.txt and website ToS before scraping. This library is for educational and research purposes
  * **Python version** : requires Python 3.10+


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
