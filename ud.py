import json, urllib2

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

maxChars = 360

def declare():
  return {"ud": "privmsg"}

def callback(self):
    try:
        message = self.message.split(self.command, 1)[1]
        try:
            r = urllib2.urlopen('http://api.urbandictionary.com/v0/define?term=%s' % '+'.join(message.split()))
            data = json.loads(r.read())
            r.close()

            try:
                defLines = data['list'][0]['definition'].splitlines()
                for line in defLines:
                    if line[-1] not in ',.?!':
                        line = line + ','
                definition = '%s: %s' % (data['list'][0]['word'], ' '.join(defLines))

                if len(definition + ' %s' % data['list'][0]['permalink']) > maxChars:
                    definition = definition[:maxChars-(5 + len(data['list'][0]['permalink']))] + '...'
                return self.msg(self.channel, definition + ' %s' % data['list'][0]['permalink'])
            except:
                return self.msg(self.channel, 'No definition for %s.' % self.message)
        except:
            return self.msg(self.channel, 'I cannot fetch this definition at the moment.')
    except:
        return self.msg(self.channel, 'You need to give me something to look for!')

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)

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
