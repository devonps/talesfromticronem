
class Description:
    def __init__(self, text='undefined'):
        self.label = text


class Material:
    def __init__(self, texture='cloth'):
        self.texture = texture


class SlotSize:
    def __init__(self, maxsize=26, populated=0):
        self.maxsize = maxsize
        self.populated = populated


class Owner:
    def __init__(self, owner=0):
        self.owner = owner


class BagInInventory:
    pass


class BagBeingUsed:
    pass
