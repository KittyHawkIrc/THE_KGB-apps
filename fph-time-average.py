sec = 0.0
for i in self.store.timepassed['#soopersekrit']:
  sec += self.store.timepassed['#soopersekrit'][i]
  sec = sec / 2
  
hours = sec / 3600
minutes = hours % 1 * 60
seconds = minutes % 1 * 60
hours = int(hours)
minutes = int(minutes)
seconds = int(seconds)

print "Average time between messages: %s hours, %s minutes, and %s seconds" % (hours, minutes, seconds)
