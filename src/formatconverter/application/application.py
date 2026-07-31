from formatconverter.cli import CLI
from formatconverter.enums import WorkMode

from .experiment_mode import experiment_mode
from .standard_mode import standard_mode
from .test_mode import test_mode


def run():
    cli = CLI()
    input = cli.parse()

    match input.work_mode:
        case WorkMode.standard: standard_mode(cli, input)
        case WorkMode.test: test_mode()
        case WorkMode.experiment: experiment_mode()
