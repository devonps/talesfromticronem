from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities, colourUtilities
from utilities.common import CommonUtils
from utilities.display import coloured_list, pointy_menu
from utilities.input_handlers import handle_game_keys
from utilities.mobileHelp import MobileUtilities


def shopkeeper_jeweller(gameworld, shopkeeper_id):
    game_config = configUtilities.load_config()
    selected_menu_option = 0
    flavour_column_text = []
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    player_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player_entity)
    player_first_name = player_names[0]


    player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)


    MobileUtilities.clear_talk_to_me_flag(gameworld=gameworld, target_entity=shopkeeper_id)
    MobileUtilities.set_spoken_to_before_flag_to_true(gameworld=gameworld, target_entity=shopkeeper_id)

    dialog_frame_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_X')
    dialog_frame_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_Y')
    dialog_frame_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                     section='gui', parameter='DIALOG_FRAME_WIDTH')

    CommonUtils.draw_dialog_ui(gameworld=gameworld, game_config=game_config, entity_speaking=shopkeeper_id)

    starter_text = "Ahhh if it isn't $1, I'm the jewellery man!"
    return_text = CommonUtils.replace_value_in_event(event_string=starter_text, par1=player_first_name)
    intro_text = return_text

    menu_options = ['Defensive', 'Balanced', 'Aggressive']
    max_menu_option = len(menu_options) - 1
    flavour_column_text.append("Something here")
    flavour_colour_string = '[color=' + colourUtilities.get('LIGHTSLATEGRAY') + ']'
    flavour_headings = ['pendant', 'earring', 'earring', 'ring', 'ring']

    valid_event = False
    while not valid_event:

        # intro text
        terminal.print_(x=dialog_frame_start_x + 2, y=dialog_frame_start_y + 2, width=dialog_frame_width - 5,
                        s=intro_text)

        pointy_menu(header='', menu_options=menu_options, menu_start_x=dialog_frame_start_x + 2,
                    menu_start_y=dialog_frame_start_y + 6, blank_line=True, selected_option=selected_menu_option,
                    colours=[colourUtilities.get('SPRINGGREEN'), colourUtilities.get('DARKOLIVEGREEN')])

        # display flavour columns
        sx = 16
        for a in range(len(flavour_headings)):
            terminal.printf(x=dialog_frame_start_x + sx, y=dialog_frame_start_y + 4, s=flavour_colour_string + flavour_headings[a])
            sx += len(flavour_headings[a]) + 3

        # display attribute to be modified
        fg = colourUtilities.get('LIGHTBLUE1')

        # display flavour text
        coloured_list(list_options=flavour_column_text[0],
                      list_x=dialog_frame_start_x + 17, list_y=dialog_frame_start_y + 9,
                      selected_option='nothing', blank_line=True, fg=fg)

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
