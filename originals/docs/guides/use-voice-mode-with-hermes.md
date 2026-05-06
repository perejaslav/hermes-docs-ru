On this page
This guide is the practical companion to the [Voice Mode feature reference](</docs/user-guide/features/voice-mode>).
If the feature page explains what voice mode can do, this guide shows how to actually use it well.
## What voice mode is good for[​](<#what-voice-mode-is-good-for> "Direct link to What voice mode is good for")
Voice mode is especially useful when:
  * you want a hands-free CLI workflow
  * you want spoken responses in Telegram or Discord
  * you want Hermes sitting in a Discord voice channel for live conversation
  * you want quick idea capture, debugging, or back-and-forth while walking around instead of typing


## Choose your voice mode setup[​](<#choose-your-voice-mode-setup> "Direct link to Choose your voice mode setup")
There are really three different voice experiences in Hermes.
Mode| Best for| Platform  
---|---|---  
Interactive microphone loop| Personal hands-free use while coding or researching| CLI  
Voice replies in chat| Spoken responses alongside normal messaging| Telegram, Discord  
Live voice channel bot| Group or personal live conversation in a VC| Discord voice channels  
A good path is:
  1. get text working first
  2. enable voice replies second
  3. move to Discord voice channels last if you want the full experience


## Step 1: make sure normal Hermes works first[​](<#step-1-make-sure-normal-hermes-works-first> "Direct link to Step 1: make sure normal Hermes works first")
Before touching voice mode, verify that:
  * Hermes starts
  * your provider is configured
  * the agent can answer text prompts normally


[code] 
    hermes  
    
[/code]
Ask something simple:
[code] 
    What tools do you have available?  
    
[/code]
If that is not solid yet, fix text mode first.
## Step 2: install the right extras[​](<#step-2-install-the-right-extras> "Direct link to Step 2: install the right extras")
### CLI microphone + playback[​](<#cli-microphone--playback> "Direct link to CLI microphone + playback")
[code] 
    pip install "hermes-agent[voice]"  
    
[/code]
### Messaging platforms[​](<#messaging-platforms> "Direct link to Messaging platforms")
[code] 
    pip install "hermes-agent[messaging]"  
    
[/code]
### Premium ElevenLabs TTS[​](<#premium-elevenlabs-tts> "Direct link to Premium ElevenLabs TTS")
[code] 
    pip install "hermes-agent[tts-premium]"  
    
[/code]
### Local NeuTTS (optional)[​](<#local-neutts-optional> "Direct link to Local NeuTTS \(optional\)")
[code] 
    python -m pip install -U neutts[all]  
    
[/code]
### Everything[​](<#everything> "Direct link to Everything")
[code] 
    pip install "hermes-agent[all]"  
    
[/code]
## Step 3: install system dependencies[​](<#step-3-install-system-dependencies> "Direct link to Step 3: install system dependencies")
### macOS[​](<#macos> "Direct link to macOS")
[code] 
    brew install portaudio ffmpeg opus  
    brew install espeak-ng  
    
[/code]
### Ubuntu / Debian[​](<#ubuntu--debian> "Direct link to Ubuntu / Debian")
[code] 
    sudo apt install portaudio19-dev ffmpeg libopus0  
    sudo apt install espeak-ng  
    
[/code]
Why these matter:
  * `portaudio` → microphone input / playback for CLI voice mode
  * `ffmpeg` → audio conversion for TTS and messaging delivery
  * `opus` → Discord voice codec support
  * `espeak-ng` → phonemizer backend for NeuTTS


## Step 4: choose STT and TTS providers[​](<#step-4-choose-stt-and-tts-providers> "Direct link to Step 4: choose STT and TTS providers")
Hermes supports both local and cloud speech stacks.
### Easiest / cheapest setup[​](<#easiest--cheapest-setup> "Direct link to Easiest / cheapest setup")
Use local STT and free Edge TTS:
  * STT provider: `local`
  * TTS provider: `edge`


This is usually the best place to start.
### Environment file example[​](<#environment-file-example> "Direct link to Environment file example")
Add to `~/.hermes/.env`:
[code] 
    # Cloud STT options (local needs no key)  
    GROQ_API_KEY=***  
    VOICE_TOOLS_OPENAI_KEY=***  
      
    # Premium TTS (optional)  
    ELEVENLABS_API_KEY=***  
    
[/code]
### Provider recommendations[​](<#provider-recommendations> "Direct link to Provider recommendations")
#### Speech-to-text[​](<#speech-to-text> "Direct link to Speech-to-text")
  * `local` → best default for privacy and zero-cost use
  * `groq` → very fast cloud transcription
  * `openai` → good paid fallback


#### Text-to-speech[​](<#text-to-speech> "Direct link to Text-to-speech")
  * `edge` → free and good enough for most users
  * `neutts` → free local/on-device TTS
  * `elevenlabs` → best quality
  * `openai` → good middle ground
  * `mistral` → multilingual, native Opus


### If you use `hermes setup`[​](<#if-you-use-hermes-setup> "Direct link to if-you-use-hermes-setup")
If you choose NeuTTS in the setup wizard, Hermes checks whether `neutts` is already installed. If it is missing, the wizard tells you NeuTTS needs the Python package `neutts` and the system package `espeak-ng`, offers to install them for you, installs `espeak-ng` with your platform package manager, and then runs:
[code] 
    python -m pip install -U neutts[all]  
    
[/code]
If you skip that install or it fails, the wizard falls back to Edge TTS.
## Step 5: recommended config[​](<#step-5-recommended-config> "Direct link to Step 5: recommended config")
[code] 
    voice:  
      record_key: "ctrl+b"  
      max_recording_seconds: 120  
      auto_tts: false  
      beep_enabled: true  
      silence_threshold: 200  
      silence_duration: 3.0  
      
    stt:  
      provider: "local"  
      local:  
        model: "base"  
      
    tts:  
      provider: "edge"  
      edge:  
        voice: "en-US-AriaNeural"  
    
[/code]
This is a good conservative default for most people.
If you want local TTS instead, switch the `tts` block to:
[code] 
    tts:  
      provider: "neutts"  
      neutts:  
        ref_audio: ''  
        ref_text: ''  
        model: neuphonic/neutts-air-q4-gguf  
        device: cpu  
    
[/code]
## Use case 1: CLI voice mode[​](<#use-case-1-cli-voice-mode> "Direct link to Use case 1: CLI voice mode")
## Turn it on[​](<#turn-it-on> "Direct link to Turn it on")
Start Hermes:
[code] 
    hermes  
    
[/code]
Inside the CLI:
[code] 
    /voice on  
    
[/code]
### Recording flow[​](<#recording-flow> "Direct link to Recording flow")
Default key:
  * `Ctrl+B`


Workflow:
  1. press `Ctrl+B`
  2. speak
  3. wait for silence detection to stop recording automatically
  4. Hermes transcribes and responds
  5. if TTS is on, it speaks the answer
  6. the loop can automatically restart for continuous use


### Useful commands[​](<#useful-commands> "Direct link to Useful commands")
[code] 
    /voice  
    /voice on  
    /voice off  
    /voice tts  
    /voice status  
    
[/code]
### Good CLI workflows[​](<#good-cli-workflows> "Direct link to Good CLI workflows")
#### Walk-up debugging[​](<#walk-up-debugging> "Direct link to Walk-up debugging")
Say:
[code] 
    I keep getting a docker permission error. Help me debug it.  
    
[/code]
Then continue hands-free:
  * "Read the last error again"
  * "Explain the root cause in simpler terms"
  * "Now give me the exact fix"


#### Research / brainstorming[​](<#research--brainstorming> "Direct link to Research / brainstorming")
Great for:
  * walking around while thinking
  * dictating half-formed ideas
  * asking Hermes to structure your thoughts in real time


#### Accessibility / low-typing sessions[​](<#accessibility--low-typing-sessions> "Direct link to Accessibility / low-typing sessions")
If typing is inconvenient, voice mode is one of the fastest ways to stay in the full Hermes loop.
## Tuning CLI behavior[​](<#tuning-cli-behavior> "Direct link to Tuning CLI behavior")
### Silence threshold[​](<#silence-threshold> "Direct link to Silence threshold")
If Hermes starts/stops too aggressively, tune:
[code] 
    voice:  
      silence_threshold: 250  
    
[/code]
Higher threshold = less sensitive.
### Silence duration[​](<#silence-duration> "Direct link to Silence duration")
If you pause a lot between sentences, increase:
[code] 
    voice:  
      silence_duration: 4.0  
    
[/code]
### Record key[​](<#record-key> "Direct link to Record key")
If `Ctrl+B` conflicts with your terminal or tmux habits:
[code] 
    voice:  
      record_key: "ctrl+space"  
    
[/code]
## Use case 2: voice replies in Telegram or Discord[​](<#use-case-2-voice-replies-in-telegram-or-discord> "Direct link to Use case 2: voice replies in Telegram or Discord")
This mode is simpler than full voice channels.
Hermes stays a normal chat bot, but can speak replies.
### Start the gateway[​](<#start-the-gateway> "Direct link to Start the gateway")
[code] 
    hermes gateway  
    
[/code]
### Turn on voice replies[​](<#turn-on-voice-replies> "Direct link to Turn on voice replies")
Inside Telegram or Discord:
[code] 
    /voice on  
    
[/code]
or
[code] 
    /voice tts  
    
[/code]
### Modes[​](<#modes> "Direct link to Modes")
Mode| Meaning  
---|---  
`off`| text only  
`voice_only`| speak only when the user sent voice  
`all`| speak every reply  
### When to use which mode[​](<#when-to-use-which-mode> "Direct link to When to use which mode")
  * `/voice on` if you want spoken replies only for voice-originating messages
  * `/voice tts` if you want a full spoken assistant all the time


### Good messaging workflows[​](<#good-messaging-workflows> "Direct link to Good messaging workflows")
#### Telegram assistant on your phone[​](<#telegram-assistant-on-your-phone> "Direct link to Telegram assistant on your phone")
Use when:
  * you are away from your machine
  * you want to send voice notes and get quick spoken replies
  * you want Hermes to function like a portable research or ops assistant


#### Discord DMs with spoken output[​](<#discord-dms-with-spoken-output> "Direct link to Discord DMs with spoken output")
Useful when you want private interaction without server-channel mention behavior.
## Use case 3: Discord voice channels[​](<#use-case-3-discord-voice-channels> "Direct link to Use case 3: Discord voice channels")
This is the most advanced mode.
Hermes joins a Discord VC, listens to user speech, transcribes it, runs the normal agent pipeline, and speaks replies back into the channel.
## Required Discord permissions[​](<#required-discord-permissions> "Direct link to Required Discord permissions")
In addition to the normal text-bot setup, make sure the bot has:
  * Connect
  * Speak
  * preferably Use Voice Activity


Also enable privileged intents in the Developer Portal:
  * Presence Intent
  * Server Members Intent
  * Message Content Intent


## Join and leave[​](<#join-and-leave> "Direct link to Join and leave")
In a Discord text channel where the bot is present:
[code] 
    /voice join  
    /voice leave  
    /voice status  
    
[/code]
### What happens when joined[​](<#what-happens-when-joined> "Direct link to What happens when joined")
  * users speak in the VC
  * Hermes detects speech boundaries
  * transcripts are posted in the associated text channel
  * Hermes responds in text and audio
  * the text channel is the one where `/voice join` was issued


### Best practices for Discord VC use[​](<#best-practices-for-discord-vc-use> "Direct link to Best practices for Discord VC use")
  * keep `DISCORD_ALLOWED_USERS` tight
  * use a dedicated bot/testing channel at first
  * verify STT and TTS work in ordinary text-chat voice mode before trying VC mode


## Voice quality recommendations[​](<#voice-quality-recommendations> "Direct link to Voice quality recommendations")
### Best quality setup[​](<#best-quality-setup> "Direct link to Best quality setup")
  * STT: local `large-v3` or Groq `whisper-large-v3`
  * TTS: ElevenLabs


### Best speed / convenience setup[​](<#best-speed--convenience-setup> "Direct link to Best speed / convenience setup")
  * STT: local `base` or Groq
  * TTS: Edge


### Best zero-cost setup[​](<#best-zero-cost-setup> "Direct link to Best zero-cost setup")
  * STT: local
  * TTS: Edge


## Common failure modes[​](<#common-failure-modes> "Direct link to Common failure modes")
### "No audio device found"[​](<#no-audio-device-found> "Direct link to "No audio device found"")
Install `portaudio`.
### "Bot joins but hears nothing"[​](<#bot-joins-but-hears-nothing> "Direct link to "Bot joins but hears nothing"")
Check:
  * your Discord user ID is in `DISCORD_ALLOWED_USERS`
  * you are not muted
  * privileged intents are enabled
  * the bot has Connect/Speak permissions


### "It transcribes but does not speak"[​](<#it-transcribes-but-does-not-speak> "Direct link to "It transcribes but does not speak"")
Check:
  * TTS provider config
  * API key / quota for ElevenLabs or OpenAI
  * `ffmpeg` install for Edge conversion paths


### "Whisper outputs garbage"[​](<#whisper-outputs-garbage> "Direct link to "Whisper outputs garbage"")
Try:
  * quieter environment
  * higher `silence_threshold`
  * different STT provider/model
  * shorter, clearer utterances


### "It works in DMs but not in server channels"[​](<#it-works-in-dms-but-not-in-server-channels> "Direct link to "It works in DMs but not in server channels"")
That is often mention policy.
By default, the bot needs an `@mention` in Discord server text channels unless configured otherwise.
## Suggested first-week setup[​](<#suggested-first-week-setup> "Direct link to Suggested first-week setup")
If you want the shortest path to success:
  1. get text Hermes working
  2. install `hermes-agent[voice]`
  3. use CLI voice mode with local STT + Edge TTS
  4. then enable `/voice on` in Telegram or Discord
  5. only after that, try Discord VC mode


That progression keeps the debugging surface small.
## Where to read next[​](<#where-to-read-next> "Direct link to Where to read next")
  * [Voice Mode feature reference](</docs/user-guide/features/voice-mode>)
  * [Messaging Gateway](</docs/user-guide/messaging>)
  * [Discord setup](</docs/user-guide/messaging/discord>)
  * [Telegram setup](</docs/user-guide/messaging/telegram>)
  * [Configuration](</docs/user-guide/configuration>)


  * [What voice mode is good for](<#what-voice-mode-is-good-for>)
  * [Choose your voice mode setup](<#choose-your-voice-mode-setup>)
  * [Step 1: make sure normal Hermes works first](<#step-1-make-sure-normal-hermes-works-first>)
  * [Step 2: install the right extras](<#step-2-install-the-right-extras>)
    * [CLI microphone + playback](<#cli-microphone--playback>)
    * [Messaging platforms](<#messaging-platforms>)
    * [Premium ElevenLabs TTS](<#premium-elevenlabs-tts>)
    * [Local NeuTTS (optional)](<#local-neutts-optional>)
    * [Everything](<#everything>)
  * [Step 3: install system dependencies](<#step-3-install-system-dependencies>)
    * [macOS](<#macos>)
    * [Ubuntu / Debian](<#ubuntu--debian>)
  * [Step 4: choose STT and TTS providers](<#step-4-choose-stt-and-tts-providers>)
    * [Easiest / cheapest setup](<#easiest--cheapest-setup>)
    * [Environment file example](<#environment-file-example>)
    * [Provider recommendations](<#provider-recommendations>)
    * [If you use `hermes setup`](<#if-you-use-hermes-setup>)
  * [Step 5: recommended config](<#step-5-recommended-config>)
  * [Use case 1: CLI voice mode](<#use-case-1-cli-voice-mode>)
  * [Turn it on](<#turn-it-on>)
    * [Recording flow](<#recording-flow>)
    * [Useful commands](<#useful-commands>)
    * [Good CLI workflows](<#good-cli-workflows>)
  * [Tuning CLI behavior](<#tuning-cli-behavior>)
    * [Silence threshold](<#silence-threshold>)
    * [Silence duration](<#silence-duration>)
    * [Record key](<#record-key>)
  * [Use case 2: voice replies in Telegram or Discord](<#use-case-2-voice-replies-in-telegram-or-discord>)
    * [Start the gateway](<#start-the-gateway>)
    * [Turn on voice replies](<#turn-on-voice-replies>)
    * [Modes](<#modes>)
    * [When to use which mode](<#when-to-use-which-mode>)
    * [Good messaging workflows](<#good-messaging-workflows>)
  * [Use case 3: Discord voice channels](<#use-case-3-discord-voice-channels>)
  * [Required Discord permissions](<#required-discord-permissions>)
  * [Join and leave](<#join-and-leave>)
    * [What happens when joined](<#what-happens-when-joined>)
    * [Best practices for Discord VC use](<#best-practices-for-discord-vc-use>)
  * [Voice quality recommendations](<#voice-quality-recommendations>)
    * [Best quality setup](<#best-quality-setup>)
    * [Best speed / convenience setup](<#best-speed--convenience-setup>)
    * [Best zero-cost setup](<#best-zero-cost-setup>)
  * [Common failure modes](<#common-failure-modes>)
    * ["No audio device found"](<#no-audio-device-found>)
    * ["Bot joins but hears nothing"](<#bot-joins-but-hears-nothing>)
    * ["It transcribes but does not speak"](<#it-transcribes-but-does-not-speak>)
    * ["Whisper outputs garbage"](<#whisper-outputs-garbage>)
    * ["It works in DMs but not in server channels"](<#it-works-in-dms-but-not-in-server-channels>)
  * [Suggested first-week setup](<#suggested-first-week-setup>)
  * [Where to read next](<#where-to-read-next>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/guides/use-voice-mode-with-hermes -->
