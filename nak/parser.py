import argparse

from .command import Command


class Parser:
    def __init__(self):
        self.command = Command()
        pass

    def create_parser(self):
        # create the top-level parser
        parser = argparse.ArgumentParser(
            description='''
Usage:
    nak [command]

available commands:
    setup         Initialize a new app, will create config at config.yml and environment at .env file
    build         Compress file as zip
    push          Upload file to app server
''',
            usage=argparse.SUPPRESS,
            epilog='Use "nak [command] --help" for more information about a command.',
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=argparse.SUPPRESS
        )
        subparsers = parser.add_subparsers(title='Available Commands', help=argparse.SUPPRESS)

        # create the parser for the "setup" command
        parser_setup = subparsers.add_parser(
            'setup',
            help='setup',
            usage=argparse.SUPPRESS,
            description='''
Usage:
    nak setup
        ''',
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser_setup.set_defaults(func=self.command.setup)
        # create the parser for the "build" command
        parser_build = subparsers.add_parser(
            'build',
            help='build',
            usage=argparse.SUPPRESS,
            description='''
Usage:
    nak build
        ''',
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser_build.set_defaults(func=self.command.build)
        # create the parser for the "push" command
        parser_push = subparsers.add_parser(
            'push',
            help='push',
            usage=argparse.SUPPRESS,
            description='''
Usage:
    nak push
        ''',
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser_push.set_defaults(func=self.command.push)
        return parser
