#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django can't be imported, we may be running with the wrong
        # Python interpreter. Try to locate a project virtualenv and
        # re-exec this script with that interpreter (Windows and POSIX).
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = ('.venv', 'venv', 'env', 'my_env', 'myenv')
        for name in candidates:
            # venv is usually one level up from the `mysite` package
            candidate = os.path.normpath(os.path.join(script_dir, '..', name))
            if os.name == 'nt':
                python_bin = os.path.join(candidate, 'Scripts', 'python.exe')
            else:
                python_bin = os.path.join(candidate, 'bin', 'python')
            if os.path.exists(python_bin):
                sys.stderr.write(f"Re-launching with project venv python: {python_bin}\n")
                os.execv(python_bin, [python_bin] + sys.argv)

        # Fall back to the original error if no project venv found.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
