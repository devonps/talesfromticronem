import tcod


def menu(con, header, options, width, screen_width, screen_height, posx, posy, foreground):

    # calculate the total height for the menu header with one line per option
    header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen window - this is where the menu options will be displayed
    window = tcod.console_new(width, height)

    # print the header, with auto-wrap
    tcod.console_set_default_foreground(window, foreground)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # print the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of 'window' to the root console
    tcod.console_blit(window, 0, 0, width, height, 0, posx, posy, 1.0, 0.7)