# Format converter

CLI приложение для конвертации файлов в другие форматы

## Технологии

![Python](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=Python&style=flat)

## Возможности

- Хранение промежуточного преставления в AST
- Расширяемая архитектура, позволяющая добавлять другие парсеры и форматоры
- Доступен перевод из `markdown` в `latex` и обратно

## Установка

```bash
git clone https://github.com/AlekseevValeriy/format-converter.git
cd format-converter
```

## Использование

```bash
cd src
python -m formatconverter -m "mode" -s "source" -p "path" -o "old_lang" -n "new_lang"
```

## Помощь

```bash
cd src
python -m formatconverter --help
```

```bash
usage: __main__.py [-h] -m {standard,test,experiment} [-s {file,directory}] [-p PATH] [-o {markdown,latex}] [-n {markdown,latex}]

options:
  -h, --help            show this help message and exit
  -m {standard,test,experiment}, --mode {standard,test,experiment}
                        work_mode
  -s {file,directory}, --source {file,directory}
                        conversion source
  -p PATH, --path PATH  the path of the coverted file
  -o {markdown,latex}, --old_lang {markdown,latex}
                        the old language of the file
  -n {markdown,latex}, --new_lang {markdown,latex}
                        the new language of the file
```

## Лицензия
Распространяется по лицензии [MIT](LICENSE).
