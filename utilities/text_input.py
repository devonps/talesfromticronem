import tcod

from loguru import logger


def text_to_entry():
    FPS = 30
    tcod.sys_set_fps(FPS)

    timer = 0
    command = ""
    x = 1
    y = 1
    w = 35
    h = 25
    key_pressed = False

    # set offscreen console for the text entry system
    text_console = tcod.console_new(w,h)
    tcod.console_set_default_background(text_console, tcod.blue)
    tcod.console_clear(text_console)
    tcod.console_print_frame(text_console,x=0,y=0,w=30,h=20,clear=False,flag=tcod.BKGND_DEFAULT,fmt='Text Entry')

    while not key_pressed:

        key = tcod.console_check_for_keypress(tcod.KEY_PRESSED)

        timer += 1
        if timer % (FPS // 8) == 0:
            if timer % (FPS // 2) == 0:
                timer = 0
                tcod.console_set_char(text_console, x, y, "_")
                tcod.console_set_char_foreground(text_console, x, y, tcod.white)
            else:
                tcod.console_set_char(text_console, x, y, " ")
                tcod.console_set_char_foreground(text_console, x, y, tcod.white)

            tcod.console_blit(text_console, 0, 0, w, h, 0, 30, 20)
            tcod.console_flush()

        if key.vk == tcod.KEY_BACKSPACE and x > 1:
            tcod.console_set_char(text_console, x, y, " ")
            tcod.console_set_char_foreground(text_console, x, y, tcod.white)
            command = command[:-1]
            x -= 1
        elif key.vk == tcod.KEY_ENTER:
            logger.info('Final word is {}', command)
            key_pressed = True
            break
        elif key.vk == tcod.KEY_ESCAPE:
            command = ""
            break
        elif key.c > 0:
            letter = chr(key.c)
            tcod.console_set_char(text_console, x, y, letter)  # print new character at appropriate position on screen
            tcod.console_set_char_foreground(text_console, x, y, tcod.white)  # make it white or something
            command += letter  # add to the string
            logger.info('key pressed --{}--', letter)
            x += 1
    return command
