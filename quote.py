# -*- coding: utf-8 -*-

import random

#Update schema
__url__ = 'https://raw.githubusercontent.com/KittyHawkIrc/modules/production/' + __name__ + '.py'
__version__ = 1.0

def declare():
    declares = ['q', 'quote', 'qa', 'quoteadd', 'qd', 'quotedel']
    return {command: 'privmsg' for command in declares}

def callback(self):
    channel = self.channel
    command = self.command.lower()
    user = self.user.split('!')[0]
    msg = self.msg
    message = self.message.split(command, 1)[1].strip()
    words = message.split()

    locker = self.locker
    dict_exists = hasattr(locker, 'quote')

    sep = ' / '
    author, index, quote, num_quotes = None, None, None, None

    if len(words) > 0 and is_nick(words[0]):
        author = words[0]

    if command in ['qa', 'quoteadd']:
        if len(words) > 1 and is_nick(author):
            quote = message[len(words[0]):].strip()

            if not dict_exists:
                locker.quote = {}
            if author not in locker.quote:
                locker.quote[author] = []

            quote_list = locker.quote[author]

            if quote not in quote_list:
                quote_list.append(quote)
                self.cache_save()   #persist cache post-restarts
                index = len(locker.quote[author])
                output = 'Quote "{q}" added as quote #{i} for user [{a}]'
            else:
                index = quote_list.index(quote) + 1
                output = 'Quote "{q}" exists as quote #{i} for user [{a}]'
        else:
            output = '{c}: <nick> <quote>'
    else:
        try:
            if command in ['qd', 'quotedel']:
                if not self.isowner:
                    output = 'Quotes can only be deleted by bot owners.'
                elif len(words) > 1 and author:
                    if words[1].lower() == 'all':
                        locker.quote[author] = []
                        output = 'Removed all quotes from user [{a}]'
                    elif is_float(words[1]):
                        locker.quote[author].pop(int(words[1]) - 1)
                        output = 'Removed quote #{i} from user [{a}]'
                    elif message[len(author):].strip() in\
                         locker.quote[author]:
                        quote = message[len(author):].strip()
                        index = locker.quote[author].index(quote)
                        locker.quote[author].pop(index)
                        index += 1
                        output = 'Removed quote #{i} from user [{a}]'
                    else:
                        output = '{c}: <nick> <quote>'
                elif len(words) > 0 and words[0].lower() == 'all':
                    locker.quote = {}
                    output = 'Removed all quotes.'
                else:
                    output = '{c}: <nick> <quote>'
            elif command in ['q', 'quote']:
                if not author:
                    author = random.choice(key_equal_weight(locker.quote))

                quote_list = locker.quote[author]
                num_quotes = len(quote_list)

                if len(words) > 1 and is_float(words[1]):
                    index = int(words[1]) - 1
                else:
                    index = random.randrange(num_quotes)

                quote = quote_list[index]

                index += 1
                output  = '{a}{s}#{i} of {n}{s}"{q}"'
        except AttributeError:
            output = 'No quotes have been added yet.'
        except IndexError:
            output = 'Quote #{i} out of range, user [{a}] had {n} quotes.'
        except KeyError:
            output = 'No quotes stored for user [{a}]'

    return msg(channel, output.format(u = user, a = author, s = sep, q = quote,
                                      c = command, i = index, n = num_quotes))

# key_equal_weight(dict_of_list) takes a dict_of_list and returns a list of its
#   keys such that there a k for every item in dict_of_list[k]
# key_equal_weight: Dict(Any: List(Any)) -> List(Any)
def key_equal_weight(dict_of_list):
    keys = []
    for key, value in dict_of_list.items():
        keys.extend([key] * len(value))
    return keys

# is_float(object_) takes any object 'object_' and returns a boolean for
#   whether it can be converted into a float
# is_float: Any -> Bool
def is_float(object_):
    try:
        float(object_)
        return True
    except:
        return False

# is_nick(string) takes 'string' and determines if it is a valid IRC nickname
# is_nick: Str -> Bool
# requires: isinstance(string, str)
def is_nick(string):
    for i, char in enumerate(string):
        if ((i > 0 and (char.isdigit() or char == '-')) or
            char.isalpha() or char in '_-\[]{}^`|'):
            continue
        else:
            return False
    return True

################################ START: Testing ################################
class api:
    def msg(self, channel, text):
        return '[%s] %s' % (channel, text)

class empty:
    pass

if __name__ == '__main__':
    def cache_save():
        print 'Cache saved'
    api = api()
    declares = declare().keys()
    setattr(api, 'cache_save', cache_save)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'channel', '#channel')
    setattr(api, 'locker', empty)
    setattr(api, 'user', 'nick!ident@host')
    setattr(api, 'isop', False)
    setattr(api, 'isowner', False)
###############nick########### START: Interactive Testing ##########################
'''
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
        elif input_split[0] == 'owner':
            setattr(api, 'isowner', True)
            setattr(api, 'isop', True)87706b9652a1e7bfd6f682d11503c3fcfc7be756
            print 'User ownered'
            continue
        elif input_split[0] == 'deowner':
            setattr(api, 'isowner', False)
            print 'User deownered'
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
