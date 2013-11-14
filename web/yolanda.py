from bottle import route, static_file, default_app

@route('/name/<name>')
def nameindex(name='Stranger'):
    return '<strong>Hello, %s!</strong>' % name
 
@route('/')
def index():
    #return '<strong>Hello World!</strong>'
	#return str(os.path.dirname(os.path.realpath(__file__)))
	return static_file('index.html',root='./static/')

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
    'runtime/repo/wsgi/views/')) 

#application=default_app()
