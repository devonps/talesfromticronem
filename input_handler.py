
def handle_main_menu(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'new_game': True}
        elif key_char == 'b':
            return {'load_game': True}
        elif key_char == 'c':
            pass
            # save current game
        elif key_char == 'd':
            return {'exit': True}
    return {}


def handle_new_race(key):
    key_char = chr(key.c)
    if key_char == 'a':
        return 'human'
    elif key_char == 'b':
        return 'elf'
    elif key_char == 'c':
        return 'orc'
    elif key_char == 'd':
        return 'troll'
    return ''


def handle_new_class(key):
    key_char = chr(key.c)
    if key_char == 'a':
        return 'necromancer'
    elif key_char == 'b':
        return 'witch doctor'
    elif key_char == 'c':
        return 'druid'
    elif key_char == 'd':
        return 'mesmer'
    elif key_char == 'e':
        return 'elementalist'
    elif key_char == 'f':
        return 'chronomancer'
    return ''


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}