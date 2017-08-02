from pint import UnitRegistry

ureg = UnitRegistry()

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 2.0

def declare():
    declares = ['bmi', 'weight', 'mass', 'height', 'setbmi']
    return {command: 'privmsg' for command in declares}

def callback(self):
    channel = self.channel
    command = self.command.lower()
    user = self.user.split('!')[0].lower()
    msg = self.msg
    isop = self.isop
    message = self.message.split(command, 1)[1].strip()
    words = message.split()

    try:
        mass, height, bmi = parse_input(message)
        mass_round = format(mass.magnitude, '.2f')
        height_round = format(height.magnitude, '.2f')
        bmi_round = format(bmi, '.2f')
        bmi_class = classify_bmi(bmi)
    except AttributeError:
        pass
    except Exception as e:
        print 'Exception: {}'.format(e)

    if command == 'setbmi':
        if not message[0].isdigit():
            if isop:
                user = message.split()[0]
            else:
                return msg(channel, 'BMI for user [{}] cannot be set by user [{}]'.format(message.split()[0], user))

        if isop or (bmi < 25 and bmi > 15):
            try:
                self.locker.bmi[user.lower()] = bmi
            except:
                self.locker.bmi = {user.lower(): bmi}

            self.cache_save()

            return msg(channel, 'BMI for user [{}] set to {} / {}'.format(user, bmi_round, bmi_class)) 
        else:
            return msg(channel, 'BMI out of range settable by [{}]'.format(user))

    else:
        if bmi:
            mass_string = '{}{:~P}'.format(mass_round, mass.units)
            height_string = '{}{:~P}'.format(height_round, height.units)
            bmi_string = '{}bmi'.format(bmi_round)

            output = [mass_string, height_string, bmi_string, bmi_class]
            
            return msg(channel, ' / '.join(output))

        if len(message) > 0:
            user = message.split()[0]
        try:
            bmi = self.locker.bmi[user.lower()]
            bmi_round = format(bmi, '.2f')
            bmi_class = classify_bmi(bmi)
            return msg(channel, '{} / {}bmi / {}'.format(user, bmi_round, bmi_class))
        except:
            return msg(channel, 'BMI not found for user [{}]'.format(user))
        

def parse_input(message):
    words = message.replace('"','inch ').replace("'",'foot ').split()
    
    heights = []
    masses = []
    bmi = None

    for i, word in enumerate(words):
        if not word[0].isdigit():
            continue
        
        if is_float(word) and (i + 1 < len(words) and not is_float(words[i + 1])):
            word = word + message_split.pop(i+1)

        if len(word) > 3 and is_float(word[:-3]) and word[-3:].lower() == 'bmi':
            bmi = float(word[:-3]) * (ureg.kg / ureg.m ** 2)
            continue

        quantity = ureg(word)
        if is_quantity(quantity):
            if str(quantity.dimensionality) == '[length]':
                heights.append(quantity)
            elif str(quantity.dimensionality) == '[mass]':
                masses.append(quantity)

    height = sum(heights)
    mass = sum(masses)

    valid = True

    if is_quantity(height) and is_quantity(mass):
        bmi = (mass / height ** 2).to(ureg.kg / ureg.m ** 2)
    elif is_quantity(bmi) and is_quantity(height):
        mass = (bmi * height ** 2).to_base_units()
    elif is_quantity(bmi) and is_quantity(mass):
        height = ((mass / bmi) ** 0.5).to_base_units()
    else:
        valid = False

    if valid:
        return mass, height, bmi.magnitude
    else:
        return None, None, None

# classify_bmi(bmi) takes number 'bmi' and returns string for whether a bmi of
#   'bmi' is one of underweight, normal, obese, or overweight, with IRC control
#   codes to colour those results.
# classify_bmi: (Int, Float, Long, Complex) -> Str
# requires: type(bmi) in [int, float, long, complex]
def classify_bmi(bmi):
    if bmi < 18.5:
        return '\002\00308underweight\017'
    if bmi < 25.0:
        return '\002\00309normal\017'
    if bmi < 30.0:
        return '\002\00307overweight\017'
    else:
        return '\002\00304obese\017'

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


##################################### TEST #####################################
class api:
    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

class empty:
    pass

if __name__ == "__main__":
    def cache_save():
        print 'Cache saved'

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
            for declare in declares:
                if declare in _input:
                    setattr(api, 'command', declare)
            setattr(api, 'message', _input)
            print callback(api)
'''
########################### END: Interactive Testing ###########################
