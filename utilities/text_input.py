import tcod

from newGame import constants


def text_entry():
    tcod.sys_set_fps(constants.TXT_PANEL_FPS)

    timer = 0
    letter_count = 0
    my_word = ""
    key_pressed = False
    max_letters = 15
    bg = tcod.grey

    # set offscreen console for the text entry system
    text_console = tcod.console_new(constants.TXT_PANEL_WIDTH,constants.TXT_PANEL_HEIGHT)
    tcod.console_set_default_background(text_console, bg)
    tcod.console_clear(text_console)
    tcod.console_print_frame(text_console,
                             x=0,
                             y=0,
                             w=constants.TXT_PANEL_WIDTH,
                             h=constants.TXT_PANEL_HEIGHT,
                             clear=False,
                             flag=tcod.BKGND_DEFAULT,
                             fmt='Name Your Character')

    while not key_pressed:

        key = tcod.console_check_for_keypress(tcod.KEY_PRESSED)
        letters_remaining = max_letters - letter_count
        letters_left = ' ' + str(letters_remaining) + ' letters left'
        timer += 1
        if timer % (constants.TXT_PANEL_FPS // 8) == 0:
            if timer % (constants.TXT_PANEL_FPS // 2) == 0:
                timer = 0
                tcod.console_set_char(text_console, constants.TXT_PANEL_WRITE_X + letter_count, constants.TXT_PANEL_WRITE_Y, "_")
                tcod.console_set_char_foreground(text_console, constants.TXT_PANEL_WRITE_X + letter_count, constants.TXT_PANEL_WRITE_Y, tcod.white)
            else:
                tcod.console_set_char(text_console, constants.TXT_PANEL_WRITE_X + letter_count, constants.TXT_PANEL_WRITE_Y, " ")
                tcod.console_set_char_foreground(text_console, constants.TXT_PANEL_WRITE_X + letter_count, constants.TXT_PANEL_WRITE_Y, tcod.white)
            # draw horizontal line
            tcod.console_hline(text_console, 1, 5, constants.TXT_PANEL_WIDTH - 2, tcod.BKGND_DEFAULT)
            # word count
            tcod.console_set_alignment(text_console, tcod.RIGHT)
            tcod.console_print_rect(con=text_console,
                                    x=constants.TXT_PANEL_WIDTH - 1,
                                    y=constants.TXT_PANEL_WRITE_Y + 2,
                                    w=constants.TXT_PANEL_WIDTH - 5,
                                    h=constants.TXT_PANEL_HEIGHT - 10,
                                    fmt=letters_left)
            # instructions
            tcod.console_set_alignment(text_console, tcod.LEFT)
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=6,
                                    w=constants.TXT_PANEL_WIDTH - 5,
                                    h=constants.TXT_PANEL_HEIGHT - 10,
                                    fmt='Controls')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=7,
                                    w=constants.TXT_PANEL_WIDTH - 5,
                                    h=constants.TXT_PANEL_HEIGHT - 10,
                                    fmt='Backspace to delete')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=8,
                                    w=constants.TXT_PANEL_WIDTH - 5,
                                    h=constants.TXT_PANEL_HEIGHT - 10,
                                    fmt='Escape to quit')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=9,
                                    w=constants.TXT_PANEL_WIDTH - 5,
                                    h=constants.TXT_PANEL_HEIGHT - 10,
                                    fmt='Enter to accept')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=10,
                                    w=constants.TXT_PANEL_WIDTH - 5,
                                    h=constants.TXT_PANEL_HEIGHT - 10,
                                    fmt='Leave blank for random name')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=11,
                                    w=constants.TXT_PANEL_WIDTH - 5,
                                    h=constants.TXT_PANEL_HEIGHT - 10,
                                    fmt='Only lowercase alphas')

            tcod.console_blit(text_console,0, 0, constants.TXT_PANEL_WIDTH,constants.TXT_PANEL_HEIGHT, 0, 20, 10)
            tcod.console_flush()

        if key.vk == tcod.KEY_BACKSPACE and letter_count > 0:
            tcod.console_set_char(text_console, constants.TXT_PANEL_WRITE_X + letter_count, constants.TXT_PANEL_WRITE_Y, " ")
            tcod.console_set_char_foreground(text_console, constants.TXT_PANEL_WRITE_X + letter_count, constants.TXT_PANEL_WRITE_Y, tcod.white)
            my_word = my_word[:-1]
            letter_count -= 1
        elif key.vk == tcod.KEY_ENTER:
            key_pressed = True
            break
        elif key.vk == tcod.KEY_ESCAPE:
            my_word = ""
            break
        elif key.c > 0:
            letter = chr(key.c)
            if ord(letter) > 96 and ord(letter) < 123:
                if letters_remaining > 0:
                    tcod.console_set_char(text_console, constants.TXT_PANEL_WRITE_X + letter_count, constants.TXT_PANEL_WRITE_Y, letter)
                    tcod.console_set_char_foreground(text_console, constants.TXT_PANEL_WRITE_X + letter_count, constants.TXT_PANEL_WRITE_Y, tcod.white)
                    my_word += letter
                    letter_count += 1
    return my_word
