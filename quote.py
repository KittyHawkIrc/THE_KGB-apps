import random

def declare():
    return {"quote": "privmsg", "quoteadd": "privmsg", "quotesearch": "privmsg"}

def callback(self):
    try:
        self.locker.quote
    except:
        self.locker.quote = []

    try:
        message = self.message.split(' ', 1)[1]
        if type(message) == int:
            index = int(message)
            message = ''
    except:
        message = ''

    if self.message.split(' ', 1)[0] == '^quoteadd':
        if self.isop:
            if message not in self.locker.quote:
                self.locker.quote.append(message)
                return self.msg(self.channel, 'Quote added')
            return self.msg(self.channel, 'I already know this quote')
        return self.msg(self.channel, 'You are not authorized to use this command')
    if self.message.split(' ', 1)[0] == '^quotesearch':
        try:
            count = 1
            results = []
            for q in self.locker.quote:
                if self.message.split(' ', 1)[1] in q:
                    results.append(count)
                count = count + 1
            try:
                return self.msg(self.channel, 'Results: [%s]' % ', '.join(results))
            except:
                return self.msg(self.channel, 'No results found')
        except:
            return self.msg(self.channel, 'I don\'t know any quotes')
    if len(self.locker.quote) > 0:
        try:
            return self.msg(self.channel, self.locker.quote[index - 1])
        except UnboundLocalError:
            return self.msg(self.channel, self.locker.quote[random.randint(0, len(self.locker.quote) - 1)])
        except IndexError:
            return self.msg(self.channel, 'I don\'t know that many quotes')
    return self.msg(self.channel, 'I don\'t know any quotes')

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)
class empty:
	pass

if __name__ == "__main__":
    api = api()
    setattr(api, 'isop', True)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'quote')
    setattr(api, 'channel', "#test")
    setattr(api, 'locker', empty)

    setattr(api, 'message', '^quote 0')
    if 'know any quotes' not in callback(api):
        print(1)
        exit(1)

    setattr(api, 'message', '^quoteadd foo')
    if 'Quote added' not in callback(api):
        print(2)
        exit(2)

    setattr(api, 'message', '^quote 0')
    if 'foo' not in callback(api):
        print(3)
        exit(3)

    setattr(api, 'message', '^quote')
    if 'foo' not in callback(api):
        print(4)
        exit(4)

    setattr(api, 'message', '^quoteadd foo')
    if 'already know' not in callback(api):
        print(5)
        exit(5)

    setattr(api, 'message', '^quoteadd bar')
    if 'Quote added' not in callback(api):
        print(6)
        exit(6)

    setattr(api, 'message', '^quote 1')
    if 'foo' not in callback(api):
        print(7)
        exit(7)

    setattr(api, 'message', '^quotesearch foo')
    if '1' not in callback(api):
        print(callback(api))
        exit(8)

    setattr(api, 'message', '^quotesearch foobar')
    if 'I don\'t know' not in callback(api):
        print(9)
        exit(9)
