On this page
YouTube transcripts to summaries, threads, blogs.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/media/youtube-content`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# YouTube Content Tool
## When to use[​](<#when-to-use> "Direct link to When to use")
Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).
Extract transcripts from YouTube videos and convert them into useful formats.
## Setup[​](<#setup> "Direct link to Setup")
[code] 
    pip install youtube-transcript-api  
    
[/code]
## Helper Script[​](<#helper-script> "Direct link to Helper Script")
`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.
[code] 
    # JSON output with metadata  
    python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"  
      
    # Plain text (good for piping into further processing)  
    python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only  
      
    # With timestamps  
    python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps  
      
    # Specific language with fallback chain  
    python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en  
    
[/code]
## Output Formats[​](<#output-formats> "Direct link to Output Formats")
After fetching the transcript, format it based on what the user asks for:
  * **Chapters** : Group by topic shifts, output timestamped chapter list
  * **Summary** : Concise 5-10 sentence overview of the entire video
  * **Chapter summaries** : Chapters with a short paragraph summary for each
  * **Thread** : Twitter/X thread format — numbered posts, each under 280 chars
  * **Blog post** : Full article with title, sections, and key takeaways
  * **Quotes** : Notable quotes with timestamps


### Example — Chapters Output[​](<#example--chapters-output> "Direct link to Example — Chapters Output")
[code] 
    00:00 Introduction — host opens with the problem statement  
    03:45 Background — prior work and why existing solutions fall short  
    12:20 Core method — walkthrough of the proposed approach  
    24:10 Results — benchmark comparisons and key takeaways  
    31:55 Q&A — audience questions on scalability and next steps  
    
[/code]
## Workflow[​](<#workflow> "Direct link to Workflow")
  1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.
  2. **Validate** : confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
  3. **Chunk if needed** : if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
  4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
  5. **Verify** : re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.


## Error Handling[​](<#error-handling> "Direct link to Error Handling")
  * **Transcript disabled** : tell the user; suggest they check if subtitles are available on the video page.
  * **Private/unavailable video** : relay the error and ask the user to verify the URL.
  * **No matching language** : retry without `--language` to fetch any available transcript, then note the actual language to the user.
  * **Dependency missing** : run `pip install youtube-transcript-api` and retry.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use](<#when-to-use>)
  * [Setup](<#setup>)
  * [Helper Script](<#helper-script>)
  * [Output Formats](<#output-formats>)
    * [Example — Chapters Output](<#example--chapters-output>)
  * [Workflow](<#workflow>)
  * [Error Handling](<#error-handling>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/media/media-youtube-content -->
