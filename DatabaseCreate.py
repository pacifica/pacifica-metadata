#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Create the database tables."""
from metadata.orm import create_tables


def main():
    """Main method to create tables."""
    create_tables()


if __name__ == '__main__':
    main()
