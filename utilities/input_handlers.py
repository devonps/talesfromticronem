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
        else:
            myevent = 'keypress'
        action = 7
    if key == terminal.TK_8:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = 'keypress'
        action = 8
    if key == terminal.TK_9:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = 'keypress'
        action = 9
    if key == terminal.TK_A:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'A'
    if key == terminal.TK_A:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'A'
    if key == terminal.TK_B:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'B'
    if key == terminal.TK_C:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'C'
    if key == terminal.TK_D:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'D'
    if key == terminal.TK_E:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'E'
    if key == terminal.TK_F:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'F'
    if key == terminal.TK_G:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'G'
    if key == terminal.TK_H:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'H'
    if key == terminal.TK_I:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'I'
    if key == terminal.TK_J:
        if terminal.check(terminal.TK_SHIFT):
            myevent = 'infopopup'
        else:
            myevent = ''
        action = 'J'

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
        index = terminal.state(terminal.TK_CHAR) - ord('A')
        if index >= 0:
            myevent = 'keypress'
            action = index

    return myevent, action
