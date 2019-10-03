from datetime import datetime


class DateTimeStamp:
    def __init__(self):
        self.dt = datetime.now().strftime('%d-%m-%Y')
        self.tm = datetime.now().time().strftime('%H:%M:%S')


class BuildName:
    def __init__(self):
        self.label = ''


class BuildRace:
    def __init__(self):
        self.label = ''


class BuildClass:
    def __init__(self):
        self.label = ''


class BuildJewellery:
    def __init__(self):
        self.label = ''


class BuildMainHand:
    def __init__(self):
        self.label = ''


class BuildOffHand:
    def __init__(self):
        self.label = ''


class BuildArmour:
    def __init__(self):
        self.label = ''


class BuildGender:
    def __init__(self):
        self.label = ''

