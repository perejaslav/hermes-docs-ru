On this page
Модель OpenAI, соединяющая зрение и язык. Позволяет выполнять zero-shot классификацию изображений, сопоставление изображений с текстом и кросс-модальный поиск. Обучалась на 400 миллионах пар изображение-текст. Используйте для поиска изображений, модерации контента или задач на стыке зрения и языка без тонкой настройки. Лучше всего подходит для общего понимания изображений.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/clip`  
Path| `optional-skills/mlops/clip`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `transformers`, `torch`, `pillow`  
Tags| `Multimodal`, `CLIP`, `Vision-Language`, `Zero-Shot`, `Image Classification`, `OpenAI`, `Image Search`, `Cross-Modal Retrieval`, `Content Moderation`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# CLIP - Contrastive Language-Image Pre-Training
Модель OpenAI, понимающая изображения на естественном языке.
## When to use CLIP[​](<#when-to-use-clip> "Direct link to When to use CLIP")
**Используйте когда:**
  * Zero-shot классификация изображений (не требует обучающих данных)
  * Оценка сходства изображения и текста
  * Семантический поиск изображений
  * Модерация контента (обнаружение NSFW, насилия)
  * Визуальные вопросы и ответы (Visual Question Answering)
  * Кросс-модальный поиск (изображение→текст, текст→изображение)


**Показатели** :
  * **25 300+ звёзд на GitHub**
  * Обучена на 400 миллионах пар изображение-текст
  * Сравнима с ResNet-50 на ImageNet (zero-shot)
  * Лицензия MIT


**Лучше использовать альтернативы** :
  * **BLIP-2** : Лучше для создания подписей (captioning)
  * **LLaVA** : Чат на основе зрения и языка
  * **Segment Anything** : Сегментация изображений


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    pip install git+https://github.com/openai/CLIP.git  
    pip install torch torchvision ftfy regex tqdm  
    
[/code]
### Zero-shot classification[​](<#zero-shot-classification> "Direct link to Zero-shot classification")
[code] 
    import torch  
    import clip  
    from PIL import Image  
      
    # Load model  
    device = "cuda" if torch.cuda.is_available() else "cpu"  
    model, preprocess = clip.load("ViT-B/32", device=device)  
      
    # Load image  
    image = preprocess(Image.open("photo.jpg")).unsqueeze(0).to(device)  
      
    # Define possible labels  
    text = clip.tokenize(["a dog", "a cat", "a bird", "a car"]).to(device)  
      
    # Compute similarity  
    with torch.no_grad():  
        image_features = model.encode_image(image)  
        text_features = model.encode_text(text)  
      
        # Cosine similarity  
        logits_per_image, logits_per_text = model(image, text)  
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()  
      
    # Print results  
    labels = ["a dog", "a cat", "a bird", "a car"]  
    for label, prob in zip(labels, probs[0]):  
        print(f"{label}: {prob:.2%}")  
    
[/code]
## Available models[​](<#available-models> "Direct link to Available models")
[code] 
    # Models (sorted by size)  
    models = [  
        "RN50",           # ResNet-50  
        "RN101",          # ResNet-101  
        "ViT-B/32",       # Vision Transformer (recommended)  
        "ViT-B/16",       # Better quality, slower  
        "ViT-L/14",       # Best quality, slowest  
    ]  
      
    model, preprocess = clip.load("ViT-B/32")  
    
[/code]
Model| Parameters| Speed| Quality  
---|---|---|---  
RN50| 102M| Fast| Good  
ViT-B/32| 151M| Medium| Better  
ViT-L/14| 428M| Slow| Best  
## Image-text similarity[​](<#image-text-similarity> "Direct link to Image-text similarity")
[code] 
    # Compute embeddings  
    image_features = model.encode_image(image)  
    text_features = model.encode_text(text)  
      
    # Normalize  
    image_features /= image_features.norm(dim=-1, keepdim=True)  
    text_features /= text_features.norm(dim=-1, keepdim=True)  
      
    # Cosine similarity  
    similarity = (image_features @ text_features.T).item()  
    print(f"Similarity: {similarity:.4f}")  
    
[/code]
## Semantic image search[​](<#semantic-image-search> "Direct link to Semantic image search")
[code] 
    # Index images  
    image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]  
    image_embeddings = []  
      
    for img_path in image_paths:  
        image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)  
        with torch.no_grad():  
            embedding = model.encode_image(image)  
            embedding /= embedding.norm(dim=-1, keepdim=True)  
        image_embeddings.append(embedding)  
      
    image_embeddings = torch.cat(image_embeddings)  
      
    # Search with text query  
    query = "a sunset over the ocean"  
    text_input = clip.tokenize([query]).to(device)  
    with torch.no_grad():  
        text_embedding = model.encode_text(text_input)  
        text_embedding /= text_embedding.norm(dim=-1, keepdim=True)  
      
    # Find most similar images  
    similarities = (text_embedding @ image_embeddings.T).squeeze(0)  
    top_k = similarities.topk(3)  
      
    for idx, score in zip(top_k.indices, top_k.values):  
        print(f"{image_paths[idx]}: {score:.3f}")  
    
[/code]
## Content moderation[​](<#content-moderation> "Direct link to Content moderation")
[code] 
    # Define categories  
    categories = [  
        "safe for work",  
        "not safe for work",  
        "violent content",  
        "graphic content"  
    ]  
      
    text = clip.tokenize(categories).to(device)  
      
    # Check image  
    with torch.no_grad():  
        logits_per_image, _ = model(image, text)  
        probs = logits_per_image.softmax(dim=-1)  
      
    # Get classification  
    max_idx = probs.argmax().item()  
    max_prob = probs[0, max_idx].item()  
      
    print(f"Category: {categories[max_idx]} ({max_prob:.2%})")  
    
[/code]
## Batch processing[​](<#batch-processing> "Direct link to Batch processing")
[code] 
    # Process multiple images  
    images = [preprocess(Image.open(f"img{i}.jpg")) for i in range(10)]  
    images = torch.stack(images).to(device)  
      
    with torch.no_grad():  
        image_features = model.encode_image(images)  
        image_features /= image_features.norm(dim=-1, keepdim=True)  
      
    # Batch text  
    texts = ["a dog", "a cat", "a bird"]  
    text_tokens = clip.tokenize(texts).to(device)  
      
    with torch.no_grad():  
        text_features = model.encode_text(text_tokens)  
        text_features /= text_features.norm(dim=-1, keepdim=True)  
      
    # Similarity matrix (10 images × 3 texts)  
    similarities = image_features @ text_features.T  
    print(similarities.shape)  # (10, 3)  
    
[/code]
## Integration with vector databases[​](<#integration-with-vector-databases> "Direct link to Integration with vector databases")
[code] 
    # Store CLIP embeddings in Chroma/FAISS  
    import chromadb  
      
    client = chromadb.Client()  
    collection = client.create_collection("image_embeddings")  
      
    # Add image embeddings  
    for img_path, embedding in zip(image_paths, image_embeddings):  
        collection.add(  
            embeddings=[embedding.cpu().numpy().tolist()],  
            metadatas=[{"path": img_path}],  
            ids=[img_path]  
        )  
      
    # Query with text  
    query = "a sunset"  
    text_embedding = model.encode_text(clip.tokenize([query]))  
    results = collection.query(  
        query_embeddings=[text_embedding.cpu().numpy().tolist()],  
        n_results=5  
    )  
    
[/code]
## Best practices[​](<#best-practices> "Direct link to Best practices")
  1. **Используйте ViT-B/32 в большинстве случаев** — Хороший баланс
  2. **Нормализуйте эмбеддинги** — Требуется для косинусного сходства
  3. **Пакетная обработка** — Более эффективно
  4. **Кэшируйте эмбеддинги** — Дорого пересчитывать
  5. **Используйте описательные метки** — Лучшая производительность zero-shot
  6. **Рекомендуется GPU** — В 10–50 раз быстрее
  7. **Предобрабатывайте изображения** — Используйте встроенную функцию preprocess


## Performance[​](<#performance> "Direct link to Performance")
Operation| CPU| GPU (V100)  
---|---|---  
Image encoding| ~200ms| ~20ms  
Text encoding| ~50ms| ~5ms  
Similarity compute| <1ms| <1ms  
## Limitations[​](<#limitations> "Direct link to Limitations")
  1. **Не подходит для детализированных задач** — Лучше всего работает с широкими категориями
  2. **Требует описательного текста** — Расплывчатые метки дают плохие результаты
  3. **Предвзятость на веб-данных** — Может содержать смещения, присущие датасетам
  4. **Нет ограничивающих рамок** — Работает только с целым изображением
  5. **Ограниченное пространственное понимание** — Слаба в определении положения/количества


## Resources[​](<#resources> "Direct link to Resources")
  * **GitHub** : <https://github.com/openai/CLIP> ⭐ 25 300+
  * **Paper** : <https://arxiv.org/abs/2103.00020>
  * **Colab** : <https://colab.research.google.com/github/openai/clip/>
  * **License** : MIT


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use CLIP](<#when-to-use-clip>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Zero-shot classification](<#zero-shot-classification>)
  * [Available models](<#available-models>)
  * [Image-text similarity](<#image-text-similarity>)
  * [Semantic image search](<#semantic-image-search>)
  * [Content moderation](<#content-moderation>)
  * [Batch processing](<#batch-processing>)
  * [Integration with vector databases](<#integration-with-vector-databases>)
  * [Best practices](<#best-practices>)
  * [Performance](<#performance>)
  * [Limitations](<#limitations>)
  * [Resources](<#resources>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-clip -->
