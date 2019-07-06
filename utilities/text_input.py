import tcod
import tcod.console
from utilities import configUtilities


def text_entry(game_config):
    TXT_PANEL_FPS = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_FPS')
    TXT_PANEL_WIDTH = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WIDTH')
    TXT_PANEL_HEIGHT = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_HEIGHT')
    TXT_PANEL_WRITE_X = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WRITE_X')
    TXT_PANEL_WRITE_Y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WRITE_Y')

    tcod.sys_set_fps(TXT_PANEL_FPS)

    timer = 0
    letter_count = 0
    my_word = ""
    key_pressed = False
    max_letters = 15
    bg = tcod.grey

    # set offscreen console for the text entry system
    text_console = tcod.console.Console(TXT_PANEL_WIDTH, TXT_PANEL_HEIGHT, 'F')
    text_console.clear(ch=32, bg=bg)
    text_console.draw_frame(x=0, y=0, width=TXT_PANEL_WIDTH, height=TXT_PANEL_HEIGHT, title='Name Your Character', clear=False, bg_blend=tcod.BKGND_DEFAULT)

    while not key_pressed:

        key = tcod.console_check_for_keypress(tcod.KEY_PRESSED)
        letters_remaining = max_letters - letter_count
        letters_left = ' ' + str(letters_remaining) + ' letters left'
        timer += 1
        if timer % (TXT_PANEL_FPS // 8) == 0:
            if timer % (TXT_PANEL_FPS // 2) == 0:
                timer = 0
                text_console.put_char(x=TXT_PANEL_WRITE_X + letter_count, y=TXT_PANEL_WRITE_Y, ch=95)
                tcod.console_set_char_foreground(text_console, TXT_PANEL_WRITE_X + letter_count, TXT_PANEL_WRITE_Y, tcod.white)
            else:
                text_console.put_char(x=TXT_PANEL_WRITE_X + letter_count, y=TXT_PANEL_WRITE_Y, ch=32)
                tcod.console_set_char_foreground(text_console, TXT_PANEL_WRITE_X + letter_count, TXT_PANEL_WRITE_Y, tcod.white)
            # draw horizontal line
            text_console.hline(x=1, y=5, width=TXT_PANEL_WIDTH - 2, bg_blend=tcod.BKGND_DEFAULT)
            # word count
            # tcod.console_set_alignment(text_console, tcod.RIGHT)
            text_console.default_alignment = tcod.RIGHT
            tcod.console_print_rect(con=text_console,
                                    x=TXT_PANEL_WIDTH - 1,
                                    y=TXT_PANEL_WRITE_Y + 2,
                                    w=TXT_PANEL_WIDTH - 5,
                                    h=TXT_PANEL_HEIGHT - 10,
                                    fmt=letters_left)
            # text_console.print_box(x=TXT_PANEL_WIDTH - 1, y=TXT_PANEL_WRITE_Y + 2, width=TXT_PANEL_WIDTH - 5,
            #                        height=TXT_PANEL_HEIGHT - 10, string=letters_left,
            #                        fg=tcod.white, bg=tcod.black, bg_blend=tcod.BKGND_DEFAULT)

            # instructions
            # tcod.console_set_alignment(text_console, tcod.LEFT)
            text_console.default_alignment = tcod.LEFT
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=6,
                                    w=TXT_PANEL_WIDTH - 5,
                                    h=TXT_PANEL_HEIGHT - 10,
                                    fmt='Controls')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=7,
                                    w=TXT_PANEL_WIDTH - 5,
                                    h=TXT_PANEL_HEIGHT - 10,
                                    fmt='Backspace to delete')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=8,
                                    w=TXT_PANEL_WIDTH - 5,
                                    h=TXT_PANEL_HEIGHT - 10,
                                    fmt='Escape to quit')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=9,
                                    w=TXT_PANEL_WIDTH - 5,
                                    h=TXT_PANEL_HEIGHT - 10,
                                    fmt='Enter to accept')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=10,
                                    w=TXT_PANEL_WIDTH - 5,
                                    h=TXT_PANEL_HEIGHT - 10,
                                    fmt='Leave blank for random name')
            tcod.console_print_rect(con=text_console,
                                    x=2,
                                    y=11,
                                    w=TXT_PANEL_WIDTH - 5,
                                    h=TXT_PANEL_HEIGHT - 10,
                                    fmt='Only lowercase alphas')

            tcod.console_blit(text_console,0, 0, TXT_PANEL_WIDTH, TXT_PANEL_HEIGHT, 0, 20, 10)
            tcod.console_flush()

        if key.vk == tcod.KEY_BACKSPACE and letter_count > 0:
            text_console.put_char(x=TXT_PANEL_WRITE_X + letter_count, y=TXT_PANEL_WRITE_Y, ch=32)
            tcod.console_set_char_foreground(text_console, TXT_PANEL_WRITE_X + letter_count, TXT_PANEL_WRITE_Y, tcod.white)
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
            if 96 < ord(letter) < 123 and letters_remaining > 0:
                text_console.put_char(x=TXT_PANEL_WRITE_X + letter_count, y=TXT_PANEL_WRITE_Y, ch=ord(letter))
                tcod.console_set_char_foreground(text_console, TXT_PANEL_WRITE_X + letter_count, TXT_PANEL_WRITE_Y, tcod.white)
                my_word += letter
                letter_count += 1
    return my_word
