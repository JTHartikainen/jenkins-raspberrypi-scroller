#
# main.py - Main file for LED scrolling REST listener
#
# Author: Jaakko Hartikainen (jaakko dot hartikainen at gmail dot com )
#
import logging
import datetime
import requests
import time
import string
import cherrypy

from cfg import config
from includes import loggerhelper

# RP
#from includes import ledmatrix as ledmatrix

# Debug
from includes import ledmatrix_dummy as ledmatrix

logger = loggerhelper.create_custom_logger(config, config.LOGGERNAME, logging.DEBUG)

class LedWebService(object):
     exposed = True

     @cherrypy.tools.accept(media='text/plain')
     def GET(self, color=1, text='foo', repeats=5):
         logger.info("GET invoked with parameters color: " + color + ", text: " + text)
         ledmatrix.scroll(text, color, repeats)

     def POST(self, length=8):
         logger.info("POST invoked")

     def PUT(self, another_string):
         logger.info("PUT invoked")

     def DELETE(self):
         logger.info("DELETE invoked")


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(LedWebService(), '/', conf)

    logger.info("Logging setup successful.")
    ledmatrix.initledmatrix()
    logger.info("LED matrix initialized")