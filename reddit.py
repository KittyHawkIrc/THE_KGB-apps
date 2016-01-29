import json, random, urllib2

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
        u = 'SwordOrSheath'
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
                return self.msg(channel,  u + ": Am I male or female? " + item[1])
            except:
                return self.msg(channel,  "Am I male or female? " + item[1])

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
    u = "joe!username@hostmask"
    c = '#test'

    if callback(api, '', True, channel=c, user=u, command='reddit', msg='^reddit') != '[%s] Please specify a subreddit!' % (c):
        print '[TESTFAIL] no arguments'
        exit(1)

    if callback(api, '', True, channel=c, user=u, command='reddit', msg='^reddit fatpeoplehate') != '[#the_kgb] HTTP Error 404: Not Found':
        print '[TESTFAIL] error catcher'
        exit(1)

    if not callback(api, '', True, channel=c, user=u, command='reddit', msg='^reddit fatlogic').startswith('[%s] ' % (c)):
        print '[TESTFAIL] Subreddit loader'
        exit(1)

    if not callback(api, '', True, channel=c, user=u, command='guess', msg='^guess').startswith('[%s] Am I male or female?' % (c)):
        print '[TESTFAIL] guess no user'
        exit(1)

    n = 'bob'
    if not callback(api, '', True, channel=c, user=u, command='guess', msg='^guess %s' % (n)).startswith('[%s] %s: Am I male or female?' % (c, n)):
        print '[TESTFAIL] guess with user'
        exit(1)
