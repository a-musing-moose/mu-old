import argparse
import os
import sys

from collections import defaultdict
from colorama import init, deinit, Fore, Style

from mu.command import base


MU_COMMANDS = [
    base.Run(),
    base.Shell(),
    base.Apps(),
]


def bootstrap():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        nargs="?",
        help="sub-command to run"
    )
    parser.add_argument(
        '-s',
        '--settings',
        dest='settings',
        default="settings.yml",
        required=False
    )
    args = parser.parse_args(sys.argv[1:2])
    os.environ['MU_SETTINGS'] = args.settings
    from mu.conf import settings
    commands = get_commands(settings)
    if args.command is None:
        parser.print_help()
        print_commands(commands)
    else:
        command_name = args.command
        if command_name not in commands:
            print("{0} is not a recognised command".format(command_name))
            print_commands(commands)
        else:
            command = commands[command_name]
            del commands
            try:
                command._go(sys.argv[2:], settings)
            except KeyboardInterrupt:
                pass


def get_commands(settings):
    commands = {}
    for command in MU_COMMANDS + settings.get_commands():
        commands[command.get_name()] = command
    return commands


def print_commands(commands):
    init()
    print("\nAvailable commands:")
    groups = defaultdict(list)
    for command in commands.values():
        groups[command.get_group()].append(command)

    for group_name in sorted(groups.keys()):
        print("{0}\n[{1}]{2}".format(
            Fore.GREEN,
            group_name,
            Style.RESET_ALL
        ))
        for command in groups[group_name]:
            command_name = "{0}{1}{2}".format(
                Fore.RED + Style.BRIGHT,
                command.get_name(),
                Style.RESET_ALL
            )
            description = command.get_description()
            if description != "":
                description = " - {0}".format(description)
            print("    {0}{1}".format(
                command_name,
                description
            ))
    deinit()
