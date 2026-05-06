На этой странице
Хостинг модифицированных серверов Minecraft (CurseForge, Modrinth).
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")

|---|---  
|Источник| Встроенный (устанавливается по умолчанию)  
|Путь| `skills/gaming/minecraft-modpack-server`  
## Справочник: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочник: полный SKILL.md")
info
Ниже приведено полное определение навыка, которое Hermes загружает при его активации. Это те инструкции, которые видит агент, когда навык активен.
# Настройка сервера Minecraft с модпаком
## Когда использовать[​](<#when-to-use> "Прямая ссылка на Когда использовать")
  * Пользователь хочет настроить модифицированный сервер Minecraft из zip-архива серверной сборки
  * Пользователю нужна помощь с конфигурацией сервера NeoForge/Forge
  * Пользователь спрашивает о настройке производительности сервера Minecraft или резервном копировании


## Сначала соберите предпочтения пользователя[​](<#gather-user-preferences-first> "Прямая ссылка на Сначала соберите предпочтения пользователя")
Перед началом настройки спросите пользователя:
  * **Название сервера / MOTD** — что должно отображаться в списке серверов?
  * **Сид (Seed)** — конкретный сид или случайный?
  * **Сложность** — мирная / лёгкая / нормальная / сложная?
  * **Режим игры** — выживание / креатив / приключение?
  * **Online mode** — true (аутентификация Mojang, лицензионные аккаунты) или false (LAN/пиратка)?
  * **Количество игроков** — сколько игроков ожидается? (влияет на настройку ОЗУ и дистанции просмотра)
  * **Выделение ОЗУ** — или пусть агент решит на основе количества модов и доступной ОЗУ?
  * **Дистанция просмотра / симуляции** — или пусть агент выберет на основе количества игроков и железа?
  * **PvP** — включено или выключено?
  * **Белый список (Whitelist)** — открытый сервер или только по списку?
  * **Резервное копирование** — нужны ли автоматические бекапы? Как часто?

Используйте разумные значения по умолчанию, если пользователю всё равно, но всегда спрашивайте перед генерацией конфига.
## Шаги[​](<#steps> "Прямая ссылка на Шаги")
### 1\\. Скачать и проверить сборку[​](<#1-download--inspect-the-pack> "Прямая ссылка на 1. Скачать и проверить сборку")
[code] 
    mkdir -p ~/minecraft-server  
    cd ~/minecraft-server  
    wget -O serverpack.zip "<URL>"  
    unzip -o serverpack.zip -d server  
    ls server/  
    
[/code]
Ищите: `startserver.sh`, установочный jar (neoforge/forge), `user_jvm_args.txt`, папку `mods/`. Проверьте скрипт, чтобы определить: тип загрузчика модов, версию и требуемую версию Java.
### 2\\. Установить Java[​](<#2-install-java> "Прямая ссылка на 2. Установить Java")
  * Minecraft 1.21+ → Java 21: `sudo apt install openjdk-21-jre-headless`
  * Minecraft 1.18-1.20 → Java 17: `sudo apt install openjdk-17-jre-headless`
  * Minecraft 1.16 и ниже → Java 8: `sudo apt install openjdk-8-jre-headless`
  * Проверка: `java -version`


### 3\\. Установить загрузчик модов[​](<#3-install-the-mod-loader> "Прямая ссылка на 3. Установить загрузчик модов")
В большинстве серверных сборок есть скрипт установки. Используйте переменную окружения INSTALL_ONLY для установки без запуска:
[code] 
    cd ~/minecraft-server/server  
    ATM10_INSTALL_ONLY=true bash startserver.sh  
    # Или для обычных сборок Forge:  
    # java -jar forge-*-installer.jar --installServer  
    
[/code]
Это скачивает библиотеки, патчит серверный jar и т.д.
### 4\\. Принять EULA[​](<#4-accept-eula> "Прямая ссылка на 4. Принять EULA")
[code] 
    echo "eula=true" > ~/minecraft-server/server/eula.txt  
    
[/code]
### 5\\. Настроить server.properties[​](<#5-configure-serverproperties> "Прямая ссылка на 5. Настроить server.properties")
Ключевые настройки для модифицированного/LAN-сервера:
[code] 
    motd=\\u00a7b\\u00a7lНазвание сервера \\u00a7r\\u00a78| \\u00a7aНазвание модпака  
    server-port=25565  
    online-mode=true          # false для LAN без аутентификации Mojang  
    enforce-secure-profile=true  # должно соответствовать online-mode  
    difficulty=hard            # большинство модпаков сбалансированы под сложную сложность  
    allow-flight=true          # ОБЯЗАТЕЛЬНО для модифицированных серверов (летающие маунты/предметы)  
    spawn-protection=0         # разрешить всем строить на спавне  
    max-tick-time=180000       # для модифицированных серверов нужен больший таймаут тиков  
    enable-command-block=true  
    
[/code]
Настройки производительности (масштабируются под железо):
[code] 
    # 2 игрока, мощная машина:  
    view-distance=16  
    simulation-distance=10  
      
    # 4-6 игроков, средняя машина:  
    view-distance=10  
    simulation-distance=6  
      
    # 8+ игроков или слабое железо:  
    view-distance=8  
    simulation-distance=4  
    
[/code]
### 6\\. Настроить аргументы JVM (user_jvm_args.txt)[​](<#6-tune-jvm-args-user_jvm_argstxt> "Прямая ссылка на 6. Настроить аргументы JVM (user_jvm_args.txt)")
Масштабируйте ОЗУ под количество игроков и модов. Эмпирическое правило для модифицированных серверов:
  * 100-200 модов: 6-12 ГБ
  * 200-350+ модов: 12-24 ГБ
  * Оставьте как минимум 8 ГБ свободными для ОС и других задач


[code] 
    -Xms12G  
    -Xmx24G  
    -XX:+UseG1GC  
    -XX:+ParallelRefProcEnabled  
    -XX:MaxGCPauseMillis=200  
    -XX:+UnlockExperimentalVMOptions  
    -XX:+DisableExplicitGC  
    -XX:+AlwaysPreTouch  
    -XX:G1NewSizePercent=30  
    -XX:G1MaxNewSizePercent=40  
    -XX:G1HeapRegionSize=8M  
    -XX:G1ReservePercent=20  
    -XX:G1HeapWastePercent=5  
    -XX:G1MixedGCCountTarget=4  
    -XX:InitiatingHeapOccupancyPercent=15  
    -XX:G1MixedGCLiveThresholdPercent=90  
    -XX:G1RSetUpdatingPauseTimePercent=5  
    -XX:SurvivorRatio=32  
    -XX:+PerfDisableSharedMem  
    -XX:MaxTenuringThreshold=1  
    
[/code]
### 7\\. Открыть брандмауэр[​](<#7-open-firewall> "Прямая ссылка на 7. Открыть брандмауэр")
[code] 
    sudo ufw allow 25565/tcp comment "Minecraft Server"  
    
[/code]
Проверка: `sudo ufw status | grep 25565`
### 8\\. Создать скрипт запуска[​](<#8-create-launch-script> "Прямая ссылка на 8. Создать скрипт запуска")
[code] 
    cat > ~/start-minecraft.sh << 'EOF'  
    #!/bin/bash  
    cd ~/minecraft-server/server  
    java @user_jvm_args.txt @libraries/net/neoforged/neoforge/<VERSION>/unix_args.txt nogui  
    EOF  
    chmod +x ~/start-minecraft.sh  
    
[/code]
Примечание: для Forge (не NeoForge) путь к файлу аргументов отличается. Проверьте `startserver.sh` для точного пути.
### 9\\. Настроить автоматическое резервное копирование[​](<#9-set-up-automated-backups> "Прямая ссылка на 9. Настроить автоматическое резервное копирование")
Создайте скрипт резервного копирования:
[code] 
    cat > ~/minecraft-server/backup.sh << 'SCRIPT'  
    #!/bin/bash  
    SERVER_DIR="$HOME/minecraft-server/server"  
    BACKUP_DIR="$HOME/minecraft-server/backups"  
    WORLD_DIR="$SERVER_DIR/world"  
    MAX_BACKUPS=24  
    mkdir -p "$BACKUP_DIR"  
    [ ! -d "$WORLD_DIR" ] && echo "[BACKUP] Нет папки world" && exit 0  
    TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)  
    BACKUP_FILE="$BACKUP_DIR/world_${TIMESTAMP}.tar.gz"  
    echo "[BACKUP] Начало в $(date)"  
    tar -czf "$BACKUP_FILE" -C "$SERVER_DIR" world  
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)  
    echo "[BACKUP] Сохранено: $BACKUP_FILE ($SIZE)"  
    BACKUP_COUNT=$(ls -1t "$BACKUP_DIR"/world_*.tar.gz 2>/dev/null | wc -l)  
    if [ "$BACKUP_COUNT" -gt "$MAX_BACKUPS" ]; then  
        REMOVE=$((BACKUP_COUNT - MAX_BACKUPS))  
        ls -1t "$BACKUP_DIR"/world_*.tar.gz | tail -n "$REMOVE" | xargs rm -f  
        echo "[BACKUP] Удалено $REMOVE старых бекапов"  
    fi  
    echo "[BACKUP] Завершено в $(date)"  
    SCRIPT  
    chmod +x ~/minecraft-server/backup.sh  
    
[/code]
Добавьте задачу в cron (каждый час):
[code] 
    (crontab -l 2>/dev/null | grep -v "minecraft/backup.sh"; echo "0 * * * * $HOME/minecraft-server/backup.sh >> $HOME/minecraft-server/backups/backup.log 2>&1") | crontab -  
    
[/code]
## Подводные камни[​](<#pitfalls> "Прямая ссылка на Подводные камни")
  * ВСЕГДА устанавливайте `allow-flight=true` для модифицированных серверов — моды с реактивными ранцами/полётом иначе будут кикать игроков
  * `max-tick-time=180000` или больше — на модифицированных серверах часто бывают долгие тики во время генерации мира
  * Первый запуск МЕДЛЕННЫЙ (несколько минут для больших сборок) — не паникуйте
  * Предупреждения «Can't keep up!» при первом запуске — это нормально, стабилизируется после начальной генерации чанков
  * Если online-mode=false, установите enforce-secure-profile=false тоже, иначе клиенты будут отклоняться
  * В startserver.sh сборки часто есть цикл автоматического перезапуска — сделайте чистый скрипт запуска без него
  * Удалите папку world/, чтобы перегенерировать мир с новым сидом
  * В некоторых сборках есть переменные окружения для управления поведением (например, ATM10 использует ATM10_JAVA, ATM10_RESTART, ATM10_INSTALL_ONLY)


## Проверка[​](<#verification> "Прямая ссылка на Проверка")
  * `pgrep -fa neoforge` или `pgrep -fa minecraft` — проверить, запущен ли сервер
  * Проверьте логи: `tail -f ~/minecraft-server/server/logs/latest.log`
  * Ищите «Done (Xs)!» в логе — сервер готов
  * Проверьте подключение: игрок добавляет IP сервера в мультиплеере


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочник: полный SKILL.md](<#reference-full-skillmd>)
  * [Когда использовать](<#when-to-use>)
  * [Сначала соберите предпочтения пользователя](<#gather-user-preferences-first>)
  * [Шаги](<#steps>)
    * [1\\. Скачать и проверить сборку](<#1-download--inspect-the-pack>)
    * [2\\. Установить Java](<#2-install-java>)
    * [3\\. Установить загрузчик модов](<#3-install-the-mod-loader>)
    * [4\\. Принять EULA](<#4-accept-eula>)
    * [5\\. Настроить server.properties](<#5-configure-serverproperties>)
    * [6\\. Настроить аргументы JVM (user_jvm_args.txt)](<#6-tune-jvm-args-user_jvm_argstxt>)
    * [7\\. Открыть брандмауэр](<#7-open-firewall>)
    * [8\\. Создать скрипт запуска](<#8-create-launch-script>)
    * [9\\. Настроить автоматическое резервное копирование](<#9-set-up-automated-backups>)
  * [Подводные камни](<#pitfalls>)
  * [Проверка](<#verification>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/gaming/gaming-minecraft-modpack-server -->
