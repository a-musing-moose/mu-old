import argparse
import re

from colorama import init, deinit, Fore, Style

from mu.runner import reloader
from mu.loading import load_from_path
from mu.apps import SessionsRunner


class BaseCommand(object):

    group = None
    description = None

    def _go(self, args, settings):
        parser = self.get_parser()
        args = parser.parse_args(args)
        return self.execute(args, settings)

    def execute(self, args, settings):
        pass

    def get_parser(self):
        parser = argparse.ArgumentParser()
        parser.description = self.get_description()
        return parser

    def get_name(self):
        s1 = re.sub(
            '(.)([A-Z][a-z]+)', r'\1_\2',
            self.__class__.__name__
        )
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def get_group(self):
        if self.group is None:
            return self.__class__.__module__.split(".")[-1]
        return self.group

    def get_description(self):
        if self.description is None:
            return ""
        return self.description


class Run(BaseCommand):

    group = "mu"
    description = "Run the μ component"

    def get_parser(self):
        parser = super(Run, self).get_parser()
        parser.add_argument(
            '-nr',
            '--no-reload',
            dest='use_reloader',
            action="store_false"
        )
        parser.add_argument(
            '-d',
            '--debug',
            dest="debug",
            action="store_true"
        )
        parser.add_argument(
            '-da',
            '--debug-app',
            dest="debug_app",
            action="store_true"
        )
        parser.add_argument(
            '-dw',
            '--debug-wamp',
            dest="debug_wamp",
            action="store_true"
        )
        parser.set_defaults(use_reloader=True, debug=False, debug_app=False,
                            debug_wamp=False)
        return parser

    def __main__(self):
        name = getattr(self.settings, "name", "components")
        print("Starting {0}".format(name))

        realm = getattr(self.settings, 'realm', 'realm1')
        router_dsn = getattr(
            self.settings,
            'router_dsn',
            'ws://127.0.0.1:8080/ws'
        )
        print("Connecting to {0} on router on {1}".format(
            realm,
            router_dsn
        ))

        runner = SessionsRunner(
            url=router_dsn,
            realm=realm,
            extra=self.settings,
            debug=self.debug,
            debug_wamp=self.debug_wamp,
            debug_app=self.debug_app
        )
        sessions = self.settings.get_session_classes()
        runner.run(sessions)

    def execute(self, args, settings):
        self.settings = settings
        self.debug = args.debug
        self.debug_wamp = args.debug_wamp
        self.debug_app = args.debug_app
        if args.use_reloader:
            reloader(self.__main__)
        else:
            self.__main__()


class Shell(BaseCommand):

    group = "mu"
    description = "Run an interactive shell"

    def execute(self, args, settings):
        try:
            from IPython import embed
        except ImportError:
            print("The mu shell requires IPython to be installed")
            return

        ns = {
            "settings": settings,
            "load_from_path": load_from_path
        }
        init()
        print("{0}# MU IMPORTS{1}".format(Style.BRIGHT, Style.RESET_ALL))
        for k, v in ns.items():
            print("{0}from {1} import {2}{3}".format(
                Fore.GREEN + Style.DIM,
                v.__module__,
                k,
                Style.RESET_ALL
            ))
        deinit()
        embed(user_ns=ns)


class Apps(BaseCommand):

    group = "mu"
    description = "List the registered apps"

    def execute(self, args, settings):
        print("{0}# REGISTERED APPS{1}".format(
            Style.BRIGHT,
            Style.RESET_ALL
        ))
        for service in settings.get_apps().values():
            print("    {0}{1}{2} - {3}".format(
                Fore.RED,
                service.get_label(),
                Style.RESET_ALL,
                service.get_name()
            ))
