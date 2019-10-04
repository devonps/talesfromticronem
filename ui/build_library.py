from loguru import logger
from utilities import configUtilities, colourUtilities
from utilities.buildLibrary import BuildLibrary
from utilities.externalfileutilities import Externalfiles
from utilities.input_handlers import handle_game_keys
from utilities.display import display_coloured_box, draw_colourful_frame, draw_clear_text_box
from utilities.jsonUtilities import read_json_file
import tcod
import tcod.console
import tcod.event


class Build:
    BUILDRACE = 0
    BUILDCLASS = 1
    BUILDJEWELLERY = 2
    BUILDMAINHAND = 3
    BUILDOFFHAND = 4
    BUILDARMOUR = 5
    BUILDGENDER = 6


def display_build_library(root_console):

    game_config = configUtilities.load_config()

    build_library_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_WIDTH')
    build_library_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_HEIGHT')
    build_library_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_FRAME_X')
    build_library_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_FRAME_Y')
    build_library_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame','BUILD_LIBRARY_FRAME_WIDTH')
    build_library_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame','BUILD_LIBRARY_FRAME_HEIGHT')
    player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',parameter='CLASSESFILE')
    saved_build_template_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_WIDTH')
    saved_build_template_height = configUtilities.get_config_value_as_integer(game_config, 'newgame','BUILD_LIBRARY_TEMPLATE_HEIGHT')
    saved_build_template_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_Y')
    saved_build_template_original_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_X')
    saved_build_pagination_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PAGINATION_X')
    saved_build_pagination_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PAGINATION_Y')
    saved_build_class_filter_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_CLASS_FILTER_X')
    saved_build_class_filter_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_CLASS_FILTER_Y')
    saved_build_page_min_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PAGE_MIN_X')
    saved_build_page_max_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PAGE_MAX_X')
    saved_build_template_info_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_INFO_X')
    saved_build_template_info_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_INFO_Y')
    saved_build_avatar_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_AVATAR_X')
    saved_build_avatar_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_AVATAR_Y')
    saved_build_code_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_CODE_X')
    saved_build_code_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_CODE_Y')
    saved_build_play_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PLAY_X')
    saved_build_play_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PLAY_Y')
    fileName = configUtilities.get_config_value_as_string(game_config, 'default', 'BUILDLIBRARYFILE')

    personal_info = 'You are known as '

    playable_classes = []
    build_library_is_displayed = True
    template_position_x = saved_build_template_original_x
    saved_build_template_x = saved_build_template_original_x
    saved_cur_avatar_x = saved_build_avatar_x
    selected_build = 0
    build_grid_selected = 1
    draw_template_ui = True
    build_codes = []
    build_names = []
    build_dates = []
    build_times = []
    decoded_build = []
    buildCount = 0
    template_view_current_min = 1
    buildZoneLeft = 0
    buildZoneRight = 1
    buildZoneTop = 2
    buildZoneBottom = 3
    buildZoneXOffset = 5
    buildZoneYOffset = 5

    # load saved builds
    buildContent = Externalfiles.load_existing_file(filename=fileName)
    for row in buildContent:
        elements = row.split(':')
        build_codes.append(elements[0])
        build_names.append(elements[1])
        build_dates.append(elements[2])
        build_times.append(elements[3])
        decoded_build.append(BuildLibrary.decode_saved_build(build_codes[buildCount]))
        buildCount += 1

    personal_info += build_names[selected_build] + 'a ' + decoded_build[selected_build][Build.BUILDGENDER] + ' ' + decoded_build[selected_build][Build.BUILDCLASS]
    personal_info += ' from the ' + decoded_build[selected_build][Build.BUILDRACE] + '.'
    personal_info += ' You are wearing ' + decoded_build[selected_build][Build.BUILDARMOUR] + ' armour and a '
    personal_info += decoded_build[selected_build][Build.BUILDJEWELLERY] + ' set of jewellery.'

    if decoded_build[selected_build][Build.BUILDMAINHAND] == decoded_build[selected_build][Build.BUILDOFFHAND]:
        personal_info += ' You are wielding a ' + decoded_build[selected_build][Build.BUILDMAINHAND] + ' in both hands.'
    else:
        personal_info += ' You are wielding a ' + decoded_build[selected_build][Build.BUILDMAINHAND] + ' in your main hand'
        personal_info += ' and a ' + decoded_build[selected_build][Build.BUILDOFFHAND] + ' in your off hand.'

    if buildCount < 10:
        template_view_current_max = buildCount
    else:
        template_view_current_max = 10
    template_view_template_max = buildCount

    # load playable classes
    class_file = read_json_file(player_class_file)
    playable_classes.append('List Only...')
    playable_classes.append('all')
    for option in class_file['classes']:
        playable_classes.append(option['name'])

    # build library console
    build_library_console = tcod.console.Console(width=build_library_width, height=build_library_height, order='F')

    # build library frame around console
    draw_colourful_frame(console=build_library_console, game_config=game_config,
                         startx=build_library_frame_x, starty=build_library_frame_y,
                         width=build_library_frame_width,
                         height=build_library_frame_height,
                         title='[ Character Build Library ]', title_loc='centre',
                         title_decorator=False,
                         corner_decorator='', corner_studs='square',
                         msg='ESC/ to go back, mouse to select.')

    while build_library_is_displayed:
        if draw_template_ui:
            draw_template_ui = False
            build_zones = []
            template_box_posx = saved_build_template_original_x
            # display build library grid
            for template_id in range(template_view_current_min, template_view_current_max + 1):
                if template_id == build_grid_selected:
                    fg = colourUtilities.YELLOW
                else:
                    fg = colourUtilities.GREEN

                display_coloured_box(console=build_library_console, title='',
                                     posx=template_box_posx, posy=saved_build_template_y,
                                     width=saved_build_template_width, height=saved_build_template_height,
                                     fg=fg, bg=tcod.black)
                build_zones.append((buildZoneXOffset + template_box_posx, buildZoneXOffset + template_box_posx + 8,
                                    buildZoneYOffset + saved_build_template_y, buildZoneYOffset + saved_build_template_y + 8))
                # draw build template info/avatar here
                if template_id < buildCount + 1:
                    build_library_console.print(x=saved_cur_avatar_x, y=saved_build_avatar_y, string=build_names[template_id - 1],
                                                fg=fg)

                template_position_x += saved_build_template_width
                saved_cur_avatar_x += saved_build_template_width
                logger.info('Build Zones {}', build_zones)
                if template_id == 5:
                    saved_build_template_y += saved_build_template_height
                    template_position_x = saved_build_template_x
                    saved_cur_avatar_x = saved_build_avatar_x
                    saved_build_avatar_y += saved_build_template_height

                template_box_posx = template_position_x

            # display pagination
            page_string = 'Showing ' + \
                          str(template_view_current_min) + '-' + \
                          str(template_view_current_max) + ' of ' + \
                          str(template_view_template_max)
            build_library_console.print(x=saved_build_pagination_x, y=saved_build_pagination_y, string=page_string,
                                        fg=colourUtilities.YELLOW1)

            if template_view_current_min > 1:
                build_library_console.print(x=saved_build_page_min_x, y=saved_build_pagination_y, string='PREV PAGE',
                                            fg=colourUtilities.BLUE)

            if template_view_template_max > template_view_current_max:
                build_library_console.print(x=saved_build_page_max_x, y=saved_build_pagination_y, string='NEXT PAGE',
                                            fg=colourUtilities.YELLOW)

            # display class filter options
            for clfilter in range(len(playable_classes)):
                build_library_console.print(x=saved_build_class_filter_x, y=saved_build_class_filter_y + clfilter, string=playable_classes[clfilter],
                                            fg=colourUtilities.BLUE)

            # display selected build template info

            draw_clear_text_box(console=build_library_console,
                                posx=saved_build_template_info_x, posy=saved_build_template_info_y,
                                width=70, height=3,
                                text=personal_info,
                                fg=colourUtilities.BLUE, bg=colourUtilities.BLACK)

            # display build code
            build_library_console.print(x=saved_build_code_x, y=saved_build_code_y, string='BUILD CODE: ' + build_codes[selected_build],
                                        fg=colourUtilities.YELLOW)

            # display PLAY button
            bz = len(build_zones) + 1
            build_zones.append((buildZoneXOffset + saved_build_play_x, buildZoneXOffset + saved_build_play_x + len('START GAME') - 1, saved_build_play_y + 4, (saved_build_play_y + 4) + 1))
            build_library_console.print(x=saved_build_play_x, y=saved_build_play_y, string='START GAME',
                                        fg=colourUtilities.RED)

            # blit to the root console
            build_library_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

        # handle player events
        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed != '':
            if event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    build_library_is_displayed = False

            if event_to_be_processed == 'mousebutton':
                if event_action[0] == 'left':
                    mx = event_action[1]
                    my = event_action[2]
                    logger.info('Mouse x {} ' + str(mx))
                    logger.info('Mouse y {} ' + str(my))
                    for zone in range(len(build_zones)):
                        if build_zones[zone][buildZoneLeft] <= mx <= build_zones[zone][buildZoneRight]:
                            if build_zones[zone][buildZoneTop] <= my <= build_zones[zone][buildZoneBottom]:
                                logger.info('Zone {} clicked', zone)

