from mu.command import BaseCommand


def test_get_name():
    command = BaseCommand()
    assert command.get_name() == 'base_command'


def test_base_command_get_group():
    command = BaseCommand()
    assert command.get_group() == 'base'


def test_base_command_get_group_with_custom_group():
    command = BaseCommand()
    command.group = "another"
    assert command.get_group() == "another"
