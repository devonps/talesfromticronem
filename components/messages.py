
class Message:
    def __init__(self, text, msgclass='all', fg="black", bg="white", fnt=""):
        self.text = text
        self.msgclass = msgclass
        self.fg = fg
        self.bg = bg
        self.fnt = fnt


# this is a generic container for ALL messages produced in the game
class MessageLog:
    stored_messages = None
    stored_log_messages = None

    def __init__(self, width, height, depth, display_from_message, display_to_message, visible_log=0):
        self.stored_messages = []
        self.stored_log_messages = []
        self.width = width
        self.height = height
        self.depth = depth
        self.display_from_message = display_from_message
        self.display_to_message = display_to_message
        self.visible_log = visible_log

