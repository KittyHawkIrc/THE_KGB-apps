include = {'cyracs', 'syracs', 'nwo-chan', 'marlow', 'marlzey', 'marlsey', 'rieldtok', 'sirius-cybernetics', 'hydrogen_cyanide', 'thorgin', 'derpydoom', 'doomclass', 'coup', 'coup_de_shitlord', 'bym', 'purpleisafruit', 'creative', 'creativenickname', 'madam_psycho_sexy', 'shitladyoftheskies', 'uvulectomy', 'moudi', 'meeblesmerble', '[deleted]'}

def declare():
    return {"overkill": "userjoin"}

def callback(self):

    if self.channel == '#fatpeoplesuck':
        u = self.user.lower.split('!',1)[0]
        if u in include:
            self.msg('ChanServ', 'voice %s %s' % (self.channel, u))
