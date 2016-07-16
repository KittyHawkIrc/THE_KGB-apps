import math, re

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

# uses m as base, each list[-1] is the number to multiply to convert to meters
# metric heights
mHeights = [['mm','millimetre','millimeter', 0.001],
			['cm','centimetre','centimeter', 0.01],
			['dm','decimetre','decimeter', 0.1],
			['m','metre','meter', 1]]
# imperial heights
iHeights = [['\'','ft','feet','foot', 0.3048],
			['\"','in','inch', 0.0254],
			['yr','yard', 0.9144]]

# uses kg as base, each list[-1] is the number to multiply to convert to kg
# metric masses
mMasses = [['mg','milligram', 0.000001],
			['cg','centigram', 0.00001],
			['dg','decigram', 0.0001],
			['g','gram', 0.001],
			['kg','kilogram', 1]]
# imperial masses
iMasses = [['oz','ou','ounce', 0.0283495],
			['lb','pound', 0.453592],
			['st','stone', 6.35029]]

# combined heights and masses
heights = mHeights + iHeights
masses = mMasses + iMasses

# lists of units for height and mass
metricUnits = [i for s in (mHeights + mMasses) for i in s if type(i) == str]
imperialUnits = [i for s in (iHeights + iMasses) for i in s if type(i) == str]
heightUnits = [i for s in heights for i in s if type(i) == str]
massUnits = [i for s in masses for i in s if type(i) == str]

def declare():
	return {'bmi': 'privmsg', 'setbmi': 'privmsg'}

def callback(self):
	channel = self.channel
	command = self.command
	user = self.user.split('!')[0].lower()
	msg = self.msg
	isop = self.isop
	message = self.message.split(command, 1)[1]

	co = count(message)
	bmi = co[0]
	mass = co[1]
	height = co[2]
	met = co[3]
	imp = co[4]

	if command == 'setbmi':
		bmi = mass / (height ** 2)

		if message.lstrip()[0] not in '1234567890':
			if isop:
				user = message.split()[0].lower()
			else:
				return msg(channel, 'You do not have the authority to set %s\'s BMI, citizen.' % message.split()[0])

		if isop or (bmi < 25 and bmi > 15):
			try:
				self.locker.bmi[user] = bmi
			except:
				self.locker.bmi = {user: bmi}
				
			self.cache_save() 	#persist cache post-restarts

			if user == self.user.split('!')[0].lower():
				return msg(channel, 'Your BMI has been set to %s, which is \002\003%s\017.' % (format(bmi, '.2f'), classifyBmi(bmi)))
			else:
				return msg(channel, '%s\'s BMI has been set to %s, which is \002\003%s\017.' % (message.split()[0], format(bmi, '.2f'), classifyBmi(bmi)))
		else:
			return msg(channel, 'Please ask a bot operator to set your BMI for you.')

	elif command == 'bmi':
		if height and mass:
			bmi = mass / (height ** 2)
			return msg(channel, 'Your BMI is %s, you are \002\003%s\017.' % (format(bmi, '.2f'), classifyBmi(bmi)))

		if height and bmi:
			mass = bmi * (height ** 2)
			if 'imperial' in message or (imp > met and 'metric' not in message):
				return msg(channel, 'Your mass is %slbs.' % format(mass / 0.453592, '.2f'))
			return msg(channel, 'Your mass is %skg.' % format(mass, '.2f'))

		if mass and bmi:
			height = math.sqrt(mass / bmi)
			if 'imperial' in message or (imp > met and 'metric' not in message):
				iHeight = mToFtIn(height)
				return msg(channel, 'Your height is %d\'%d".' % (iHeight[0], iHeight[1]))
			return msg(channel, 'Your height is %sm.' % format(height, '.2f'))

		if len(message) < 1 or message.lstrip()[0] not in '1234567890':
			if len(message) > 0:
				user = message.split()[0].lower()
			try:
				bmi = self.locker.bmi[user]

				if user == self.user.split('!')[0].lower():
					return msg(channel, 'Your BMI is %s, which is \002\003%s\017.' % (format(bmi, '.2f'), classifyBmi(bmi)))
				else:
					return msg(channel, '%s\'s BMI is %s, which is \002\003%s\017.' % (message.split()[0], format(bmi, '.2f'), classifyBmi(bmi)))

			except:
				if user == self.user.split('!')[0].lower():
					return msg(channel, 'Your BMI has not been set yet')
				else:
					return msg(channel, '%s\'s BMI has not been set yet' % message.split()[0])
		return msg(channel, 'Invalid input.')

def classifyBmi(bmi):
	if bmi < 18.5:
		return '08underweight'
	if bmi < 25.0:
		return '09normal'
	if bmi < 30.0:
		return '07FAT'
	else:
		return '04FAT AS FUCK'

def mToFtIn(meters):
	feet = int(meters // 0.3048)
	inches = int(meters / 0.3048 % 1 * 12)
	return [feet, inches]

def count(message):
	# counters for accumulated mass/height/bmi values
	mass = 0.0
	height = 0.0
	bmi = 0.0

	# counters for number of metric/imperial units
	metric = 0
	imperial = 0

	parameters = parseMessage(message)

	for parameter in parameters:
		p1 = ''.join(parameter[1:]).rstrip('es')

		# check if unit is imperial or metric (used for returning mass/height)
		if p1 in metricUnits:
			metric += 1
		elif p1 in imperialUnits:
			imperial += 1

		# check if unit is a height/mass unit or is 'bmi'
		if p1 in [u2.rstrip('es') for u2 in [u1 for u1 in heightUnits]]:
			for unit in heights:
				if p1 in [u.rstrip('es') for u in unit[:-1]]:
					height += parameter[0] * unit[-1]
					break
		if p1 in [u2.rstrip('es') for u2 in [u1 for u1 in massUnits]]:
			for unit in masses:
				if p1 in [u.rstrip('es') for u in unit[:-1]]:
					mass += parameter[0] * unit[-1]
					break
		elif p1 == 'bmi':
			bmi += parameter[0]

	return [bmi, mass, height, metric, imperial]

def split(text, separators):
	for separator in separators:
		text = text.replace(separator, ' %s ' % separator)

	return [i.strip() for i in text.split(' ')]

def parseMessage(message):
	parameters = []

	reFloat = re.compile('(\d+)?[.]?\d+')
	reString = re.compile('[^\.\d]+')

	messageSplit = split(message.lower(), heightUnits + massUnits + ['bmi'])

	for item in messageSplit:
		if item:
			floatSearch = reFloat.search(item)
			stringSearch = reString.search(item)

			# handles cases where no space between value and unit
			if floatSearch and stringSearch:
				parameters.append([float(reFloat.search(item).group()), reString.search(item).group()])
			# handles cases where there is a space between the value and unit
			elif floatSearch:
				parameters.append([float(reFloat.search(item).group())])
			elif stringSearch and len(parameters) > 0:
				parameters[-1].append(reString.search(item).group())

	# handles cases where inches is not included (ie: 5'6 for 5'6")
	for i, item in enumerate(parameters):
		if i > 0 and parameters[i - 1][1] == '\'' and len(item) < 2:
			item.append('\"')

	return parameters

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)
class empty:
	pass

'''
# interactive testing:
api = api()
setattr(api, 'type', 'privmsg')
setattr(api, 'channel', "#test")
setattr(api, 'command', 'bmi')
setattr(api, 'locker', empty)
setattr(api, 'user', 'joe!username@hostmask')
setattr(api, 'isop', False)
while(True):
	_input = raw_input('Enter message here: ')
	if _input == 'op':
		setattr(api, 'isop', True)
		print 'User opped'
	elif _input == 'deop':
		setattr(api, 'isop', False)
		print 'User deopped'
	elif _input == 'quit':
		exit()
	else:
		if 'setbmi' in _input:
			setattr(api, 'command', 'setbmi')
		else:
			setattr(api, 'command', 'bmi')
		setattr(api, 'message', _input)
		print callback(api)
'''
if __name__ == "__main__":
	api = api()
	setattr(api, 'type', 'privmsg')
	setattr(api, 'channel', "#test")
	setattr(api, 'locker', empty)
	setattr(api, 'user', 'joe!username@hostmask')

	setattr(api, 'isop', False)
	setattr(api, 'command', 'bmi')
	setattr(api, 'message', '^bmi 5\'6\" 130lbs')
	if 'Your BMI is' not in callback(api):
		exit(1)

	setattr(api, 'command', 'setbmi')
	setattr(api, 'message', '^setbmi 5\' 6\" 180lbs')
	if 'Please ask' not in callback(api):
		exit(2)

	setattr(api, 'command', 'bmi')
	setattr(api, 'message', '^bmi')
	if 'Your BMI has not' not in callback(api):
		exit(3)

	setattr(api, 'message', '^bmi Joe')
	if 'Your BMI has not' not in callback(api):
		exit(4)

	setattr(api, 'message', '^bmi Jeb')
	if 'Jeb\'s BMI has not' not in callback(api):
		exit(5)

	setattr(api, 'command', 'setbmi')
	setattr(api, 'message', '^setbmi 5\'6\" 130lbs')
	if 'Your BMI has been' not in callback(api):
		exit(6)

	setattr(api, 'command', 'bmi')
	setattr(api, 'message', '^bmi')
	if 'Your BMI is' not in callback(api):
		exit(7)

	setattr(api, 'message', '^bmi Joe')
	if 'Your BMI is' not in callback(api):
		exit(8)

	setattr(api, 'user', 'jeb!username@hostmask')
	setattr(api, 'message', '^bmi Joe')
	if 'Joe\'s BMI is' not in callback(api):
		exit(9)

	setattr(api, 'command', 'setbmi')
	setattr(api, 'message', '^setbmi Joe 5\'6" 180lbs')
	if 'You do not' not in callback(api):
		exit(10)

	setattr(api, 'isop', True)
	setattr(api, 'message', '^setbmi Joe 5\'6" 180lbs')
	if 'Joe\'s BMI has been' not in callback(api):
		exit(11)

	setattr(api, 'message', '^setbmi 5\'6" 180lbs')
	if 'Your BMI has been' not in callback(api):
		exit(12)
