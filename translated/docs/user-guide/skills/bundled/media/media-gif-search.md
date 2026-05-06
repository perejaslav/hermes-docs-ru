На этой странице
Поиск и загрузка GIF из Tenor через curl и jq.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на метаданные навыка")
|   
|---|---  
|Источник| Встроенный (устанавливается по умолчанию)  
|Путь| `skills/media/gif-search`  
|Версия| `1.1.0`  
|Автор| Hermes Agent  
|Лицензия| MIT  
|Теги| `GIF`, `Media`, `Search`, `Tenor`, `API`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это то, что агент видит в качестве инструкций, когда навык активен.
# GIF Search (Tenor API)
Поиск и загрузка GIF напрямую через Tenor API с помощью curl. Дополнительные инструменты не требуются.
## Когда использовать[​](<#when-to-use> "Прямая ссылка на раздел «Когда использовать»")
Полезно для поиска реакционных GIF, создания визуального контента и отправки GIF в чат.
## Настройка[​](<#setup> "Прямая ссылка на раздел «Настройка»")
Установите ваш Tenor API ключ в переменных окружения (добавьте в `~/.hermes/.env`):
[code] 
    TENOR_API_KEY=your_key_here  
    
[/code]
Получите бесплатный API ключ на <https://developers.google.com/tenor/guides/quickstart> — ключ Tenor API в Google Cloud Console бесплатен и имеет щедрые лимиты запросов.
## Предварительные требования[​](<#prerequisites> "Прямая ссылка на раздел «Предварительные требования»")
  * `curl` и `jq` (оба стандартны для macOS/Linux)
  * переменная окружения `TENOR_API_KEY`


## Поиск GIF[​](<#search-for-gifs> "Прямая ссылка на раздел «Поиск GIF»")
[code] 
    # Search and get GIF URLs  
    curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.gif.url'  
      
    # Get smaller/preview versions  
    curl -s "https://tenor.googleapis.com/v2/search?q=nice+work&limit=3&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.tinygif.url'  
    
[/code]
## Загрузка GIF[​](<#download-a-gif> "Прямая ссылка на раздел «Загрузка GIF»")
[code] 
    # Search and download the top result  
    URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')  
    curl -sL "$URL" -o celebration.gif  
    
[/code]
## Получение полных метаданных[​](<#get-full-metadata> "Прямая ссылка на раздел «Получение полных метаданных»")
[code] 
    curl -s "https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}" | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url, dimensions: .media_formats.gif.dims}'  
    
[/code]
## Параметры API[​](<#api-parameters> "Прямая ссылка на раздел «Параметры API»")
Параметр| Описание  
|---|---  
`q`| Поисковый запрос (URL-кодировка пробелов как `+`)  
`limit`| Максимум результатов (1-50, по умолчанию 20)  
`key`| API ключ (из переменной окружения `$TENOR_API_KEY`)  
`media_filter`| Фильтр форматов: `gif`, `tinygif`, `mp4`, `tinymp4`, `webm`  
`contentfilter`| Безопасность: `off`, `low`, `medium`, `high`  
`locale`| Язык: `en_US`, `es`, `fr` и др.  
## Доступные медиаформаты[​](<#available-media-formats> "Прямая ссылка на раздел «Доступные медиаформаты»")
Каждый результат содержит несколько форматов в `.media_formats`:
Формат| Назначение  
|---|---  
`gif`| Полноразмерный GIF  
`tinygif`| Маленький превью GIF  
`mp4`| Видеоверсия (меньший размер файла)  
`tinymp4`| Маленькое превью видео  
`webm`| WebM видео  
`nanogif`| Крошечная миниатюра  
## Примечания[​](<#notes> "Прямая ссылка на раздел «Примечания»")
  * URL-кодируйте запрос: пробелы как `+`, спецсимволы как `%XX`
  * Для отправки в чат URL `tinygif` легче по весу
  * URL GIF можно использовать напрямую в markdown: `![alt](https://github.com/NousResearch/hermes-agent/blob/main/skills/media/gif-search/url)`


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Настройка](<#setup>)
  * [Предварительные требования](<#prerequisites>)
  * [Поиск GIF](<#search-for-gifs>)
  * [Загрузка GIF](<#download-a-gif>)
  * [Получение полных метаданных](<#get-full-metadata>)
  * [Параметры API](<#api-parameters>)
  * [Доступные медиаформаты](<#available-media-formats>)
  * [Примечания](<#notes>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/media/media-gif-search -->
