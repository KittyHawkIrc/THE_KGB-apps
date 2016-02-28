import math, re

heights = [['mm','millimetre','millimeter', 0.001],
			['cm','centimetre','centimeter', 0.01],
			['dm','decimetre','decimeter', 0.1],
			['m','metre','meter', 1],
			['\'','ft','feet','foot', 0.3048],
			['\"','in', 0.0254],
			['yr','yard', 0.9144]]
masses = [['mg','milligram', 0.000001],
			['cg','centigram', 0.00001],
			['dg','decigram', 0.0001],
			['g','gram', 0.001],
			['kg','kilogram', 1],
			['oz','ou','ounce', 0.0283495],
			['lb','pound', 0.453592],
			['st','stone', 6.35029]]

heightUnits = [i for s in heights for i in s if type(i) == str]
massUnits = [i for s in masses for i in s if type(i) == str]

def declare():
	return {'bmi': 'privmsg'}

def callback(self):
	u = self.message.split('!').lower()[0]
	p1 = self.message.split(' ').lower()[1]
	
	if p1 in self.locker.bmi:
		try:
			bmi = self.locker.bmi[u]
		except:
			try:
				_ = self.locker.bmi
			except:
				self.locker.bmi = dict()
			return self.msg(channel, "%s has yet to set their BMI" % (p1.capitalize))
		
		if bmi < 18.5:
			o = '\002\00308underweight'
		elif bmi > 24:
			o = '\002\00307close to overweight'
		elif bmi > 25:
			o = '\002\00304overweight'
		else:
			o = '\002\00309in a normal healthy range'
		
		return self.msg(self.channel, '%s\'s BMI is %s. This BMI is %s.' % (p1.capitalize(), format(bmi,'\.2f'), o))
	
	ca = calc(self)
	bmi = ca[0]
	mass = ca[1]
	height = ca[2]
	
	if p1 == 'set':
		try:
			self.locker.bmi[u] = mass / (height ** 2)
		except:
			self.locker.bmi = {u : mass / (height ** 2)}
		
		return self.msg(self.channel,"Your BMI is set to be %s" % (format(self.locker.bmi[u],'\.2f')))
	elif height > 0 and mass >= 0 and bmi == 0:
		bmi = mass / (height ** 2)

		output = 'Your BMI is %s, you are \002\003' % format(bmi, '.2f')

		if bmi < 18.5:
			output += '08underweight'
		elif bmi < 25.0:
			output += '09normal'
		elif bmi < 30.0:
			output += '07FAT'
		else:
			output += '04FAT AS FUCK'

		return self.msg(self.channel, output + '\017.')
	elif height > 0 and bmi > 0:
		mass = bmi * (height ** 2)

		return self.msg(self.channel, 'Your mass is %skg.' % format(mass, '.2f'))
	elif bmi > 0:
		height = math.sqrt(mass / bmi)

		return self.msg(self.channel, 'Your height is %sm' % format(height, '.2f'))

def calc(self):
	mass = 0.0
	height = 0.0
	bmi = 0.0
	
	message = self.message.split(self.command, 1)[1]
	
	parameters = parseMessage(message)

	for parameter in parameters:
		if parameter[1] in heightUnits:
			for unit in heights:
				if parameter[1] in unit[:-1]:
					height += parameter[0] * unit[-1]
		elif parameter[1] in massUnits:
			for unit in masses:
				if parameter[1] in unit[:-1]:
					mass += parameter[0] * unit[-1]
		elif parameter[1].lower() == 'bmi':
			bmi = parameter[0]
	
	return [bmi,mass,height]

def split(text, separators):
	for separator in separators:
		text = text.replace(separator, '%s ' % separator)

	return [i.strip() for i in text.split(' ')]

def parseMessage(message):
	parameters = []

	reFloat = re.compile('(\d+[.])?\d+')
	reString = re.compile('[^\.\d]+')

	messageSplit = split(message, heightUnits + massUnits + ['bmi'])

	for item in messageSplit:
		floatSearch = reFloat.search(item)
		stringSearch = reString.search(item)

		if floatSearch and stringSearch:
			parameters.append([float(reFloat.search(item).group()), reString.search(item).group().lower()])
		elif floatSearch:
			parameters.append([float(reFloat.search(item).group())])
		elif stringSearch and len(parameters) > 0:
			parameters[-1].append(reString.search(item).group().lower().rstrip('s'))

	for i, item in enumerate(parameters):
		if i > 0 and parameters[i - 1][1] == '\'' and len(item) < 2:
			item.append('\"')

	return parameters

class api:
  def msg(self, channel, text):
	return "[%s] %s" % (channel, text)

if __name__ == "__main__":
	api = api()
	setattr(api, 'isop', True)
	setattr(api, 'type', 'privmsg')
	setattr(api, 'command', 'bmi')
	setattr(api, 'user', 'joe!username@hostmask')
	setattr(api, 'channel', "#test")
	setattr(api, 'message', '^bmi 5\'6\" 130lbs')
	setattr(api, 'locker', empty)

	if "Your BMI is 20.98" not in callback(api):
		exit(1)
	setattr(api, 'message', '^bmi set 5\'6\" 130lbs')
	if "Your BMI is set to be 20.98" not in callback(api):
		exit(2)
	setattr(api, 'message', '^bmi joe')
	if "Joe's BMI is 20.98" not in callback(api):
		exit(3)
	setattr(api, 'message', '^bmi john')
	if "John has yet to set their BMI" not in callback(api):
		exit(4)
