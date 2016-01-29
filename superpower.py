spdb =  {
        "creative":"turning everything into corn",
        "marlow":"creating buncy balls and quicksand",
        "terriblefuhrer":"controlling the trees",
        "ruston":"controlling squirrels",
        "redubious":"turning inorganic matter into glass",
        "homersimpson":"shooting Christmas lights out of his wrists like spiderman",
        "rieldtok":"instantly giving anyone an orgasm",
        "gyst":"making any liquid into bubbles",
        "uvulectomy":"having superpowered sneezes",
        "marvin":"having the power of conversation",
        "[deleted]":"turning into gas powered vehicles",
        "justnotfair":"turning plants into weapons, and is also not black",
        "moudi":"turning into rocks",
        "dr_durex":"controlling paper",
        "nwo-chan":"boiling liquid instantly",
        "billdred":"just flying. That's it.",
        "madam_psycho_sexy":"yarn bombing things",
        "fphrefugee":"shooting icicles out of her eyes",
        "coup_de_shitlord":"being a cyborg with a hot dog cannon arm",
        "skruff":"instantly predicting the outcome of sports games!",
        "purpleisafruit":"throwing fruit at anyone and it would explode like a grenade!"
    }

def declare():
    return {"superpower": "privmsg"}

def callback(self):
    if self.channel.startswith('#'):
        var = self.message.split()

        if var[1] == "help":
            return self.msg(self.channel,"^superpower username")
            

        try:
            return self.msg(self.channel,"%s's superpower is %s" % (var[1], spdb[var[1].lower()]))
            
        except:
            return self.msg(self.channel,"%s's not on the list" % (var[1]))
           

class api:
        def msg(self, channel, text):
            return "[%s] %s" % (channel, text)

if __name__ == "__main__":
        api = api()
        u = "joe!username@hostmask"
        c = '#test'

        setattr(api, 'isop', True)
        setattr(api, 'type', 'privmsg')
        setattr(api, 'command', 'superpower')
        setattr(api, 'message', '^superpower Moudi')
        setattr(api, 'user', 'joe!username@hostmask')
        setattr(api, 'channel', '#test')

        #if callback(api) != "[%s] Moudi's superpower is turning into rocks" % (c):
        #       exit(1)
