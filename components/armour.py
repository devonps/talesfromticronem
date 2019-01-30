
class Location:
    def __init__(self, text='undefined'):
        self.label = text


class LocationAKA:
    def __init__(self, text = ''):
        self.label = text


class Set:
    def __init__(self, label=''):
        self.label = label


class Quality:
    def __init__(self, label=''):
        self.label = label


class Weight:
    def __init__(self, label=''):
        self.label = label


class Defense:
    def __init__(self, value=0):
        self.value = value


class Describable:
    def __init__(self, prefix='', suffix='', location_aka='', level=0):
        self.prefix = prefix
        self.suffix = suffix
        self.location_aka = location_aka
        self.level = level


class AttributeBonus:
    def __init__(self, majorname='', majorbonus=0, minoronename='', minoronebonus=0, minortwoname='', minortwobonus=0):
        self.majorName = majorname
        self.majorBonus = majorbonus
        self.minorOneName = minoronename
        self.minorOneBonus = minoronebonus
        self.minorTwoName = minortwoname
        self.minorTwoBonus = minortwobonus
