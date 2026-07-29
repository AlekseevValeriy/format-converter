import argparse
from pathlib import Path

from formatconverter.enums import ConvertMode, LangsEnum
from formatconverter.objects.dataclasses import ParsedInput


class CLI:
    def parse(self) -> ParsedInput:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "mode",
            help="conversion mode",
            choices=[ConvertMode.file.name, ConvertMode.directory.name],
        )
        parser.add_argument("path", help="the path of the coverted file", type=Path)
        parser.add_argument(
            "old_lang",
            help="the old language of the file",
            type=str,
            choices=[LangsEnum.markdown.name, LangsEnum.latex.name],
        )
        parser.add_argument(
            "new_lang",
            help="the new language of the file",
            type=str,
            choices=[LangsEnum.markdown.name, LangsEnum.latex.name],
        )

        args = parser.parse_args()
        return ParsedInput(ConvertMode[args.mode], args.path, LangsEnum[args.old_lang], LangsEnum[args.new_lang])

    def info(self, data):
        print(data)
        
    def error(self, data):
        print(f"[ERROR] {data}")