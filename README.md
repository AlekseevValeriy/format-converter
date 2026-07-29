# Format converter

CLI приложения для конвертации файлов в другие форматы

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
python -m formatconverter "mode" "path" "old_lang" "new_lang"
```

## Помощь

```bash
cd src
python -m formatconverter --help
```

```bash
usage: __main__.py [-h] {file,directory} path {markdown,latex} {markdown,latex}

positional arguments:
  {file,directory}  conversion mode
  path              the path of the coverted file
  {markdown,latex}  the old language of the file
  {markdown,latex}  the new language of the file

options:
  -h, --help        show this help message and exit
```

## Лицензия
Распространяется по лицензии [MIT](LICENSE).
