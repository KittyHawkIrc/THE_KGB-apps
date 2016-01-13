def declare():
	return {"brainfuck": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
	if channel.startswith('#'):
		DEFAULT_COUNTER = 1000000
		counter = DEFAULT_COUNTER
		index = 0
		array = [0] * 20
		lastRepeat = []
		output = ""
		disabled = -1
		i = 0
		c = 0
		
		while i < len(msg):
			c = msg[i]
			i += 1
			counter -= 1
	
			if counter <= 0:
				self.msg(channel, "Command exceeded %s ticks." % (DEFAULT_COUNTER))
				return("Command exceeded %s ticks." % (DEFAULT_COUNTER)) 
			
			if c == '[':
				if array[index] == 0:
					disabled = len(lastRepeat)
				lastRepeat.append(i)
			elif c == ']':
				if array[index] == 0:
					lastRepeat.pop()
					if len(lastRepeat) <= disabled:
						disabled = -1
				else:
					i = lastRepeat.pop()-1
			elif disabled > 0:
				#print("disabled")
				if len(lastRepeat) > disabled:
					continue
				else:
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
				#print(".")
				output += chr(array[index])
			else:
				continue
	
			#print(c+":"+str(index)+":"+str(array))
			
			#try:
			if array[index] > 255:
				array[index] = 0
			elif array[index] < 0:
				array[index] = 255
	
		self.msg(channel, output[:133])
		return output[:133]


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
	
	t1 = callback(api, type, isop, command=hook, msg="^brainfuck ++++++++++++++++++++++++++++++++++++++++++++++++++++++++..............", channel=channel, user=user)
	t2 = callback(api, type, isop, command=hook, msg="^brainfuck +++++ +++++ initialize counter (cell #0) to 10 [ use loop to set 70/100/30/10 > +++++ ++ add 7 to cell #1 > +++++ +++++ add 10 to cell #2 > +++ add 3 to cell #3 > + add 1 to cell #4 <<<< - decrement counter (cell #0) ] > ++ . print 'H' > + . print 'e' +++++ ++ . print 'l' . print 'l' +++ . print 'o' > ++ . print ' ' << +++++ +++++ +++++ . print 'W' > . print 'o' +++ . print 'r' ----- - . print 'l' ----- --- . print 'd' > + . print '!' > . print '\n'", channel="", user=user)
	t3 = callback(api, type, isop, command=hook, msg="^brainfuck ++[++++.]", channel=channel, user=user)
	t4 = callback(api, type, isop, command=hook, msg="-[-.]", channel=channel, user=user)
	
	callback(api, type, isop, command=hook, msg=msg, channel=channel, user=user)
	if t1 != "88888888888888":
		exit(1)
	if t2 != "Hello World!\n":
		exit(2)
	if t3 != 'Command exceeded 1000000 ticks.':
		exit(3)
	if t4 != 'þýüûúùø÷öõôóòñðïîíìëêéèçæåäãâáàßÞÝÜÛÚÙØ×ÖÕÔÓÒÑÐÏÎÍÌËÊÉÈÇÆÅÄÃÂÁÀ¿¾½¼»º¹¸·¶µ´³²±°¯®\xad¬«ª©¨§¦¥¤£¢¡\xa0\x9f\x9e\x9d\x9c\x9b':
		exit(4)
