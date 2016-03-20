import json, urllib2

maxChars = 360

def declare():
  return {"ud": "privmsg"}

def callback(self):
    try:
        r = urllib2.urlopen('http://api.urbandictionary.com/v0/define?term=%s' % '+'.join(self.message.split(' ')[1:]))
        data = json.load(r)
        if data['result_type'] != 'no_results':
            defLines = data['list'][0]['definition'].splitlines()
            for line in defLines:
                if line[-1] not in ',.?!':
                    line = line + ','
            definition = '%s: %s %s' % (self.message, data['list'][0]['permalink'], ' '.join(defLines))

            if len(definition) > maxChars:
                definition = definition[:maxChars-4] + '...'
            return self.msg(self.channel, definition)
        else:
            return self.msg(self.channel, 'No definition for %s.' % self.message)
    except:
		return self.msg(self.channel, 'I cannot fetch this definition at the moment.')

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

    if "urbanup" not in callback(api):
        exit(1)
