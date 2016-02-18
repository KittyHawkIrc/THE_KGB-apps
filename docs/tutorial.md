# KittyHawk module tutorial

##Declaring hooks
All modules must declare hooks. A hook is a set of option(s) and cases that are added in to the runtime to expand the scope and functionality of KittyHawk.

First, start by creating the initial declare callback function. It returns a dict of hooks.

```
def declare():
    return {"hello": "privmsg"}
```

In this example the hook type **privmsg** is specified with the hook name **hello**. If we assume the command key (typically ^) is its default this means that KittyHawk will run the module only if `key + hook name` is called. In this case that would be `^hello`.

Not all hooks are commands, actions like `userjoin` and messages from syncs can also be used, where the hook name is usually the modules name.

### Other hook types

In a module where we wanted to auto-voice users when they join a channel we'd specify something like the following:

```
def declare():
    return {"autovoice": "userjoin"}
```

If we wanted to specify `userjoin` and a couple hooks, we can do this too.

```
def declare():
    return {"hello": "privmsg", "autojoin": "userjoin", "greet": "privmsg"}
```

## The callback

The real bread of the module is the callback function, this is executed every time the hook declared prior is called. These all start exactly the same:

```
def callback(self):
```
The self object is documented in the [API documentation](api.md).

Now that we've got our `hello` hook added, let's first check the users permissions before moving forward so we know what to say next.

```
if self.isowner:
    user_type = 'owner'
    
elif self.isop:
    user_type = 'operator'
    
else:
    user_type = 'user'
```
Here we're setting the value of the `user_type` string based on permissions, noting that while `self.isop` is true for owners, `self.isowner` being first causes the if statement to finish.

### Showing the user

Next we just need to print our finished string to the channel, so just toss in an extra line:

```
self.msg(self.channel, "And a hello to you too, %s %s!" % (user_type, self.user))
```

If you have the [API documentation](api.md) open this line should be pretty self-explanatory.

### The finished code
 
 By now you should have a fully working and completed `^hello` hook and module all ready to add. This should look like the following:
 
 ```
def declare():
    return {"hello": "privmsg"}
    
def callback(self):
	if self.isowner:
	    user_type = 'owner'
	    
	elif self.isop:
	    user_type = 'operator'
	    
	else:
	    user_type = 'user'
	    
	self.msg(self.channel, "And a hello to you too, %s %s!" % (user_type, self.user))
 ```


## Executing code on load

Code written out of functions is executed only once on the first `mod_load`, but can be accessed by functions later. Note that `mod_load` or restarting would totally reset anything stored.

 ```
 api_key = getapikey()
 
def declare():
    return {"translate": "privmsg"}
    
def callback(self):
    text = self.message.split(' ', 1)[1]
	self.msg(self.channel, translate(api_key, text))  
 ```
 
 Note that while the `translate` and `getapikey()` functions are made up. Also note that text is the data after the ^translate part in `^translate wie heisst du`.