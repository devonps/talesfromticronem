from bearlibterminal import terminal


def which_ui_hotspot_was_clicked(mx, my):
    hotspot_clicked = - 99

    if mx == 69 and my == 48:
        hotspot_clicked = 10  # message log 1

    if mx == 71 and my == 48:
        hotspot_clicked = 11  # message log 2

    if mx == 73 and my == 48:
        hotspot_clicked = 12  # message log 3

    if mx == 75 and my == 48:
        hotspot_clicked = 13  # message log 4

    # check for spell bar being clicked 0 through 9
    if 5 <= mx <= 50:
        if my == 51:
            hc, fluff = divmod(mx, 5)
            if fluff == 0:
                hotspot_clicked = hc - 1

    return hotspot_clicked


def handle_game_keys():
    action = ''
    myevent = ''

    key = terminal.read()

    if key == terminal.TK_1:
        myevent = 'keypress'
        action = '1'
    if key == terminal.TK_2:
        myevent = 'keypress'
        action = '2'
    if key == terminal.TK_3:
        myevent = 'keypress'
        action = '3'
    if key == terminal.TK_4:
        myevent = 'keypress'
        action = '4'
    if key == terminal.TK_5:
        myevent = 'keypress'
        action = '5'
    if key == terminal.TK_6:
        myevent = 'keypress'
        action = '6'
    if key == terminal.TK_7:
        myevent = 'keypress'
        action = '7'
    if key == terminal.TK_8:
        myevent = 'keypress'
        action = '8'
    if key == terminal.TK_9:
        myevent = 'keypress'
        action = '9'
    if key == terminal.TK_0:
        myevent = 'keypress'
        action = '0'

    if key == terminal.TK_ESCAPE:
        myevent = 'keypress'
        action = 'quit'
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
    if key == terminal.TK_ENTER:
        myevent = 'keypress'
        action = 'enter'
    if key == terminal.TK_MOUSE_MOVE:
        myevent = 'mousemove'
        action = (terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y))
    if key == terminal.TK_MOUSE_LEFT:
        myevent = 'mouseleftbutton'
        action = (terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y))
    if key == terminal.TK_MOUSE_RIGHT:
        myevent = 'mouserightbutton'
        action = (terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y))

    index = terminal.state(terminal.TK_CHAR) - ord('a')
    if index >= 0:
        myevent = 'keypress'
        action = index

    return myevent, action
