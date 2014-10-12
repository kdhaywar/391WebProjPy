from webpages.pageprovider import PageProvider

__author__ = 'HenryPabst'

import cherrypy
import config


if __name__ == "__main__":
    cherrypy.config.update({"server.socket_host": config.IP,
                            "server.socket_port": config.PORT
                            })
    cherrypy.quickstart(PageProvider(), "/")
