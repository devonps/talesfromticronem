from bearlibterminal import terminal


def handle_game_keys():
    action = None
    myevent = None

    key = terminal.read()

    #
    # ENTITY SELECT KEYS
    #
    if key == terminal.TK_TAB:
        myevent = 'keypress'
        action = 'tab'
    #
    # SPELL BAR HOTKEYS
    #
    if key == terminal.TK_1:
        myevent = 'keypress'
        action = 1
    if key == terminal.TK_2:
        myevent = 'keypress'
        action = 2
    if key == terminal.TK_3:
        myevent = 'keypress'
        action = 3
    if key == terminal.TK_4:
        myevent = 'keypress'
        action = 4
    if key == terminal.TK_5:
        myevent = 'keypress'
        action = 5
    if key == terminal.TK_6:
        myevent = 'keypress'
        action = 6
    if key == terminal.TK_7:
        myevent = 'keypress'
        action = 7
    if key == terminal.TK_8:
        myevent = 'keypress'
        action = 8
    if key == terminal.TK_9:
        myevent = 'keypress'
        action = 9
    if key == terminal.TK_0:
        myevent = 'keypress'
        action = 0

    # ACCEPT/DELETE/QUIT KEYS
    if key == terminal.TK_ESCAPE:
        myevent = 'keypress'
        action = 'quit'
    if key == terminal.TK_ENTER:
        myevent = 'keypress'
        action = 'enter'
    if key == terminal.TK_BACKSPACE:
        myevent = 'keypress'
        action = 'delete'

    #
    # MOVEMENT KEYS
    #
    if key == terminal.TK_UP:
        myevent = 'keypress'
        action = 'up'
    if key == terminal.TK_DOWN:
        myevent = 'keypress'
        action = 'down'
    if key == terminal.TK_LEFT:
        myevent = 'keypress'
        action = 'left'
    if key == terminal.TK_RIGHT:
        myevent = 'keypress'
        action = 'right'

    #
    # MOUSE ACTIONS
    #
    if key == terminal.TK_MOUSE_MOVE:
        myevent = 'mousemove'
        action = (terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y))
    if key == terminal.TK_MOUSE_LEFT:
        myevent = 'mouseleftbutton'
        action = (terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y))
    if key == terminal.TK_MOUSE_RIGHT:
        myevent = 'mouserightbutton'
        action = (terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y))

    #
    # general keyboard
    #
    if myevent is None:
        index = terminal.state(terminal.TK_CHAR) - ord('A')
        if index >= 0:
            myevent = 'keypress'
            action = index

    return myevent, action
