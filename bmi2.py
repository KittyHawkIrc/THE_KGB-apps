# Pastebin JI5ugwWt
# -*- coding: utf-8 -*-

from pint import UnitRegistry
from arsenic_helper import *

ureg = UnitRegistry()
ureg.define('bmi = kilogram / meter ** 2')

units = ['ca', 'uk2', 'us', 'si']

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 2.1

# declare() sets the strings that trigger this module.
# declare: None -> Dict{Str: Str}
def declare():
    declares = ['bmi', 'weight', 'mass', 'height', 'setbmi']
    return {command: 'privmsg' for command in declares}

def callback(self):
    message = replace_smartquote(self.message.split(self.command, 1)[1]).strip()
    words = message.split()

    username = self.profile.username

    try:
        weight, height, bmi = parse_input(words)
    except AttributeError:
        weight, height, bmi = None, None, None

    if self.command == 'setbmi':
        if bmi:
            if self.profile.isop or (30 > bmi.magnitude > 16):
                if self.profileManager.getuser_bynick(words[0]):
                    username = self.profileManager.getuser_bynick(words[0]).username
                elif self.profileManager.getuser_byname(words[0]):
                    username = self.profileManager.getuser_byname(words[0]).username

                self.profileManager.update(username,
                                           height=height.to(ureg.m).magnitude,
                                           weight=weight.to(ureg.kg).magnitude)
                output = 'BMI for user [{u}] set to {b:.4g~P} / {b_c}'
            elif not (self.profileManager.getuser_bynick(words[0]) or
                      self.profileManager.getuser_byname(words[0])):
                output = 'BMI "{b:.4g~P}" out of range settable by [{u}]'
            else:
                output = 'BMI for user [{w[0]}] cannot be set by user [{u}]'
        else:
            output = '{u}: ^setbmi <magnitude> <unit>...'

    elif self.command in ['bmi', 'weight', 'mass', 'height']:
        try:
            if self.profile.unit:
                unit = self.profile.unit

            for i in units:
                if i in words:
                    unit = i

            if len(message) == 0:
                profile = self.profile
            elif self.profileManager.getuser_byname(words[0]):
                profile = self.profileManager.getuser_byname(words[0])
            elif self.profileManager.getuser_bynick(words[0]):
                profile = self.profileManager.getuser_bynick(words[0])

            try:
                if profile:
                    username = profile.username
                    height = profile.height * ureg.m
                    weight = profile.weight * ureg.kg
                    bmi = (weight / height ** 2).to(ureg.bmi)
            except:
                pass

            if unit == 'us':
                weight = weight.to(ureg.lb)

            output = '{u} / {m:.4g~P} / {h:.4g~P} / {b:.4g~P} / {b_c}'
        except:
            if len(message) == 0:
                output = '{u}: ^setbmi <magnitude> <unit>...'
            elif profile:
                output = 'User [{u}] has no BMI set'
            else:
                output = '{c}: <none> | <nick> | <name> | <magnitude> <unit>...'

        if unit == 'us':
            output = output.replace('h:.4g~P', 'i_h')

    return self.msg(self.channel, output.format(w = words,  u = username,
                                                b = bmi, m = weight, h = height,
                                                c = self.command,
                                                i_h = to_feet_inches(height),
                                                b_c = classify_bmi(bmi)))

# parse_input(words) takes string 'message' and attempts to extract and return
#   heights, weights, and BMIs from the string.
# parse_input: Listof(Str) -> (Quantity None), (Quantity None), (Quantity None)
def parse_input(words):
    # create variables
    heights = []
    weights = []
    bmi = None

    for i, word in enumerate(words):
        # only allow numbers to be processed
        if not word[0].isdigit():
            continue

        # allow for spaces between magnitudes and units by concatenating word
        #   with following word
        if is_float(word) and (i+1 < len(words) and not is_float(words[i+1])):
            word = ' '.join((word, words.pop(i+1)))

        # otherwise, check for quantities recognized by ureg
        quantity = ureg.Quantity(word)
        if is_quantity(quantity):
            if str(quantity.dimensionality) == '[length]':
                heights.append(quantity)
            elif str(quantity.dimensionality) == '[mass]':
                weights.append(quantity)
            elif str(quantity.dimensionality) == '[mass] / [length] ** 2':
                bmi = quantity

    # sum quantities recognized by ureg
    height = sum(heights)
    weight = sum(weights)

    # fill in missing quantity with maths
    if is_quantity(height) and is_quantity(weight):
        bmi = (weight / height ** 2).to(ureg.bmi)
    elif is_quantity(bmi) and is_quantity(height):
        weight = (bmi * height ** 2).to(ureg.kg)
    elif is_quantity(bmi) and is_quantity(weight):
        height = ((weight / bmi) ** 0.5).to(ureg.m)

    # return tuple in order of weight, height (as weight/height^2=bmi)
    return weight, height, bmi

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

# replace_smartquote(string) takes string and replaces all instances of
#   quotation marks with their respective unit (foot or inch).
# replace_smartquote: Str -> Str
def replace_smartquote(string):
    foot_symbols = ["'", "‘", "’"]
    inch_symbols = ['"', '“', '”']

    for symbol in foot_symbols:
        string = string.replace(symbol, 'foot ')

    for symbol in inch_symbols:
        string = string.replace(symbol, 'inch ')

    return string

# is_quantity(object_) takes any object 'object_' and returns a boolean for
#   whether it is of the type 'Quantity'
# is_quantity: Any -> Bool
def is_quantity(object_):
    return type(object_).__name__ == 'Quantity'

def is_float(string):
    try:
        float(string)
        return True
    except:
        return False

'''
#####################################TEST#######################################
class api:
    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

class profile:
    pass

if __name__ == "__main__":
    api = api()
    profile = profile()

    setattr(profile, 'username', 'user')
    setattr(profile, 'nickname', 'nick')
    setattr(profile, 'ident', 'ident')
    setattr(profile, 'hostname', '@host.name')
    setattr(profile, 'userhost', 'nick!ident@host.name')
    setattr(profile, 'lat', 0)
    setattr(profile, 'lon', 0)
    setattr(profile, 'unit', 'us')
    setattr(profile, 'gender', 1)
    setattr(profile, 'height', 1.85)
    setattr(profile, 'weight', 75)
    setattr(profile, 'privacy', False)
    setattr(profile, 'isverified', True)
    setattr(profile, 'isop', True)
    setattr(profile, 'trusted', True)

    setattr(api, 'isop', profile.isop)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'hello')
    setattr(api, 'message', '^hello')
    setattr(api, 'user', profile.userhost)
    setattr(api, 'channel', '#test')
    setattr(api, 'profile', profile)

    while(True):
        message = raw_input('Enter message here: ')
        if message[0] == '^':
            setattr(api, 'command', message.split()[0][1:])
        setattr(api, 'message', message)
        print callback(api)

###################################END TEST#####################################
'''
