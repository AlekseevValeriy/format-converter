from formatconverter.cli import CLI
from formatconverter.convert import convert
from formatconverter.converters import LatexConverter, MarkdownConverter
from formatconverter.enums import ConvertMode, LangsEnum
from formatconverter.file_system import FileSystem
from formatconverter.objects import ConvertPack, ScenarioData
from formatconverter.parsers import LatexParser, MarkdownParser

scenarios = [
    ScenarioData(
        scenario_condition=lambda old, new: (
            (old, new) == (LangsEnum.latex, LangsEnum.markdown)
        ),
        convert_pack=ConvertPack(LatexParser(), MarkdownConverter()),
        old_suffix="tex",
        new_suffix="md"
    ),
    ScenarioData(
        scenario_condition=lambda old, new: (
            (old, new) == (LangsEnum.markdown, LangsEnum.latex)
        ),
        convert_pack=ConvertPack(MarkdownParser(), LatexConverter()),
        old_suffix="md",
        new_suffix="tex"
    ),
]


def run():
    cli = CLI()
    fs = FileSystem()
    files_content = []
    new_dir = None
    scenario = None

    input = cli.parse()

    for temp_scenario in scenarios:
        if temp_scenario.scenario_condition(input.old_lang, input.new_lang):
            scenario = temp_scenario
            break
    else:
        cli.error("Нет подходящего сценария")
        raise SystemExit(1)

    match input.convert_mode:
        case ConvertMode.file:
            files_content.append(fs.get_file_content(input.path))
            new_dir = input.path.parent
        case ConvertMode.directory:
            files_content = fs.get_files_content(input.path)
            new_dir = input.path

    new_dir = fs.mkdir(new_dir, suffix=f"_{scenario.new_suffix}")

    for file_content in files_content:
        if file_content.path.suffix == scenario.old_suffix:
            file_content.path =  fs.add_suffix(file_content.path, f".{scenario.new_suffix}")
            file_content.content = convert(file_content.content, scenario.convert_pack)

    fs.write_files(files_content)
