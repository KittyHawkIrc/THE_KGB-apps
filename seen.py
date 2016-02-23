import datetime
users = {}

def declare():
    return {"seen": "userjoin", "seen": "privmsg"}

def callback(self):
  u = self.user.split('!')[0]
  
  if self.type == 'userjoin':
    users[u] = [datetime.datetime.now(),self.channel]
  else:
    u2 = self.message.split(' ')[1]
    try:
      if u2 == u:
        return self.msg(self.channel, 'Just whois yourself, you fool')
      else:
        return self.msg(self.channel, '%s was last seen joining %s at %s. Also fuck proper formatting. Who do you think you are, a stripper? You don\'t tell me what to do.' % (u2, users[u2][0], users[u2][1]))
    except:
        return self.msg(self.channel, 'I have not seen this person yet. Please try later. Thank you.')

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
    
    if 'Just whois yourself, you fool' not in callback(api):
        exit(1)
    setattr(api, 'user', 'john!username@hostmask')
    if 'joe was last seen joining #test at' not in callback(api):
        exit(2)
    setattr(api, 'message', '^seen jack')
    if 'I have not seen this erson yet. Please try later. Thank you' not in callback(api):
        exit(3)
