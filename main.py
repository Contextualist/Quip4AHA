import traceback
import logging
logging.basicConfig(level=logging.INFO)

from NewDoc import NewDoc
from AssignHost import AssignHost
from UpdateWeather import UpdateWeather

from flask import Flask
app = Flask(__name__)
#app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def assign():
    AssignAction = AssignHost()
    return AssignAction.do()

@app.route('/b/<ad_hoc_host>')
def assign_m(ad_hoc_host):
    AssignAction = AssignHost(Host=ad_hoc_host.split('+'))
    return AssignAction.do()

@app.route('/newdoc')
def newdoc():
    NewDocAction = NewDoc()
    return NewDocAction.do()

@app.route('/updateweather')
def updateweather():
    UpdateAction = UpdateWeather()
    return UpdateAction.do()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

@app.errorhandler(Exception)
def handle_exception(e):
    tb = traceback.format_exc()
    logging.error(tb)
    return tb, e.code if 'code' in dir(e) else 500
