import json, urllib, urllib2

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

fCountries = ['Belize', 'Guam', 'Puerto Rico', 'United States', 'US Virgin Islands']
iCountries = ['Liberia', 'Myanmar', 'United States']

def declare():
  return {"w": "privmsg", "setlocation": "privmsg"}

def callback(self):
    channel = self.channel
    command = self.command
    user = self.user.split('!')[0].lower()
    msg = self.msg
    message = self.message.split(command, 1)[1].strip()
    if command == 'w':
        try:
            if message:
                try:
                    query = self.locker.location[message]
                except:
                    query = message
            else:
                try:
                    query = self.locker.location[user]
                except:
                    return msg(channel, 'You have not set a location yet.')

            #sourced from example code for Yahoo Weather API
            baseurl = 'https://query.yahooapis.com/v1/public/yql?'
            yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")' % query
            yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
            result = urllib2.urlopen(yql_url)
            data = json.loads(result.read())
            result.close()

            try:
                city = data['query']['results']['channel']['location']['city']
                region = data['query']['results']['channel']['location']['region']
                country = data['query']['results']['channel']['location']['country']
                cond = data['query']['results']['channel']['item']['condition']['text']
                temp = data['query']['results']['channel']['item']['condition']['temp']
                humid = data['query']['results']['channel']['atmosphere']['humidity']
                wSpeed = data['query']['results']['channel']['wind']['speed']
                wDir = degToDirection(int(data['query']['results']['channel']['wind']['direction']))

                weather = '%s, %s, %s / %s / ' % (city, region, country, cond)

                if country.strip() in fCountries:
                    weather += '%s%sF /' % (temp, decode('!b64:wrA='))
                else:
                    weather += '%s%sC /' % (FToC(int(temp)), decode('!b64:wrA='))

                weather += ' Humidity: %s%% /' % humid

                if country.strip() in iCountries:
                    weather += ' Wind: %smph %s' % (wSpeed, wDir)
                else:
                    weather += ' Wind: %skm/h %s' % (miToKm(int(wSpeed)), wDir)

                weather = ' '.join(weather.split())

                return msg(channel, weather)
            except:
                return msg(channel, 'I cannot find the weather for %s' % message)
        except:
            return msg(channel, 'I cannot fetch the weather at this moment.')
    if command == 'setlocation':
        if len(message) > 0:
            try:
                self.locker.location[user] = message
            except:
                self.locker.location = {user: message}
            return msg(channel, 'Location for user %s set to %s' % (self.user.split('!')[0], message))
        return msg(channel, 'You did not give me a location to set!')

def FToC(fahrenheit):
    return int(round((fahrenheit - 32) / 1.8))

def miToKm(miles):
    return int(round(miles * 1.60934))

def degToDirection(deg):
    directions = ['NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N']
    start = 11.25
    span = 22.5
    count = 0

    while(start + span < 360):
        if deg >= start and deg <= start + span:
            return directions[count]
        count += 1
        start += span

    return 'N'

def decode(code_str):
    try:
        code_str = code_str.split('!')[1]
        code_func = coding[code_str.split(':')[0]][1]
        return code_func(code_str.split(':')[1])
    except:
        return False

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)
class empty:
	pass

'''
# interactive testing:
api = api()
setattr(api, 'type', 'privmsg')
setattr(api, 'channel', "#test")
setattr(api, 'command', 'w')
setattr(api, 'locker', empty)
setattr(api, 'user', 'joe!username@hostmask')
while(True):
    _input = raw_input('Enter message here: ')
    if 'setlocation' in _input:
        setattr(api, 'command', 'setlocation')
    else:
        setattr(api, 'command', 'w')
    setattr(api, 'message', _input)
    print callback(api)
'''

if __name__ == "__main__":
    api = api()
    setattr(api, 'type', 'privmsg')
    setattr(api, 'channel', "#test")
    setattr(api, 'command', 'w')
    setattr(api, 'locker', empty)
    setattr(api, 'user', 'joe!username@hostmask')

    setattr(api, 'command', 'w')
    setattr(api, 'message', '^w')
    if 'You have not' not in callback(api):
    	exit(1)

    setattr(api, 'message', '^w Los Angeles')
    if 'Los Angeles, CA' not in callback(api):
    	exit(2)

    setattr(api, 'command', 'setlocation')
    setattr(api, 'message', '^setlocation Los Angeles')
    if 'Location for' not in callback(api):
    	exit(3)

    setattr(api, 'command', 'w')
    setattr(api, 'message', '^w')
    if 'Los Angeles, CA' not in callback(api):
    	exit(4)

    setattr(api, 'user', 'jeb!username@hostmask')
    setattr(api, 'message', '^w joe')
    if 'Los Angeles, CA' not in callback(api):
    	exit(5)
