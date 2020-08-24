from bearlibterminal import terminal

from utilities import configUtilities, colourUtilities
from utilities.common import CommonUtils
from utilities.display import pointy_horizontal_menu
from utilities.input_handlers import handle_game_keys
from utilities.jewelleryManagement import JewelleryUtilities
from utilities.mobileHelp import MobileUtilities


def shopkeeper_jeweller(gameworld, shopkeeper_id):
    game_config = configUtilities.load_config()
    selected_menu_option = 0
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

    menu_options = ['Defensive', 'Balanced', 'Offensive']
    trinket_headings = ['Gemstone', 'Attribute', 'Uplift', 'Bonus']
    flavour_headings = ['pendant', 'ring', 'ring', 'earring', 'earring']
    max_menu_option = len(menu_options) - 1
    flavour_colour_string = '[color=' + colourUtilities.get('LIGHTSLATEGRAY') + ']'
    flavour_colour_content = '[color=' + colourUtilities.get('YELLOW4') + ']'

    defensive_package, balanced_package, offensive_package = JewelleryUtilities.load_jewellery_package_based_on_class(
        playable_class=player_class, game_config=game_config)

    valid_event = False
    while not valid_event:

        # intro text
        terminal.print_(x=dialog_frame_start_x + 2, y=dialog_frame_start_y + 2, width=dialog_frame_width - 5,
                        s=intro_text)

        # display package menu options
        pointy_horizontal_menu(header='', menu_options=menu_options, menu_start_x=dialog_frame_start_x + 13,
                               menu_start_y=dialog_frame_start_y + 5, selected_option=selected_menu_option,
                               colours=[colourUtilities.get('SPRINGGREEN'), colourUtilities.get('DARKOLIVEGREEN')])

        # display flavour columns
        sx = dialog_frame_start_x + 3
        sy = dialog_frame_start_y + 10
        for a in range(len(flavour_headings)):
            terminal.printf(x=sx, y=sy, s=flavour_colour_string + flavour_headings[a])
            sy += 2

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
        current_package = []
        if selected_menu_option == 0:
            current_package = defensive_package
        if selected_menu_option == 1:
            current_package = balanced_package
        if selected_menu_option == 2:
            current_package = offensive_package

        display_jewellery_package(sx=dialog_frame_start_x + 13, sy=dialog_frame_start_y + 10, flavour_colour_content=flavour_colour_content, jewellery_package=current_package)

        # blit the console
        terminal.refresh()

        event_to_be_processed, event_action = handle_game_keys()
        if event_action == 'quit':
            valid_event = True
        if event_action in ('left', 'right'):
            selected_menu_option = CommonUtils.move_menu_selection(event_action=event_action,
                                                                   selected_menu_option=selected_menu_option,
                                                                   max_menu_option=max_menu_option)
        if event_action == 'enter':
            valid_event = True
            # apply shopkeeper bonus


def display_jewellery_package(sx, sy, flavour_colour_content, jewellery_package):

    this_gem_details = JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['neck'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['neck'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[1] + '    ')
    sy += 2
    this_gem_details = JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['ring1'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['ring1'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[2] + '    ')
    sy += 2
    this_gem_details = JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['ring2'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['ring2'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[2] + '    ')
    sy += 2
    this_gem_details = JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['earring1'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['earring1'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[3] + '    ')
    sy += 2
    this_gem_details = JewelleryUtilities.get_gemstone_details(this_gemstone=jewellery_package[0]['earring2'])
    terminal.printf(x=sx, y=sy, s=flavour_colour_content + jewellery_package[0]['earring2'] + '    ')
    terminal.printf(x=sx + 10, y=sy, s=flavour_colour_content + this_gem_details[0] + '    ')
    terminal.printf(x=sx + 23, y=sy, s=flavour_colour_content + this_gem_details[3] + '    ')