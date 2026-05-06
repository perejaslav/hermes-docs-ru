On this page
When using [OpenRouter](<https://openrouter.ai>) as your LLM provider, Hermes Agent supports **provider routing** — fine-grained control over which underlying AI providers handle your requests and how they're prioritized.
OpenRouter routes requests to many providers (e.g., Anthropic, Google, AWS Bedrock, Together AI). Provider routing lets you optimize for cost, speed, quality, or enforce specific provider requirements.
## Configuration[​](<#configuration> "Direct link to Configuration")
Add a `provider_routing` section to your `~/.hermes/config.yaml`:
[code] 
    provider_routing:  
      sort: "price"           # How to rank providers  
      only: []                # Whitelist: only use these providers  
      ignore: []              # Blacklist: never use these providers  
      order: []               # Explicit provider priority order  
      require_parameters: false  # Only use providers that support all parameters  
      data_collection: null   # Control data collection ("allow" or "deny")  
    
[/code]
info
Provider routing only applies when using OpenRouter. It has no effect with direct provider connections (e.g., connecting directly to the Anthropic API).
## Options[​](<#options> "Direct link to Options")
### `sort`[​](<#sort> "Direct link to sort")
Controls how OpenRouter ranks available providers for your request.
Value| Description  
---|---  
`"price"`| Cheapest provider first  
`"throughput"`| Fastest tokens-per-second first  
`"latency"`| Lowest time-to-first-token first
[code] 
    provider_routing:  
      sort: "price"  
    
[/code]  
### `only`[​](<#only> "Direct link to only")
Whitelist of provider names. When set, **only** these providers will be used. All others are excluded.
[code] 
    provider_routing:  
      only:  
        - "Anthropic"  
        - "Google"  
    
[/code]
### `ignore`[​](<#ignore> "Direct link to ignore")
Blacklist of provider names. These providers will **never** be used, even if they offer the cheapest or fastest option.
[code] 
    provider_routing:  
      ignore:  
        - "Together"  
        - "DeepInfra"  
    
[/code]
### `order`[​](<#order> "Direct link to order")
Explicit priority order. Providers listed first are preferred. Unlisted providers are used as fallbacks.
[code] 
    provider_routing:  
      order:  
        - "Anthropic"  
        - "Google"  
        - "AWS Bedrock"  
    
[/code]
### `require_parameters`[​](<#require_parameters> "Direct link to require_parameters")
When `true`, OpenRouter will only route to providers that support **all** parameters in your request (like `temperature`, `top_p`, `tools`, etc.). This avoids silent parameter drops.
[code] 
    provider_routing:  
      require_parameters: true  
    
[/code]
### `data_collection`[​](<#data_collection> "Direct link to data_collection")
Controls whether providers can use your prompts for training. Options are `"allow"` or `"deny"`.
[code] 
    provider_routing:  
      data_collection: "deny"  
    
[/code]
## Practical Examples[​](<#practical-examples> "Direct link to Practical Examples")
### Optimize for Cost[​](<#optimize-for-cost> "Direct link to Optimize for Cost")
Route to the cheapest available provider. Good for high-volume usage and development:
[code] 
    provider_routing:  
      sort: "price"  
    
[/code]
### Optimize for Speed[​](<#optimize-for-speed> "Direct link to Optimize for Speed")
Prioritize low-latency providers for interactive use:
[code] 
    provider_routing:  
      sort: "latency"  
    
[/code]
### Optimize for Throughput[​](<#optimize-for-throughput> "Direct link to Optimize for Throughput")
Best for long-form generation where tokens-per-second matters:
[code] 
    provider_routing:  
      sort: "throughput"  
    
[/code]
### Lock to Specific Providers[​](<#lock-to-specific-providers> "Direct link to Lock to Specific Providers")
Ensure all requests go through a specific provider for consistency:
[code] 
    provider_routing:  
      only:  
        - "Anthropic"  
    
[/code]
### Avoid Specific Providers[​](<#avoid-specific-providers> "Direct link to Avoid Specific Providers")
Exclude providers you don't want to use (e.g., for data privacy):
[code] 
    provider_routing:  
      ignore:  
        - "Together"  
        - "Lepton"  
      data_collection: "deny"  
    
[/code]
### Preferred Order with Fallbacks[​](<#preferred-order-with-fallbacks> "Direct link to Preferred Order with Fallbacks")
Try your preferred providers first, fall back to others if unavailable:
[code] 
    provider_routing:  
      order:  
        - "Anthropic"  
        - "Google"  
      require_parameters: true  
    
[/code]
## How It Works[​](<#how-it-works> "Direct link to How It Works")
Provider routing preferences are passed to the OpenRouter API via the `extra_body.provider` field on every API call. This applies to both:
  * **CLI mode** — configured in `~/.hermes/config.yaml`, loaded at startup
  * **Gateway mode** — same config file, loaded when the gateway starts


The routing config is read from `config.yaml` and passed as parameters when creating the `AIAgent`:
[code] 
    providers_allowed  ← from provider_routing.only  
    providers_ignored  ← from provider_routing.ignore  
    providers_order    ← from provider_routing.order  
    provider_sort      ← from provider_routing.sort  
    provider_require_parameters ← from provider_routing.require_parameters  
    provider_data_collection    ← from provider_routing.data_collection  
    
[/code]
tip
You can combine multiple options. For example, sort by price but exclude certain providers and require parameter support:
[code]
    provider_routing:  
      sort: "price"  
      ignore: ["Together"]  
      require_parameters: true  
      data_collection: "deny"  
    
[/code]
## Default Behavior[​](<#default-behavior> "Direct link to Default Behavior")
When no `provider_routing` section is configured (the default), OpenRouter uses its own default routing logic, which generally balances cost and availability automatically.
Provider Routing vs. Fallback Models
Provider routing controls which **sub-providers within OpenRouter** handle your requests. For automatic failover to an entirely different provider when your primary model fails, see [Fallback Providers](</docs/user-guide/features/fallback-providers>).
  * [Configuration](<#configuration>)
  * [Options](<#options>)
    * [`sort`](<#sort>)
    * [`only`](<#only>)
    * [`ignore`](<#ignore>)
    * [`order`](<#order>)
    * [`require_parameters`](<#require_parameters>)
    * [`data_collection`](<#data_collection>)
  * [Practical Examples](<#practical-examples>)
    * [Optimize for Cost](<#optimize-for-cost>)
    * [Optimize for Speed](<#optimize-for-speed>)
    * [Optimize for Throughput](<#optimize-for-throughput>)
    * [Lock to Specific Providers](<#lock-to-specific-providers>)
    * [Avoid Specific Providers](<#avoid-specific-providers>)
    * [Preferred Order with Fallbacks](<#preferred-order-with-fallbacks>)
  * [How It Works](<#how-it-works>)
  * [Default Behavior](<#default-behavior>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing -->
