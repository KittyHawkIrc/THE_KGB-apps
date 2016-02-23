import datetime
users = {"none" : [datetime.datetime.now(),"#none"]}

def declare():
    return {"seen": "userjoin", "seen": "privmsg"}

def callback(self):
  u = self.user.lower().split('!')[0]
  
  if self.type != 'privmsg':
    users[u] = [datetime.datetime.now(),self.channel]
    self.msg('#THE_KGB', '%s : %s, %s' % (u,datetime.datetime.now(),self.channel))
  else:
    u2 = self.message.split(' ')[1].lower()
    try:
      if u2 == u:
        return self.msg(self.channel, '/whois %s' % (u))
      else:
        return self.msg(self.channel, '%s was last seen joining %s at %s. It is currently %s' % (u2, users[u2][1], users[u2][0], datetime.datetime.now()))
    except:
        return self.msg(self.channel, 'I have not seen %s yet. Please try later. Thank you.' % (u2))

class api:
    def msg(self, channel, text):
        print "[%s] %s" % (channel, text)
        return "[%s] %s" % (channel, text)

if __name__ == "__main__":
    api = api()
    setattr(api, 'type', 'userjoin')
    setattr(api, 'user', 'joe!username@hostmask')
    setattr(api, 'channel', '#test')
    setattr(api, 'ver', '1.1.8')
    callback(api)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'message', '^seen joe')
    
    if '/whois ' not in callback(api):
        exit(1)
    setattr(api, 'user', 'john!username@hostmask')
    if 'joe was last seen joining #test at' not in callback(api):
        exit(2)
    setattr(api, 'message', '^seen jack')
    if 'I have not seen %s yet. Please try later. Thank you.' % ('jack') not in callback(api):
        exit(3)
