On this page
SAM: zero-shot сегментация изображений по точкам, рамкам, маскам.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Bundled (installed by default)  |
|Path| `skills/mlops/models/segment-anything`  |
|Version| `1.0.0`  |
|Author| Orchestra Research  |
|License| MIT  |
|Dependencies| `segment-anything`, `transformers>=4.30.0`, `torch>=1.7.0`  |
|Tags| `Multimodal`, `Image Segmentation`, `Computer Vision`, `SAM`, `Zero-Shot`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Segment Anything Model (SAM)
Полное руководство по использованию Segment Anything Model от Meta AI для zero-shot сегментации изображений.
## When to use SAM[​](<#when-to-use-sam> "Direct link to When to use SAM")
**Используйте SAM когда:**
  * Нужно сегментировать любой объект на изображениях без обучения под конкретную задачу
  * Вы создаёте интерактивные инструменты разметки с подсказками в виде точек/рамок
  * Генерируете обучающие данные для других моделей компьютерного зрения
  * Нужен zero-shot перенос на новые домены изображений
  * Строите пайплайны обнаружения/сегментации объектов
  * Обрабатываете медицинские, спутниковые или специализированные изображения


**Ключевые особенности:**
  * **Zero-shot сегментация** : Работает на любых доменах изображений без дообучения
  * **Гибкие подсказки** : Точки, ограничивающие рамки или предыдущие маски
  * **Автоматическая сегментация** : Автоматически генерирует маски всех объектов
  * **Высокое качество** : Обучена на 1,1 миллиарда масок из 11 миллионов изображений
  * **Несколько размеров моделей** : ViT-B (самая быстрая), ViT-L, ViT-H (самая точная)
  * **Экспорт в ONNX** : Развёртывание в браузерах и на периферийных устройствах


**Альтернативы:**
  * **YOLO/Detectron2** : Для обнаружения объектов в реальном времени с классами
  * **Mask2Former** : Для семантической/паноптической сегментации с категориями
  * **GroundingDINO + SAM** : Для сегментации по текстовым подсказкам
  * **SAM 2** : Для сегментации видео


## Quick start[​](<#quick-start> "Direct link to Quick start")
### Installation[​](<#installation> "Direct link to Installation")
[code] 
    # From GitHub  
    pip install git+https://github.com/facebookresearch/segment-anything.git  
      
    # Optional dependencies  
    pip install opencv-python pycocotools matplotlib  
      
    # Or use HuggingFace transformers  
    pip install transformers  
    
[/code]
### Download checkpoints[​](<#download-checkpoints> "Direct link to Download checkpoints")
[code] 
    # ViT-H (largest, most accurate) - 2.4GB  
    wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth  
      
    # ViT-L (medium) - 1.2GB  
    wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth  
      
    # ViT-B (smallest, fastest) - 375MB  
    wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth  
    
[/code]
### Basic usage with SamPredictor[​](<#basic-usage-with-sampredictor> "Direct link to Basic usage with SamPredictor")
[code] 
    import numpy as np  
    from segment_anything import sam_model_registry, SamPredictor  
      
    # Load model  
    sam = sam_model_registry["vit_h"](https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/models/segment-anything/checkpoint="sam_vit_h_4b8939.pth")  
    sam.to(device="cuda")  
      
    # Create predictor  
    predictor = SamPredictor(sam)  
      
    # Set image (computes embeddings once)  
    image = cv2.imread("image.jpg")  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
    predictor.set_image(image)  
      
    # Predict with point prompts  
    input_point = np.array([[500, 375]])  # (x, y) coordinates  
    input_label = np.array([1])  # 1 = foreground, 0 = background  
      
    masks, scores, logits = predictor.predict(  
        point_coords=input_point,  
        point_labels=input_label,  
        multimask_output=True  # Returns 3 mask options  
    )  
      
    # Select best mask  
    best_mask = masks[np.argmax(scores)]  
    
[/code]
### HuggingFace Transformers[​](<#huggingface-transformers> "Direct link to HuggingFace Transformers")
[code] 
    import torch  
    from PIL import Image  
    from transformers import SamModel, SamProcessor  
      
    # Load model and processor  
    model = SamModel.from_pretrained("facebook/sam-vit-huge")  
    processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")  
    model.to("cuda")  
      
    # Process image with point prompt  
    image = Image.open("image.jpg")  
    input_points = [[[450, 600]]]  # Batch of points  
      
    inputs = processor(image, input_points=input_points, return_tensors="pt")  
    inputs = {k: v.to("cuda") for k, v in inputs.items()}  
      
    # Generate masks  
    with torch.no_grad():  
        outputs = model(**inputs)  
      
    # Post-process masks to original size  
    masks = processor.image_processor.post_process_masks(  
        outputs.pred_masks.cpu(),  
        inputs["original_sizes"].cpu(),  
        inputs["reshaped_input_sizes"].cpu()  
    )  
    
[/code]
## Core concepts[​](<#core-concepts> "Direct link to Core concepts")
### Model architecture[​](<#model-architecture> "Direct link to Model architecture")
[code] 
    SAM Architecture:  
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐  
    │  Image Encoder  │────▶│ Prompt Encoder  │────▶│  Mask Decoder   │  
    │     (ViT)       │     │ (Points/Boxes)  │     │ (Transformer)   │  
    └─────────────────┘     └─────────────────┘     └─────────────────┘  
            │                       │                       │  
       Image Embeddings      Prompt Embeddings         Masks + IoU  
       (computed once)       (per prompt)             predictions  
    
[/code]
### Model variants[​](<#model-variants> "Direct link to Model variants")
Модель| Чекпоинт| Размер| Скорость| Точность
---|---|---|---|---|---
ViT-H| `vit_h`| 2.4 ГБ| Медленнее всех| Наилучшая
ViT-L| `vit_l`| 1.2 ГБ| Средняя| Хорошая
ViT-B| `vit_b`| 375 МБ| Быстрее всех| Хорошая
### Prompt types[​](<#prompt-types> "Direct link to Prompt types")
Подсказка| Описание| Сценарий использования
---|---|---
Point (foreground)| Клик по объекту| Выбор одного объекта
Point (background)| Клик вне объекта| Исключение областей
Bounding box| Прямоугольник вокруг объекта| Крупные объекты
Previous mask| Маска низкого разрешения| Итеративное уточнение
## Interactive segmentation[​](<#interactive-segmentation> "Direct link to Interactive segmentation")
### Point prompts[​](<#point-prompts> "Direct link to Point prompts")
[code] 
    # Single foreground point  
    input_point = np.array([[500, 375]])  
    input_label = np.array([1])  
      
    masks, scores, logits = predictor.predict(  
        point_coords=input_point,  
        point_labels=input_label,  
        multimask_output=True  
    )  
      
    # Multiple points (foreground + background)  
    input_points = np.array([[500, 375], [600, 400], [450, 300]])  
    input_labels = np.array([1, 1, 0])  # 2 foreground, 1 background  
      
    masks, scores, logits = predictor.predict(  
        point_coords=input_points,  
        point_labels=input_labels,  
        multimask_output=False  # Single mask when prompts are clear  
    )  
    
[/code]
### Box prompts[​](<#box-prompts> "Direct link to Box prompts")
[code] 
    # Bounding box [x1, y1, x2, y2]  
    input_box = np.array([425, 600, 700, 875])  
      
    masks, scores, logits = predictor.predict(  
        box=input_box,  
        multimask_output=False  
    )  
    
[/code]
### Combined prompts[​](<#combined-prompts> "Direct link to Combined prompts")
[code] 
    # Box + points for precise control  
    masks, scores, logits = predictor.predict(  
        point_coords=np.array([[500, 375]]),  
        point_labels=np.array([1]),  
        box=np.array([400, 300, 700, 600]),  
        multimask_output=False  
    )  
    
[/code]
### Iterative refinement[​](<#iterative-refinement> "Direct link to Iterative refinement")
[code] 
    # Initial prediction  
    masks, scores, logits = predictor.predict(  
        point_coords=np.array([[500, 375]]),  
        point_labels=np.array([1]),  
        multimask_output=True  
    )  
      
    # Refine with additional point using previous mask  
    masks, scores, logits = predictor.predict(  
        point_coords=np.array([[500, 375], [550, 400]]),  
        point_labels=np.array([1, 0]),  # Add background point  
        mask_input=logits[np.argmax(scores)][None, :, :],  # Use best mask  
        multimask_output=False  
    )  
    
[/code]
## Automatic mask generation[​](<#automatic-mask-generation> "Direct link to Automatic mask generation")
### Basic automatic segmentation[​](<#basic-automatic-segmentation> "Direct link to Basic automatic segmentation")
[code] 
    from segment_anything import SamAutomaticMaskGenerator  
      
    # Create generator  
    mask_generator = SamAutomaticMaskGenerator(sam)  
      
    # Generate all masks  
    masks = mask_generator.generate(image)  
      
    # Each mask contains:  
    # - segmentation: binary mask  
    # - bbox: [x, y, w, h]  
    # - area: pixel count  
    # - predicted_iou: quality score  
    # - stability_score: robustness score  
    # - point_coords: generating point  
    
[/code]
### Customized generation[​](<#customized-generation> "Direct link to Customized generation")
[code] 
    mask_generator = SamAutomaticMaskGenerator(  
        model=sam,  
        points_per_side=32,          # Grid density (more = more masks)  
        pred_iou_thresh=0.88,        # Quality threshold  
        stability_score_thresh=0.95,  # Stability threshold  
        crop_n_layers=1,             # Multi-scale crops  
        crop_n_points_downscale_factor=2,  
        min_mask_region_area=100,    # Remove tiny masks  
    )  
      
    masks = mask_generator.generate(image)  
    
[/code]
### Filtering masks[​](<#filtering-masks> "Direct link to Filtering masks")
[code] 
    # Sort by area (largest first)  
    masks = sorted(masks, key=lambda x: x['area'], reverse=True)  
      
    # Filter by predicted IoU  
    high_quality = [m for m in masks if m['predicted_iou'] > 0.9]  
      
    # Filter by stability score  
    stable_masks = [m for m in masks if m['stability_score'] > 0.95]  
    
[/code]
## Batched inference[​](<#batched-inference> "Direct link to Batched inference")
### Multiple images[​](<#multiple-images> "Direct link to Multiple images")
[code] 
    # Process multiple images efficiently  
    images = [cv2.imread(f"image_{i}.jpg") for i in range(10)]  
      
    all_masks = []  
    for image in images:  
        predictor.set_image(image)  
        masks, _, _ = predictor.predict(  
            point_coords=np.array([[500, 375]]),  
            point_labels=np.array([1]),  
            multimask_output=True  
        )  
        all_masks.append(masks)  
    
[/code]
### Multiple prompts per image[​](<#multiple-prompts-per-image> "Direct link to Multiple prompts per image")
[code] 
    # Process multiple prompts efficiently (one image encoding)  
    predictor.set_image(image)  
      
    # Batch of point prompts  
    points = [  
        np.array([[100, 100]]),  
        np.array([[200, 200]]),  
        np.array([[300, 300]])  
    ]  
      
    all_masks = []  
    for point in points:  
        masks, scores, _ = predictor.predict(  
            point_coords=point,  
            point_labels=np.array([1]),  
            multimask_output=True  
        )  
        all_masks.append(masks[np.argmax(scores)])  
    
[/code]
## ONNX deployment[​](<#onnx-deployment> "Direct link to ONNX deployment")
### Export model[​](<#export-model> "Direct link to Export model")
[code] 
    python scripts/export_onnx_model.py \\  
        --checkpoint sam_vit_h_4b8939.pth \\  
        --model-type vit_h \\  
        --output sam_onnx.onnx \\  
        --return-single-mask  
    
[/code]
### Use ONNX model[​](<#use-onnx-model> "Direct link to Use ONNX model")
[code] 
    import onnxruntime  
      
    # Load ONNX model  
    ort_session = onnxruntime.InferenceSession("sam_onnx.onnx")  
      
    # Run inference (image embeddings computed separately)  
    masks = ort_session.run(  
        None,  
        {  
            "image_embeddings": image_embeddings,  
            "point_coords": point_coords,  
            "point_labels": point_labels,  
            "mask_input": np.zeros((1, 1, 256, 256), dtype=np.float32),  
            "has_mask_input": np.array([0], dtype=np.float32),  
            "orig_im_size": np.array([h, w], dtype=np.float32)  
        }  
    )  
    
[/code]
## Common workflows[​](<#common-workflows> "Direct link to Common workflows")
### Workflow 1: Annotation tool[​](<#workflow-1-annotation-tool> "Direct link to Workflow 1: Annotation tool")
[code] 
    import cv2  
      
    # Load model  
    predictor = SamPredictor(sam)  
    predictor.set_image(image)  
      
    def on_click(event, x, y, flags, param):  
        if event == cv2.EVENT_LBUTTONDOWN:  
            # Foreground point  
            masks, scores, _ = predictor.predict(  
                point_coords=np.array([[x, y]]),  
                point_labels=np.array([1]),  
                multimask_output=True  
            )  
            # Display best mask  
            display_mask(masks[np.argmax(scores)])  
    
[/code]
### Workflow 2: Object extraction[​](<#workflow-2-object-extraction> "Direct link to Workflow 2: Object extraction")
[code] 
    def extract_object(image, point):  
        \"\"\"Extract object at point with transparent background.\"\"\"  
        predictor.set_image(image)  
      
        masks, scores, _ = predictor.predict(  
            point_coords=np.array([point]),  
            point_labels=np.array([1]),  
            multimask_output=True  
        )  
      
        best_mask = masks[np.argmax(scores)]  
      
        # Create RGBA output  
        rgba = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)  
        rgba[:, :, :3] = image  
        rgba[:, :, 3] = best_mask * 255  
      
        return rgba  
    
[/code]
### Workflow 3: Medical image segmentation[​](<#workflow-3-medical-image-segmentation> "Direct link to Workflow 3: Medical image segmentation")
[code] 
    # Process medical images (grayscale to RGB)  
    medical_image = cv2.imread("scan.png", cv2.IMREAD_GRAYSCALE)  
    rgb_image = cv2.cvtColor(medical_image, cv2.COLOR_GRAY2RGB)  
      
    predictor.set_image(rgb_image)  
      
    # Segment region of interest  
    masks, scores, _ = predictor.predict(  
        box=np.array([x1, y1, x2, y2]),  # ROI bounding box  
        multimask_output=True  
    )  
    
[/code]
## Output format[​](<#output-format> "Direct link to Output format")
### Mask data structure[​](<#mask-data-structure> "Direct link to Mask data structure")
[code] 
    # SamAutomaticMaskGenerator output  
    {  
        "segmentation": np.ndarray,  # H×W binary mask  
        "bbox": [x, y, w, h],        # Bounding box  
        "area": int,                 # Pixel count  
        "predicted_iou": float,      # 0-1 quality score  
        "stability_score": float,    # 0-1 robustness score  
        "crop_box": [x, y, w, h],    # Generation crop region  
        "point_coords": [[x, y]],    # Input point  
    }  
    
[/code]
### COCO RLE format[​](<#coco-rle-format> "Direct link to COCO RLE format")
[code] 
    from pycocotools import mask as mask_utils  
      
    # Encode mask to RLE  
    rle = mask_utils.encode(np.asfortranarray(mask.astype(np.uint8)))  
    rle["counts"] = rle["counts"].decode("utf-8")  
      
    # Decode RLE to mask  
    decoded_mask = mask_utils.decode(rle)  
    
[/code]
## Performance optimization[​](<#performance-optimization> "Direct link to Performance optimization")
### GPU memory[​](<#gpu-memory> "Direct link to GPU memory")
[code] 
    # Use smaller model for limited VRAM  
    sam = sam_model_registry["vit_b"](https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/models/segment-anything/checkpoint="sam_vit_b_01ec64.pth")  
      
    # Process images in batches  
    # Clear CUDA cache between large batches  
    torch.cuda.empty_cache()  
    
[/code]
### Speed optimization[​](<#speed-optimization> "Direct link to Speed optimization")
[code] 
    # Use half precision  
    sam = sam.half()  
      
    # Reduce points for automatic generation  
    mask_generator = SamAutomaticMaskGenerator(  
        model=sam,  
        points_per_side=16,  # Default is 32  
    )  
      
    # Use ONNX for deployment  
    # Export with --return-single-mask for faster inference  
    
[/code]
## Common issues[​](<#common-issues> "Direct link to Common issues")
Проблема| Решение
---|---
Out of memory| Используйте модель ViT-B, уменьшите размер изображения
Slow inference| Используйте ViT-B, уменьшите points_per_side
Poor mask quality| Попробуйте другие подсказки, используйте рамку + точки
Edge artifacts| Используйте фильтрацию по stability_score
Small objects missed| Увеличьте points_per_side
## References[​](<#references> "Direct link to References")
  * **[Advanced Usage](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/models/segment-anything/references/advanced-usage.md>)** \\- Пакетная обработка, дообучение, интеграция
  * **[Troubleshooting](<https://github.com/NousResearch/hermes-agent/blob/main/skills/mlops/models/segment-anything/references/troubleshooting.md>)** \\- Частые проблемы и решения


## Resources[​](<#resources> "Direct link to Resources")
  * **GitHub** : <https://github.com/facebookresearch/segment-anything>
  * **Paper** : <https://arxiv.org/abs/2304.02643>
  * **Demo** : <https://segment-anything.com>
  * **SAM 2 (Video)** : <https://github.com/facebookresearch/segment-anything-2>
  * **HuggingFace** : <https://huggingface.co/facebook/sam-vit-huge>


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use SAM](<#when-to-use-sam>)
  * [Quick start](<#quick-start>)
    * [Installation](<#installation>)
    * [Download checkpoints](<#download-checkpoints>)
    * [Basic usage with SamPredictor](<#basic-usage-with-sampredictor>)
    * [HuggingFace Transformers](<#huggingface-transformers>)
  * [Core concepts](<#core-concepts>)
    * [Model architecture](<#model-architecture>)
    * [Model variants](<#model-variants>)
    * [Prompt types](<#prompt-types>)
  * [Interactive segmentation](<#interactive-segmentation>)
    * [Point prompts](<#point-prompts>)
    * [Box prompts](<#box-prompts>)
    * [Combined prompts](<#combined-prompts>)
    * [Iterative refinement](<#iterative-refinement>)
  * [Automatic mask generation](<#automatic-mask-generation>)
    * [Basic automatic segmentation](<#basic-automatic-segmentation>)
    * [Customized generation](<#customized-generation>)
    * [Filtering masks](<#filtering-masks>)
  * [Batched inference](<#batched-inference>)
    * [Multiple images](<#multiple-images>)
    * [Multiple prompts per image](<#multiple-prompts-per-image>)
  * [ONNX deployment](<#onnx-deployment>)
    * [Export model](<#export-model>)
    * [Use ONNX model](<#use-onnx-model>)
  * [Common workflows](<#common-workflows>)
    * [Workflow 1: Annotation tool](<#workflow-1-annotation-tool>)
    * [Workflow 2: Object extraction](<#workflow-2-object-extraction>)
    * [Workflow 3: Medical image segmentation](<#workflow-3-medical-image-segmentation>)
  * [Output format](<#output-format>)
    * [Mask data structure](<#mask-data-structure>)
    * [COCO RLE format](<#coco-rle-format>)
  * [Performance optimization](<#performance-optimization>)
    * [GPU memory](<#gpu-memory>)
    * [Speed optimization](<#speed-optimization>)
  * [Common issues](<#common-issues>)
  * [References](<#references>)
  * [Resources](<#resources>)





<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/mlops/mlops-models-segment-anything -->
