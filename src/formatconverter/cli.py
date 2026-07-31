import argparse
from pathlib import Path

from formatconverter.enums import ConvertMode, LangsEnum, WorkMode
from formatconverter.objects.dataclasses import ParsedInput


class CLI:
    def parse(self) -> ParsedInput:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-m", "--mode",
            help="work_mode",
            choices=[
                WorkMode.standard.name,
                WorkMode.test.name,
                WorkMode.experiment.name,
            ],
            default=WorkMode.standard.name,
            required=True,
        )
        
        parser.add_argument(
            "-s", "--source",
            help="conversion source",
            choices=[ConvertMode.file.name, ConvertMode.directory.name],
            default=ConvertMode.file.name,
            required=False,
        )
        parser.add_argument(
            "-p", "--path", help="the path of the coverted file", type=Path, required=False
        )
        parser.add_argument(
            "-o", "--old_lang",
            help="the old language of the file",
            type=str,
            choices=[LangsEnum.markdown.name, LangsEnum.latex.name],
            required=False,
        )
        parser.add_argument(
            "-n", "--new_lang",
            help="the new language of the file",
            type=str,
            choices=[LangsEnum.markdown.name, LangsEnum.latex.name],
            required=False,
        )

        args = parser.parse_args()
        
        match WorkMode[args.mode]:
            case WorkMode.standard:
                return ParsedInput(
                    WorkMode[args.mode],
                    ConvertMode[args.source],
                    args.path,
                    LangsEnum[args.old_lang],
                    LangsEnum[args.new_lang],
                )
            case WorkMode.test | WorkMode.experiment:
                return ParsedInput(
                    WorkMode[args.mode],
                    None,
                    None,
                    None,
                    None
                )

        

    def info(self, data):
        print(data)

    def error(self, data):
        print(f"[ERROR] {data}")
