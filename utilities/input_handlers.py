import tcod

from components import mobiles, userInput
from loguru import logger

def handle_keys(mouse, key, gameworld, player):
    # movement
    player_velocity_component = gameworld.component_for_entity(player, mobiles.Velocity)
    position_component = gameworld.component_for_entity(player, mobiles.Position)
    ev = tcod.sys_wait_for_event(tcod.EVENT_KEY, key, mouse, flush=False)
    if ev & tcod.EVENT_KEY_PRESS:
        if key.vk == tcod.KEY_UP:
            player_velocity_component.dy = -1
            position_component.hasMoved = True
            return {'player_moved': True}
        elif key.vk == tcod.KEY_DOWN:
            player_velocity_component.dy = 1
            position_component.hasMoved = True
            return {'player_moved': True}
        elif key.vk == tcod.KEY_LEFT:
            player_velocity_component.dx = -1
            position_component.hasMoved = True
            return {'player_moved': True}
        elif key.vk == tcod.KEY_RIGHT:
            player_velocity_component.dx = 1
            position_component.hasMoved = True
            return {'player_moved': True}

        # non-movement keys
        if key.vk == tcod.KEY_ENTER:
            return{'text': True}
        elif key.vk == tcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle full screen
            return {'fullscreen': True}

        elif key.vk == tcod.KEY_ESCAPE:
            # Exit the game
            return {'exit': True}

    return {}


def handle_main_menu(key, mouse, gameworld):
    key_char = chr(key.c)
    if key.vk == tcod.KEY_CHAR:
        logger.info('keyboard option {}', key_char)
        if key_char == 'a':
            return {'new_game': True}
        elif key_char == 'b':
            return {'load_game': True}
        elif key_char == 'c':
            pass
            # save current game
        elif key_char == 'd':
            return {'exit': True}
        elif key_char == 'e':
            return {'player_seed': True}
    if mouse:
        player_input_entity = get_user_input_entity(gameworld)
        mouse_component = gameworld.component_for_entity(player_input_entity, userInput.Mouse)
        keyboard_component = gameworld.component_for_entity(player_input_entity, userInput.Keyboard)

        if mouse_component.lbutton:
            logger.info('Mouse/text option is {}', keyboard_component.keypressed)
            if keyboard_component.keypressed == 'a':
                return {'new_game': True}
            elif keyboard_component.keypressed == 'b':
                return {'load_game': True}
            elif keyboard_component.keypressed == 'c':
                pass
                # save current game
            elif keyboard_component.keypressed == 'd':
                return {'exit': True}
            elif keyboard_component.keypressed == 'e':
                return {'player_seed': True}
    return {}


def handle_new_race(key, mouse):
    key_char = chr(key.c)
    if key.vk == tcod.KEY_CHAR:
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


def get_user_input_entity(gameworld):
    for ent, (k, m) in gameworld.get_components(userInput.Mouse, userInput.Keyboard):
        return ent