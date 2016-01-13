def declare():
	return {"brainfuck": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
	if channel.startswith('#'):
		DEFAULT_COUNTER = 1000000
		counter = DEFAULT_COUNTER
		index = 0
		array = [0] * 30000
		lastRepeat = []
		output = ""
		disabled = -1
		c = 0
		
		while c > len(msg):
			c += 1
			
			if counter <= 0:
				self.msg(channel, "Command exceeded %s ticks." % (DEFAULT_COUNTER)) 
			
			if c == '[':
				if array[index] == 0:
					c+=1
					disabled = len(lastRepeat)
				lastRepeat.append(c)
			elif c == ']':
				if array[index] == 0:
					lastRepeat.pop(c)
					if len(lastRepeat) <= disabled:
						disabled = -1
				else:
					index = lastRepeat.pop(c)
			elif disabled >= 0:
				if len(lastRepeat) > disabled:
					continue
				else
					disabled = False
					c -= 1
			elif c == '+':
				array[index] += 1
			elif c == '-':
				array[index] -= 1
			elif c == '>':
				index += 1
			elif c == '<':
				index -= 1
			elif c == '.':
				output += chr(array[index])
			else:
				continue
			
			if array[index] > 255:
				array[index] = 0
			elif array[index] < 0:
				array[index] = 255
		
		return output

class api:
	def msg(self, channel, text):
		print "[%s] %s" % (channel, text)

if __name__ == "__main__":
	api = api()

	hook = list(declare())[0]

	msg = "^pimp"
	user = "joe!username@hostmask"
	channel = "#test"
	type = "privmsg"
	isop = True

	callback(api, type, isop, command=hook, msg=msg, channel=channel, user=user)
	if callback(api, type, isop, command=hook, msg="^brainfuck ++++++++++++++++++++++++++++++++++++++++++++++++++++++++..............", channel=channel, user=user) != "88888888888888":
		exit(1)
	if callback(api, type, isop, command=hook, msg="^brainfuck +++++ +++++ initialize counter (cell #0) to 10 [ use loop to set 70/100/30/10 > +++++ ++ add 7 to cell #1 > +++++ +++++ add 10 to cell #2 > +++ add 3 to cell #3 > + add 1 to cell #4 <<<< - decrement counter (cell #0) ] > ++ . print 'H' > + . print 'e' +++++ ++ . print 'l' . print 'l' +++ . print 'o' > ++ . print ' ' << +++++ +++++ +++++ . print 'W' > . print 'o' +++ . print 'r' ----- - . print 'l' ----- --- . print 'd' > + . print '!' > . print '\n'", channel="", user=user) != "Hello World!":
		exit(1)
