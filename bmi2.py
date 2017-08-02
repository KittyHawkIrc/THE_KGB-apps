# -*- coding: utf-8 -*-

from pint import UnitRegistry

ureg = UnitRegistry()
ureg.define('bmi = kilogram / meter **2')

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 2.0

# declare() sets the strings that trigger this module.
# declare: None -> Dict{Str: Str}
def declare():
    declares = ['bmi', 'weight', 'mass', 'height', 'setbmi']
    return {command: 'privmsg' for command in declares}

def callback(self):
    channel = self.channel
    command = self.command.lower()
    user = self.user.split('!')[0]
    msg = self.msg
    isop = self.isop
    message = self.message.split(command, 1)[1].strip()
    words = message.split()

    try:
        mass, height, bmi = parse_input(message)
    except AttributeError:
        pass

    if mass and height and bmi:
        if command == 'setbmi' and len(words) > 0:
            set_other = not message[0].isdigit() and isop
            set_self = bool(message[0].isdigit() and bmi.magnitude < 25)

            if set_other or set_self:
                if set_other:
                    user = words[0]
                try:
                    self.locker.bmi2[user.lower()] = (mass, height)
                except:
                    self.locker.bmi2 = {user.lower(): (mass, height)}

                self.cache_save()

                output = 'BMI for user [{u}] set to {b:.4g~P} / {b_c}'
            elif set_self:
                output = 'BMI [{b:.4g~P}] out of range settable by [{u}]'
            else:
                output = 'BMI for user [{w[0]}] cannot be set by user [{u}]'
        else:
            output = '{m:.4g~P} / {h:.4g~P} / {b:.4g~P} / {b_c}'
    elif mass or height or bmi or command == 'setbmi':
        output = 'Insufficient input given for {c}'
    else:
        if len(message) > 0:
            user = words[0]
        try:
            mass, height = self.locker.bmi2[user.lower()]
            if command == 'bmi':
                bmi = (mass / height ** 2).to(ureg.bmi)
                output = '{u} / {b:.4g~P} / {b_c}'
            elif command == 'height':
                output = '{u} / {h:.4g~P}'
            else:
                output = '{u} / {m:.4g~P}'
        except:
            if command == 'bmi':
                try:
                    bmi = self.locker.bmi[user.lower()] * ureg.bmi
                    output = '{u} / {b} / {b_c}'
                except:
                    output = 'BMI not found for user [{u}]'
            else:
                output = 'User [{u}] has not updated their info since migration to bmi2, try setting BMI again'

    if height and height.units == ureg.foot:
        output = output.replace('h:.4g~P', 'i_h')

    return msg(channel, output.format(w = words,   b = bmi,
                                      u = user,    m = mass,
                                      c = command, h = height,
                                      i_h = to_feet_inches(height),
                                      b_c = classify_bmi(bmi)))

# parse_input(message) takes string 'message' and attempts to extract and return
#   heights, masses, and BMIs from the string.
# parse_input: Str -> (Quantity None), (Quantity None), (Quantity None)
def parse_input(message):
    # replace ' and " with inch and feet before splitting message
    words = replace_foot_inch_symbol(message).split()

    # create variables
    heights = []
    masses = []
    bmi = None

    for i, word in enumerate(words):
        # only allow numbers to be processed
        if not word[0].isdigit():
            continue

        # allow for spaces between magnitudes and units by concatenating word
        #   with following word
        if is_float(word) and (i+1 < len(words) and not is_float(words[i+1])):
            word = ' '.join((word, words.pop(i+1)))

        # check for bmi values included
        if len(word) > 3 and is_float(word[:-3]) and word[-3:].lower() == 'bmi':
            bmi = float(word[:-3]) * (ureg.kg / ureg.m ** 2)
            continue

        # otherwise, check for quantities recognized by ureg
        quantity = ureg.Quantity(word)
        if is_quantity(quantity):
            if str(quantity.dimensionality) == '[length]':
                heights.append(quantity)
            elif str(quantity.dimensionality) == '[mass]':
                masses.append(quantity)

    # sum quantities recognized by ureg
    height = sum(heights)
    mass = sum(masses)

    # fill in missing quantity with maths
    if is_quantity(height) and is_quantity(mass):
        bmi = (mass / height ** 2).to(ureg.bmi)
    elif is_quantity(bmi) and is_quantity(height):
        mass = (bmi * height ** 2).to_base_units()
    elif is_quantity(bmi) and is_quantity(mass):
        height = ((mass / bmi) ** 0.5).to_base_units()
    else:
        return None, None, None

    # return tuple in order of mass, height (as mass/height^2=bmi)
    return mass, height, bmi

# classify_bmi(bmi) takes quantity 'bmi' and returns string for whether a bmi of
#   'bmi' is one of underweight, normal, obese, or overweight, with IRC control
#   codes to colour those results.
# classify_bmi: Quantity -> (Str None)
# requires: bmi.dimensionality == {'[length]': -2.0, '[mass]': 1.0}
def classify_bmi(bmi):
    try:
        if bmi.magnitude < 18.5:
            return '\002\00308underweight\017'
        if bmi.magnitude < 25.0:
            return '\002\00309normal\017'
        if bmi.magnitude < 30.0:
            return '\002\00307overweight\017'
        else:
            return '\002\00304obese\017'
    except:
        return None

# to_feet_inches(quantity) takes length 'quantity' and returns a tuple of the
#   length in feet and inches.
# to_feet_inches: Quantity -> (Str None)
# requires: quantity.dimensionality == {'[length]': 1.0}
def to_feet_inches(quantity):
    try:
        imperial_height_str = '{.magnitude:.0f}\'{.magnitude:.4g}"'
        feet = int(quantity.to(ureg.foot).magnitude) * ureg.foot
        inches = (quantity - feet).to(ureg.inch)
        return imperial_height_str.format(feet, inches)
    except:
        return None

# replace_foot_inch_symbol(string) takes string and replaces all instances of
#   quotation marks with their respective unit (foot or inch).
# replace_foot_inch_symbol: Str -> Str
def replace_foot_inch_symbol(string):
    foot_symbols = ["'", "‘", "’"]
    inch_symbols = ['"', '“', '”']

    for symbol in foot_symbols:
        string = string.replace(symbol, 'foot ')

    for symbol in inch_symbols:
        string = string.replace(symbol, 'inch ')

    return string

# is_imperial(quantity) returns whether 'quantity' is an imperial unit or not.
# is_imperial: Quantity -> Bool
def is_imperial(quantity):
    if (quantity.units in dir(ureg.sys.US) or
        quantity.units in dir(ureg.sys.imperial)):
        return True
    return False

# is_float(object_) takes any object 'object_' and returns a boolean for
#   whether it can be converted into a float
# is_float: Any -> Bool
def is_float(object_):
    try:
        float(object_)
        return True
    except:
        return False

# is_quantity(object_) takes any object 'object_' and returns a boolean for
#   whether it is of the type 'Quantity'
# is_quantity: Any -> Bool
def is_quantity(object_):
    return type(object_).__name__ == 'Quantity'

################################ START: Testing ################################
class api:
    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

class empty:
    pass

if __name__ == "__main__":

    api = api()
    declares = ['bmi', 'weight', 'mass', 'height', 'setbmi']
    setattr(api, 'cache_save', cache_save)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'channel', "#channel")
    setattr(api, 'locker', empty)
    setattr(api, 'user', 'nick!ident@host')
    setattr(api, 'isop', False)
########################## START: Interactive Testing ##########################
'''
    def cache_save():
        print 'Cache saved'
    while(True):
        _input = raw_input('Enter message here: ')
        input_split = _input.split()
        if input_split[0] == 'op':
            setattr(api, 'isop', True)
            print 'User opped'
            continue
        elif input_split[0] == 'deop':
            setattr(api, 'isop', False)
            print 'User deopped'
            continue
        elif input_split[0] == 'user' and len(input_split) > 1:
            setattr(api, 'user', input_split[1])
            print 'User changed to {}'.format(input_split[1])
            continue
        elif input_split[0] == 'quit':
            break
        elif len(_input) > 0 and input_split[0][1:] in declares:
            setattr(api, 'command', _input.split()[0][1:])
            setattr(api, 'message', _input)
            print callback(api)
            continue
'''
########################### END: Interactive Testing ###########################

################################# END: Testing #################################
