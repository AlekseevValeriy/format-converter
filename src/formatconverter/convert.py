from formatconverter.objects.dataclasses import ConvertPack
from formatconverter.objects.types import Text


def convert(text: list[str], pack: ConvertPack) -> Text:
    node = pack.parser.parse(text)
    generater_code = pack.code_generator.generate(node)

    return generater_code
