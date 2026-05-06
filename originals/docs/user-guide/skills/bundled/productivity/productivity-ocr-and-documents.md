On this page
Extract text from PDFs/scans (pymupdf, marker-pdf).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Bundled (installed by default)  
Path| `skills/productivity/ocr-and-documents`  
Version| `2.3.0`  
Author| Hermes Agent  
License| MIT  
Tags| `PDF`, `Documents`, `Research`, `Arxiv`, `Text-Extraction`, `OCR`  
Related skills| [`powerpoint`](</docs/user-guide/skills/bundled/productivity/productivity-powerpoint>)  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# PDF & Document Extraction
For DOCX: use `python-docx` (parses actual document structure, far better than OCR). For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support). This skill covers **PDFs and scanned documents**.
## Step 1: Remote URL Available?[​](<#step-1-remote-url-available> "Direct link to Step 1: Remote URL Available?")
If the document has a URL, **always try`web_extract` first**:
[code] 
    web_extract(urls=["https://arxiv.org/pdf/2402.03300"])  
    web_extract(urls=["https://example.com/report.pdf"])  
    
[/code]
This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.
Only use local extraction when: the file is local, web_extract fails, or you need batch processing.
## Step 2: Choose Local Extractor[​](<#step-2-choose-local-extractor> "Direct link to Step 2: Choose Local Extractor")
Feature| pymupdf (~25MB)| marker-pdf (~3-5GB)  
---|---|---  
**Text-based PDF**|  ✅| ✅  
**Scanned PDF (OCR)**|  ❌| ✅ (90+ languages)  
**Tables**|  ✅ (basic)| ✅ (high accuracy)  
**Equations / LaTeX**|  ❌| ✅  
**Code blocks**|  ❌| ✅  
**Forms**|  ❌| ✅  
**Headers/footers removal**|  ❌| ✅  
**Reading order detection**|  ❌| ✅  
**Images extraction**|  ✅ (embedded)| ✅ (with context)  
**Images → text (OCR)**|  ❌| ✅  
**EPUB**|  ✅| ✅  
**Markdown output**|  ✅ (via pymupdf4llm)| ✅ (native, higher quality)  
**Install size**|  ~25MB| ~3-5GB (PyTorch + models)  
**Speed**|  Instant| ~1-14s/page (CPU), ~0.2s/page (GPU)  
**Decision** : Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.
If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."
* * *
## pymupdf (lightweight)[​](<#pymupdf-lightweight> "Direct link to pymupdf \(lightweight\)")
[code] 
    pip install pymupdf pymupdf4llm  
    
[/code]
**Via helper script** :
[code] 
    python scripts/extract_pymupdf.py document.pdf              # Plain text  
    python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown  
    python scripts/extract_pymupdf.py document.pdf --tables      # Tables  
    python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images  
    python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages  
    python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages  
    
[/code]
**Inline** :
[code] 
    python3 -c "  
    import pymupdf  
    doc = pymupdf.open('document.pdf')  
    for page in doc:  
        print(page.get_text())  
    "  
    
[/code]
* * *
## marker-pdf (high-quality OCR)[​](<#marker-pdf-high-quality-ocr> "Direct link to marker-pdf \(high-quality OCR\)")
[code] 
    # Check disk space first  
    python scripts/extract_marker.py --check  
      
    pip install marker-pdf  
    
[/code]
**Via helper script** :
[code] 
    python scripts/extract_marker.py document.pdf                # Markdown  
    python scripts/extract_marker.py document.pdf --json         # JSON with metadata  
    python scripts/extract_marker.py document.pdf --output_dir out/  # Save images  
    python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)  
    python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy  
    
[/code]
**CLI** (installed with marker-pdf):
[code] 
    marker_single document.pdf --output_dir ./output  
    marker /path/to/folder --workers 4    # Batch  
    
[/code]
* * *
## Arxiv Papers[​](<#arxiv-papers> "Direct link to Arxiv Papers")
[code] 
    # Abstract only (fast)  
    web_extract(urls=["https://arxiv.org/abs/2402.03300"])  
      
    # Full paper  
    web_extract(urls=["https://arxiv.org/pdf/2402.03300"])  
      
    # Search  
    web_search(query="arxiv GRPO reinforcement learning 2026")  
    
[/code]
## Split, Merge & Search[​](<#split-merge--search> "Direct link to Split, Merge & Search")
pymupdf handles these natively — use `execute_code` or inline Python:
[code] 
    # Split: extract pages 1-5 to a new PDF  
    import pymupdf  
    doc = pymupdf.open("report.pdf")  
    new = pymupdf.open()  
    for i in range(5):  
        new.insert_pdf(doc, from_page=i, to_page=i)  
    new.save("pages_1-5.pdf")  
    
[/code]
[code] 
    # Merge multiple PDFs  
    import pymupdf  
    result = pymupdf.open()  
    for path in ["a.pdf", "b.pdf", "c.pdf"]:  
        result.insert_pdf(pymupdf.open(path))  
    result.save("merged.pdf")  
    
[/code]
[code] 
    # Search for text across all pages  
    import pymupdf  
    doc = pymupdf.open("report.pdf")  
    for i, page in enumerate(doc):  
        results = page.search_for("revenue")  
        if results:  
            print(f"Page {i+1}: {len(results)} match(es)")  
            print(page.get_text("text"))  
    
[/code]
No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.
* * *
## Notes[​](<#notes> "Direct link to Notes")
  * `web_extract` is always first choice for URLs
  * pymupdf is the safe default — instant, no models, works everywhere
  * marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
  * Both helper scripts accept `--help` for full usage
  * marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
  * For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
  * For PowerPoint: see the `powerpoint` skill (uses python-pptx)


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [Step 1: Remote URL Available?](<#step-1-remote-url-available>)
  * [Step 2: Choose Local Extractor](<#step-2-choose-local-extractor>)
  * [pymupdf (lightweight)](<#pymupdf-lightweight>)
  * [marker-pdf (high-quality OCR)](<#marker-pdf-high-quality-ocr>)
  * [Arxiv Papers](<#arxiv-papers>)
  * [Split, Merge & Search](<#split-merge--search>)
  * [Notes](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-ocr-and-documents -->
