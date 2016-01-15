# the_kgb (arsenic) module documentation

## Why write modules?

Typically commands are a simple key/value system, where you pass a command and it responds with whatever value is required. If you want to have dynamically changing text for something like a converter or translator you'll be required to write one.


## Adding modules

Before we focus on writing modules, let's first learn how to add modules.

First verify you're an owner by running the command ``^hello`` in any channel he's in, he should respond by greeting you with the word owner in the reply. If this is not the case you will be unable to load modules.

Now that you know you're an owner, message it the following data: ``mod_inject [module] [url]``

Do not add brackets, the module name is the `whatever.py` without the `.py` part. The URL is a raw link to the source of the module.

Now that the modules installed it has to be loaded to be processed. to do this run the following: ``mod_load [module]``.

### Tips:
* The module name is normally the file.py but without the file extension.
* Do not include the brackets.
* The URL **must** be a direct link to the file, and not a file host or pastebin.

## What's an owner or operator? 
**Operators**: Operators are the traditional bot controller, they have access to most basic commands like adding or removing traditional commands and changing topics.

**Owners**: Written in the config file, owners can't be modified during runtime and have permissions in the event of a loss of the database. This special user has permissions over features that could break or alter the bot itself. Things like loading modules, runtime patching, and loading modules requires permission from an owner.