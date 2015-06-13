#!/usr/bin/env python2
#!coding=utf-8

import click
import os

from docker_collector_agent import main_loop


@click.group()
def cli():
    pass


@click.command()
@click.option("--server", "-s",
              default=None,
              help="Docker collector server address")
def run(server):
    if server is not None:
        os.environ["DOCKER_COLL_SERVER"] = server
    main_loop()


cli.add_command(run)


if __name__ == '__main__':
    cli()
