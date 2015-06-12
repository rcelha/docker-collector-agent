#!/usr/bin/env python2
#!coding=utf-8

import os
import json
from pprint import pprint as pp

from docker import Client


def get_docker_coll_server():
    val = os.getenv("DOCKER_COLL_SERVER")
    if not val:
        val = "http://www.google.com"
    return val


def send_data(data):
    url = get_docker_coll_server()
    pp(data)
    pp(url)


def collect_data(docker_client, container_id):
    stats = {}
    for ii in docker_client.stats(container_id, True):
        stats.update(ii)
        break

    top = docker_client.top(container_id)
    result_top = []
    for ii in top[u'Processes']:
        tmp = {}
        for k,v in enumerate(top[u'Titles']):
            tmp[v] = ii[k]
        result_top.append(tmp)
    stats['top'] = result_top
    return stats

def main_loop():
    docker_client = Client()
    containers = docker_client.containers()

    for i in containers:
        data = collect_data(docker_client, i[u'Id'])
        send_data(data)


import click
@click.group()
def cli():
    pass

@click.command()
def run():
    main_loop()

cli.add_command(run)

if __name__ == '__main__':
    cli()
