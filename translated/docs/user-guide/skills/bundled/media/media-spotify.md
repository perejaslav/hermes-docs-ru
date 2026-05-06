On this page
Spotify: воспроизведение, поиск, очередь, управление плейлистами и устройствами.
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   |
|---|---|
|Source| Встроенный (установлен по умолчанию)  |
|Path| `skills/media/spotify`  |
|Version| `1.0.0`  |
|Author| Hermes Agent  |
|License| MIT  |
|Tags| `spotify`, `music`, `playback`, `playlists`, `media`  |
|Related skills| [`gif-search`](</docs/user-guide/skills/bundled/media/media-gif-search>)  |
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при активации этого навыка. Это то, что агент видит в качестве инструкций, когда навык активен.
# Spotify
Управление учётной записью Spotify пользователя через набор инструментов Hermes Spotify (7 инструментов). Руководство по настройке: <https://hermes-agent.nousresearch.com/docs/user-guide/features/spotify>
## When to use this skill[​](<#when-to-use-this-skill> "Direct link to When to use this skill")
Пользователь говорит что-то вроде «включи X», «пауза», «пропустить», «добавь в очередь X», «что играет», «найди X», «добавь в мой плейлист X», «создай плейлист», «сохрани это в мою библиотеку» и т.п.
## The 7 tools[​](<#the-7-tools> "Direct link to The 7 tools")
  * `spotify_playback` — воспроизведение, пауза, следующий, предыдущий, перемотка, установка повтора, перемешивания, громкости, получение состояния, получение текущего трека, недавно воспроизведённое
  * `spotify_devices` — список, перенос
  * `spotify_queue` — получить, добавить
  * `spotify_search` — поиск по каталогу
  * `spotify_playlists` — список, получить, создать, добавить элементы, удалить элементы, обновить детали
  * `spotify_albums` — получить, треки
  * `spotify_library` — список/сохранить/удалить с `kind: "tracks"|"albums"`


Действия, изменяющие воспроизведение, требуют Spotify Premium; поиск/библиотека/плейлисты работают на Free.
## Canonical patterns (minimize tool calls)[​](<#canonical-patterns-minimize-tool-calls> "Direct link to Canonical patterns \\(minimize tool calls\\)")
### "Play <artist/track/album>"[​](<#play-artisttrackalbum> "Direct link to \"Play <artist/track/album>\"")
Один поиск, затем воспроизведение по URI. НЕ перебирайте результаты поиска, описывая их, если только пользователь не запросил варианты.
[code] 
    spotify_search({"query": "miles davis kind of blue", "types": ["album"], "limit": 1})  
    → got album URI spotify:album:1weenld61qoidwYuZ1GESA  
    spotify_playback({"action": "play", "context_uri": "spotify:album:1weenld61qoidwYuZ1GESA"})  
    
[/code]
Для «включи какого-нибудь <исполнителя>» (без конкретной песни) предпочтительнее `types: ["artist"]` и воспроизведение через контекстный URI исполнителя — Spotify обработает умное перемешивание. Если пользователь говорит «песню» или «этот трек», ищите через `types: ["track"]` и передавайте `uris: [track_uri]` для воспроизведения.
### "What's playing?" / "What am I listening to?"[​](<#whats-playing--what-am-i-listening-to> "Direct link to \"What's playing?\" / \"What am I listening to?\"")
Один вызов — не объединяйте get_state после get_currently_playing.
[code] 
    spotify_playback({"action": "get_currently_playing"})  
    
[/code]
Если возвращается 204/пусто (`is_playing: false`), сообщите пользователю, что ничего не играет. Не повторяйте попытку.
### "Pause" / "Skip" / "Volume 50"[​](<#pause--skip--volume-50> "Direct link to \"Pause\" / \"Skip\" / \"Volume 50\"")
Прямое действие, предварительная проверка не требуется.
[code] 
    spotify_playback({"action": "pause"})  
    spotify_playback({"action": "next"})  
    spotify_playback({"action": "set_volume", "volume_percent": 50})  
    
[/code]
### "Add to my <playlist name> playlist"[​](<#add-to-my-playlist-name-playlist> "Direct link to \"Add to my <playlist name> playlist\"")
  1. `spotify_playlists list` чтобы найти ID плейлиста по имени
  2. Получить URI трека (из текущего воспроизведения или поиска)
  3. `spotify_playlists add_items` с playlist_id и URI


[code] 
    spotify_playlists({"action": "list"})  
    → found "Late Night Jazz" = 37i9dQZF1DX4wta20PHgwo  
    spotify_playback({"action": "get_currently_playing"})  
    → current track uri = spotify:track:0DiWol3AO6WpXZgp0goxAV  
    spotify_playlists({"action": "add_items",  
                       "playlist_id": "37i9dQZF1DX4wta20PHgwo",  
                       "uris": ["spotify:track:0DiWol3AO6WpXZgp0goxAV"]})  
    
[/code]
### "Create a playlist called X and add the last 3 songs I played"[​](<#create-a-playlist-called-x-and-add-the-last-3-songs-i-played> "Direct link to \"Create a playlist called X and add the last 3 songs I played\"")
[code] 
    spotify_playback({"action": "recently_played", "limit": 3})  
    spotify_playlists({"action": "create", "name": "Focus 2026"})  
    → got playlist_id back in response  
    spotify_playlists({"action": "add_items", "playlist_id": <id>, "uris": [<3 uris>]})  
    
[/code]
### "Save / unsave / is this saved?"[​](<#save--unsave--is-this-saved> "Direct link to \"Save / unsave / is this saved?\"")
Используйте `spotify_library` с правильным `kind`.
[code] 
    spotify_library({"kind": "tracks", "action": "save", "uris": ["spotify:track:..."]})  
    spotify_library({"kind": "albums", "action": "list", "limit": 50})  
    
[/code]
### "Transfer playback to my <device>"[​](<#transfer-playback-to-my-device> "Direct link to \"Transfer playback to my <device>\"")
[code] 
    spotify_devices({"action": "list"})  
    → pick the device_id by matching name/type  
    spotify_devices({"action": "transfer", "device_id": "<id>", "play": true})  
    
[/code]
## Critical failure modes[​](<#critical-failure-modes> "Direct link to Critical failure modes")
**`403 Forbidden — No active device found`** при любом действии с воспроизведением означает, что Spotify не запущен нигде. Сообщите пользователю: «Сначала откройте Spotify на телефоне/компьютере/веб-плеере, запустите любой трек на секунду, затем повторите попытку». Не повторяйте вызов инструмента вслепую — он завершится с той же ошибкой. Вы можете вызвать `spotify_devices list` для подтверждения; пустой список означает отсутствие активного устройства.
**`403 Forbidden — Premium required`** означает, что пользователь на Free и попытался изменить воспроизведение. Не повторяйте попытку; сообщите, что это действие требует Premium. Операции чтения всё ещё работают (поиск, плейлисты, библиотека, get_state).
**`204 No Content` на `get_currently_playing`** НЕ является ошибкой — это означает, что ничего не играет. Инструмент возвращает `is_playing: false`. Просто сообщите об этом пользователю.
**`429 Too Many Requests`** = ограничение частоты запросов. Подождите и повторите попытку один раз. Если это продолжается, вы зациклились — остановитесь.
**`401 Unauthorized` после повтора** — токен обновления отозван. Скажите пользователю выполнить `hermes auth spotify` снова.
## URI and ID formats[​](<#uri-and-id-formats> "Direct link to URI and ID formats")
Spotify использует три взаимозаменяемых формата ID. Инструменты принимают все три и нормализуют:
  * URI: `spotify:track:0DiWol3AO6WpXZgp0goxAV` (предпочтительно)
  * URL: `https://open.spotify.com/track/0DiWol3AO6WpXZgp0goxAV`
  * Bare ID: `0DiWol3AO6WpXZgp0goxAV`


Если сомневаетесь, используйте полные URI. Результаты поиска возвращают URI в поле `uri` — передавайте их напрямую.
Типы сущностей: `track`, `album`, `artist`, `playlist`, `show`, `episode`. Используйте правильный тип для действия — `spotify_playback.play` с `context_uri` ожидает альбом/плейлист/исполнителя; `uris` ожидает массив URI треков.
## What NOT to do[​](<#what-not-to-do> "Direct link to What NOT to do")
  * **Не вызывайте`get_state` перед каждым действием.** Spotify принимает play/pause/skip без предварительной проверки. Проверяйте состояние только когда пользователь спросил «что играет» или вам нужно понять устройство/трек.
  * **Не описывайте результаты поиска, если вас не просили.** Если пользователь сказал «включи X», найдите, возьмите верхний URI, включите. Он услышит, что это не то, если это не то.
  * **Не повторяйте попытку при`403 Premium required` или `403 No active device`.** Это постоянные ошибки до действия пользователя.
  * **Не используйте`spotify_search` для поиска плейлиста по имени** — это ищет в публичном каталоге Spotify. Пользовательские плейлисты получаются через `spotify_playlists list`.
  * **Не смешивайте`kind: "tracks"` с URI альбомов** в `spotify_library` (или наоборот). Инструмент нормализует ID, но конечная точка API отличается.


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to use this skill](<#when-to-use-this-skill>)
  * [The 7 tools](<#the-7-tools>)
  * [Canonical patterns (minimize tool calls)](<#canonical-patterns-minimize-tool-calls>)
    * ["Play <artist/track/album>"](<#play-artisttrackalbum>)
    * ["What's playing?" / "What am I listening to?"](<#whats-playing--what-am-i-listening-to>)
    * ["Pause" / "Skip" / "Volume 50"](<#pause--skip--volume-50>)
    * ["Add to my <playlist name> playlist"](<#add-to-my-playlist-name-playlist>)
    * ["Create a playlist called X and add the last 3 songs I played"](<#create-a-playlist-called-x-and-add-the-last-3-songs-i-played>)
    * ["Save / unsave / is this saved?"](<#save--unsave--is-this-saved>)
    * ["Transfer playback to my <device>"](<#transfer-playback-to-my-device>)
  * [Critical failure modes](<#critical-failure-modes>)
  * [URI and ID formats](<#uri-and-id-formats>)
  * [What NOT to do](<#what-not-to-do>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/media/media-spotify -->
