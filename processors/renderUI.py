import esper
from bearlibterminal import terminal
from loguru import logger
from components import mobiles, items
from mapRelated import fov
from utilities import configUtilities, mobileHelp, common
from utilities.gamemap import GameMapUtilities
from utilities.spellHelp import SpellUtilities
from static.data import constants


class RenderUI(esper.Processor):
    def __init__(self, game_map, gameworld):
        self.game_map = game_map
        self.gameworld = gameworld

    def process(self, game_config, advance_game_turn):
        # render the game map
        fov_map = self.render_map(self.gameworld, game_config, self.game_map)
        # self.render_items(game_config, self.gameworld)
        self.render_mobiles(gameworld=self.gameworld, game_config=game_config, game_map=self.game_map, fov_map=fov_map)

        # render spell effects that are living on the game map, e.g. AoE effects or necro marks or wells
        # one idea is that I store the centre of the AoE spell on the game map cell and then use that spell
        # entity reference to draw out the AoE effects
        self.render_aoe_effects(gameworld=self.gameworld, game_config=game_config, game_map=self.game_map)

    @staticmethod
    def clear_map_layer(gameworld, game_config):
        player_has_moved = mobileHelp.MobileUtilities.has_player_moved(gameworld, game_config)
        if player_has_moved:
            terminal.bkcolor('black')
            terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH), terminal.state(terminal.TK_HEIGHT))

    @staticmethod
    def render_aoe_effects(gameworld, game_config, game_map):
        colour_code = constants.COLOUR_CODES_SPELL_AOE_GENERAL_EFFECT
        camera_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='VIEWPORT_WIDTH')
        camera_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='VIEWPORT_HEIGHT')
        screen_offset_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_X')
        screen_offset_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_Y')
        aoe_top_left_corner = constants.ASCII_SINGLE_TOP_LEFT
        aoe_bottom_left_corner = constants.ASCII_SINGLE_BOTTOM_LEFT
        aoe_top_right_corner = constants.ASCII_SINGLE_TOP_RIGHT
        aoe_bottom_right_corner = constants.ASCII_SINGLE_BOTTOM_RIGHT
        aoe_horizontal = constants.ASCII_SINGLE_HORIZONTAL
        aoe_vertical = constants.ASCII_SINGLE_VERTICAL

        # this holds the start x/y map positions left of the players current position
        camera_x, camera_y = common.CommonUtils.calculate_camera_position(gameworld=gameworld,
                                                                          camera_width=camera_width,
                                                                          camera_height=camera_height,
                                                                          game_map=game_map)

        for _ in range(camera_height):
            cam_x = camera_x
            for _ in range(camera_width):
                map_x = cam_x
                map_y = camera_y
                spell_entity_list = GameMapUtilities.get_list_of_spells_at_this_map_location(game_map=game_map, x=map_x, y=map_y)
                if len(spell_entity_list) > 0:
                    for spell_entity in spell_entity_list:
                        rem_turns = SpellUtilities.get_spell_lives_for_counter(gameworld=gameworld,
                                                                               spell_entity=spell_entity)
                        aoe_central_x = SpellUtilities.get_spell_aoe_central_x(gameworld=gameworld,
                                                                               spell_entity=spell_entity)
                        aoe_central_y = SpellUtilities.get_spell_aoe_central_y(gameworld=gameworld,
                                                                               spell_entity=spell_entity)
                        if rem_turns > 0:

                            # top left
                            RenderUI.print_char_to_the_screen(print_char=99, tile=99, colour_code=colour_code,
                                                              char_to_display=aoe_top_left_corner,
                                                              scr_pos_x=(aoe_central_x + screen_offset_x) - 1,
                                                              scr_pos_y=(aoe_central_y + screen_offset_y) - 1)
                            # top middle
                            RenderUI.print_char_to_the_screen(print_char=99, tile=99, colour_code=colour_code,
                                                              char_to_display=aoe_horizontal,
                                                              scr_pos_x=(aoe_central_x + screen_offset_x),
                                                              scr_pos_y=(aoe_central_y + screen_offset_y) - 1)
                            # top right
                            RenderUI.print_char_to_the_screen(print_char=99, tile=99, colour_code=colour_code,
                                                              char_to_display=aoe_top_right_corner,
                                                              scr_pos_x=(aoe_central_x + screen_offset_x) + 1,
                                                              scr_pos_y=(aoe_central_y + screen_offset_y) - 1)
                            # middle left
                            RenderUI.print_char_to_the_screen(print_char=99, tile=99, colour_code=colour_code,
                                                              char_to_display=aoe_vertical,
                                                              scr_pos_x=(aoe_central_x + screen_offset_x) - 1,
                                                              scr_pos_y=aoe_central_y + screen_offset_y)
                            # middle right
                            RenderUI.print_char_to_the_screen(print_char=99, tile=99, colour_code=colour_code,
                                                              char_to_display=aoe_vertical,
                                                              scr_pos_x=(aoe_central_x + screen_offset_x) + 1,
                                                              scr_pos_y=aoe_central_y + screen_offset_y)
                            # bottom left
                            RenderUI.print_char_to_the_screen(print_char=99, tile=99, colour_code=colour_code,
                                                              char_to_display=aoe_bottom_left_corner,
                                                              scr_pos_x=(aoe_central_x + screen_offset_x) - 1,
                                                              scr_pos_y=(aoe_central_y + screen_offset_y) + 1)
                            # bottom middle
                            RenderUI.print_char_to_the_screen(print_char=99, tile=99, colour_code=colour_code,
                                                              char_to_display=aoe_horizontal,
                                                              scr_pos_x=aoe_central_x + screen_offset_x,
                                                              scr_pos_y=(aoe_central_y + screen_offset_y) + 1)
                            # bottom right
                            RenderUI.print_char_to_the_screen(print_char=99, tile=99, colour_code=colour_code,
                                                              char_to_display=aoe_bottom_right_corner,
                                                              scr_pos_x=(aoe_central_x + screen_offset_x) + 1,
                                                              scr_pos_y=(aoe_central_y + screen_offset_y) + 1)
                        else:
                            GameMapUtilities.remove_spell_entity_from_map_location(game_map=game_map, x=aoe_central_x, y=aoe_central_y, spell_entity=spell_entity)
                cam_x += 1
            camera_y += 1

    @staticmethod
    def render_map(gameworld, game_config, game_map):
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_DOOR')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')
        tile_type_dungeon_entrance = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_DUNGEON_ENTRANCE')
        tile_type_guard_hut = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_GUARD_HUT')

        player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld)
        player_map_pos_x = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        player_map_pos_y = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        camera_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='VIEWPORT_WIDTH')
        camera_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='VIEWPORT_HEIGHT')
        screen_offset_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_X')
        screen_offset_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_Y')

        # this holds the start x/y map positions left of the players current position
        camera_x, camera_y = common.CommonUtils.calculate_camera_position(gameworld=gameworld,
                                                                          camera_width=camera_width,
                                                                          camera_height=camera_height,
                                                                          game_map=game_map)

        config_prefix = 'ASCII_'
        config_prefix_wall = config_prefix + 'WALL_'
        original_char_to_display = constants.ASCII_DNG_EMPTY_0
        colour_code = "[color=RENDER_VISIBLE_ENTITIES_LIST]"
        fov_map = fov.FieldOfView(game_map=game_map)
        player_fov = fov.FieldOfView.create_fov_from_raycasting(fov_map, startx=player_map_pos_x, starty=player_map_pos_y,
                                                                game_config=game_config)

        RenderUI.clear_map_layer(gameworld=gameworld, game_config=game_config)

        for scr_pos_y in range(camera_height):
            cam_x = camera_x
            for scr_pos_x in range(camera_width):
                char_to_display = original_char_to_display
                map_x = cam_x
                map_y = camera_y
                print_char = False
                tile = GameMapUtilities.get_type_of_tile(game_map=game_map, x=map_x, y=map_y)
                tile_assignment = game_map.tiles[map_x][map_y].assignment
                visible = fov.FieldOfView.get_fov_map_point(player_fov, map_x, map_y)
                if visible:
                    colour_code = "[color=RENDER_VISIBLE_ENTITIES_LIST]"
                    print_char = True
                    game_map.tiles[map_x][map_y].explored = True
                    if tile == tile_type_floor:
                        char_to_display = constants.ASCII_DNG_FLOOR_0
                        colour_code = constants.COLOUR_CODES_FLOOR_INSIDE_FOV

                    if tile == tile_type_wall:
                        char_to_display = common.CommonUtils.get_unicode_ascii_char(game_config=game_config,
                                                                                    config_prefix=config_prefix_wall,
                                                                                    tile_assignment=tile_assignment)

                    if tile == tile_type_door:
                        char_to_display = constants.ASCII_DNG_DOOR_0

                    if tile == tile_type_dungeon_entrance:
                        char_to_display = constants.ASCII_DNG_GUARD_HUT

                elif game_map.tiles[map_x][map_y].explored:
                    colour_code = "[color=grey]"
                    print_char = True
                    if tile == tile_type_floor:
                        char_to_display = constants.ASCII_DNG_FLOOR_0
                        colour_code = constants.COLOUR_CODES_FLOOR_OUTSIDE_FOV
                    if tile == tile_type_wall:
                        char_to_display = common.CommonUtils.get_unicode_ascii_char(game_config=game_config,
                                                                                    config_prefix=config_prefix_wall,
                                                                                    tile_assignment=tile_assignment)
                    if tile == tile_type_door:
                        char_to_display = constants.ASCII_DNG_DOOR_0

                RenderUI.print_char_to_the_screen(print_char=print_char, tile=tile, colour_code=colour_code,
                                                  char_to_display=char_to_display,
                                                  scr_pos_x=scr_pos_x + screen_offset_x,
                                                  scr_pos_y=scr_pos_y + screen_offset_y)
                cam_x += 1
            camera_y += 1

        return player_fov


    @staticmethod
    def print_char_to_the_screen(print_char, tile, colour_code, char_to_display, scr_pos_x, scr_pos_y):
        if print_char and tile > 0:
            string_to_print = colour_code + '[' + char_to_display + ']'
            terminal.printf(x=scr_pos_x, y=scr_pos_y, s=string_to_print)

    @staticmethod
    def to_camera_coordinates(game_config, game_map, x, y, gameworld):

        camera_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='VIEWPORT_WIDTH')
        camera_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='VIEWPORT_HEIGHT')

        camera_x, camera_y = common.CommonUtils.calculate_camera_position(gameworld=gameworld,
                                                                          camera_width=camera_width,
                                                                          camera_height=camera_height,
                                                                          game_map=game_map)

        (x, y) = (x - camera_x, y - camera_y)

        if x < 0 or y < 0 or x >= camera_width or y >= camera_height:
            return -99, -99  # if it's outside the view, return nothing

        return int(x), int(y)

    @staticmethod
    def render_mobiles(game_config, gameworld, game_map, fov_map):
        player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld)
        visible_entities = []
        screen_offset_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_X')
        screen_offset_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='SCREEN_OFFSET_Y')

        for ent, (rend, pos, dialog) in gameworld.get_components(mobiles.Renderable, mobiles.Position,
                                                                 mobiles.DialogFlags):
            if rend.is_visible:
                flag_setting = ''
                display_char = mobileHelp.MobileUtilities.get_mobile_glyph(gameworld=gameworld, entity=ent)
                x = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=ent)
                y = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=ent)
                visible = fov.FieldOfView.get_fov_map_point(fov_map, x, y)
                if visible:
                    (x, y) = RenderUI.to_camera_coordinates(game_config=game_config, game_map=game_map, x=x, y=y,
                                                            gameworld=gameworld)
                    if x != -99:
                        fg = mobileHelp.MobileUtilities.get_mobile_fg_render_colour(gameworld=gameworld, entity=ent)
                        bg = mobileHelp.MobileUtilities.get_mobile_bg_render_colour(gameworld=gameworld, entity=ent)
                        if dialog.talk_to_me:
                            flag_setting = 'talk_to_me'
                        RenderUI.render_entity(posx=x + screen_offset_x, posy=y + screen_offset_y, glyph=display_char,
                                               fg=fg, bg=bg, flag=flag_setting)
                        if ent != player_entity:
                            visible_entities.append(ent)

        mobileHelp.MobileUtilities.set_ai_visible_entities(gameworld=gameworld, target_entity=player_entity,
                                                           visible_entities=visible_entities)

    @staticmethod
    def render_items(game_config, gameworld):
        map_view_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='MAP_VIEW_DRAW_X')
        map_view_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='MAP_VIEW_DRAW_Y')
        for ent, (rend, loc) in gameworld.get_components(items.RenderItem, items.Location):
            if rend.is_true:
                draw_pos_x = map_view_across + loc.x
                draw_pos_y = map_view_down + loc.y
                display_char = mobileHelp.MobileUtilities.get_mobile_glyph(gameworld=gameworld, entity=ent)
                fg = mobileHelp.MobileUtilities.get_mobile_fg_render_colour(gameworld=gameworld, entity=ent)
                bg = mobileHelp.MobileUtilities.get_mobile_bg_render_colour(gameworld=gameworld, entity=ent)
                RenderUI.render_entity(posx=draw_pos_x, posy=draw_pos_y, glyph=display_char, fg=fg, bg=bg)

    @staticmethod
    def render_entity(posx, posy, glyph, fg, bg, flag=None):
        str_to_print = "[color=" + str(fg) + "][font=dungeon][bkcolor=" + str(bg) + "]" + glyph
        if flag == 'talk_to_me':
            str_to_print += "[offset=0, -8][+][color=red]^[/color]"
        terminal.printf(x=posx, y=posy, s=str_to_print)
