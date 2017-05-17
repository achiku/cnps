# -*- coding: utf-8 -*-
import click

from . import __version__


class RatemallCLI(click.MultiCommand):

    """ratemall CLI main class"""

    def list_commands(self, ctx):
        """return available modules"""
        return ['connpass']

    def get_command(self, ctx, name):
        """get command"""
        try:
            mod = __import__('ratemall.' + name, None, None, ['cli'])
            return mod.cli
        except ImportError:
            pass


cli = RatemallCLI(help="rate your meetup participants (v{0})".format(__version__))


if __name__ == '__main__':
    cli()
