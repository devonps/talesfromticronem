from bearlibterminal import terminal
from utilities import configUtilities, colourUtilities
from utilities.common import CommonUtils
from utilities.display import pointy_vertical_menu
from utilities.input_handlers import handle_game_keys
from utilities.mobileHelp import MobileUtilities
from utilities.weaponManagement import WeaponUtilities


def shopkeeper_weaponsmith(gameworld, shopkeeper_id):
    game_config = configUtilities.load_config()
    selected_menu_option = 0
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    player_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player_entity)
    player_first_name = player_names[0]

    player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)

    MobileUtilities.clear_talk_to_me_flag(gameworld=gameworld, target_entity=shopkeeper_id)
    MobileUtilities.set_spoken_to_before_flag_to_true(gameworld=gameworld, target_entity=shopkeeper_id)

    available_weapons = WeaponUtilities.get_available_weapons_for_class(selected_class=player_class,
                                                                        game_config=game_config)
    max_menu_option = len(available_weapons) - 1
    weapon_description, weapon_wielded, weapon_description, weapon_quality, weapon_damage_ranges = WeaponUtilities.get_weapon_flavour_info(
        game_config=game_config, available_weapons=available_weapons)

    dialog_frame_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_X')
    dialog_frame_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_Y')
    dialog_frame_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                     section='gui', parameter='DIALOG_FRAME_WIDTH')

    CommonUtils.draw_dialog_ui(gameworld=gameworld, game_config=game_config, entity_speaking=shopkeeper_id)

    starter_text = "Welcome $1, If you don't already know, I can supply weapons for you!"
    intro_text = CommonUtils.replace_value_in_event(event_string=starter_text, par1=player_first_name)

    # intro text
    terminal.print_(x=dialog_frame_start_x + 2, y=dialog_frame_start_y + 2, width=dialog_frame_width - 5,
                    s=intro_text)

    valid_event = False
    while not valid_event:

        # pointy menu of valid weapons for the playable class
        pointy_vertical_menu(header='', menu_options=available_weapons, menu_start_x=dialog_frame_start_x + 2,
                             menu_start_y=dialog_frame_start_y + 6, blank_line=True,
                             selected_option=selected_menu_option,
                             colours=[colourUtilities.get('SPRINGGREEN'), colourUtilities.get('DARKOLIVEGREEN')])

        # weapon flavour text
        # This is a 2-handed sword, it is of normal quality, and does between 55 and 99 direct damage per target.
        weapon_flavour_text = build_weapon_flavour_text(weapon_damage_ranges=weapon_damage_ranges, selected_menu_option=selected_menu_option)
        terminal.print_(x=dialog_frame_start_x + 14, y=dialog_frame_start_y + 6, width=dialog_frame_width - 15,
                        s=weapon_flavour_text)

        # blit the console
        terminal.refresh()

        event_to_be_processed, event_action = handle_game_keys()
        if event_action == 'quit':
            valid_event = True
        if event_action in ('up', 'down'):
            selected_menu_option = CommonUtils.move_menu_selection(event_action=event_action,
                                                                   selected_menu_option=selected_menu_option,
                                                                   max_menu_option=max_menu_option)
        if event_action == 'enter':
            valid_event = True
            # apply shopkeeper bonus


def build_weapon_flavour_text(weapon_damage_ranges, selected_menu_option):

    wpn_dam = weapon_damage_ranges[selected_menu_option]
    weapon_min_damage = wpn_dam.get('min')
    weapon_max_damage = wpn_dam.get('max')
    weapon_flavour_text = 'Deals between '
    weapon_flavour_text += str(weapon_min_damage) + ' and ' + str(weapon_max_damage) + ' direct damage.'
    
    return weapon_flavour_text
