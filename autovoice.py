channels = {'#fatpeoplesuck' '#fathateelite'}

def declare():
    return {"autovoice": "userjoin"}

def callback(self):
    if self.channel in channels:
        self.mode(channel ,True, 'v', mask=user)
