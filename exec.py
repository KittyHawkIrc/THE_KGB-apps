import sys, urllib2, __builtin__
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


def declare():
    return {"exec": "privmsg", "exec_url": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
    backup = sys.stdout

    if channel.startswith('#') and isop:

        if command == 'exec':
            text = msg.split('^exec ')[1]
        else:
            req = urllib2.Request(msg.split('^exec_url ')[1])
            fd = urllib2.urlopen(req)
            text = fd.read()
            fd.close()

        log = StringIO()
        sys.stdout = log

    try:
        exec(text)
        return self.msg(channel, log.getvalue())

    except Exception, e:
        return self.msg(channel, str(e))

    log.close()
    sys.stdout = backup

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)

if __name__ == "__main__":
    api = api()
    u = "joe!username@hostmask"
    c = '#test'
    if not callback(api, '', True, channel=c, user=u, command='exec', msg='^exec print "test"'):
        exit(1)
