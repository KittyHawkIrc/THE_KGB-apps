import json, urllib2
try:
    from unidecode import unidecode
except:
    def unidecode(uni):
        return str(uni)

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

maxChars = 360

def declare():
  return {"ud": "privmsg"}

def callback(self):
    message = self.message.split(self.command, 1)[1].strip()
    if message:
        try:
            r = urllib2.urlopen('http://api.urbandictionary.com/v0/define?term=' + '+'.join(message.split()))
            data = json.loads(r.read())
            r.close()
        except:
            return self.msg(self.channel, 'I cannot fetch this definition at the moment.')

        try:
            definition = '%s: %s' % (data['list'][0]['word'], ' '.join(data['list'][0]['definition'].splitlines()))
            while('  ' in definition):
                definition = definition.replace('  ', ' ')

            if len(definition + ' %s' % data['list'][0]['permalink']) > maxChars:
                definition = definition[:maxChars-(4 + len(data['list'][0]['permalink']))] + '...'
            return unidecode(unicode(self.msg(self.channel, str(definition + ' %s' % data['list'][0]['permalink'])))
        except:
            return self.msg(self.channel, 'No definition for %s.' % message)
    return self.msg(self.channel, 'You need to give me something to look for!')

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)

'''
# interactive testing:
api = api()
setattr(api, 'type', 'privmsg')
setattr(api, 'channel', "#test")
setattr(api, 'command', 'ud')
setattr(api, 'user', 'joe!username@hostmask')
setattr(api, 'isop', False)
while(True):
	_input = raw_input('Enter message here: ')
	setattr(api, 'message', _input)
	print callback(api)
'''

if __name__ == "__main__":
    api = api()
    setattr(api, 'isop', True)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'ud')
    setattr(api, 'user', 'joe!username@hostmask')
    setattr(api, 'channel', "#test")
    setattr(api, 'message', '^ud Hitler')

    print callback(api)

    if "urbanup" not in callback(api):
        exit(1)
