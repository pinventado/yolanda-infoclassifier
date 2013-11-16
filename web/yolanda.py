from bottle import route, static_file
from gevent import queue
import gevent, json, pymongo, zlib

#twitter_listener - contains link to twitter assigned by app.py

import imp
settings = imp.load_source('settings', os.environ['OPENSHIFT_DATA_DIR']+'/settings.py')
twitter_listener.register(mongo_store)

def mongo_store(tweet):
   conn = pymongo.MongoClient('mongodbo://'+settings.MONGO_USER+':'+settings.MONGO_PWD+'@widmore.mongohq.com:10000/yolanda')
   tbl = conn['yolanda']['tweet']
   tbl.insert(zlib.compress(tweet))

def show_tweet(tweet, args):
	body = args[0]
	body.put(json.dumps(tweet))
        body.put(StopIteration)

def wait_tweet(body):
	twitter_listener.register(show_tweet, body)

@route('/get-tweet')
def get_tweet():
    body = queue.Queue()
    gevent.spawn(wait_tweet, body)
    return body
 
@route('/')
def index():
	return static_file('index.html',root=os.path.join(os.path.dirname(__file__), 'static'))

@route('/<path:path>')
def path(path):
	return static_file(path ,root=os.path.join(os.path.dirname(__file__), 'static'))

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
    'runtime/repo/wsgi/views/')) 
