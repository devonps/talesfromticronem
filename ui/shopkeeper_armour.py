from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities, armourManagement, common, display, input_handlers, mobileHelp


def shopkeeper_armour(gameworld, shopkeeper_id):
    game_config = configUtilities.load_config()
    selected_menu_option = 0
    flavour_column_text = []
    player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    player_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player_entity)
    player_first_name = player_names[0]

    mobileHelp.MobileUtilities.clear_talk_to_me_flag(gameworld=gameworld, target_entity=shopkeeper_id)
    mobileHelp.MobileUtilities.set_spoken_to_before_flag_to_true(gameworld=gameworld, target_entity=shopkeeper_id)

    dialog_frame_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_X')
    dialog_frame_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_Y')
    dialog_frame_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                     section='gui', parameter='DIALOG_FRAME_WIDTH')

    common.CommonUtils.draw_dialog_ui(gameworld=gameworld, game_config=game_config, entity_speaking=shopkeeper_id)

    armour_details, as_prefix_list, px_att_bonus, px_att_name, px_flavour = armourManagement.ArmourUtilities.get_all_armour_modifiers()

    as_display_name = armour_details[0]
    as_material = armour_details[1]
    flavour_column_text.append(px_flavour)

    starter_text = "Ahhh if it isn't $1"
    return_text = common.CommonUtils.replace_value_in_event(event_string=starter_text, par1=player_first_name)
    intro_text = return_text + ", and, I see you're wearing some " + as_material + ' ' + as_display_name + ' armour, ' + 'tell me, what kind of modifier would you like adding?'

    menu_options = as_prefix_list
    max_menu_option = len(menu_options) - 1

    # armour column titles
    flavour_colour_string = '[color=SHOPKEEPER_ARMOUR_COLUMN_FLAVOUR]'
    flavour_coloumn_one_title = 'Flavour'
    flavour_column_one_string = flavour_colour_string + flavour_coloumn_one_title

    valid_event = False
    while not valid_event:

        # intro text
        terminal.print_(x=dialog_frame_start_x + 2, y=dialog_frame_start_y + 2, width=dialog_frame_width - 5,
                        s=intro_text)

        display.pointy_vertical_menu(header='', menu_options=menu_options, menu_start_x=dialog_frame_start_x + 3,
                             menu_start_y=dialog_frame_start_y + 9, blank_line=True, selected_option=selected_menu_option)

        # display flavour columns
        terminal.printf(x=dialog_frame_start_x + 15, y=dialog_frame_start_y + 8, s=flavour_column_one_string)

        # display attribute to be modified
        fg = "[color=SHOPKEEPER_ARMOUR_ATTRIBUTE_FLAVOUR]"

        # display flavour text
        display.coloured_list(list_options=flavour_column_text[0],
                      list_x=dialog_frame_start_x + 17, list_y=dialog_frame_start_y + 9,
                      selected_option='nothing', blank_line=True, fg=fg)

        # blit the console
        terminal.refresh()

        event_to_be_processed, event_action = input_handlers.handle_game_keys()
        if event_action == 'quit':
            valid_event = True
        if event_action in ('up', 'down'):
            selected_menu_option = common.CommonUtils.move_menu_selection(event_action=event_action,
                                                                   selected_menu_option=selected_menu_option,
                                                                   max_menu_option=max_menu_option)
        if event_action == 'enter':
            valid_event = True
            # apply shopkeeper bonus
            logger.debug('Armour modifier chosen is {}', as_prefix_list[selected_menu_option])
            logger.debug('Attribute to be modified is {}', px_att_name[selected_menu_option])
            logger.debug('Attribute bonus is {}', px_att_bonus[selected_menu_option])

            armour_set = armourManagement.ArmourUtilities.create_full_armour_set(gameworld=gameworld, prefix=as_prefix_list[selected_menu_option],
                                                                armourset='Embroided')
            armourManagement.ArmourUtilities.equip_full_set_of_armour(gameworld=gameworld, entity=player_entity, armourset=armour_set)

            armourManagement.ArmourUtilities.apply_major_attribute_bonus_to_full_armourset(gameworld=gameworld,
                                                                          player_entity=player_entity,
                                                                          attribute_name=as_prefix_list[selected_menu_option],
                                                                          attribute_bonus=px_att_bonus[
                                                                            selected_menu_option])

            armourManagement.ArmourUtilities.set_mobile_derived_armour_attribute(gameworld=gameworld, entity=player_entity)
            mobileHelp.MobileUtilities.set_mobile_derived_attributes(gameworld=gameworld, entity=player_entity)
