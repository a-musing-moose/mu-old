from mu.command.base import BaseCommand, Components


# BASE COMMAND TESTS


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


def test_base_command_get_description():
    command = BaseCommand()
    assert command.get_description() == ""


def test_base_command_get_description_with_custom_description():
    command = BaseCommand()
    command.description = "description"
    assert command.get_description() == "description"


# COMPONENTS COMMAND TEST


def test_components_command_is_in_mu_group():
    command = Components()
    assert command.get_group() == "mu"


def test_components_command_name_is_components():
    command = Components()
    assert command.get_name() == "components"
