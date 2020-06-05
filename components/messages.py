
class Message:
    def __init__(self, text, msgclass=0, fg="black", bg="white", fnt=""):
        self.text = text
        self.msgclass = msgclass
        self.fg = fg
        self.bg = bg
        self.fnt = fnt


# this is a generic container for ALL messages produced in the game
class MessageLog:
    stored_messages = None
    stored_log_messages = None

    def __init__(self, visible_log):
        self.stored_messages = []
        self.stored_log_messages = []
        self.display_from_message = 0
        self.display_to_message = 9
        self.visible_log = visible_log
        self.log_id = 0

