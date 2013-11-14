from bottle import route, static_file
import gevent

@route('/name/<name>')
def nameindex(name='Stranger'):
    return '<strong>Hello, %s!</strong>' % name

@route('/get-tweet')
def get_tweet():
    yield ' ' * 1200
    yield '<html><body><h1>Hi '
    gevent.sleep(10)
    yield 'There</h1></body></html>'

 
@route('/')
def index():
	return static_file('index.html',root=os.path.join(os.path.dirname(__file__), 'static'))

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
    'runtime/repo/wsgi/views/')) 
