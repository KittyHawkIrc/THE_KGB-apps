import datetime

channels = {'#soopersekrit'}

def declare():
    return {"timepassed": "syncmsg"}

def callback(self):
  if self.outgoing_channel in channels:
    #check if time's been set
    try:
      time = self.locker.time[outgoing_channel]
    except:
      self.locker.time[outgoing_channel] = datetime.datetime.now()
      return
    
    diff = datetime.datetime.now() - time
    
    if diff.total_seconds() < 600:
      self.locker.time[outgoing_channel] = datetime.datetime.now()
      return
    
    hours = diff.total_seconds() / 3600
    minutes = hours % 1 * 60
    hours = int(hours)
    
    #set this time in the locker
    self.locker.time[outgoing_channel] = datetime.datetime.now()
    
    self.msg(outgoing_channel, 'It's been %s hours and %s minutes since the last message was sent in %s'%(hours, minutes, incoming_channel))
