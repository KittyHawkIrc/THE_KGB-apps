import urllib2
from time import ctime

#c = channel
#u = user giving/taking points
#t = target who's points are being modified
#p = points being taken/removed
def addPoints(self, c, u, t, p):
	ts = ctime()
	up = 0
	tp = 0

	assert p == 1 or p == -1

	if u not in self.locker.pimpdb[c]:
		self.locker.pimpdb[c][u] = 4
		pimpToChan(self, "%s <%s> %s added to db with %s points" % (ts,c,u,self.locker.pimpdb[c][u]))
	elif self.locker.pimpdb[c][u] > 0:
		self.locker.pimpdb[c][u] = int(self.locker.pimpdb[c][u]) - 1
	else:
		self.msg(channel, "%s: You ain't got no pimp points" % (u))
		pimpToChan(self, "%s <%s> %s[%s]'s attempted to change %s[%s]'s points by %s" % (ts,c,u,self.locker.pimpdb[c][u],t,self.locker.pimpdb[c][t],p))
		return

	try: #modifies users points
		self.locker.pimpdb[c][t] += p
	except:
		self.locker.pimpdb[c][t] = 5 + p
		pimpToChan(self, "%s <%s> %s added to db with %s points" % (ts,c,t,self.locker.pimpdb[c][t]-p))

	pimpToChan(self, "%s <%s> %s[%s]'s changes %s[%s]'s points by %s" % (ts,c,u,self.locker.pimpdb[c][u]-p,t,self.locker.pimpdb[c][t]-p,p))

def pimpToChan(self, s):
	for k,v in self.locker.pimpToChandb.items():
		if v:
			self.msg(k, s)

def declare():
	return {"pimp": "privmsg"}

def callback():
	u = self.user.lower().split('!')[0]
	c = self.channel
	if self.channel.startswith('#'):

		chan = self.channel.lower()

		var = self.message.lower().split()

		try:
			target = var[1]
		except:
			target = u

		try:
			com = var[2]
		except:
			com = 'get'

		if chan not in self.locker.pimpdb:
			self.locker.pimpdb[chan] = {}

		if u == target and com != 'get':
			self.self.msg(chan, "%s: Y'all can't pimp yourself, ma nigga" % (u))
			return

		if com == '+1':
			addPoints(self, chan, u, target, 1)
		elif com == '-1':
			addPoints(self, chan, u, target, 1)
		elif com == 'get':
			try:
				pimp = self.locker.pimpdb[chan][target]
				if pimp > 0:
					self.self.msg(self.channel, "that nigga got %s pimp points up in this bitch" % (pimp))
				else:
					self.self.msg(self.channel, "that nigga got %s bitch points" % (pimp))
			except:
				pimp = 5
				self.self.msg(self.channel, "that nigga got 5 pimp points up in this bitch")

				if u in self.locker.pimpdb[c]:
					u_p = self.locker.pimpdb[c][u]
				else:
					u_p = 5

				if target in self.locker.pimpdb[c]:
					target_p = self.locker.pimpdb[c][target]
				else:
					target_p = 5

				pimpToChan(self, "%s <%s> %s[%s]'s checked %s[%s]'s points" % (ctime(), chan, u, u_p, target, target_p))
		else:
			self.self.msg(self.channel, "%s: Nigga, you really think you that og, just giving out more points like that?" % (u))

	elif self.isop: #format as pimp [self.command] [self.channel] [target] [value]
		var = self.message.lower().split()
		com = var[1]
		ts = ctime()

		try:
			chan = var[2]
			target = var[3]
		except:
			if not (com == 'load' or com == 'dump' or com == 'inflate' or com == 'addtoall'):
				return

		try:
			val = var[4]
		except:
			val = 5

		if com == 'set':
			try:
				pval = self.locker.pimpdb[chan][target]
				self.locker.pimpdb[chan][target] = int(val)
				self.self.msg(u, "%s's score in %s is now set to %s" % (target, chan, val))
				pimpToChan(self, "%s <%s> %s[%s]'s points set to %s by op %s" % (ts, chan, target, pval, val, u))
			except:
				self.self.msg(u, "%s doesn't exist in %s" % (target, chan))

		elif com == 'add':
			try:
				self.locker.pimpdb[chan][target] += val
				self.self.msg(u, "%s's score in %s is now set to %s" % (target, chan, val))
				pimpToChan(self, "%s <%s> %s[%s]'s points increased by %s, by op %s" % (ts, chan, target, self.locker.pimpdb[chan][target]-val, val, u))
			except:
				self.self.msg("Doesn't %s exist in %s" % (target, chan))

		elif com == 'remove':
			if target in self.locker.pimpdb[chan]:
				val = self.locker.pimpdb[chan][target]
				self.locker.pimpdb[chan].pop(target)
				self.self.msg(u, "%s is now removed from that self.channel's list" % (target))
				pimpToChan(self, "%s <%s> %s removed from db with %s points by op %s" % (ts, chan, target, val, u))

			else:
				self.self.msg(u, "%s is not in that self.channel's list")

		elif com == 'new':
			if chan not in self.locker.pimpdb:
				self.locker.pimpdb[chan] = {}

			if target not in self.locker.pimpdb[chan]:
				self.locker.pimpdb[chan][target] = int(val)
				self.self.msg(u, "%s is now added to the self.channel with %s points" % (target, val))
				pimpToChan(self, "%s <%s> %s added to db with %s points by op %s" % (ts, chan, target, val, u))

			else:
				self.self.msg(u, "%s is already in the self.channel with %s points, please remove them before adding them again" % (target, val))

		elif com == 'dump':
			self.self.msg(u, str(self.locker.pimpdb))
			pimpToChan(self, "%s <>  All self.channel values dumped by op %s" % (ts, u))

		elif com == 'load':
			req = urllib2.Request(self.message.lower().split('load')[1])
			fd = urllib2.urlopen(req)
			self.locker.pimpdb = eval(fd.read())
			fd.close()
			pimpToChan(self, "%s <> All self.channel values dumped by op %s" % (ts, u))

		elif com == 'inflate': #target == value to multiply by
			for k, v in self.locker.pimpdb[chan].items():
				if v > 0:
					self.locker.pimpdb[chan][k] *= int(target)
				else:
					self.locker.pimpdb[chan][k] /= int(target)
			pimpToChan(self, "%s <%s> Inflated by %s, by op %s" % (ts, chan, target, u))

		elif com == 'addtoall': #target == value to add to each self.user
			for k,v in self.locker.pimpdb[chan].items():
				self.locker.pimpdb[chan][k] += int(target)
			pimpToChan(self, "%s <%s> Increased by %s, by op %s" % (ts, chan, target, u))

		elif com == 'pimptoself.channel': #target == "on", otherwise assumed "off"
			if target == "on":
				self.locker.pimpToChandb[chan] = True
			else:
				self.locker.pimpToChandb[chan] = False
			self.self.msg(u, "Added to database")
			pimpToChan(self, "%s <> %s added to self.locker.pimpToChandb by %s with state op %s" % (ts, chan, u, target))

		else:
			self.self.msg(u, "unavailable")

#initialize dbs if they don't exist
if not hasattr(self.locker, 'pimpToChandb'):
	self.locker.pimpToChandb = {
		"#secretpimps" : True
	}
if not hasattr(self.locker, 'pimpdb'):
	self.locker.pimpdb = {}

class api:
	def msg(self, channel, text):
		print "[%s] %s" % (channel, text)

if __name__ == "__main__":
	api = api()
	setattr(api, 'isop', True)
	setattr(api, 'type', 'privmsg')
	setattr(api, 'command', 'pimp')
	setattr(api, 'message', '^pimp')
	setattr(api, 'user', 'joe!username@hostmask')
	setattr(api, 'channel', '#test')
	
	callback(api)
	
	api.message = "^pimp jonnycarter +1"
	
	callback(api)
