import json, time, urllib2
try:
    from unidecode import unidecode
except:
    def unidecode(uni):
        return str(uni)

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

locationCache = {}

def declare():
  return {"w": "privmsg", "time": "privmsg", "setlocation": "privmsg"}

def callback(self):
    fApiKey = self.config_get('ApiKey').split()[0] #remove extra formatting if present
    channel = self.channel
    command = self.command
    user = self.user.split('!')[0]
    message = self.message.split(self.command, 1)[1].strip()
    msg = self.msg

    if command == 'setlocation':
        if len(message) > 0:
            try:
                self.locker.location[user] = message
            except:
                self.locker.location = {user: message}
            self.cache_save()
            return msg(channel, 'Location for user %s set to %s' % (self.user.split('!')[0], message))
        return msg(channel, 'You did not give me a location to set.')

    if command == 'w':
        gLocation = getLocation(self)
        if type(gLocation) == str:
            return msg(channel, gLocation)
        else:
            location = gLocation [0]
            private = gLocation[1]
            rUser = gLocation[2]

        gLatLong = getLatLong(location)
        if type(gLocation) == str:
            return msg(channel, gLocation)
        else:
            name = gLatLong[0]
            lat = gLatLong[1]
            lng = gLatLong[2]

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

            if private:
                weather = '%s / %s / %i%s / Humidity: %i%% / Wind: %i%s %s / High: %i%s / Low: %i%s' %\
                          (rUser, cond, temp, tempUnit, humid, speed, windUnit, bearing, high, tempUnit, low, tempUnit)
            else:
                weather = '%s / %s / %i%s / Humidity: %i%% / Wind: %i%s %s / High: %i%s / Low: %i%s' %\
                          (name, cond, temp, tempUnit, humid, speed, windUnit, bearing, high, tempUnit, low, tempUnit)

            weather = unidecode(unicode(' '.join(weather.split())))

            return msg(channel, weather)
        except:
            if private and user == rUser:
                return msg(channel, 'Sorry, I cannot fetch your weather.')
            if private:
                return msg(channel, 'Sorry, I cannot fetch the weather at %s\'s location.' % rUser)
            return msg(channel, 'Sorry, I cannot fetch the weather at %s.' % location)

    if command == 'time':
        gLocation = getLocation(self)
        if type(gLocation) == str:
            return msg(channel, gLocation)
        else:
            location = gLocation [0]
            private = gLocation[1]
            rUser = gLocation[2]

        gLatLong = getLatLong(location)
        if type(gLocation) == str:
            return msg(channel, gLocation)
        else:
            name = gLatLong[0]
            lat = gLatLong[1]
            lng = gLatLong[2]

        try:
            currentTime = time.time()
            baseurl = 'https://maps.googleapis.com/maps/api/timezone/json?location='
            params = '%s,%s&timestamp=%s' % (lat, lng, currentTime)
            r = urllib2.urlopen(baseurl + params)
            timedata = json.loads(r.read())
            r.close()

            dst = timedata['dstOffset']
            raw = timedata['rawOffset']
            timezone = timedata['timeZoneName']

            currentTime = time.gmtime(currentTime + dst + raw)

            if private:
                timeinfo = '%s / %s / %s / DST: %s' %\
                           (rUser, timezone, time.strftime("%I:%M %p", currentTime), bool(dst))
            else:
                timeinfo = '%s / %s / %s / DST: %s' %\
                           (name, timezone, time.strftime("%I:%M %p", currentTime), bool(dst))

            timeinfo = unidecode(unicode(' '.join(timeinfo.split())))

            return msg(channel, timeinfo)
        except:
            if private and user == rUser:
                return msg(channel, 'Sorry, I cannot fetch your time, try looking at a clock.')
            if private:
                return msg(channel, 'Sorry, I cannot fetch the time at %s\'s location.' % rUser)
            return msg(channel, 'Sorry, I cannot fetch the time at %s.' % location)

def getLocation(self):
    user = self.user.split('!')[0]
    message = self.message.split(self.command, 1)[1].strip()
    if message:
        try:
            location = self.locker.location[message.lower()]
            rUser = message
            private = True
        except:
            location = message
            rUser = user
            private = False
    else:
        try:
            location = self.locker.location[user.lower()]
            rUser = user
            private = True
        except:
            return 'You have not set a location yet.'
    return [location, private, rUser]

def getLatLong(location):
    if location in locationCache:
        name = locationCache[location][0]
        lat = locationCache[location][1]
        lng = locationCache[location][2]
    else:
        try:
            baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
            r = urllib2.urlopen(baseurl + '+'.join(location.split()))
            geodata = json.loads(r.read())
            r.close()

            name = geodata['results'][0]['formatted_address']
            lat = geodata['results'][0]['geometry']['location']['lat']
            lng = geodata['results'][0]['geometry']['location']['lng']

            locationCache[location] = [name, lat, lng]
        except:
            return 'Sorry, I cannot find the location of %s.' % location
    return [name, lat, lng]

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
		return '[%s] %s' % (channel, text)
class empty:
	pass

'''
# interactive testing:
def cache_save():
    print 'Cache saved'
def config_get(item):
    return 'ffbdb8ef8349e1d93e5c3d503dfda8a8'
api = api()
setattr(api, 'cache_save', cache_save)
setattr(api, 'config_get', config_get)
setattr(api, 'type', 'privmsg')
setattr(api, 'channel', "#test")
setattr(api, 'command', 'w')
setattr(api, 'locker', empty)
setattr(api, 'user', 'joe!username@hostmask')
while(True):
    _input = raw_input('Enter message here: ')
    if '^setlocation' in _input:
        setattr(api, 'command', 'setlocation')
    if '^time' in _input:
        setattr(api, 'command', 'time')
    if '^w' in _input:
        setattr(api, 'command', 'w')
    setattr(api, 'message', _input)
    print callback(api)
'''

if __name__ == "__main__":
    def cache_save():
        print 'Cache saved'
    def config_get(item):
        return 'ffbdb8ef8349e1d93e5c3d503dfda8a8'
    api = api()
    setattr(api, 'cache_save', cache_save)
    setattr(api, 'config_get', config_get)
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

    setattr(api, 'command', 'time')
    setattr(api, 'message', '^time')
    print callback(api)
    if 'You have not' not in callback(api):
    	exit(3)

    setattr(api, 'message', '^time Los Angeles')
    print callback(api)
    if 'Pacific' not in callback(api):
    	exit(4)

    setattr(api, 'command', 'setlocation')
    setattr(api, 'message', '^setlocation Los Angeles')
    print callback(api)
    if 'Location for' not in callback(api):
    	exit(5)

    setattr(api, 'command', 'w')
    setattr(api, 'message', '^w')
    print callback(api)
    if 'joe /' not in callback(api):
    	exit(6)

    setattr(api, 'command', 'time')
    setattr(api, 'message', '^time')
    print callback(api)
    if 'joe /' not in callback(api):
    	exit(7)

    setattr(api, 'command', 'w')
    setattr(api, 'user', 'jeb!username@hostmask')
    setattr(api, 'message', '^w joe')
    print callback(api)
    if 'joe /' not in callback(api):
    	exit(8)

    setattr(api, 'command', 'time')
    setattr(api, 'user', 'jeb!username@hostmask')
    setattr(api, 'message', '^time joe')
    print callback(api)
    if 'joe /' not in callback(api):
    	exit(9)
