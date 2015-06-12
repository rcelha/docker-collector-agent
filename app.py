#!/usr/bin/env python2
#!coding=utf-8

import click

from docker_collector_agent import main_loop


@click.group()
def cli():
    pass


@click.command()
def run():
    main_loop()


cli.add_command(run)


if __name__ == '__main__':
    cli()
