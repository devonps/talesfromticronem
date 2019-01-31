

class Type:
    def __init__(self, label=''):
        self.label = label


class Material:
    def __init__(self, label=''):
        self.label = label


class Describable:
    # component1 is the main thing for the piece of jewellery, e.g. a hook for an earring
    # component2 is the setting that holds the jewel
    # component3 is the jewel
    def __init__(self, component1='', component2='', component3=''):
        self.component1 = component1
        self.component2 = component2
        self.component3 = component3


class ImprovementTo:
    def __init__(self,stat1name='', stat1bonus=0, stat2name='', stat2bonus=0, stat3name='', stat3bonus=0):
        self.stat1name = stat1name
        self.stat1bonus = stat1bonus
        self.stat2name = stat2name
        self.stat2bonus = stat2bonus
        self.stat3name = stat3name
        self.stat3bonus = stat3bonus


class Equipped:
    def __init__(self, isequipped=False):
        self.label = isequipped
