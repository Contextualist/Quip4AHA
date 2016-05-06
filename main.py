from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    import time
    import datetime
    import traceback
    import quip
    NextWednesday = datetime.datetime.today() + datetime.timedelta(days = 5)
    NextWednesdayN = NextWednesday.strftime("%m%d")
    NextWednesdayS = NextWednesday.strftime("%B %d")
    if NextWednesdayS[-2] == "0":
      NextWednesdayS = NextWednesdayS[:-2] + NextWednesdayS[-1];
    ctx = """<p class='line'>Good Morning AHA!<br/>
    """ % (NextWednesdayS) # &#8203; (or &#x200b;) stands for a place-holder for a blank <p>
    client = quip.QuipClient(access_token="Wk9EQU1BcDZFS04=|1483091850|CF037JVoITJPnAET8aHWnZwEZACvrIm7jtkRIQCaX3g=")
    client.new_document(content=ctx, format="html", title=NextWednesdayN, member_ids=["LHEAOAhm7YS"])
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
