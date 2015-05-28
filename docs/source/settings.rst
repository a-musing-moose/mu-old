.. _settings:

========
Settings
========

.. contents::
    :local:
    :depth: 1


Core Settings
=============

Here's a list of settings available in the Mu core and their default values.

.. setting:: name

name
----

Default: ``components``

The name of the project, the combination of all defined services

.. setting:: router_dsn

router_dsn
----------

Default: ``ws://127.0.0.1:8080/ws``

The DSN of the crossbar/WAMP router

.. setting:: realm

realm
-----

Default: ``realm1``

The name of the WAMP realm to join.


.. setting:: apps

Default: ``[]`` (Empty list)

The list of service modules. Each module should define a ``config`` attribute
in it's ``__init__`` module which is an instance of a ``mu.apps.AppConfig``
class.
Example:

.. code-block:: yaml

    services:
        - mymodule
        - aothermodule


Environmental Variables in Settings
===================================

It is possible to define settings to be picked up from environmental variables
using a specific YAML format:

.. code-block:: yaml

    a_setting:
        env: A_SETTING
        default: default value

In the example above, the setting ``a_setting`` will be taken from the
environmental variable ``A_SETTING`` if it exists. If not, then the value
``"default value"`` will be used.

.. warning::
    Currently there is no method to convert environmental variables to any
    other data type than ``str``.
