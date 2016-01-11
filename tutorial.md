# Module tutorial

Modules are bits of python code loaded by THE_KGB during runtime that provide features in the form of ^ commands and on user joins.

This is done by adding hooks in to THE_KGB's runtime for commands and actions declared in a callback function in the module. 

## Why write modules?

Typically commands are a simple key/value system, where you pass a command and it responds with whatever value is required. If you want to have dynamically changing text for something like a converter or translator you'd be required to write one.


## Adding modules

Before we focus on writing modules, let's first learn how to add modules.

First verify you're an operator by running the command ``^hello`` in any channel he's in, he should respond by greeting you with the word operator in the reply. If this is not the case you will be unable to load modules.

Now that you know you're an operator, message it the following data: ``mod_inject [module] [url]``

Do not add brackets, the module name is the `whatever.py` without the `.py` part. The URL is a raw link to the source of the module.

Now that the modules installed it has to be loaded to be processed. to do this run the following: ``mod_load [module]`` following the same rule as above.

## Writing the actual module

A module is composed of 2 required callback functions where anything else is optional. Things added not in the functions themselves will persist every call.

### The declare function
The declare function is only called once on `mod_load` to create all the initial hooks, it typically looks as follows: 

```
def declare():
	return {"hello": "privmsg"}
```

This function accepts no arguments, returning a dict of all options and hooks. The left side is the command to hook in to, the right is the type of hook. 

**DO NOT USE A ^ IN THE DECLARE**

The following hook types are accepted:

* privmsg
* userjoin


### The callback function

The callback function is called whenever the hook is activated, with quite a few arguments passed. 

The function typically looks like:

```
def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):

    if channel.startswith('#'):

        if isop:
            self.msg(channel, "And a hello to you too, operator %s!" % (user))
        else:
            self.msg(channel, "And a hello to you too, %s!" % (user))
```

The arguments are:

* self
* type
* isop
* command
* msg
* user
* channel
* mode


#### self
This argument is a twistedirc class that provides you access to functions listed on [this page](http://twistedmatrix.com/documents/8.1.0/api/twisted.words.protocols.irc.IRCClient.html), it typically serves as the only way you'll perform any actions during the runtime of your module.

It typcally looks like: `self.msg(user, 'Hello!')`

#### type

This argument returns a string of the type of hook called, like ``privmsg``.

#### isop

This is a boolian argument that tells us if the user has permissions as an operator, its usage is shown in the example for this function.

#### command

This is typically the `^command` ran that activated the callback, it does not include a ^.

#### msg 

This is the raw message sent when the command was called, fully including the ^.

#### user

This is the user who activated the hook, it's in full `nick!username@hostmask` format. Note that many commands in self require just the nick so be sure to `user.split('!')[0]` to fetch it.

#### channel 

This is the channel the command was ran in, keep in mind that if it was messaged the channel is THE_KGB's current nickname so if you try to `self.msg(channel, 'text')` you will cause a loop.

#### mode 

The mode set, odds are this will never be set.
