#!/usr/bin/env python2
#!coding=utf-8

import os
import errno
import json
import requests
import warnings
from pprint import pprint as pp

from docker import Client


def get_docker_coll_server():
    val = os.getenv("DOCKER_COLL_SERVER")
    if not val:
        raise EnvironmentError(errno.EINVAL, "value for DOCKER_COLL_SERVER not found")
    return val


def send_data(data):
    url = get_docker_coll_server()
    req = requests.post(url, data=json.dumps(data))
    if not req.ok:
        msg = ("Error while sending data "
               "to %(url)s. \n"
               "status code: '%(status_code)s' "
               "message: '%(message)s' " 
               "data sent: \n\t %(data)s "
               "")
        msg = msg % dict(url=url,
                     status_code=req.status_code,
                     message=req.reason,
                     data=data)
        warnings.warn(msg)


def collect_data(docker_client, container):
    data = {}
    container_id = container[u'Id']
    data['container'] = container
    for ii in docker_client.stats(container_id, True):
        data['stats'] = ii
        break

    top = docker_client.top(container_id)
    result_top = []
    for ii in top[u'Processes']:
        tmp = {}
        for k,v in enumerate(top[u'Titles']):
            tmp[v] = ii[k]
        result_top.append(tmp)
    data['top'] = result_top
    return data

def main_loop():
    docker_client = Client()

    while True:
        containers = docker_client.containers()
        for i in containers:
            data = collect_data(docker_client, i)
            send_data(data)
