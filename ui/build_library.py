from loguru import logger
from utilities import configUtilities
from utilities import colourUtilities
from utilities.input_handlers import handle_game_keys
from utilities.display import display_coloured_box, draw_colourful_frame

import tcod
import tcod.console
import tcod.event

from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities


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

    personal_info = 'You are known as Steve D a, male, witch doctor from the Dilga race.'

    playable_classes = []
    build_library_is_displayed = True
    template_position_x = saved_build_template_original_x
    saved_build_template_x = saved_build_template_original_x
    saved_cur_avatar_x = saved_build_avatar_x
    template_view_current_min = 1
    template_view_current_max = 10
    template_view_template_max = 100
    selected_template = 0
    draw_template_ui = True

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
                         msg='ESC/ to go back, up & down arrows to select, enter to accept choice')

    while build_library_is_displayed:
        if draw_template_ui:
            draw_template_ui = False
            template_box_posx = saved_build_template_original_x
            # display build library grid
            for template_id in range(1, 11):
                if template_id == selected_template:
                    fg = colourUtilities.YELLOW
                else:
                    fg = colourUtilities.GREEN

                display_coloured_box(console=build_library_console, title='',
                                     posx=template_box_posx, posy=saved_build_template_y,
                                     width=saved_build_template_width, height=saved_build_template_height,
                                     fg=fg, bg=tcod.black)

                # draw build template info/avatar here
                build_library_console.print(x=saved_cur_avatar_x, y=saved_build_avatar_y, string='NECRO',
                                            fg=fg)

                template_position_x += saved_build_template_width
                saved_cur_avatar_x += saved_build_template_width

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
            build_library_console.print(x=saved_build_template_info_x, y=saved_build_template_info_y, string=personal_info,
                                        fg=colourUtilities.BLUE)


            # display PLAY button



            build_library_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

        # handle player events
        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed != '':
            if event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    build_library_is_displayed = False

            if event_to_be_processed == 'mouse':
                pass