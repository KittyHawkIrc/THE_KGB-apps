#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 2.0


def declare():
    return {"overkill": "userjoin"}

def callback(self):
    if self.channel == '#fatpeoplesuck' and self.profile.isverified:
        self.mode(self.channel, True, 'v', user=self.profile.nickname)
