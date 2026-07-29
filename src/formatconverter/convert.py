from formatconverter.objects.dataclasses import ConvertPack
from formatconverter.objects.types import Text


def convert(text: Text, pack: ConvertPack) -> Text:
    node = pack.parser.parse(text)
    converted_text = pack.converter.convert(node)

    return converted_text
