On this page
Пиксель-арт с эпохальными палитрами (NES, Game Boy, PICO-8).
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---  |
Source| Встроенный (установлен по умолчанию)  |
Path| `skills/creative/pixel-art`  |
Version| `2.0.0`  |
Author| dodo-reach  |
License| MIT  |
Tags| `creative`, `pixel-art`, `arcade`, `snes`, `nes`, `gameboy`, `retro`, `image`, `video`  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# Pixel Art
Конвертируйте любое изображение в ретро-пиксель-арт, а затем опционально анимируйте в короткий MP4 или GIF с эффектами соответствующей эпохи (дождь, светлячки, снег, искры).
С этим навыком поставляются два скрипта:
  * `scripts/pixel_art.py` — фото → пиксель-арт PNG (дизеринг Флойда-Стейнберга)
  * `scripts/pixel_art_video.py` — пиксель-арт PNG → анимированный MP4 (+ опционально GIF)


Каждый можно импортировать или запускать напрямую. Пресеты привязываются к аппаратным палитрам, когда нужны цвета, соответствующие эпохе (NES, Game Boy, PICO-8 и т.д.), или используйте адаптивную N-цветную квантизацию для стиля аркад/SNES.
## When to Use[​](<#when-to-use> "Direct link to When to Use")
  * Пользователь хочет ретро-пиксель-арт из исходного изображения
  * Пользователь просит стиль NES / Game Boy / PICO-8 / C64 / аркада / SNES
  * Пользователь хочет короткую зацикленную анимацию (сцена дождя, ночное небо, снег и т.д.)
  * Постеры, обложки альбомов, посты в соцсетях, спрайты, персонажи, аватары


## Workflow[​](<#workflow> "Direct link to Workflow")
Перед генерацией подтвердите стиль с пользователем. Разные пресеты дают очень разные результаты, а перегенерация затратна.
### Step 1 — Offer a style[​](<#step-1--offer-a-style> "Direct link to Step 1 — Offer a style")
Вызовите `clarify` с 4 репрезентативными пресетами. Выбирайте набор в зависимости от того, что просит пользователь — не вываливайте все 14.
Меню по умолчанию, когда намерение пользователя неясно:
[code] 
    clarify(  
        question="Какой стиль пиксель-арта вы хотите?",  
        choices=[  
            "arcade — жирный, коренастый стиль аркад 80-х (16 цветов, 8px)",  
            "nes — аппаратная палитра Nintendo 8-bit (54 цвета, 8px)",  
            "gameboy — 4-оттеночный зелёный Game Boy DMG",  
            "snes — более чистый 16-битный вид (32 цвета, 4px)",  
        ],  
    )  
    
[/code]
Когда пользователь уже назвал эпоху (например, «аркада 80-х», «Gameboy»), пропустите `clarify` и используйте соответствующий пресет напрямую.
### Step 2 — Offer animation (optional)[​](<#step-2--offer-animation-optional> "Direct link to Step 2 — Offer animation (optional)")
Если пользователь попросил видео/GIF или результат может выиграть от движения, спросите, какую сцену:
[code] 
    clarify(  
        question="Хотите анимировать? Выберите сцену или пропустите.",  
        choices=[  
            "night — звёзды + светлячки + листья",  
            "urban — дождь + неоновые импульсы",  
            "snow — падающие снежинки",  
            "skip — только изображение",  
        ],  
    )  
    
[/code]
НЕ вызывайте `clarify` более двух раз подряд. Один раз для стиля, один раз для сцены, если анимация возможна. Если пользователь явно запросил конкретный стиль и сцену в своём сообщении, пропустите `clarify` полностью.
### Step 3 — Generate[​](<#step-3--generate> "Direct link to Step 3 — Generate")
Запустите `pixel_art()` сначала; если запрошена анимация, передайте результат в `pixel_art_video()`.
## Preset Catalog[​](<#preset-catalog> "Direct link to Preset Catalog")
Пресет| Эпоха| Палитра| Блок| Лучше всего для  
---|---|---|---|---  
`arcade`| Аркады 80-х| adaptive 16| 8px| Жирные постеры, героический арт  
`snes`| 16-бит| adaptive 32| 4px| Персонажи, детализированные сцены  
`nes`| 8-бит| NES (54)| 8px| Настоящий вид NES  
`gameboy`| DMG консоль| 4 оттенка зелёного| 8px| Монохромный Game Boy  
`gameboy_pocket`| Pocket консоль| 4 оттенка серого| 8px| Монохромный GB Pocket  
`pico8`| PICO-8| 16 фикс.| 6px| Стиль фэнтези-консоли  
`c64`| Commodore 64| 16 фикс.| 8px| Домашний компьютер 8-bit  
`apple2`| Apple II hi-res| 6 фикс.| 10px| Экстремальное ретро, 6 цветов  
`teletext`| BBC Teletext| 8 чистых| 10px| Коренастые основные цвета  
`mspaint`| Windows MS Paint| 24 фикс.| 8px| Ностальгический десктоп  
`mono_green`| CRT фосфор| 2 зелёных| 6px| Эстетика терминала/CRT  
`mono_amber`| CRT янтарный| 2 янтарных| 6px| Вид янтарного монитора  
`neon`| Киберпанк| 10 неоновых| 6px| Vaporwave/cyber  
`pastel`| Мягкая пастель| 10 пастельных| 6px| Kawaii / нежный  
Именованные палитры находятся в `scripts/palettes.py` (см. `references/palettes.md` для полного списка — всего 28 именованных палитр). Любой пресет можно переопределить:
[code] 
    pixel_art("in.png", "out.png", preset="snes", palette="PICO_8", block=6)  
    
[/code]
## Scene Catalog (for video)[​](<#scene-catalog-for-video> "Direct link to Scene Catalog (for video)")
Сцена| Эффекты  
---|---  
`night`| Мерцающие звёзды + светлячки + дрейфующие листья  
`dusk`| Светлячки + искры  
`tavern`| Пылинки + тёплые искры  
`indoor`| Пылинки  
`urban`| Дождь + неоновые импульсы  
`nature`| Листья + светлячки  
`magic`| Искры + светлячки  
`storm`| Дождь + молнии  
`underwater`| Пузырьки + световые искры  
`fire`| Угольки + искры  
`snow`| Снежинки + искры  
`desert`| Мерцание жара + пыль  
## Invocation Patterns[​](<#invocation-patterns> "Direct link to Invocation Patterns")
### Python (import)[​](<#python-import> "Direct link to Python (import)")
[code] 
    import sys  
    sys.path.insert(0, "/home/teknium/.hermes/skills/creative/pixel-art/scripts")  
    from pixel_art import pixel_art  
    from pixel_art_video import pixel_art_video  
      
    # 1. Convert to pixel art  
    pixel_art("/path/to/photo.jpg", "/tmp/pixel.png", preset="nes")  
      
    # 2. Animate (optional)  
    pixel_art_video(  
        "/tmp/pixel.png",  
        "/tmp/pixel.mp4",  
        scene="night",  
        duration=6,  
        fps=15,  
        seed=42,  
        export_gif=True,  
    )  
    
[/code]
### CLI[​](<#cli> "Direct link to CLI")
[code] 
    cd /home/teknium/.hermes/skills/creative/pixel-art/scripts  
      
    python pixel_art.py in.jpg out.png --preset gameboy  
    python pixel_art.py in.jpg out.png --preset snes --palette PICO_8 --block 6  
      
    python pixel_art_video.py out.png out.mp4 --scene night --duration 6 --gif  
    
[/code]
## Pipeline Rationale[​](<#pipeline-rationale> "Direct link to Pipeline Rationale")
**Конвертация в пиксели:**
  1. Усиление контраста/цвета/резкости (сильнее для маленьких палитр)
  2. Постеризация для упрощения тональных областей перед квантизацией
  3. Уменьшение масштаба на `block` с `Image.NEAREST` (жёсткие пиксели, без интерполяции)
  4. Квантизация с дизерингом Флойда-Стейнберга — по адаптивной N-цветной палитре ИЛИ именованной аппаратной палитре
  5. Увеличение обратно с `Image.NEAREST`


Квантизация ПОСЛЕ уменьшения масштаба сохраняет дизеринг выровненным по финальной сетке пикселей. Квантизация до удалила бы диффузию ошибки на деталях, которые исчезают.
**Видео-наложение:**
  * Копирует базовый кадр каждый тик (статический фон)
  * Накладывает не сохраняющие состояние покадровые отрисовки частиц (одна функция на эффект)
  * Кодируется через ffmpeg `libx264 -pix_fmt yuv420p -crf 18`
  * Опциональный GIF через `palettegen` + `paletteuse`


## Dependencies[​](<#dependencies> "Direct link to Dependencies")
  * Python 3.9+
  * Pillow (`pip install Pillow`)
  * ffmpeg в PATH (нужен только для видео — Hermes устанавливает этот пакет)


## Pitfalls[​](<#pitfalls> "Direct link to Pitfalls")
  * Ключи палитр чувствительны к регистру (`"NES"`, `"PICO_8"`, `"GAMEBOY_ORIGINAL"`).
  * Очень маленькие источники (<100px в ширину) «схлопываются» под блоками 8-10px. Увеличьте источник, если он крошечный.
  * Дробный `block` или `palette` сломают квантизацию — используйте положительные целые числа.
  * Количество частиц в анимации настроено для холстов ~640x480. Для очень больших изображений может понадобиться второй проход с другим seed для плотности.
  * `mono_green` / `mono_amber` форсируют `color=0.0` (десатурация). Если переопределить и сохранить хрому, 2-цветная палитра может дать полосы на гладких областях.
  * Цикл `clarify`: вызывайте максимум дважды за раз (стиль, затем сцена). Не засыпайте пользователя новыми вопросами.


## Verification[​](<#verification> "Direct link to Verification")
  * PNG создан по указанному пути вывода
  * Чёткие квадратные блоки пикселей видны при размере блока пресета
  * Количество цветов соответствует пресету (проверьте на глаз или выполните `Image.open(p).getcolors()`)
  * Видео — валидный MP4 (`ffprobe` может открыть его) с ненулевым размером


## Attribution[​](<#attribution> "Direct link to Attribution")
Именованные аппаратные палитры и процедурные анимационные циклы в `pixel_art_video.py` портированы из [pixel-art-studio](<https://github.com/Synero/pixel-art-studio>) (MIT). См. `ATTRIBUTION.md` в директории навыка для подробностей.
  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use](<#when-to-use>)
  * [Workflow](<#workflow>)
    * [Step 1 — Offer a style](<#step-1--offer-a-style>)
    * [Step 2 — Offer animation (optional)](<#step-2--offer-animation-optional>)
    * [Step 3 — Generate](<#step-3--generate>)
  * [Preset Catalog](<#preset-catalog>)
  * [Scene Catalog (for video)](<#scene-catalog-for-video>)
  * [Invocation Patterns](<#invocation-patterns>)
    * [Python (import)](<#python-import>)
    * [CLI](<#cli>)
  * [Pipeline Rationale](<#pipeline-rationale>)
  * [Dependencies](<#dependencies>)
  * [Pitfalls](<#pitfalls>)
  * [Verification](<#verification>)
  * [Attribution](<#attribution>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-pixel-art -->
