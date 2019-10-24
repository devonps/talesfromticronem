
from bearlibterminal import terminal


def handle_game_keys():
    action = ''
    myevent = ''

    key = terminal.read()
    if key == terminal.TK_ESCAPE:
        myevent = 'keypress'
        action = 'quit'
    if key == terminal.TK_UP:
        myevent = 'keypress'
        action = 'up'
    if key == terminal.TK_DOWN:
        myevent = 'keypress'
        action = 'down'
    if key == terminal.TK_ENTER:
        myevent = 'keypress'
        action = 'enter'
    if key == terminal.TK_MOUSE_MOVE:
        myevent = 'mousemove'
        action = (terminal.TK_MOUSE_X, terminal.TK_MOUSE_Y)
    if key == terminal.TK_MOUSE_LEFT:
        myevent = 'mouseleftbutton'
        action = (terminal.TK_MOUSE_X, terminal.TK_MOUSE_Y)
    if key == terminal.TK_MOUSE_RIGHT:
        myevent = 'mouserightbutton'
        action = (terminal.TK_MOUSE_X, terminal.TK_MOUSE_Y)

    return myevent, action
