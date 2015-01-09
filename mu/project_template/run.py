#! /usr/bin/env python3
import sys

from mu.runner import ComponentRunner

if __name__ == '__main__':
    runner = ComponentRunner(sys.argv)
    runner.run()
