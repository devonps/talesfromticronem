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
    spell_bar_hotkeys = [terminal.TK_1, terminal.TK_2, terminal.TK_3, terminal.TK_4, terminal.TK_5, terminal.TK_6, terminal.TK_7, terminal.TK_8, terminal.TK_9, terminal.TK_0]

    if key in spell_bar_hotkeys:
        myevent = 'keypress'
        action = int(chr(ord('1')))

    # ACCEPT KEYS
    if key == terminal.TK_ESCAPE:
        myevent = 'keypress'
        action = 'quit'
    if key == terminal.TK_ENTER:
        myevent = 'keypress'
        action = 'enter'

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
    # ACTION KEYS
    #
    if key == terminal.TK_M:
        if terminal.check(terminal.TK_SHIFT):
            myevent = ''
            action = ''
        else:
            myevent = 'keypress'
            action = 'log'

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
        index = terminal.state(terminal.TK_CHAR) - ord('a')
        if index >= 0:
            myevent = 'keypress'
            action = index

    return myevent, action
