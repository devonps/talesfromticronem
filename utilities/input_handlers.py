from bearlibterminal import terminal


def handle_game_keys():
    action = None
    myevent = None

    key = terminal.read()

    #
    # ENTITY SPY PAGE SELECTION
    #
    if key == terminal.TK_TAB:
        myevent = 'keypress'
        action = 'tab'
    #
    # SPELL CAST / INFO KEYS
    #
    if key == terminal.TK_1:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = 'keypress'
        action = 1
    if key == terminal.TK_2:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = 'keypress'
        action = 2
    if key == terminal.TK_3:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = 'keypress'
        action = 3
    if key == terminal.TK_4:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = 'keypress'
        action = 4
    if key == terminal.TK_5:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = 'keypress'
        action = 5
    if key == terminal.TK_6:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = 'keypress'
        action = 6
    if key == terminal.TK_7:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        elif terminal.check(terminal.TK_CONTROL):
            myevent = 'swap'
        else:
            myevent = 'keypress'
        action = 7
    if key == terminal.TK_8:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        elif terminal.check(terminal.TK_CONTROL):
            myevent = 'swap'
        else:
            myevent = 'keypress'
        action = 8
    if key == terminal.TK_9:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        elif terminal.check(terminal.TK_CONTROL):
            myevent = 'swap'
        else:
            myevent = 'keypress'
        action = 9
    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_A:
        myevent = 'infopopup'
        action = 'A'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_B:
        myevent = 'infopopup'
        action = 'B'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_C:
        myevent = 'infopopup'
        action = 'C'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_D:
        myevent = 'infopopup'
        action = 'D'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_E:
        myevent = 'infopopup'
        action = 'E'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_F:
        myevent = 'infopopup'
        action = 'F'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_G:
        myevent = 'infopopup'
        action = 'G'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_H:
        myevent = 'infopopup'
        action = 'H'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_I:
        myevent = 'infopopup'
        action = 'I'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_J:
        myevent = 'infopopup'
        action = 'J'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_T:
        myevent = 'chat'
        action = 'T'

    if terminal.check(terminal.TK_SHIFT) and key == terminal.TK_Z:
        myevent = 'death'
        action = 'Z'

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
    # move to next message log
    #
    if key == terminal.TK_M:
        myevent = 'keypress'
        action = 'log'

    #
    # general keyboard
    #
    if myevent is None:
        index = terminal.state(terminal.TK_CHAR)
        if index >= 0:
            myevent = 'keypress'
            action = index

    return myevent, action
