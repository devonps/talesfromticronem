
class Message:
    def __init__(self, text, msgclass='all', fg="black", bg="white", fnt=""):
        self.text = text
        self.msgclass = msgclass
        self.fg = fg
        self.bg = bg
        self.fnt = fnt


# this is a generic container for ALL messages produced in the game
class MessageLog:
    storedMessages = None

    def __init__(self, width, height, depth, display_from_message, display_to_message, visibleLog):
        self.storedMessages = []
        self.width = width
        self.height = height
        self.depth = depth
        self.display_from_message = display_from_message
        self.display_to_message = display_to_message
        self.visibleLog = visibleLog

