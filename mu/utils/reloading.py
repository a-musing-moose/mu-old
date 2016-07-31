import logging
import os
import sys

from watchdog.observers import Observer

from mu.apps.runner import close_loop_cleanly

log = logging.getLogger(__name__)


class ExitingProcessor(object):

    def dispatch(self, event):
        log.debug("Notifier Status: RESTARTING")
        os._exit(3)


class Notifier(object):

    def __init__(self):
        self._observer = Observer()
        handler = ExitingProcessor()
        for path in filter(os.path.exists, sys.path):
            self._observer.schedule(handler, path, recursive=True)

    def start(self):
        self._observer.start()
        log.debug("Notifier Status: STARTED")

    def stop(self):
        self._observer.stop()
        self._observer.join()


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
        notifier = Notifier()
        notifier.start()
        main_func()
        notifier.stop()
        close_loop_cleanly()
    else:
        try:
            exit_code = restart_with_reloader()
            if exit_code < 0:
                os.kill(os.getpid(), -exit_code)
            else:
                sys.exit(exit_code)
        except KeyboardInterrupt:
            pass
