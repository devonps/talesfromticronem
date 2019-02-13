import tcod
import textwrap
from newGame import constants


class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages =[]
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # split the lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]
            # Add the new line as a Message object, with the text and the color
            revised_msg = f'{line: <{constants.MSG_PANEL_MESSAGE_LENGTH}}'
            self.messages.append(Message(revised_msg, message.color))