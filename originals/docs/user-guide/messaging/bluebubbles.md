On this page
Connect Hermes to Apple iMessage via [BlueBubbles](<https://bluebubbles.app/>) — a free, open-source macOS server that bridges iMessage to any device.
## Prerequisites[​](<#prerequisites> "Direct link to Prerequisites")
  * A **Mac** (always on) running [BlueBubbles Server](<https://bluebubbles.app/>)
  * Apple ID signed into Messages.app on that Mac
  * BlueBubbles Server v1.0.0+ (webhooks require this version)
  * Network connectivity between Hermes and the BlueBubbles server


## Setup[​](<#setup> "Direct link to Setup")
### 1\. Install BlueBubbles Server[​](<#1-install-bluebubbles-server> "Direct link to 1. Install BlueBubbles Server")
Download and install from [bluebubbles.app](<https://bluebubbles.app/>). Complete the setup wizard — sign in with your Apple ID and configure a connection method (local network, Ngrok, Cloudflare, or Dynamic DNS).
### 2\. Get your Server URL and Password[​](<#2-get-your-server-url-and-password> "Direct link to 2. Get your Server URL and Password")
In BlueBubbles Server → **Settings → API** , note:
  * **Server URL** (e.g., `http://192.168.1.10:1234`)
  * **Server Password**


### 3\. Configure Hermes[​](<#3-configure-hermes> "Direct link to 3. Configure Hermes")
Run the setup wizard:
[code] 
    hermes gateway setup  
    
[/code]
Select **BlueBubbles (iMessage)** and enter your server URL and password.
Or set environment variables directly in `~/.hermes/.env`:
[code] 
    BLUEBUBBLES_SERVER_URL=http://192.168.1.10:1234  
    BLUEBUBBLES_PASSWORD=your-server-password  
    
[/code]
### 4\. Authorize Users[​](<#4-authorize-users> "Direct link to 4. Authorize Users")
Choose one approach:
**DM Pairing (recommended):** When someone messages your iMessage, Hermes automatically sends them a pairing code. Approve it with:
[code] 
    hermes pairing approve bluebubbles <CODE>  
    
[/code]
Use `hermes pairing list` to see pending codes and approved users.
**Pre-authorize specific users** (in `~/.hermes/.env`):
[code] 
    BLUEBUBBLES_ALLOWED_USERS=user@icloud.com,+15551234567  
    
[/code]
**Open access** (in `~/.hermes/.env`):
[code] 
    BLUEBUBBLES_ALLOW_ALL_USERS=true  
    
[/code]
### 5\. Start the Gateway[​](<#5-start-the-gateway> "Direct link to 5. Start the Gateway")
[code] 
    hermes gateway run  
    
[/code]
Hermes will connect to your BlueBubbles server, register a webhook, and start listening for iMessage messages.
## How It Works[​](<#how-it-works> "Direct link to How It Works")
[code] 
    iMessage → Messages.app → BlueBubbles Server → Webhook → Hermes  
    Hermes → BlueBubbles REST API → Messages.app → iMessage  
    
[/code]
  * **Inbound:** BlueBubbles sends webhook events to a local listener when new messages arrive. No polling — instant delivery.
  * **Outbound:** Hermes sends messages via the BlueBubbles REST API.
  * **Media:** Images, voice messages, videos, and documents are supported in both directions. Inbound attachments are downloaded and cached locally for the agent to process.


## Environment Variables[​](<#environment-variables> "Direct link to Environment Variables")
Variable| Required| Default| Description  
---|---|---|---  
`BLUEBUBBLES_SERVER_URL`| Yes| —| BlueBubbles server URL  
`BLUEBUBBLES_PASSWORD`| Yes| —| Server password  
`BLUEBUBBLES_WEBHOOK_HOST`| No| `127.0.0.1`| Webhook listener bind address  
`BLUEBUBBLES_WEBHOOK_PORT`| No| `8645`| Webhook listener port  
`BLUEBUBBLES_WEBHOOK_PATH`| No| `/bluebubbles-webhook`| Webhook URL path  
`BLUEBUBBLES_HOME_CHANNEL`| No| —| Phone/email for cron delivery  
`BLUEBUBBLES_ALLOWED_USERS`| No| —| Comma-separated authorized users  
`BLUEBUBBLES_ALLOW_ALL_USERS`| No| `false`| Allow all users  
Auto-marking messages as read is controlled by the `send_read_receipts` key under `platforms.bluebubbles.extra` in `~/.hermes/config.yaml` (default: `true`). There is no corresponding environment variable.
## Features[​](<#features> "Direct link to Features")
### Text Messaging[​](<#text-messaging> "Direct link to Text Messaging")
Send and receive iMessages. Markdown is automatically stripped for clean plain-text delivery.
### Rich Media[​](<#rich-media> "Direct link to Rich Media")
  * **Images:** Photos appear natively in the iMessage conversation
  * **Voice messages:** Audio files sent as iMessage voice messages
  * **Videos:** Video attachments
  * **Documents:** Files sent as iMessage attachments


### Tapback Reactions[​](<#tapback-reactions> "Direct link to Tapback Reactions")
Love, like, dislike, laugh, emphasize, and question reactions. Requires the BlueBubbles [Private API helper](<https://docs.bluebubbles.app/helper-bundle/installation>).
### Typing Indicators[​](<#typing-indicators> "Direct link to Typing Indicators")
Shows "typing..." in the iMessage conversation while the agent is processing. Requires Private API.
### Read Receipts[​](<#read-receipts> "Direct link to Read Receipts")
Automatically marks messages as read after processing. Requires Private API.
### Chat Addressing[​](<#chat-addressing> "Direct link to Chat Addressing")
You can address chats by email or phone number — Hermes resolves them to BlueBubbles chat GUIDs automatically. No need to use raw GUID format.
## Private API[​](<#private-api> "Direct link to Private API")
Some features require the BlueBubbles [Private API helper](<https://docs.bluebubbles.app/helper-bundle/installation>):
  * Tapback reactions
  * Typing indicators
  * Read receipts
  * Creating new chats by address


Without the Private API, basic text messaging and media still work.
## Troubleshooting[​](<#troubleshooting> "Direct link to Troubleshooting")
### "Cannot reach server"[​](<#cannot-reach-server> "Direct link to "Cannot reach server"")
  * Verify the server URL is correct and the Mac is on
  * Check that BlueBubbles Server is running
  * Ensure network connectivity (firewall, port forwarding)


### Messages not arriving[​](<#messages-not-arriving> "Direct link to Messages not arriving")
  * Check that the webhook is registered in BlueBubbles Server → Settings → API → Webhooks
  * Verify the webhook URL is reachable from the Mac
  * Check `hermes logs gateway` for webhook errors (or `hermes logs -f` to follow in real-time)


### "Private API helper not connected"[​](<#private-api-helper-not-connected> "Direct link to "Private API helper not connected"")
  * Install the Private API helper: [docs.bluebubbles.app](<https://docs.bluebubbles.app/helper-bundle/installation>)
  * Basic messaging works without it — only reactions, typing, and read receipts require it


  * [Prerequisites](<#prerequisites>)
  * [Setup](<#setup>)
    * [1\. Install BlueBubbles Server](<#1-install-bluebubbles-server>)
    * [2\. Get your Server URL and Password](<#2-get-your-server-url-and-password>)
    * [3\. Configure Hermes](<#3-configure-hermes>)
    * [4\. Authorize Users](<#4-authorize-users>)
    * [5\. Start the Gateway](<#5-start-the-gateway>)
  * [How It Works](<#how-it-works>)
  * [Environment Variables](<#environment-variables>)
  * [Features](<#features>)
    * [Text Messaging](<#text-messaging>)
    * [Rich Media](<#rich-media>)
    * [Tapback Reactions](<#tapback-reactions>)
    * [Typing Indicators](<#typing-indicators>)
    * [Read Receipts](<#read-receipts>)
    * [Chat Addressing](<#chat-addressing>)
  * [Private API](<#private-api>)
  * [Troubleshooting](<#troubleshooting>)
    * ["Cannot reach server"](<#cannot-reach-server>)
    * [Messages not arriving](<#messages-not-arriving>)
    * ["Private API helper not connected"](<#private-api-helper-not-connected>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/bluebubbles -->
