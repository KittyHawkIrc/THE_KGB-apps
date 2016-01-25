channels = {'#fatpeoplesuck' '#fathateelite'}
ignore = {self.nickname,'}o{','FatStats','justnotfair'}

def declare():
    return {"autovoice": "userjoin"}

def callback(self):
    if self.channel in channels and not in ignore:
        self.mode(channel ,True, 'v', mask=user)
