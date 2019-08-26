#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging

import cherrypy

from peregrine_mail.app import app

logger = logging.getLogger('peregrine')


def cherrypy_server():
    cherrypy.tree.graft(app, '/')

    cherrypy.config.update({
        'engine.autoreload_on': False,
        'log.screen': False,
        'server.socket_port': app.config['PEREGRINE_MAIL']['port'],
        'server.socket_host': app.config['PEREGRINE_MAIL']['host']
    })

    cherrypy.engine.start()
    logger.info(f'Peregrine mail started on '
                f'http://{app.config["PEREGRINE_MAIL"]["host"]}:{app.config["PEREGRINE_MAIL"]["port"]}')
    try:
        cherrypy.engine.block()
    finally:
        cherrypy.engine.stop()


if __name__ == '__main__':
    cherrypy_server()
