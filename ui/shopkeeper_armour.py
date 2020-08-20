from bearlibterminal import terminal
from loguru import logger

from utilities import colourUtilities, configUtilities
from utilities.armourManagement import ArmourUtilities
from utilities.common import CommonUtils
from utilities.display import coloured_list, pointy_menu
from utilities.input_handlers import handle_game_keys
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities


def shopkeeper_armour(gameworld, player_names, shopkeeper_id):
    game_config = configUtilities.load_config()
    player_first_name = player_names[0]
    selected_menu_option = 0
    flavour_column_text = []
    player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

    MobileUtilities.clear_talk_to_me_flag(gameworld=gameworld, target_entity=shopkeeper_id)
    MobileUtilities.set_spoken_to_before_flag_to_true(gameworld=gameworld, target_entity=shopkeeper_id)

    dialog_frame_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_X')
    dialog_frame_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_Y')
    dialog_frame_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                     section='gui', parameter='DIALOG_FRAME_WIDTH')

    CommonUtils.draw_dialog_ui(gameworld=gameworld, game_config=game_config, entity_speaking=shopkeeper_id)

    armour_details, as_prefix_list, px_att_bonus, px_att_name, px_flavour = get_all_armour_modifiers(game_config=game_config)

    as_display_name = armour_details[0]
    as_material = armour_details[1]
    flavour_column_text.append(px_flavour)

    starter_text = "Ahhh if it isn't $1"
    return_text = CommonUtils.replace_value_in_event(event_string=starter_text, par1=player_first_name)
    intro_text = return_text + ", and, I see you're wearing some " + as_material + ' ' + as_display_name + ' armour, ' + 'tell me, what kind of modifier would you like adding?'

    menu_options = as_prefix_list
    max_menu_option = len(menu_options) - 1

    # armour column titles
    flavour_colour_string = '[color=' + colourUtilities.get('LIGHTSLATEGRAY') + ']'
    flavour_coloumn_one_title = 'Flavour'
    flavour_column_one_string = flavour_colour_string + flavour_coloumn_one_title

    valid_event = False
    while not valid_event:

        # intro text
        terminal.print_(x=dialog_frame_start_x + 2, y=dialog_frame_start_y + 2, width=dialog_frame_width - 5,
                        s=intro_text)

        pointy_menu(header='', menu_options=menu_options, menu_start_x=dialog_frame_start_x + 3,
                    menu_start_y=dialog_frame_start_y + 9, blank_line=True, selected_option=selected_menu_option,
                    colours=[colourUtilities.get('SPRINGGREEN'), colourUtilities.get('DARKOLIVEGREEN')])

        # display flavour columns
        terminal.printf(x=dialog_frame_start_x + 15, y=dialog_frame_start_y + 8, s=flavour_column_one_string)

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
            logger.debug('Armour modifier chosen is {}', as_prefix_list[selected_menu_option])
            logger.debug('Attribute to be modified is {}', px_att_name[selected_menu_option])
            logger.debug('Attribute bonus is {}', px_att_bonus[selected_menu_option])

            armour_worn_on_head = MobileUtilities.is_entity_wearing_head_armour(gameworld=gameworld, entity=player_entity)
            if armour_worn_on_head:
                armour_entity = ArmourUtilities.get_armour_entity_from_body_location(gameworld=gameworld, entity=player_entity, bodylocation='head')
                attribute_bonus_list = ArmourUtilities.get_armour_major_attributes(gameworld=gameworld, entity=armour_entity)

                logger.debug('Armour entity on head is {}', armour_entity)
                logger.debug('Attribute bonus list {}', attribute_bonus_list)


def get_all_armour_modifiers(game_config):
    armourset_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                parameter='ARMOURSETFILE')
    armour_file = read_json_file(armourset_file)

    pxstring = 'prefix'
    attvaluestring = 'attributebonus'
    attnamestring = 'attributename'

    as_prefix_list = []
    px_flavour = []
    px_att_bonus = []
    armour_details = []
    px_att_name = []

    for armourset in armour_file['armoursets']:
        if armourset['startset'] == 'true':
            armour_details.append(armourset['displayname'])
            armour_details.append(armourset['material'])
            as_prefix_list = armourset['prefixlist'].split(",")
            prefix_count = armourset['prefixcount']
            attribute_bonus_count = armourset['attributebonuscount']

            for px in range(1, prefix_count + 1):
                prefix_string = pxstring + str(px)
                px_flavour.append(armourset[prefix_string]['flavour'])

                if attribute_bonus_count > 1:
                    att_bonus_string = attvaluestring + str(px)
                    att_name_string = attnamestring + str(px)
                else:
                    att_bonus_string = attvaluestring + str(1)
                    att_name_string = attnamestring + str(1)

                px_att_bonus.append(armourset[prefix_string][att_bonus_string])
                px_att_name.append(armourset[prefix_string][att_name_string])

    return armour_details, as_prefix_list, px_att_bonus, px_att_name, px_flavour