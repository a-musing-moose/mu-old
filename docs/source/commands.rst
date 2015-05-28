.. _commands:

========
Commands
========

.. contents::
    :local:
    :depth: 1

Built In Commands
=================

Mu has a number of built in commands to get you up and running. Mu commands can
be run via the command link script ``manage.py``

Core Arguments
--------------

``-h, --help``
    Print out the usage help message.

``-s SETTINGS, --settings SETTINGS``
    Pass in the settings file you wish to use.

Commands
--------

``apps``
    Lists the registered apps

``run``
    Runs the registered appplication sessions

``shell``
    Opens an interactive ipython shell


Custom Commands
===============

You can also add you own, custom commands to mu. Customer commands are classes
that extend ``mu.command.BaseCommand``. Example:

.. code-block:: python

    from mu.command import BaseCommand


    class PrintCommand(BaseCommand):
        group = "mycommands"
        description = "this is my command"

        def execute(self, args, settings):
            print("HERE")

The above example simply prints ``HERE`` when ``./manage.py print_command`` is
run. When help text is printed out, it will be shown under the section
``[mycommands]``. If no ``group`` is supplied, then the name of the module the
command is defined in is used.


The ensure that mu sees your custom commands you need to ensure that instance
of your command classes are returned by the ``get_commands`` method of your
AppConfig. e.g.:

.. code-block:: python

    from mu.apps import AppConfig
    from .sessions import TestSession
    from .commands import PrintCommand


    class AnAppConfig(AppConfig):
        name = "A Test Service"
        label = "anapp"
        session_class = TestSession

    def get_commands(self):
        return [PrintCommand()]

