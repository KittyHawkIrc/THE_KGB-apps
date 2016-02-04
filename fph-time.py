import datetime

diff = datetime.datetime.now() - self.lockerbox['#fatpeoplehate#soopersekrit'].time['#soopersekrit']

hours = diff.total_seconds() / 3600
minutes = hours % 1 * 60
hours = int(hours)

print "It's been %s hours and %s minutes since the last message was sent in %s (total %s seconds)" % (hours, minutes, '#FatPeopleHate',diff.total_seconds())
