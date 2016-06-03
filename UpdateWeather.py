import re
import json
import urllib2
from quip4aha import QuipClient4AHA, week, InvalidOperation

class UpdateWeather(object):

    SIMP = {'Clear':'sunny',
            'Mostly Cloudy':'mostly cloudy', 'Partly Cloudy':'partly cloudy', 'Overcast':'cloudy',
            'Thunderstorm':'rainy', 'Chance of a Thunderstorm':'rainy', 'Rain':'rainy'}
    
    def __init__(self):
        self.NextNDay = 0
        self.Condition = ''
        self.RainPercentage = ''
        self.TemperatureC = ''
        self.TemperatureF = ''
        self.client = QuipClient4AHA()
        
    def do(self):
        '''
        ==================FORECAST DATA==================
        '''
        self.NextNDay = week.DaysTo('next Wednesday')
        if self.NextNDay > 3:
            raise InvalidOperation("Unable to get the weather for Wednesday: "
                                   "WunderStation only gives prediction for today and 3 days ahead.")
        response = json.loads(urllib2.urlopen(
            "http://api.wunderground.com/api/01702baefa3fbf8e/forecast/q/CN/Guangzhou.json").read())
        data = response['forecast']['simpleforecast']['forecastday'][self.NextNDay]
        self.Condition = self.SIMP.get(data['conditions'], data['conditions'].lower())
        self.RainPercentage = data['pop']
        self.TemperatureC = data['high']['celsius']
        self.TemperatureF = data['high']['fahrenheit']
        
        '''
        ====================DOC CATCHER====================
        '''
        docID = self.client.get_latest_script_ID()
        html = self.client.get_thread(id=docID)['html']
        
        '''
        ====================DATA EMBED====================
        '''
        SID, date = re.search(
            r"<p id='([a-zA-Z0-9]{11})'.*?>Good Morning AHA.+?Wednesday\, ([\w ]+)\..+?<\/p>", html).group(1,2)
        ctx = ("Good Morning AHA!<br/>"
               "It is Wednesday, %s. "
               "The weather for today is %s. "
               "There is %s%% chance of rain. "
               "The high temperature today will be %s degrees Celsius, which is %s degrees Fahrenheit.") % (
                   date, self.Condition, "%s %s" % ("an" if self.RainPercentage=='80' else "a", self.RainPercentage),
                   self.TemperatureC, self.TemperatureF)
        
        '''
        ====================POST DATA====================
        '''
        self.client.edit_document(thread_id=docID, content=ctx, format="html",
                                  operation=self.client.REPLACE_SECTION, section_id=SID)
        return "Done!"


if __name__=='__main__':
    UpdateAction = UpdateWeather()
    UpdateAction.do()
