from formatconverter.cli import CLI
from formatconverter.code_generators import LatexCodeGenerator, MarkdownCodeGenerator
from formatconverter.convert import convert
from formatconverter.enums import ConvertMode, LangsEnum
from formatconverter.file_system import FileSystem
from formatconverter.objects.dataclasses import ConvertPack, ParsedInput, ScenarioData
from formatconverter.parsers import LatexParser, MarkdownParser

scenarios = [
    ScenarioData(
        scenario_condition=lambda old, new: (
            (old, new) == (LangsEnum.latex, LangsEnum.markdown)
        ),
        convert_pack=ConvertPack(LatexParser(), MarkdownCodeGenerator()),
        old_suffix="tex",
        new_suffix="md",
    ),
    ScenarioData(
        scenario_condition=lambda old, new: (
            (old, new) == (LangsEnum.markdown, LangsEnum.latex)
        ),
        convert_pack=ConvertPack(MarkdownParser(), LatexCodeGenerator()),
        old_suffix="md",
        new_suffix="tex",
    ),
]

def standard_mode(cli: CLI, input: ParsedInput):
    if (
        not input.path
        or not input.path.exists()
        or not input.new_lang
        or not input.old_lang
    ):
        cli.error("Некорректные входные данные")
        return
    
    fs = FileSystem()
    files_content = []
    new_dir = None
    scenario = None

    for temp_scenario in scenarios:
        if temp_scenario.scenario_condition(input.old_lang, input.new_lang):
            scenario = temp_scenario
            cli.info("Найден соответствующий сценарий")
            break
    else:
        cli.error("Нет подходящего сценария")
        raise SystemExit(1)

    if input.path.is_file():
        files_content.append(fs.get_file_content(input.path))
        new_dir = input.path.parent
    elif input.path.is_dir():
        files_content = fs.get_files_content(input.path)
        new_dir = input.path
    else:
        cli.error("Указан некорректный путь")
        raise SystemExit(1)

    if not new_dir:
        cli.error("Некорректный путь выходной директории")
        return

    new_dir = fs.mkdir(new_dir, suffix=f"_{scenario.new_suffix}")

    for file_content in files_content:
        if file_content.path.suffix.lstrip(".") == scenario.old_suffix:
            file_content.path = fs.concat(new_dir, file_content.path)
            file_content.path =  fs.add_suffix(file_content.path, f".{scenario.new_suffix}")

            file_content.content = [
                f"{a}\n" for a in convert(file_content.content, scenario.convert_pack)
            ]

    fs.write_files(files_content)

    cli.info("Файлы записаны")