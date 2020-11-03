from bearlibterminal import terminal

from utilities import configUtilities, common, display, input_handlers, itemsHelp, jewelleryManagement, mobileHelp, scorekeeper, spellHelp


def shopkeeper_jewellery(gameworld, shopkeeper_id):
    game_config = configUtilities.load_config()
    selected_menu_option = 0
    player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
    player_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player_entity)
    player_first_name = player_names[0]

    player_class = mobileHelp.MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)

    mobileHelp.MobileUtilities.clear_talk_to_me_flag(gameworld=gameworld, target_entity=shopkeeper_id)
    mobileHelp.MobileUtilities.set_spoken_to_before_flag_to_true(gameworld=gameworld, target_entity=shopkeeper_id)

    dialog_frame_start_x = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_X')
    dialog_frame_start_y = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                       section='gui', parameter='DIALOG_FRAME_START_Y')
    dialog_frame_width = configUtilities.get_config_value_as_integer(configfile=game_config,
                                                                     section='gui', parameter='DIALOG_FRAME_WIDTH')

    common.CommonUtils.draw_dialog_ui(gameworld=gameworld, game_config=game_config, entity_speaking=shopkeeper_id)

    starter_text = "Ahhh if it isn't $1, I'm the jewellery man!"
    intro_text = common.CommonUtils.replace_value_in_event(event_string=starter_text, par1=player_first_name)

    menu_options = ['Defensive', 'Balanced', 'Offensive']
    trinket_headings = ['Gemstone', 'Attribute', 'Uplift', 'Bonus']
    flavour_headings = ['pendant', 'ring', 'ring', 'earring', 'earring']
    max_menu_option = len(menu_options) - 1
    flavour_colour_string = '[color=SHOPKEEPER_JEWELLER_COLUMN_FLAVOUR]'
    flavour_colour_content = '[color=SHOPKEEPER_JEWELLER_FLAVOUR]'
    current_package = []

    defensive_package, balanced_package, offensive_package = jewelleryManagement.JewelleryUtilities.load_jewellery_package_based_on_class(
        playable_class=player_class, game_config=game_config)

    current_package.append(defensive_package)
    current_package.append(balanced_package)
    current_package.append(offensive_package)

    # intro text
    terminal.print_(x=dialog_frame_start_x + 2, y=dialog_frame_start_y + 2, width=dialog_frame_width - 5,
                    s=intro_text)

    # display trinket headings
    hx = dialog_frame_start_x + 13
    sy = dialog_frame_start_y + 7
    terminal.printf(x=hx, y=sy, s=flavour_colour_string + trinket_headings[0])
    hx += len(trinket_headings[0]) + 2
    terminal.printf(x=hx, y=sy, s=flavour_colour_string + trinket_headings[1])
    hx += len(trinket_headings[1]) + 2
    terminal.printf(x=hx, y=sy, s=flavour_colour_string + trinket_headings[2])
    hx += len(trinket_headings[2]) + 2
    terminal.printf(x=hx, y=sy, s=flavour_colour_string + trinket_headings[3])

    # display flavour columns
    sx = dialog_frame_start_x + 3
    sy = dialog_frame_start_y + 10
    for a in range(len(flavour_headings)):
        terminal.printf(x=sx, y=sy, s=flavour_colour_string + flavour_headings[a])
        sy += 2

    valid_event = False
    while not valid_event:

        # display package menu options
        display.pointy_horizontal_menu(header='', menu_options=menu_options, menu_start_x=dialog_frame_start_x + 13,
                               menu_start_y=dialog_frame_start_y + 5, selected_option=selected_menu_option)

        display_jewellery_package(sx=dialog_frame_start_x + 13, sy=dialog_frame_start_y + 10,
                                  flavour_colour_content=flavour_colour_content,
                                  jewellery_package=current_package[selected_menu_option])

        # blit the console
        terminal.refresh()

        event_to_be_processed, event_action = input_handlers.handle_game_keys()
        if event_action == 'quit':
            valid_event = True
        if event_action in ('left', 'right'):
            selected_menu_option = common.CommonUtils.move_menu_selection(event_action=event_action,
                                                                   selected_menu_option=selected_menu_option,
                                                                   max_menu_option=max_menu_option)
        if event_action == 'enter':
            valid_event = True
            # apply shopkeeper bonus

            # create jewellery set based on the balanced package
            # this is a temp approach being used for utility spells

            jewellery_package = menu_options[selected_menu_option]

            jewelleryManagement.JewelleryUtilities.create_jewellery_for_utility_spells(gameworld=gameworld, game_config=game_config,
                                                                   jewellery_set=jewellery_package.lower())

            set_spellbar_utility_spells(gameworld=gameworld, player_entity=player_entity)


def set_spellbar_utility_spells(gameworld, player_entity):
    pendent_entity = jewelleryManagement.JewelleryUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld,
                                                                                entity=player_entity,
                                                                                bodylocation='neck')
    left_ear_entity = jewelleryManagement.JewelleryUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld,
                                                                                 entity=player_entity,
                                                                                 bodylocation='lear')
    right_ear_entity = jewelleryManagement.JewelleryUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld,
                                                                                  entity=player_entity,
                                                                                  bodylocation='rear')

    if pendent_entity > 0:
        sp1 = itemsHelp.ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=pendent_entity)
        spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp1, slot=6, player_entity=player_entity)
        spell_name = spellHelp.SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=sp1)
        updated_spell_name = spell_name.replace(" ", "_")
        updated_spell_name += "_cast"
        scorekeeper.ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld, event_name=updated_spell_name.lower(),
                                                             event_starting_value=0)

    if left_ear_entity > 0:
        sp2 = itemsHelp.ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=left_ear_entity)
        spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp2, slot=7, player_entity=player_entity)
        spell_name = spellHelp.SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=sp2)
        updated_spell_name = spell_name.replace(" ", "_")
        updated_spell_name += "_cast"
        scorekeeper.ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld, event_name=updated_spell_name.lower(),
                                                             event_starting_value=0)

    if right_ear_entity > 0:
        sp3 = itemsHelp.ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=right_ear_entity)
        spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp3, slot=8, player_entity=player_entity)
        spell_name = spellHelp.SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=sp3)
        updated_spell_name = spell_name.replace(" ", "_")
        updated_spell_name += "_cast"
        scorekeeper.ScorekeeperUtilities.register_scorekeeper_meta_event(gameworld=gameworld, event_name=updated_spell_name.lower(),
                                                             event_starting_value=0)


def display_jewellery_package(sx, sy, flavour_colour_content, jewellery_package):
    this_gem_details = jewelleryManagement.JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['neck'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['neck'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[1] + '    ')
    sy += 2
    this_gem_details = jewelleryManagement.JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['ring1'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['ring1'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[2] + '    ')
    sy += 2
    this_gem_details = jewelleryManagement.JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['ring2'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['ring2'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[2] + '    ')
    sy += 2
    this_gem_details = jewelleryManagement.JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['earring1'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['earring1'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[3] + '    ')
    sy += 2
    this_gem_details = jewelleryManagement.JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['earring2'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['earring2'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[3] + '    ')
