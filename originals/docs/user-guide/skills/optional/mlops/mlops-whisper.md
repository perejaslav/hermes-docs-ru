On this page
OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model sizes from tiny (39M params) to large (1550M params). Use for speech-to-text, podcast transcription, or multilingual audio processing. Best for robust, multilingual ASR.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/whisper`  
Path| `optional-skills/mlops/whisper`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `openai-whisper`, `transformers`, `torch`  
Tags| `Whisper`, `Speech Recognition`, `ASR`, `Multimodal`, `Multilingual`, `OpenAI`, `Speech-To-Text`, `Transcription`, `Translation`, `Audio Processing`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Whisper - Robust Speech Recognition
OpenAI's multilingual speech recognition model.
## When to use Whisper[​](<#when-to-use-whisper> "Direct link to When to use Whisper")
**Use when:**
  * Speech-to-text transcription (99 languages)
  * Podcast/video transcription
  * Meeting notes automation
  * Translation to English
  * Noisy audio transcription
  * Multilingual audio processing


**Metrics** :
  * **72,900+ GitHub stars**
  * 99 languages supported
  * Trained on 680,000 hours of audio
  * MIT License


**Use alternatives instead** :
  * **AssemblyAI** : Managed API, speaker diarization
  * **Deepgram** : Real-time streaming ASR
  * **Google Speech-to-Text** : Cloud-based


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Requires Python 3.8-3.11  
    pip install -U openai-whisper  
      
    # Requires ffmpeg  
    # macOS: brew install ffmpeg  
    # Ubuntu: sudo apt install ffmpeg  
    # Windows: choco install ffmpeg  
    
[/code]
### Basic transcription[​](<#basic-transcription> "Direct link to Basic transcription")
[code] 
    import whisper  
      
    # Load model  
    model = whisper.load_model("base")  
      
    # Transcribe  
    result = model.transcribe("audio.mp3")  
      
    # Print text  
    print(result["text"])  
      
    # Access segments  
    for segment in result["segments"]:  
        print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")  
    
[/code]
## Model sizes[​](<#model-sizes> "Direct link to Model sizes")
[code] 
    # Available models  
    models = ["tiny", "base", "small", "medium", "large", "turbo"]  
      
    # Load specific model  
    model = whisper.load_model("turbo")  # Fastest, good quality  
    
[/code]
Model| Parameters| English-only| Multilingual| Speed| VRAM  
---|---|---|---|---|---  
tiny| 39M| ✓| ✓| ~32x| ~1 GB  
base| 74M| ✓| ✓| ~16x| ~1 GB  
small| 244M| ✓| ✓| ~6x| ~2 GB  
medium| 769M| ✓| ✓| ~2x| ~5 GB  
large| 1550M| ✗| ✓| 1x| ~10 GB  
turbo| 809M| ✗| ✓| ~8x| ~6 GB  
**Recommendation** : Use `turbo` for best speed/quality, `base` for prototyping
## Transcription options[​](<#transcription-options> "Direct link to Transcription options")
### Language specification[​](<#language-specification> "Direct link to Language specification")
[code] 
    # Auto-detect language  
    result = model.transcribe("audio.mp3")  
      
    # Specify language (faster)  
    result = model.transcribe("audio.mp3", language="en")  
      
    # Supported: en, es, fr, de, it, pt, ru, ja, ko, zh, and 89 more  
    
[/code]
### Task selection[​](<#task-selection> "Direct link to Task selection")
[code] 
    # Transcription (default)  
    result = model.transcribe("audio.mp3", task="transcribe")  
      
    # Translation to English  
    result = model.transcribe("spanish.mp3", task="translate")  
    # Input: Spanish audio → Output: English text  
    
[/code]
### Initial prompt[​](<#initial-prompt> "Direct link to Initial prompt")
[code] 
    # Improve accuracy with context  
    result = model.transcribe(  
        "audio.mp3",  
        initial_prompt="This is a technical podcast about machine learning and AI."  
    )  
      
    # Helps with:  
    # - Technical terms  
    # - Proper nouns  
    # - Domain-specific vocabulary  
    
[/code]
### Timestamps[​](<#timestamps> "Direct link to Timestamps")
[code] 
    # Word-level timestamps  
    result = model.transcribe("audio.mp3", word_timestamps=True)  
      
    for segment in result["segments"]:  
        for word in segment["words"]:  
            print(f"{word['word']} ({word['start']:.2f}s - {word['end']:.2f}s)")  
    
[/code]
### Temperature fallback[​](<#temperature-fallback> "Direct link to Temperature fallback")
[code] 
    # Retry with different temperatures if confidence low  
    result = model.transcribe(  
        "audio.mp3",  
        temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)  
    )  
    
[/code]
## Command line usage[​](<#command-line-usage> "Direct link to Command line usage")
[code] 
    # Basic transcription  
    whisper audio.mp3  
      
    # Specify model  
    whisper audio.mp3 --model turbo  
      
    # Output formats  
    whisper audio.mp3 --output_format txt     # Plain text  
    whisper audio.mp3 --output_format srt     # Subtitles  
    whisper audio.mp3 --output_format vtt     # WebVTT  
    whisper audio.mp3 --output_format json    # JSON with timestamps  
      
    # Language  
    whisper audio.mp3 --language Spanish  
      
    # Translation  
    whisper spanish.mp3 --task translate  
    
[/code]
## Batch processing[​](<#batch-processing> "Direct link to Batch processing")
[code] 
    import os  
      
    audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]  
      
    for audio_file in audio_files:  
        print(f"Transcribing {audio_file}...")  
        result = model.transcribe(audio_file)  
      
        # Save to file  
        output_file = audio_file.replace(".mp3", ".txt")  
        with open(output_file, "w") as f:  
            f.write(result["text"])  
    
[/code]
## Real-time transcription[​](<#real-time-transcription> "Direct link to Real-time transcription")
[code] 
    # For streaming audio, use faster-whisper  
    # pip install faster-whisper  
      
    from faster_whisper import WhisperModel  
      
    model = WhisperModel("base", device="cuda", compute_type="float16")  
      
    # Transcribe with streaming  
    segments, info = model.transcribe("audio.mp3", beam_size=5)  
      
    for segment in segments:  
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")  
    
[/code]
## GPU acceleration[​](<#gpu-acceleration> "Direct link to GPU acceleration")
[code] 
    import whisper  
      
    # Automatically uses GPU if available  
    model = whisper.load_model("turbo")  
      
    # Force CPU  
    model = whisper.load_model("turbo", device="cpu")  
      
    # Force GPU  
    model = whisper.load_model("turbo", device="cuda")  
      
    # 10-20× faster on GPU  
    
[/code]
## Integration with other tools[​](<#integration-with-other-tools> "Direct link to Integration with other tools")
### Subtitle generation[​](<#subtitle-generation> "Direct link to Subtitle generation")
[code] 
    # Generate SRT subtitles  
    whisper video.mp4 --output_format srt --language English  
      
    # Output: video.srt  
    
[/code]
### With LangChain[​](<#with-langchain> "Direct link to With LangChain")
[code] 
    from langchain.document_loaders import WhisperTranscriptionLoader  
      
    loader = WhisperTranscriptionLoader(file_path="audio.mp3")  
    docs = loader.load()  
      
    # Use transcription in RAG  
    from langchain_chroma import Chroma  
    from langchain_openai import OpenAIEmbeddings  
      
    vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())  
    
[/code]
### Extract audio from video[​](<#extract-audio-from-video> "Direct link to Extract audio from video")
[code] 
    # Use ffmpeg to extract audio  
    ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav  
      
    # Then transcribe  
    whisper audio.wav  
    
[/code]
## Best practices[​](<#best-practices> "Direct link to Best practices")
  1. **Use turbo model** \- Best speed/quality for English
  2. **Specify language** \- Faster than auto-detect
  3. **Add initial prompt** \- Improves technical terms
  4. **Use GPU** \- 10-20× faster
  5. **Batch process** \- More efficient
  6. **Convert to WAV** \- Better compatibility
  7. **Split long audio** \- <30 min chunks
  8. **Check language support** \- Quality varies by language
  9. **Use faster-whisper** \- 4× faster than openai-whisper
  10. **Monitor VRAM** \- Scale model size to hardware


## Performance[​](<#performance> "Direct link to Performance")
Model| Real-time factor (CPU)| Real-time factor (GPU)  
---|---|---  
tiny| ~0.32| ~0.01  
base| ~0.16| ~0.01  
turbo| ~0.08| ~0.01  
large| ~1.0| ~0.05  
_Real-time factor: 0.1 = 10× faster than real-time_
## Language support[​](<#language-support> "Direct link to Language support")
Top-supported languages:
  * English (en)
  * Spanish (es)
  * French (fr)
  * German (de)
  * Italian (it)
  * Portuguese (pt)
  * Russian (ru)
  * Japanese (ja)
  * Korean (ko)
  * Chinese (zh)


Full list: 99 languages total
## Limitations[​](<#limitations> "Direct link to Limitations")
  1. **Hallucinations** \- May repeat or invent text
  2. **Long-form accuracy** \- Degrades on >30 min audio
  3. **Speaker identification** \- No diarization
  4. **Accents** \- Quality varies
  5. **Background noise** \- Can affect accuracy
  6. **Real-time latency** \- Not suitable for live captioning


## Resources[​](<#resources> "Direct link to Resources")
  * **GitHub** : <https://github.com/openai/whisper> ⭐ 72,900+
  * **Paper** : <https://arxiv.org/abs/2212.04356>
  * **Model Card** : <https://github.com/openai/whisper/blob/main/model-card.md>
  * **Colab** : Available in repo
  * **License** : MIT


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use Whisper](<#when-to-use-whisper>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Basic transcription](<#basic-transcription>)
  * [Model sizes](<#model-sizes>)
  * [Transcription options](<#transcription-options>)
    * [Language specification](<#language-specification>)
    * [Task selection](<#task-selection>)
    * [Initial prompt](<#initial-prompt>)
    * [Timestamps](<#timestamps>)
    * [Temperature fallback](<#temperature-fallback>)
  * [Command line usage](<#command-line-usage>)
  * [Batch processing](<#batch-processing>)
  * [Real-time transcription](<#real-time-transcription>)
  * [GPU acceleration](<#gpu-acceleration>)
  * [Integration with other tools](<#integration-with-other-tools>)
    * [Subtitle generation](<#subtitle-generation>)
    * [With LangChain](<#with-langchain>)
    * [Extract audio from video](<#extract-audio-from-video>)
  * [Best practices](<#best-practices>)
  * [Performance](<#performance>)
  * [Language support](<#language-support>)
  * [Limitations](<#limitations>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-whisper -->
