import json, random, urllib2

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

def declare():
    return {"reddit": "privmsg", "guess": "privmsg"}

def callback(self):
    channel = self.channel
    command = self.command
    user = self.user
    msg = self.message
    type = self.type
    isop = self.isop

    if command == 'guess':
        u = 'FitOrFat'
    else:
        try:
            u = str(msg.split(' ', 1)[1])
        except:
            return self.msg(channel, "Please specify a subreddit!")

    try:

        req = urllib2.Request("https://www.reddit.com/r/" + u + "/new.json", headers={ 'User-Agent': 'UNIX:the_kgb:reddit https://github.com/stqism/THE_KGB-apps' })
        fd = urllib2.urlopen(req)
        reddit_api = json.loads(fd.read())
        fd.close()

        cringe = []

        for i in reddit_api['data']['children']:
            url = i['data']['url']
            title = i['data']['title']
            selfpost = bool(i['data']['is_self'])
            post = "https://reddit.com" + i['data']['permalink']

            if 'imgur' in url:

                if 'http://i.imgur.com' in url:  #force https
                    url = 'https://i.imgur.com/%s' % (url.split('/')[3])

                if 'http://' in url and '/a/' not in url:   #direct URLs
                    if 'gallery' in url:
                        url = 'https://i.imgur.com/%s.jpg' % (url.split('/')[4])
                    else:
                        url = 'https://i.imgur.com/%s.jpg' % (url.split('/')[3])

            cringe.append([title, url, post])

        item = random.choice(cringe)

        if command == 'guess':

            try:
                u = str(msg.split(' ', 1)[1])
                return self.msg(channel,  u + ": Am I fit or fat? " + item[1])
            except:
                return self.msg(channel,  "Am I fit or fat? " + item[1])

        else:

            if not selfpost:
                via = "     (via: " + item[2] + ")"
                return self.msg(channel, str(item[0] + " " + item[1] + via))
            else:
                return self.msg(channel, str(item[0] + " " + item[1]))

    except Exception, e:
        return self.msg('#the_kgb', str(e))


class api:
    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

if __name__ == "__main__":
    api = api()
    c = "#test"

    setattr(api, 'isop', True)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'reddit')
    setattr(api, 'user', 'joe!username@hostmask')
    setattr(api, 'channel', c)

    setattr(api, 'message', '^reddit')
    if callback(api) != '[%s] Please specify a subreddit!' % (c):
        print '[TESTFAIL] no arguments'
        exit(1)

    setattr(api, 'message', '^reddit fatpeoplehate')
    if callback(api) != '[#the_kgb] HTTP Error 404: Not Found':
        print '[TESTFAIL] error catcher'
        exit(1)

    setattr(api, 'message', '^reddit fatlogic')
    if not callback(api).startswith('[%s] ' % (c)):
        print '[TESTFAIL] Subreddit loader'
        exit(1)

    setattr(api, 'message', '^guess')
    setattr(api, 'command', 'guess')
    if not callback(api).startswith('[%s] Am I fit or fat?' % (c)):
        print '[TESTFAIL] guess no user'
        print '[%s] Am I male or female?' % (c)
        exit(1)

    n = 'bob'
    setattr(api, 'message', '^guess %s' % (n))
    if not callback(api).startswith('[%s] %s: Am I fit or fat?' % (c, n)):
        print '[TESTFAIL] guess with user'
        exit(1)
