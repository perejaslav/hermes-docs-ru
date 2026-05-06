На этой странице
Hermes предоставляет защищённые точки расширения (extension hooks) на `HermesCLI`, чтобы обёрточные CLI могли добавлять виджеты, привязки клавиш и настройки макета без переопределения метода `run()` длиной более 1000 строк. Это сохраняет ваше расширение независимым от внутренних изменений.
## Точки расширения[​](<#extension-points> "Прямая ссылка на Точки расширения")
Доступно пять точек расширения:
Хук| Назначение| Переопределить, когда...  
---|---|---  
`_get_extra_tui_widgets()`| Внедрение виджетов в макет| Нужен постоянный элемент UI (панель, строка состояния, мини-плеер)  
`_register_extra_tui_keybindings(kb, *, input_area)`| Добавление горячих клавиш| Нужны хоткеи (переключение панелей, элементы управления, модальные сочетания)  
`_build_tui_layout_children(**widgets)`| Полный контроль над порядком виджетов| Нужно изменить порядок или обернуть существующие виджеты (редко)  
`process_command()`| Добавление пользовательских слэш-команд| Нужна обработка `/mycommand` (существующий хук)  
`_build_tui_style_dict()`| Пользовательские стили prompt_toolkit| Нужны свои цвета или стили (существующий хук)  
Первые три — новые защищённые хуки. Последние два уже существовали.
## Быстрый старт: обёрточный CLI[​](<#quick-start-a-wrapper-cli> "Прямая ссылка на Быстрый старт: обёрточный CLI")
[code] 
    #!/usr/bin/env python3  
    """my_cli.py — Пример обёрточного CLI, расширяющего Hermes."""  
      
    from cli import HermesCLI  
    from prompt_toolkit.layout import FormattedTextControl, Window  
    from prompt_toolkit.filters import Condition  
      
      
    class MyCLI(HermesCLI):  
      
        def __init__(self, **kwargs):  
            super().__init__(**kwargs)  
            self._panel_visible = False  
      
        def _get_extra_tui_widgets(self):  
            """Добавить переключаемую информационную панель над строкой состояния."""  
            cli_ref = self  
            return [  
                Window(  
                    FormattedTextControl(lambda: "📊 Моя пользовательская панель"),  
                    height=1,  
                    filter=Condition(lambda: cli_ref._panel_visible),  
                ),  
            ]  
      
        def _register_extra_tui_keybindings(self, kb, *, input_area):  
            """F2 переключает пользовательскую панель."""  
            cli_ref = self  
      
            @kb.add("f2")  
            def _toggle_panel(event):  
                cli_ref._panel_visible = not cli_ref._panel_visible  
      
        def process_command(self, cmd: str) -> bool:  
            """Добавить слэш-команду /panel."""  
            if cmd.strip().lower() == "/panel":  
                self._panel_visible = not self._panel_visible  
                state = "видима" if self._panel_visible else "скрыта"  
                print(f"Панель теперь {state}")  
                return True  
            return super().process_command(cmd)  
      
      
    if __name__ == "__main__":  
        cli = MyCLI()  
        cli.run()  
    
[/code]
Запустите его:
[code] 
    cd ~/.hermes/hermes-agent  
    source .venv/bin/activate  
    python my_cli.py  
    
[/code]
## Справочник хуков[​](<#hook-reference> "Прямая ссылка на Справочник хуков")
### `_get_extra_tui_widgets()`[​](<#_get_extra_tui_widgets> "Прямая ссылка на _get_extra_tui_widgets")
Возвращает список виджетов prompt_toolkit для вставки в TUI-макет. Виджеты появляются **между spacer'ом и строкой состояния** — над областью ввода, но под основным выводом.
[code] 
    def _get_extra_tui_widgets(self) -> list:  
        return []  # по умолчанию: нет дополнительных виджетов  
    
[/code]
Каждый виджет должен быть контейнером prompt_toolkit (например, `Window`, `ConditionalContainer`, `HSplit`). Используйте `ConditionalContainer` или `filter=Condition(...)` чтобы сделать виджеты переключаемыми.
[code] 
    from prompt_toolkit.layout import ConditionalContainer, Window, FormattedTextControl  
    from prompt_toolkit.filters import Condition  
      
    def _get_extra_tui_widgets(self):  
        return [  
            ConditionalContainer(  
                Window(FormattedTextControl("Статус: подключено"), height=1),  
                filter=Condition(lambda: self._show_status),  
            ),  
        ]  
    
[/code]
### `_register_extra_tui_keybindings(kb, *, input_area)`[​](<#_register_extra_tui_keybindingskb--input_area> "Прямая ссылка на _register_extra_tui_keybindingskb--input_area")
Вызывается после того, как Hermes регистрирует свои собственные привязки клавиш, и до построения макета. Добавляйте свои привязки клавиш к `kb`.
[code] 
    def _register_extra_tui_keybindings(self, kb, *, input_area):  
        pass  # по умолчанию: нет дополнительных привязок клавиш  
    
[/code]
Параметры:
  * **`kb`** — Экземпляр `KeyBindings` для prompt_toolkit-приложения
  * **`input_area`** — Основной виджет `TextArea`, если нужно читать или изменять пользовательский ввод


[code] 
    def _register_extra_tui_keybindings(self, kb, *, input_area):  
        cli_ref = self  
      
        @kb.add("f3")  
        def _clear_input(event):  
            input_area.text = ""  
      
        @kb.add("f4")  
        def _insert_template(event):  
            input_area.text = "/search "  
    
[/code]
**Избегайте конфликтов** со встроенными привязками клавиш: `Enter` (отправка), `Escape Enter` (новая строка), `Ctrl-C` (прерывание), `Ctrl-D` (выход), `Tab` (принять автодополнение). Функциональные клавиши F2+ и Ctrl-комбинации обычно безопасны.
### `_build_tui_layout_children(**widgets)`[​](<#_build_tui_layout_childrenwidgets> "Прямая ссылка на _build_tui_layout_childrenwidgets")
Переопределяйте это только когда вам нужен полный контроль над порядком виджетов. Для большинства расширений используйте `_get_extra_tui_widgets()` вместо этого.
[code] 
    def _build_tui_layout_children(self, *, sudo_widget, secret_widget,  
        approval_widget, clarify_widget, model_picker_widget=None,  
        spinner_widget=None, spacer, status_bar, input_rule_top,  
        image_bar, input_area, input_rule_bot, voice_status_bar,  
        completions_menu) -> list:  
    
[/code]
Реализация по умолчанию возвращает (любые `None` виджеты отфильтровываются):
[code] 
    [  
        Window(height=0),       # якорь  
        sudo_widget,            # запрос пароля sudo (условный)  
        secret_widget,          # запрос секретного ввода (условный)  
        approval_widget,        # подтверждение опасных команд (условный)  
        clarify_widget,         # UI уточняющих вопросов (условный)  
        model_picker_widget,    # оверлей выбора модели (условный)  
        spinner_widget,         # спиннер "думаю" (условный)  
        spacer,                 # заполняет оставшееся вертикальное пространство  
        *self._get_extra_tui_widgets(),  # ВАШИ ВИДЖЕТЫ ИДУТ ЗДЕСЬ  
        status_bar,             # строка состояния модели/токенов/контекста  
        input_rule_top,         # ─── граница над вводом  
        image_bar,              # индикатор прикреплённых изображений  
        input_area,             # ввод текста пользователем  
        input_rule_bot,         # ─── граница под вводом  
        voice_status_bar,       # статус голосового режима (условный)  
        completions_menu,       # выпадающее меню автодополнения  
    ]  
    
[/code]
## Схема макета[​](<#layout-diagram> "Прямая ссылка на Схема макета")
Макет по умолчанию сверху вниз:
  1. **Область вывода** — прокручиваемая история диалога
  2. **Spacer**
  3. **Дополнительные виджеты** — из `_get_extra_tui_widgets()`
  4. **Строка состояния** — модель, контекст %, прошедшее время
  5. **Панель изображений** — количество прикреплённых изображений
  6. **Область ввода** — пользовательский запрос
  7. **Голосовой статус** — индикатор записи
  8. **Меню автодополнения** — подсказки автодополнения


## Советы[​](<#tips> "Прямая ссылка на Советы")
  * **Обновляйте отображение** после изменений состояния: вызовите `self._invalidate()`, чтобы инициировать перерисовку prompt_toolkit.
  * **Доступ к состоянию агента**: `self.agent`, `self.model`, `self.conversation_history` — всё доступно.
  * **Пользовательские стили**: Переопределите `_build_tui_style_dict()` и добавьте записи для ваших пользовательских классов стилей.
  * **Слэш-команды**: Переопределите `process_command()`, обрабатывайте свои команды и вызывайте `super().process_command(cmd)` для всего остального.
  * **Не переопределяйте`run()`** без крайней необходимости — хуки расширения существуют именно для того, чтобы избежать этой связанности.


  * [Точки расширения](<#extension-points>)
  * [Быстрый старт: обёрточный CLI](<#quick-start-a-wrapper-cli>)
  * [Справочник хуков](<#hook-reference>)
    * [`_get_extra_tui_widgets()`](<#_get_extra_tui_widgets>)
    * [`_register_extra_tui_keybindings(kb, *, input_area)`](<#_register_extra_tui_keybindingskb--input_area>)
    * [`_build_tui_layout_children(**widgets)`](<#_build_tui_layout_childrenwidgets>)
  * [Схема макета](<#layout-diagram>)
  * [Советы](<#tips>)



<!-- Источник: https://hermes-agent.nousresearch.com/docs/developer-guide/extending-the-cli -->
