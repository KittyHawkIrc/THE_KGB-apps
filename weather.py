import json, urllib2

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

gApiKey = 'AIzaSyCfy-symUGtmzsqO6_sb0UKtO0YHLoDT_M'
fApiKey = 'ffbdb8ef8349e1d93e5c3d503dfda8a8'
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
        if message:
            try:
                query = self.locker.location[message.lower()]
            except:
                query = message
        else:
            try:
                query = self.locker.location[user]
            except:
                return msg(channel, 'You have not set a location yet.')

        try:
            baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
            r = urllib2.urlopen(baseurl + '+'.join(query.split()) + '&key=' + gApiKey)
            geodata = json.loads(r.read())
            r.close()

            name = geodata['results'][0]['formatted_address']
            lat = geodata['results'][0]['geometry']['location']['lat']
            lng = geodata['results'][0]['geometry']['location']['lng']

            try:
                baseurl = 'https://api.forecast.io/forecast/'
                options = '?units=auto&exclude=minutely,hourly'
                r = urllib2.urlopen(baseurl + fApiKey + '/%s,%s' % (lat, lng) + options)
                wdata = json.loads(r.read())
                r.close()

                current = wdata['currently']
                daily = wdata['daily']
                units = wdata['flags']['units']

                tempUnit = 'C'
                if units == 'us':
                    tempUnit = 'F'
                    windUnit = 'mph'
                elif units == 'si':
                    windUnit = 'm/s'
                elif units == 'ca':
                    windUnit = 'km/h'
                elif units == 'uk2':
                    windUnit = 'mph'

                temp = round(current['temperature'])
                cond = current['summary']
                humid = current['humidity'] * 100
                speed = round(current['windSpeed'])
                bearing = degToDirection(current['windBearing'])
                high = round(daily['data'][0]['temperatureMax'])
                low = round(daily['data'][0]['temperatureMin'])

                weather = '%s / %s / %i%s / Humidity: %i%% / Wind: %i%s %s / High: %i%s / Low: %i%s' %\
                          (name, cond, temp, tempUnit, humid, speed, windUnit, bearing, high, tempUnit, low, tempUnit)

                weather = ' '.join(weather.split())

                return msg(channel, weather)
            except:
                return msg(channel, 'I cannot find the weather for %s' % query)
        except:
            return msg(channel, 'I cannot find the location of %s' % query)

    if command == 'setlocation':
        if len(message) > 0:
            try:
                self.locker.location[user] = message
            except:
                self.locker.location = {user: message}
            self.cache_save()
            return msg(channel, 'Location for user %s set to %s' % (self.user.split('!')[0], message))
        return msg(channel, 'You did not give me a location to set!')

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

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)
class empty:
	pass
'''
# interactive testing:
api = api()
def cache_save():
	print 'Cache saved'
setattr(api, 'cache_save', cache_save)
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
    def cache_save():
        print 'Cache saved'
    api = api()
    setattr(api, 'cache_save', cache_save)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'channel', "#test")
    setattr(api, 'command', 'w')
    setattr(api, 'locker', empty)
    setattr(api, 'user', 'joe!username@hostmask')

    setattr(api, 'command', 'w')
    setattr(api, 'message', '^w')
    print callback(api)
    if 'You have not' not in callback(api):
    	exit(1)

    setattr(api, 'message', '^w Los Angeles')
    print callback(api)
    if 'Los Angeles, CA' not in callback(api):
    	exit(2)

    setattr(api, 'command', 'setlocation')
    setattr(api, 'message', '^setlocation Los Angeles')
    print callback(api)
    if 'Location for' not in callback(api):
    	exit(3)

    setattr(api, 'command', 'w')
    setattr(api, 'message', '^w')
    print callback(api)
    if 'Los Angeles, CA' not in callback(api):
    	exit(4)

    setattr(api, 'user', 'jeb!username@hostmask')
    setattr(api, 'message', '^w joe')
    print callback(api)
    if 'Los Angeles, CA' not in callback(api):
    	exit(5)
