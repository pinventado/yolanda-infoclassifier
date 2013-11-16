#!/usr/bin/env python

#
# This file may be used instead of Apache mod_wsgi to run your python
# web application in a different framework.  A few examples are
# provided (cherrypi, gevent), but this file may be altered to run
# whatever framework is desired - or a completely customized service.
#
import imp
import os

try:
   zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                           'virtenv', 'bin', 'activate_this.py')
   execfile(zvirtenv, dict(__file__ = zvirtenv) )
except IOError:
   pass

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#


#
#  main():
#
from gevent import monkey; monkey.patch_all()
import bottle, zlib, pymongo

#def mongo_store(tweet, args):
   #tbl.insert(zlib.compress(tweet))


if __name__ == '__main__':
   ip   = os.environ['OPENSHIFT_PYTHON_IP']
   port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
   yolanda = imp.load_source('yolanda', 'web/yolanda.py')
   imp.load_source('utils','bg/utils.py')
   twitter_listener = imp.load_source('twitter_listener','bg/twitter_listener.py')
   twitter = twitter_listener.TwitterListener()
   yolanda.twitter_listener = twitter

   settings = imp.load_source('settings', os.environ['OPENSHIFT_DATA_DIR']+'/settings.py')
   #conn = pymongo.MongoClient('mongodb://'+settings.MONGO_USER+':'+settings.MONGO_PWD+'@widmore.mongohq.com:10000/yolanda')
   #tbl = conn['yolanda']['tweet']
   #twitter.register(mongo_store)

   twitter.start()
   bottle.run(host=ip, port=port, server='gevent')

'''
   fwtype="wsgiref"
   for fw in ("gevent", "cherrypy", "flask"):
      try:
         imp.find_module(fw)
         fwtype = fw
      except ImportError:
         pass

   print('Starting WSGIServer type %s on %s:%d ... ' % (fwtype, ip, port))
   if fwtype == "gevent":
      from gevent.pywsgi import WSGIServer
      WSGIServer((ip, port), app.application).serve_forever()

   elif fwtype == "cherrypy":
      from cherrypy import wsgiserver
      server = wsgiserver.CherryPyWSGIServer(
         (ip, port), app.application, server_name=os.environ['OPENSHIFT_APP_DNS'])
      server.start()

   elif fwtype == "flask":
      from flask import Flask
      server = Flask(__name__)
      server.wsgi_app = app.application
      server.run(host=ip, port=port)

   else:
      from wsgiref.simple_server import make_server
      make_server(ip, port, app.application).serve_forever()
'''
