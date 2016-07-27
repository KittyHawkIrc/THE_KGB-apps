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
    return {"convert":"privmsg", "fuckbym":"privmsg"}

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

def prettytemp(unit):

    if unit == 'degC':
        return 'celsius'

    elif unit == 'degF':
        return 'fahrenheit'

    elif unit == 'degK':
        return 'kelvin'

    elif unit == 'degR':
        return 'rankine'

    else:
        return unit

def stringparse(text): #it took me 15 mintues to write a better string parser than bym took a week
    text_list = text.split()

    if len(text_list) < 2:  #2c f is the smallest I can think of
        return False, False, False

    unit2 = text_list[len(text_list) - 1] #it's implied the last string is always going to be the conversion
                                      #thus, '2 cm wooooo 2k16 wooooo in' would still work

    if text_list[0].isdigit(): #2 cm
        num = text_list[0]
        unit1 = text_list[1]

    else:   #2c/2cm/etc
        num = ''
        unit1 = ''

        for i in text_list[0]:
            if i.isdigit():
                num += i
            elif i.isalpha():
                unit1 += i

    unit1 = tempconv(unit1) #fixing any naming issues
    unit2 = tempconv(unit2)

    return unit1, int(num), unit2


def callback(self): #remove_bym
    unit1, num, unit2 = stringparse(self.message.split(' ', 1)[1])

    if unit1 == False:
        return self.msg(self.channel, "Error, it doesn't look like you're trying to convert properly")

    try:
        num, unit2 = '{0}'.format(convert(num, unit(unit1)).to(unit2)).split() #dirty, but it works perfectly
        unit2 = prettytemp(unit2)                                               #things bym can't say ^
        num = round(float(num), 3)

    except:
        return self.msg(self.channel, 'Conversion error!')

    return self.msg(self.channel, "%s %s(s)" % (num, unit2))


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
    setattr(api, 'message', '^convert 18cm in')

    if not 'inch' in callback(api):
        exit(1)

    setattr(api, 'message', '^convert 18 cm to in')
    if not 'inch' in callback(api):
        exit(2)

    setattr(api, 'message', '^convert 18 cm in')
    if not 'inch' in callback(api):
        exit(3)

    setattr(api, 'message', '^convert 18cm in in')
    if not 'inch' in callback(api):
        exit(4)
