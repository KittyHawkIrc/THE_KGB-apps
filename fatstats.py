def declare():
    return {"kickspam": "privmsg", "banspam": "privmsg", "unbanspam": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
    if command == 'kickspam':
        self.kick('#fatpeoplehate', 'FatStats')

    elif command == 'banspam':
        self.mode('#fatpeoplehate' ,True, 'b', mask='*!*@FPH.Statbot')

    elif command == 'unbanspam':
        self.mode('#fatpeoplehate' ,False, 'b', mask='*!*@FPH.Statbot')
