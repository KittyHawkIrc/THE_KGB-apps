# -*- coding: utf-8 -*-

import json, urllib2

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

def declare():
  return {"np": "privmsg", "setlastfm": "privmsg"}

def callback(self):
    key = self.config_get('apikey')
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
            url = 'https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='
            if len(message) == 0:
                url += self.locker.lastfm[user.lower()]
                u = user
            else:
                try:
                    url += self.locker.lastfm[message.split()[0].lower()]
                    u = message.split()[0]
                except:
                    url += message.split()[0]
                    u = message.split()[0]
            url += '&api_key=%s&format=json' % key
            r = urllib2.urlopen(url)
            json = json.loads(r.read())['recenttracks']['track'][0]
            r.close()
            
            now_playing = '%s np: ' % u
            now_playing_list = []
            # use try's to bulletproof the code (api does not always return all the information it can)
            try:
                if json['name']:
                    now_playing_list.append('{} {}' % ('🎵', json['name']))
            except:
                pass
            try:
                if json['artist']['#text']:
                    now_playing_list.append('{} {}' % ('🎤', json['artist']['#text']))
            except:
                pass
            try:
                if json['album']['#text']:
                    now_playing_list.append('{} {}' % ('💽', json['album']['#text']))
            except:
                pass

            now_playing = now_playing + ' / '.join(npList)
            return msg(channel, now_playing)
        except Exception as e:
            return msg(channel, e)

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
setattr(api, 'command', 'np')
setattr(api, 'locker', empty)
setattr(api, 'user', 'nick!ident@host')
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
    setattr(api, 'user', 'nick!ident@host')

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
