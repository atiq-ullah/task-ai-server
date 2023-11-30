#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

from django.core.management import execute_from_command_line

load_dotenv()


def main():
    """Run administrative tasks."""
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
