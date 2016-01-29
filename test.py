import datetime

channels = {'#the_kgb'}

def declare():
    return {"test": "syncmsg"}

def callback(self):
  if self.outgoing_channel.lower() in channels:
    self.msg(self.outgoing_channel, "This is a test")
