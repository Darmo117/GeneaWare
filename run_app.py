#!/usr/bin/python3
import os
import pathlib
import sys

import app.gui


def main():
    lock_file = pathlib.Path('.lock')
    if lock_file.exists():
        print('The application is already running!', file=sys.stderr)
        sys.exit(1)
    with lock_file.open(mode='w') as f:
        f.write(str(os.getpid()))
    code = app.gui.Application.run()
    lock_file.unlink(missing_ok=True)
    sys.exit(code)


if __name__ == '__main__':
    main()
