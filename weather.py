# -*- coding: utf-8 -*-

import json, urllib2

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 2.0

units = ['ca', 'uk2', 'us', 'si']

def declare():
    return {"w": "privmsg", "setlocation": "privmsg", "setunit": "privmsg"}

def callback(self):
    message = self.message.split(self.command, 1)[1].strip()

    username = self.profile.username

    if self.command == 'setlocation':
        if len(message) > 0:
            add, lat, lon = geocode(message)
            self.profileManager.update(username, lat=lat, lon=lon)
            return self.msg(self.channel, '[%s]\'s location set to "%s"' % (username, add))
        return self.msg(self.channel, 'Invalid input for geocoding.')

    if self.command == 'setunit':
        if len(message) > 0 and message.split()[0].lower() in units:
            self.profileManager.update(username, unit=message.split()[0].lower())
            return self.msg(self.channel, '[%s]\'s units set to "%s"' % (username, message.split()[0].lower()))
        return self.msg(self.channel, '"%s" is not a valid unit, valid units are %s' % (message.split()[0], units))

    if self.command == 'w':
        if self.profile.unit:
            unit = self.profile.unit
        else:
            unit = 'auto'

        for i in units:
            if i in message.split():
                unit = i
                message_list = message.split()
                message_list.remove(unit)
                message = ' '.join(message_list)

        if len(message) == 0:
            profile = self.profile
            name, lat, lon = profile.username, profile.lat, profile.lon
        elif self.profileManager.getuser_byname(message):
            profile = self.profileManager.getuser_byname(message)
            name, lat, lon = profile.username, profile.lat, profile.lon
        elif self.profileManager.getuser_bynick(message):
            profile = self.profileManager.getuser_bynick(message)
            name, lat, lon = profile.nickname, profile.lat, profile.lon
        else:
            name, lat, lon = geocode(message)

        if not lat or not lon:
            return self.msg(self.channel, 'Location data not found.')

        baseurl = 'https://api.darksky.net/forecast/{k}/{lat},{lon}?units={u}&exclude=minutely,hourly'

        try:
            r = urllib2.urlopen(baseurl.format(k=self.config_get('apikey'), lat=lat, lon=lon, u=unit))

            data = json.loads(r.read())
            r.close()
        except HTTPError:
            return self.msg(self.channel, 'Error: Cannot connect to weather API.')

        current = data['currently']
        unit = data['flags']['units']
        daily = data['daily']

        if unit == 'us':
            tempUnit = u'°F'
            windUnit = 'mph'
        elif unit == 'si':
            tempUnit = u'°C'
            windUnit = 'm/s'
        elif unit == 'ca':
            tempUnit = u'°C'
            windUnit = 'km/h'
        elif unit == 'uk2':
            tempUnit = u'°C'
            windUnit = 'mph'

        weather = name

        # try/except for api does not always return all possible data
        try:
            weather += ' / %s ' % current['summary']
        except:
            pass
        try:
            weather += '/ %i%s ' % (round(current['temperature']), tempUnit)
        except:
            pass
        try:
            weather += '/ Feels like: %i%s ' % (round(current['apparentTemperature']), tempUnit)
        except:
            pass
        try:
            weather += '/ Humidity: %i%% ' % (current['humidity'] * 100)
        except:
            pass
        try:
            weather += '/ Wind: %i%s ' % (round(current['windSpeed']), windUnit)
            try:
                weather += '%s ' % cardinalize(current['windBearing'])
            except:
                pass
        except:
            pass
        try:
            weather += '/ High: %i%s ' % (round(daily['data'][0]['temperatureMax']), tempUnit)
        except:
            pass
        try:
            weather += '/ Low: %i%s ' % (round(daily['data'][0]['temperatureMin']), tempUnit)
        except:
            pass
        try:
            weather += '/ %s' % daily['summary']
        except:
            pass

        return self.msg(self.channel, weather)

def geocode(location):
    try:
        baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
        r = urllib2.urlopen(baseurl + '+'.join(location.split()))
        geodata = json.loads(r.read())
        r.close()

        add = geodata['results'][0]['formatted_address']
        lat = geodata['results'][0]['geometry']['location']['lat']
        lon = geodata['results'][0]['geometry']['location']['lng']
    except:
        add, lat, lon = None, None, None
    finally:
        return add, lat, lon

def cardinalize(deg):
    directions = [u'↓',u'↙',u'←',u'↖',u'↑',u'↗',u'→',u'↘']

    span = 360.0/len(directions)
    start = span/-2.0

    count = 0

    while(start + span < 360):
        if deg >= start and deg <= start + span:
            return directions[count]
        count += 1
        start += span

    return u'↓'
