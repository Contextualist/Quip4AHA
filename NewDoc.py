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
It is Wednesday, %s. The weather for today is __. There is __%% chance of rain. The high temperature today will be __ degrees Celsius, which is __ degrees Fahrenheit.</p>
<p class='line'>&#8203;</p>
<p class='line'><b>Now for this week in history:</b></p>
<p class='line'>&#8203;</p>
<p class='line'>&#8203;</p>
<p class='line'><b>In World News:</b></p>
<p class='line'>&#8203;</p>
<p class='line'>&#8203;</p>
<p class='line'><b>Now for the fun facts:</b></p>
<p class='line'>&#8203;</p>
<p class='line'>&#8203;</p>
<p class='line'><b>In AHA News:</b></p>
<p class='line'>&#8203;</p>
<p class='line'>&#8203;</p>
<p class='line'>We will close with this/these verse(s) from</p>
<p class='line'>&#8203;</p>
<p class='line'>This is all for today AHA broadcasting thank you for listening, and as always stay classy AHA!</p>
""" % (NextWednesdayS) # &#8203; (or &#x200b;) stands for a place-holder for a blank <p>

try:
  client = quip.QuipClient(access_token="Wk9EQU1BcDZFS04=|1483091850|CF037JVoITJPnAET8aHWnZwEZACvrIm7jtkRIQCaX3g=")
  client.new_document(content=ctx, format="html", title=NextWednesdayN, member_ids=["PCeAOAQx6sO"])
except:
  out = open('error.txt','w')
  out.write(traceback.format_exc())
  out.close()