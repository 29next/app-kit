import argparse

from .command import Command


class Parser:
    def __init__(self):
        self.command = Command()
        pass

    def _add_config_arguments(self, parser):
        parser.add_argument('-u', '--user_email', dest="user_email", help=argparse.SUPPRESS)
        parser.add_argument('-p', '--password', dest="password", help=argparse.SUPPRESS)
        parser.add_argument('-c', '--client_id', dest="client_id", help=argparse.SUPPRESS)
        parser.add_argument('-e', '--env', dest="env", default='development', help=argparse.SUPPRESS)

    def create_parser(self):
        option_commands = '''
options:
    '-u', '--user_email'             User email for authenticate
    '-p', '--password'               User password for authenticate
    '-c', '--client_id'              App client id'''

        # create the top-level parser
        parser = argparse.ArgumentParser(
            description='''
Usage:
    nak [command] [options]

available commands:
    setup         Initialize a new app, will create config at config.yml and environment at .env file
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
    nak setup [options]
        ''' + option_commands,
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser_setup.set_defaults(func=self.command.setup)
        self._add_config_arguments(parser_setup)

        # create the parser for the "build" command
        parser_build = subparsers.add_parser(
            'build',
            help='build',
            usage=argparse.SUPPRESS,
            description='''
Usage:
    nak build [options]
        ''' + option_commands,
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser_build.set_defaults(func=self.command.build)
        self._add_config_arguments(parser_build)

        # create the parser for the "push" command
        parser_push = subparsers.add_parser(
            'push',
            help='push',
            usage=argparse.SUPPRESS,
            description='''
Usage:
    nak push [options]
        ''' + option_commands,
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser_push.set_defaults(func=self.command.push)
        self._add_config_arguments(parser_push)

        return parser
