# Module dedicated to this Nirvana cover of a David Bowie song
# https://open.spotify.com/track/15VRO9CQwMpbqUYA7e6Hwg

from pint import UnitRegistry

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

#fuck bym
unit = UnitRegistry() #can't code for shit
convert = unit.Quantity #like how do you fuck up conversions that bad

def declare():  #SERIOUSLY. no one used the 30000 hooks in here.
    return {"convert":"privmsg", "fuckbym":"privmsg", "c":"privmsg"}

def tempconv(unit):     #the library is a little iffy on names
    c = ['c', 'celc', 'celsius']
    f = ['f', 'far', 'fahrenheit']
    k = ['k', 'kel', 'kelvin']
    r = ['r', 'rank', 'rankine']

    unit = unit.lower()

    if unit in c:
        return 'degC'

    elif unit in f:
        return 'degF'

    elif unit in k:
        return 'degK'

    elif unit in r:
        return 'degR'

    else:
        return unit

def prettytemp(unit, num):

    if unit == 'degC':
        return 'C'

    elif unit == 'degF':
        return 'F'

    elif unit == 'degK':
        return 'K'

    elif unit == 'degR':
        return 'R'

    elif unit == 'foot':
        return 'feet'

    else:
        if num == 1:
            return unit
        else:
            return unit + 's'

def stringparse(text): #it took me 15 mintues to write a better string parser than bym took a week
    text_list = text.split()

    if len(text_list) < 1:  #18F is the smallest I can think of
        return False, False, False

    unit2 = text_list[len(text_list) - 1] #it's implied the last string is always going to be the conversion
                                      #thus, '2 cm wooooo 2k16 wooooo in' would still work

    if text_list[0].replace('.', '').isdigit(): #2 cm (decimal workaround)
        num = text_list[0]
        unit1 = text_list[1]

    elif text_list[0].isalpha(): # ^c kg lbs
        num = 1
        unit1 = text_list[0]

    else:   #2c/2cm/etc
        num = ''
        unit1 = ''

        for i in text_list[0]:
            if i.isdigit():
                num += i
            elif i.isalpha():
                unit1 += i
            elif i == '.': #decimal workaround
                num += i

    unit1 = tempconv(unit1) #fixing any naming issues
    unit2 = tempconv(unit2)

    if len(text_list) <= 2 and unit1.startswith('deg'): #support single item conversions for temp
        if unit1 == 'degF': #We can safely assume this is either 18f or 18 f
            unit2 = 'degC'

        elif unit1 == 'degC':
            unit2 = 'degF'

    return unit1, float(num), unit2


def callback(self): #remove_bym
    try:
        unit1, num, unit2 = stringparse(self.message.split(' ', 1)[1])
    except:
        return self.msg(self.msg, 'You have to actually add things after the command')

    if unit1 == False:
        return self.msg(self.channel, "Error, it doesn't look like you're trying to convert properly")

    try:
        num, unit2 = '{0}'.format(convert(num, unit(unit1)).to(unit2)).split() #dirty, but it works perfectly

        num = str(round(float(num), 3)).replace('.0', '') #fix 123.0 bug
        unit2 = prettytemp(unit2, float(num))                                               #things bym can't say ^

    except Exception as e:
        return self.msg(self.channel, 'Conversion error! (%s)' % (e))

    return self.msg(self.channel, "%s %s" % (num, unit2))


class api: #You're now known as remove_bym
    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

if __name__ == "__main__":
    api = api()
    setattr(api, 'isop', True)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'convert')
    setattr(api, 'channel', "#test")
    setattr(api, 'user', 'joe!username@hostmask')

    setattr(api, 'message', '^convert 18.5 cm in')
    if not 'inchs' in callback(api):
        exit(1)

    setattr(api, 'message', '^convert 5 cm to mm')
    if '.0' in callback(api):
        exit(2)

    setattr(api, 'message', '^convert kg lbs')
    if not 'pounds' in callback(api):
        exit(3)

    setattr(api, 'message', '^c 18f')
    if not 'C' in callback(api):
        exit(4)
