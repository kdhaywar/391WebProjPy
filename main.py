import os
from webpages.pageprovider import PageProvider

__author__ = 'HenryPabst'

import cherrypy
import config


if __name__ == "__main__":
    cherrypy.config.update({"server.socket_host": config.IP,
                           "server.socket_port": config.PORT
                            })
    conf = {
        "/": {
            "tools.sessions.on": True, #Allow sessions.
            "tools.sessions.timeout": 60, #Sessions will timeout after 60 minutes.
            "tools.staticdir.root": os.path.abspath(os.getcwd()),
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "static"
        }
    }
    cherrypy.quickstart(PageProvider(), "/", conf)
