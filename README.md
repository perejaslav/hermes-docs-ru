# Документация Hermes Agent — Перевод на русский 🇷🇺

[![Status](https://img.shields.io/badge/статус-100%25%20переведено-brightgreen)](https://hermes-agent.nousresearch.com/docs)

Полный перевод документации [Hermes Agent](https://hermes-agent.nousresearch.com) — open-source CLI AI-агента от Nous Research.

## Что внутри

- **293 страницы** документации, полностью переведённые с английского на русский
- Все оригинальные markdown-файлы сохранены в `originals/`
- Все переводы в `translated/` с идентичной структурой директорий
- `translation_state.json` — отслеживание прогресса перевода
- `update_check.py` — проверка обновлений оригинальной документации
- `scrape.py` — инструмент для первичного скачивания

## Структура проекта

```
~/hermes-docs-ru/
├── originals/              # Оригинальные .md файлы (скачанные с сайта)
│   └── docs/...
├── translated/             # Переводы на русский (та же структура)
│   └── docs/...
├── small_batches/
│   └── _batches.json       # Определения батчей для перевода
├── scrape.py               # Инструмент скачивания
├── update_check.py         # Проверка обновлений
└── translation_state.json  # Состояние перевода
```

## Как переводили

Перевод выполнен AI-субагентами (`delegate_task` в Hermes Agent), по 1-2 страницы на батч, 3 батча параллельно. Ключевая методология:

1. **Фаза A (субагенты)** — каждый читает оригинал, переводит, сохраняет в `translated/`
2. **Фаза B (родитель)** — после всех субагентов синхронизирует `translated/` с `translation_state.json`
3. **Split-стратегия** — файлы >60KB разбиваются на части, переводятся отдельно, затем склеиваются
4. **Без race condition** — субагенты не пишут в общее состояние, только родитель

## Обновление

Когда в документации Hermes Agent появятся новые страницы:

```bash
cd ~/hermes-docs-ru
python3 update_check.py           # проверить, что нового
python3 update_check.py --apply   # скачать новое, подготовить к переводу
```

Затем запустить workflow перевода только для новых/изменённых страниц.

## English version

For the English description of this project, see [README.en.md](README.en.md).

## Лицензия

Переведённый контент распространяется на тех же условиях, что и оригинальная документация Hermes Agent.
