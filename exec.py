import sys, urllib.request, urllib.error, urllib.parse

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

try:
    from io import StringIO
except:
    from io import StringIO


def declare():
    return {"exec": "privmsg", "exec_url": "privmsg"}

def callback(self):
    backup = sys.stdout

    if self.channel.startswith('#') and self.isowner:
        if self.command == 'exec':
            text = self.message.split('^exec ')[1]
        else:
            req = urllib.request.Request(self.message.split('^exec_url ')[1])
            fd = urllib.request.urlopen(req)
            text = fd.read()
            fd.close()

        log = StringIO()
        sys.stdout = log

        try:
            exec(text)
            return self.msg(self.channel, log.getvalue())

        except Exception as e:
            return self.msg(self.channel, str(e))

        log.close()
        sys.stdout = backup

class api:
    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

if __name__ == "__main__":
    api = api()
    setattr(api, 'isop', True)
    setattr(api, 'isowner', True)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'exec')
    setattr(api, 'message', '^exec print "test"')
    setattr(api, 'user', 'joe!username@hostmask')
    setattr(api, 'channel', '#test')

    if not callback(api):
        exit(1)
