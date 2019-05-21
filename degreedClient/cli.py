# -*- coding: utf-8 -*-

"""Console script for degreedClient."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for degreedClient."""
    click.echo("Replace this message by putting your code into "
               "degreedClient.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
