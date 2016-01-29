import datetime

channels = {'#the_kgb'}

def declare():
    return {"timepassed": "syncmsg"}

def callback(self):
  if self.outgoing_channel.lower() in channels:
    #check if time's been set
    try:
      time = self.locker.time[self.outgoing_channel]
    except:
        try:
            self.locker.time[self.outgoing_channel] = datetime.datetime.now()
        except:
            self.locker.time = {self.outgoing_channel: datetime.datetime.now()}
        return

    diff = datetime.datetime.now() - time

    if diff.total_seconds() < 600:
      self.locker.time[self.outgoing_channel] = datetime.datetime.now()
      return

    hours = diff.total_seconds() / 3600
    minutes = hours % 1 * 60
    hours = int(hours)

    #set this time in the locker
    self.locker.time[self.outgoing_channel] = datetime.datetime.now()

    self.msg(self.outgoing_channel, "It's been %s hours and %s minutes since the last message was sent in %s (total %s seconds)" % (hours, minutes, self.incoming_channel,diff.total_seconds()))
