# -*- coding: utf-8 -*-

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
  return {"np": "privmsg", "setlastfm": "privmsg"}

def callback(self):
    fApiKey = self.config_get('LfmApiKey').split()[0] #remove extra formatting if present
    channel = self.channel
    command = self.command
    user = self.user.split('!')[0]
    message = self.message.split(self.command, 1)[1].strip()
    msg = self.msg

    if command == 'setlastfm':
        if len(message) > 0:
            try:
                self.locker.lastfm[user.lower()] = message.split()[0]
            except:
                self.locker.lastfm = {user.lower(): message.split()[0]}
            self.cache_save()
            return msg(channel, 'Last.FM for user %s set to %s' % (self.user.split('!')[0], message))
        return

    if command == 'np':
        try:
            baseurl = 'http://ws.audioscrobbler.com/2.0/?'
            method = 'method=user.getrecenttracks'
            if len(message) == 0:
                lfmUser = 'user=%s' % self.locker.lastfm[user.lower()]
                u = user.lower()
            else:
                try:
                    lfmUser = 'user=%s' % self.locker.lastfm[message.split()[0]]
                    u = message.split()[0]
                except:
                    lfmUser = 'user=%s' % message.split()[0]
                    u = message.split()[0]
            key = 'api_key=%s' % fApiKey
            fmt = 'format=json'
            params = [method, lfmUser, key, fmt]
            r = urllib2.urlopen(baseurl + '&'.join(params))
            data = json.loads(r.read())
            r.close()
            lfmData = data['recenttracks']['track']
            nowPlaying = '%s now playing: ' % u

            # use try's to bulletproof the code (api does not always return all the information it can)
            try:
                nowPlaying += lfmData[0]['name']
            except:
                pass
            try:
                nowPlaying += ' / %s' % lfmData[0]['artist']['#text']
            except:
                pass
            try:
                nowPlaying += ' / %s.' % lfmData[0]['album']['#text']
            except:
                pass

            return msg(channel, nowPlaying)
        except Exception, e:
            print e

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
    return '48a737c88c910cb86a38dd012fe27745'
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
    if '^setlastfm' in _input:
        setattr(api, 'command', 'setlastfm')
    if '^np' in _input:
        setattr(api, 'command', 'np')
    setattr(api, 'message', _input)
    print callback(api)
'''

if __name__ == "__main__":
    def cache_save():
        print 'Cache saved'
    def config_get(item):
        return '48a737c88c910cb86a38dd012fe27745'
    api = api()
    setattr(api, 'cache_save', cache_save)
    setattr(api, 'config_get', config_get)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'channel', "#test")
    setattr(api, 'locker', empty)
    setattr(api, 'user', 'joe!username@hostmask')

    setattr(api, 'command', 'np')
    setattr(api, 'message', '^np rj')
    print callback(api)
    if 'rj' not in callback(api):
    	exit(1)

    setattr(api, 'command', 'setlastfm')
    setattr(api, 'message', '^setlastfm rj')
    print callback(api)
    if 'Last.FM for' not in callback(api):
    	exit(2)

    setattr(api, 'command', 'np')
    setattr(api, 'message', '^np')
    print callback(api)
    if 'joe' not in callback(api):
    	exit(3)

    setattr(api, 'command', 'np')
    setattr(api, 'user', 'jeb!username@hostmask')
    setattr(api, 'message', '^np joe')
    print callback(api)
    if 'joe' not in callback(api):
    	exit(4)

    print 'All tests passed.'
