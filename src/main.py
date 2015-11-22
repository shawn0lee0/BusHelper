#-*-coding:utf-8-*-  
#qpy:webapp:公交路线查询
#qpy://127.0.0.1:8081/
"""
公交路线查询

@Author river
"""

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, redirect

import urllib2
import os
import json
#### 常量定义 #########
ASSETS = "/assets/"
ROOT = os.path.dirname(os.path.abspath(__file__))


######### QPYTHON WEB SERVER ###############

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        #sys.stderr.close()
        import threading 
        threading.Thread(target=self.server.shutdown).start() 
        #self.server.shutdown()
        self.server.server_close() 
        print "# QWEBAPPEND"


######### BUILT-IN ROUTERS ###############
def __exit():
    global server
    server.stop()

def __ping():
    return "ok"

def server_static(filepath):
    return static_file(filepath, root=ROOT+'/assets')

def home():
    return template('index.html')


######### WEBAPP ROUTERS ###############
app = Bottle()
app.route('/', method='GET')(home)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
app.route('/assets/<filepath:path>', method='GET')(server_static)

try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8081")
    app.run(server=server,reloader=False)
except Exception,ex:
    print "Exception: %s" % repr(ex)


