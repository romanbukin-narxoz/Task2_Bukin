# Как запустить Task 3

Архив содержит продолжение Task 2. Сохрани резервную копию старой папки, затем перенеси содержимое этой папки в существующий репозиторий Task2_Bukin с заменой файлов. Старую папку .git сохраняй. Файлы первой лабораторной не удаляй.

## Что уже сделано

В архиве уже есть выполненный ноутбук, сырые замеры, CSV, графики PNG и PDF, математическая модель, README и отчёт reports/Task3_Report.md. Они получены настоящим запуском кода, но только на 10 искусственных письмах из Task 2. Полноценное исследование на реальных письмах ещё не выполнено. Этот архив нельзя описывать как результаты на реальном корпусе.

В этой среде ячейки выполнены по порядку через IPython с сохранением настоящего вывода. Обычное ядро Jupyter здесь недоступно. Для выполнения требования Restart & Run All обязательно запусти команды ниже на своём компьютере.

## Повторный запуск на Windows

Открой папку Task2_Bukin. В адресной строке Проводника введи cmd и нажми Enter. Команды ниже вводи по одной. Используй Python 3.12, как в Task 2.

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-task3.txt
.venv\Scripts\python.exe -m ipykernel install --user --name python3 --display-name "Python 3"
.venv\Scripts\python.exe src\run_task3.py
```

Если рабочая .venv уже есть, первую команду можно пропустить. Дождись сообщения Task 3 analysis completed. Скрипт перезаписывает замеры, графики, отчёт и выводы ноутбука. Время выполнения моделей на твоём компьютере будет другим.

## Настоящие данные

Нужен разрешённый к использованию набор реальных писем с метками ham/spam. CSV должен содержать id,text,label; идентификаторы уникальные. Опиши источник и лицензию в docs/dataset.md, удали дубликаты и разделяй связанные цепочки писем так, чтобы не было утечки между обучением и тестом. Положи файл в data/private/emails.csv. Эта папка исключена из Git.

```bat
.venv\Scripts\python.exe src\run_task3.py --config configs\research.json
```

Без этого файла команда исследования не запустится. Не заменяй отсутствующие результаты придуманными числами. После запуска прочитай обновлённый отчёт и обсуди результаты.

## Что загружать в GitHub

Обнови существующий репозиторий Task2_Bukin. Если используешь загрузку через сайт, включи папки src, configs, docs, notebooks, reports, data/sample, data/raw, data/processed и файлы README.md, START_TASK3_RU.md, requirements-task3.txt, requirements.txt, config.json, .gitignore. Не загружай .venv, __pycache__, .ipynb_checkpoints, results и data/private. Скрытый файл .gitignore также нужно обновить.

Вариант через Git из существующего клона:

```bat
git status
git add README.md START_TASK3_RU.md requirements-task3.txt .gitignore src configs docs notebooks reports data/sample data/raw/test_run.jsonl data/processed
git diff --cached --stat
git commit -m "Add Task 3 analysis notebook and figures"
git push
```

Проверь список перед commit: в нём не должно быть окружения или частных писем. Если преподавателю нужен релиз, после проверки можно создать на GitHub релиз с тегом task3-smoke-v1 и названием Task 3 synthetic pipeline check. Для реального исследования используй отдельный тег после запуска настоящего корпуса.

## Что сдавать в LMS

По заданию подходят ссылка на публичный репозиторий и PDF либо Markdown. В этом архиве отчёт в разрешённом формате Markdown: reports/Task3_Report.md. Перед сдачей учитывай ограничение: сейчас работа демонстрационная. Для завершения исследовательской части нужен реальный корпус либо согласование такого объёма с преподавателем.
