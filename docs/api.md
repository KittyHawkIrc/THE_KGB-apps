# API Reference

The Arsenic superclass provides a fairly large number of functions and variables to make designing modules easy. Note that all things mentioned here must start with `self.`

## Variables

These are traditional variables passed by Arsenic, many of them started out as arguments in the early API.


### isop
This is a boolian indicating if the user of the command is an operator or not.

```
if self.isop:
	do something
```
***
### isowner
This is a boolian indicating if the user of the command is an owner or not, when this is true isop is always true.

```
if self.isowner:
	do something
```
***
### type
This is a string declaring the type of hook used to activate the callback, this is one of the following:

* privmsg
* userjoin

```
if self.type == 'privmsg':
	do something
```
***
### command
This is a string which contains the name of the actual `^command` passed to activate it. Note that it will never include the key character. (defaults to ^)

```
if self.command == 'hello':
    do something
```
***
### message
This is a string containing the full message including the hook.

```
print self.message
>>> ^echo I am a bot
print self.command
>>> echo
print self.message.split(self.command, 1)[1]
>>> I am a bot
```
***
### user
This is the full hostmask of the user calling the command, it goes in `nickname!username@hostname` order.

```
print self.user
>>> joe!rocks@isp.com
name = self.user.split('!',1)[0]
print 'Hello, !' % (name)
>>> Hello, Joe!
```
***
### channel
This the a string of the channel the modules being called from, please be aware that when the bot is messaged the channel is `self.nickname` and not `self.user`. **Failure to follow this can cause infinite loops!**

```
if self.channel.startswith('#'):
	self.msg(self.channel, 'we are in a channel!')
else:
	name = self.user.split('!',1)[0]
	self.msg(name, 'We are messaging!')

```
***
### ver
Typically only used for supporting specific API versions, returns a string.

```
print self.ver
>>> '1.0.0'
```
***
### nickname
This is the bots own nickname, useful for ignoring itself.

```
print self.nickname
>>> 'supercoolbot107'
```
***
## Functions

### msg(channel, message)
This function sends the message to the specified channel, silently failing if the channel isn't joined.

```
self.msg(self.channel, 'Hi guys!')
```
***
### me(channel, message)
This function is just like msg but performs an action like /me would.

```
self.me(self.channel, 'dances')
```
***
### notice(channel, message)
This function sends a notice, sorta like using /notice.

```
self.notice(self.channel, 'I want to piss people off with alerts.')
```
***
### away(optional=message)
This sets the bot as away.

```
self.away('brb!')
```
***
### back()
This sets marks the bot as returned.

```
self.back()
```
***
### join(channel, optional=key)
Joins a channel, providing a key if needed.

```
self.join('#secret-test-channel')
self.msg('#secret-test-channel', 'Hey friends!')
```
***
### leave(channel, optional=reason)
Normally parts from a channel optionally stating why in the message.

```
self.leave('secret-test-channel', 'Too secret for me tbh')
```
***
### kick(channel, user, optional=reason)
Attempts to kick a user from a channel with an optional reason, fails silently if this does not work.

```
self.kick('#top-secret-channel', annoying_troll, 'Trolling')
```
***
### topic(channel, optional=topic)
Sets the topic of the channel, when no topic is passed it blanks it out. Note that this also silently fails.

```
self.topic('#secret-room', 'Welcome to the secret!')
```
***
### mode(channel, set, modes, optional=user, optional=limit)
This sets the mode of a channel to the letters passed to modes. `set` is a boolian that controls if the mode should be enabled on or off. Limit is used for flags like +l that limit the number of users. User is who to apply the flag to.

```
self.msg(self.channel, True, 'o', user='alan')
>>> the_kgb sets mode +o on alan
```
***
### setNick(nickname)
Attempts to set the bots nickname to this, note that it will silently fail without feedback if taken so please check self.nickname.

```
while self.nickname != 'admin':
	self.setNick('admin')

```
***
## persistent storage

### store
Store is a system for sharing data between modules with minimal external work. All data stored in it is 100% public to all other modules.

To store and read data simply add a new attribute and set a value, it can then be accessed anywhere else during the life of the program.

*Module a*:

```
self.store.counter = 0
self.store.oldvalue = 3
```

*Module b*:

```
value = self.store.oldvalue
print value
>>> 3
self.store.counter += 1
self.store.newvalue = value + 1
```

*Module a*:

```
print self.store.counter
>>> 1
print self.store.newvalue
>>> 4
print value
>>> NameError: name 'value' is not defined
```

***
### locker
Lockers expand on the concept of store while removing the shared aspect, letting us use scope to create per-module stores, much like lockers. This is handy when you're worried about modules naming persisting variables the same thing or want to protect data from other modules.

*Module a*:

```
self.store.value = 1
self.locker.value = 2
```

*Module b*:

```
print self.store.value
>>> 1
print self.locker.value
>>> persist instance has no attribute 'value'
self.store.value = 5
self.locker.value = 6
```

*Module a*:

```
print self.store.value
>>> 5
print self.locker.value
>>> 2
```

## Configuration settings
The long term configuration system allows you to store data like API keys and passwords in an isolated scope helping prevent issues like people storing billable API keys directly in a modules source code.

Operators: please run help_config to manage data outside of modules.

***
### config_set(item, value)
Stores data to the config file.

```
self.config_set('api_key', '123456')
```
***
### config_get(item, default=False)
Fetches a value from a config item. Returns optional default if not found, or False otherwise.

```
self.config_get('api_key')
>>> 123456
```
***
### config_remove(item, value)
Removes an item, returns False if it doesn't exist.

```
self.config_remove('api_key')
>>> True

self.config_remove('fake_item')
>>> False
```
