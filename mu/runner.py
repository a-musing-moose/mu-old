import argparse
import os
import pyinotify
import sys

from autobahn.asyncio.wamp import ApplicationRunner
from mu.loading import load_from_path

from asyncio import get_event_loop


class AsyncioNotifier(pyinotify.Notifier):

    def __init__(self, watch_manager, loop, callback=None,
                 default_proc_fun=None, read_freq=0, threshold=0,
                 timeout=None):
        self.loop = loop
        self.handle_read_callback = callback
        super(AsyncioNotifier, self).__init__(
            watch_manager,
            default_proc_fun,
            read_freq,
            threshold, timeout
        )
        loop.add_reader(self._fd, self.handle_read)

    def stop(self):
        self.loop.remove_reader(self._fd)
        super(AsyncioNotifier, self).stop(self)

    def handle_read(self, *args, **kwargs):
        self.read_events()
        self.process_events()
        if self.handle_read_callback is not None:
            self.handle_read_callback(self)


class ExitingProcessor(pyinotify.ProcessEvent):
    def process_default(self, event):
        if event.pathname.endswith(".py"):
            print("Change detected...\n")
            sys.exit(3)


def init_watch():

    wm = pyinotify.WatchManager()
    mask = (
        pyinotify.IN_MODIFY |
        pyinotify.IN_DELETE |
        pyinotify.IN_ATTRIB |
        pyinotify.IN_MOVED_FROM |
        pyinotify.IN_MOVED_TO |
        pyinotify.IN_CREATE
    )
    wm.add_watch(sys.path, mask, rec=True)

    loop = get_event_loop()
    notifier = AsyncioNotifier(
        wm,
        loop,
        default_proc_fun=ExitingProcessor()
    )
    return notifier


def restart_with_reloader():
    while True:
        args = [sys.executable]
        args += ['-W%s' % o for o in sys.warnoptions]
        args += sys.argv
        if sys.platform == "win32":
            args = ['"{0}"'.format(arg) for arg in args]
        new_environ = os.environ.copy()
        new_environ["RUN_MAIN"] = 'true'
        exit_code = os.spawnve(os.P_WAIT, sys.executable, args, new_environ)
        if exit_code != 3:
            return exit_code


def reloader(main_func):
    if os.environ.get("RUN_MAIN") == "true":
        notifier = init_watch()
        main_func()
        notifier.stop()
    else:
        try:
            exit_code = restart_with_reloader()
            if exit_code < 0:
                os.kill(os.getpid(), -exit_code)
            else:
                sys.exit(exit_code)
        except KeyboardInterrupt:
            pass


class ComponentRunner(object):

    def __init__(self, args):
        self.args = args

    def __main__(self):
        name = getattr(self.settings, "name", "component")
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

        runner = ApplicationRunner(
            url=router_dsn,
            realm=realm,
            extra=self.settings
        )
        component = getattr(self.settings, "component", None)
        if component is None:
            raise Exception(
                "You must provided a component in your settings file"
            )
        runner.run(load_from_path(component))

    def run(self):
        parser = argparse.ArgumentParser(description="Run the μ component")
        parser.add_argument(
            '-s',
            '--settings',
            dest='settings',
            default="settings.json"
        )
        args = parser.parse_args()
        os.environ['MU_SETTINGS'] = args.settings
        from mu.conf import settings
        self.settings = settings
        reloader(self.__main__)
