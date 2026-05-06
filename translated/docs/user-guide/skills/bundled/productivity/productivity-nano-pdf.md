На этой странице
Редактирование текста/опечаток/заголовков PDF через CLI nano-pdf (NL-подсказки).
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")
|   
|---|---  
|Источник| Встроенный (устанавливается по умолчанию)  
|Путь| `skills/productivity/nano-pdf`  
|Версия| `1.0.0`  
|Автор| community  
|Лицензия| MIT  
|Теги| `PDF`, `Documents`, `Editing`, `NLP`, `Productivity`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Именно эти инструкции видит агент, когда навык активен.
# nano-pdf
Редактируйте PDF-файлы с помощью инструкций на естественном языке. Укажите страницу и опишите, что нужно изменить.
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на Предварительные требования")
[code] 
    # Install with uv (recommended — already available in Hermes)  
    uv pip install nano-pdf  
      
    # Or with pip  
    pip install nano-pdf  
    
[/code]
## Использование[​](<#usage> "Прямая ссылка на Использование")
[code] 
    nano-pdf edit <file.pdf> <page_number> "<instruction>"  
    
[/code]
## Примеры[​](<#examples> "Прямая ссылка на Примеры")
[code] 
    # Change a title on page 1  
    nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"  
      
    # Update a date on a specific page  
    nano-pdf edit report.pdf 3 "Update the date from January to February 2026"  
      
    # Fix content  
    nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"  
    
[/code]
## Примечания[​](<#notes> "Прямая ссылка на Примечания")
  * Номера страниц могут быть с отсчётом от 0 или от 1 в зависимости от версии — если правка применяется не к той странице, повторите с ±1
  * Всегда проверяйте полученный PDF после редактирования (используйте `read_file` для проверки размера файла или откройте его)
  * Инструмент использует LLM под капотом — требуется API-ключ (проверьте `nano-pdf --help` для настройки)
  * Хорошо работает для текстовых изменений; сложные модификации макета могут потребовать другого подхода


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Предварительные требования](<#prerequisites>)
  * [Использование](<#usage>)
  * [Примеры](<#examples>)
  * [Примечания](<#notes>)



<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/productivity/productivity-nano-pdf -->
