import esper
import time

from bearlibterminal import terminal
from loguru import logger

from components import mobiles, items
from mapRelated.fov import FieldOfView
from utilities import configUtilities, formulas
from utilities.mobileHelp import MobileUtilities
from utilities.common import CommonUtils


class RenderUI(esper.Processor):
    def __init__(self, game_map, gameworld):
        self.game_map = game_map
        self.gameworld = gameworld

    def process(self, game_config):
        start_time = time.perf_counter()
        # render the game map
        fov_map = self.render_map(self.gameworld, game_config, self.game_map)
        self.render_items(game_config, self.gameworld)
        visible_entities = self.render_mobiles(gameworld=self.gameworld, game_config=game_config, fov_map=fov_map)

        if len(visible_entities) > 0:
            self.render_entity_display_panel(gameworld=self.gameworld, game_config=game_config,
                                             visible_entities=visible_entities)

        end_time = time.perf_counter()
        logger.info('Time taken to render game display {}', (end_time - start_time))

    @staticmethod
    def clear_map_layer():
        terminal.bkcolor('black')
        terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH), terminal.state(terminal.TK_HEIGHT))

    @staticmethod
    def render_entity_display_panel(gameworld, game_config, visible_entities):

        # right hand side divider
        for dy in range(47):
            terminal.printf(x=62, y=dy, s="[color=red][font=dungeon]▒")

        image_start_x_pos = 64
        entity_y_draw_pos = 4
        str_colour_msg = "[color="

        str_to_print = "[color=white]" + "Visible Entities"
        terminal.printf(x=64, y=1, s=str_to_print)

        for entity in visible_entities:
            glyph = MobileUtilities.get_mobile_glyph(gameworld=gameworld, entity=entity)
            fg = MobileUtilities.get_mobile_fg_render_colour(gameworld=gameworld, entity=entity)
            bg = MobileUtilities.get_mobile_bg_render_colour(gameworld=gameworld, entity=entity)
            list_of_conditions = MobileUtilities.get_current_condis_applied_to_mobile(
                gameworld=gameworld, entity=entity)
            list_of_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld,
                                                                                entity=entity)
            current_health = MobileUtilities.get_mobile_derived_current_health(gameworld=gameworld, entity=entity)
            maximum_health = MobileUtilities.get_mobile_derived_maximum_health(gameworld=gameworld, entity=entity)

            display_percentage = formulas.calculate_percentage(low_number=current_health, max_number=maximum_health)

            str_to_print = str_colour_msg + fg + "][font=dungeon][bkcolor=" + bg + "]" + glyph + ' '
            str_colour = "red"
            if display_percentage > 89:
                str_colour = "green"
            elif 90 > display_percentage > 30:
                str_colour = "orange"
            str_to_print += str_colour_msg + str_colour + "]H:" + str(display_percentage) + "% "
            if len(list_of_boons) > 0:
                str_to_print += "[color=green]b:[/color]"
                for boon in list_of_boons:
                    str_colour += boon['displayChar']
                str_to_print += " [/color]"

            if len(list_of_conditions) > 0:
                str_to_print += "[color=red]c:"
                for condition in list_of_conditions:
                    str_to_print += condition['displayChar']
                str_to_print += "[/color]"

            terminal.printf(x=image_start_x_pos, y=entity_y_draw_pos, s=str_to_print)
            entity_y_draw_pos += 1

    @staticmethod
    def render_map(gameworld, game_config, game_map):
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_DOOR')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')

        player_has_moved = MobileUtilities.has_player_moved(gameworld, game_config)
        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        player_map_pos_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        player_map_pos_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        hardcoded_zoom_factor = 10
        hardcoded_viewport_margin = 10

        vp_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_WIDTH')
        vp_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_HEIGHT')
        vp_x_offset = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_START_X')
        vp_y_offset = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_START_Y')

        map_width = game_map.width
        map_x_max = min(player_map_pos_x + vp_width, map_width)

        viewport_from_x = int(player_map_pos_x - (vp_width / 2))
        viewport_to_x = int(player_map_pos_x + (vp_width / 2))
        viewport_from_y = int(player_map_pos_y - (vp_height / 2))
        viewport_to_y = int(player_map_pos_y + (vp_height / 2))

        if viewport_from_x < 0:
            viewport_from_x = 0

        if viewport_from_y < 0:
            viewport_from_y = 0


        config_prefix = 'ASCII_'
        config_prefix_wall = config_prefix + 'WALL_'
        config_prefix_floor = config_prefix + 'FLOOR_'
        config_prefix_door = config_prefix + 'DOOR_'
        char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_floor, tile_assignment=0)
        unicode_string_to_print = '[font=dungeon]['
        colour_code = "[color=black]"
        fov_map = FieldOfView(game_map=game_map)
        player_fov = FieldOfView.create_fov_map_via_raycasting(fov_map, startx=player_map_pos_x, starty=player_map_pos_y,
                                                               game_config=game_config)

        if player_has_moved:
            RenderUI.clear_map_layer()

        # the loops display the MAP tiles surrounding the player
        for y in range(viewport_from_y, viewport_to_y):
            for x in range(viewport_from_x, viewport_to_x):
                if x < map_x_max:
                    print_char = False
                    tile = game_map.tiles[x][y].type_of_tile
                    tile_assignment = game_map.tiles[x][y].assignment
                    visible = FieldOfView.get_fov_map_point(player_fov, x, y)
                    if visible:
                        print_char = True
                        colour_code = "[color=white]"
                        game_map.tiles[x][y].explored = True
                        if tile == tile_type_floor:
                            char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_floor, tile_assignment=0)
                        if tile == tile_type_wall:
                            char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_wall, tile_assignment=tile_assignment)
                        if tile == tile_type_door:
                            char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_door, tile_assignment=0)
                    elif game_map.tiles[x][y].explored:
                        colour_code = "[color=grey]"
                        print_char = True
                        if tile == tile_type_floor:
                            char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_floor, tile_assignment=0)
                        if tile == tile_type_wall:
                            char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_wall, tile_assignment=tile_assignment)
                        if tile == tile_type_door:
                            char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_door, tile_assignment=0)

                    if print_char and tile > 0:
                        str = colour_code + unicode_string_to_print + char_to_display + ']'
                        terminal.printf(x=vp_x_offset + x, y=vp_y_offset + y, s=str)
        return player_fov

    @staticmethod
    def render_mobiles(game_config, gameworld, fov_map):
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        visible_entities = []
        vp_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_START_Y')

        vp_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_WIDTH')

        for ent, (rend, pos, desc) in gameworld.get_components(mobiles.Renderable, mobiles.Position,
                                                               mobiles.Describable):
            if rend.isVisible:
                map_pos_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=ent)
                map_pos_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=ent)
                fg = desc.foreground
                bg = desc.background
                if FieldOfView.get_fov_map_point(fov_map, map_pos_x, map_pos_y):
                    if map_pos_x > vp_width:
                        mpx = int(map_pos_x / vp_width)
                    else:
                        mpx = map_pos_x
                    RenderUI.render_entity(posx=mpx, posy=vp_height + map_pos_y, glyph=desc.glyph, fg=fg, bg=bg)
                    if ent != player_entity:
                        visible_entities.append(ent)

        MobileUtilities.set_visible_entities(gameworld=gameworld, target_entity=player_entity, visible_entities=visible_entities)
        return visible_entities

    @staticmethod
    def render_items(game_config, gameworld):
        map_view_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='MAP_VIEW_DRAW_X')
        map_view_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='MAP_VIEW_DRAW_Y')
        for ent, (rend, loc, desc) in gameworld.get_components(items.RenderItem, items.Location, items.Describable):
            if rend.isTrue:
                draw_pos_x = map_view_across + loc.x
                draw_pos_y = map_view_down + loc.y
                RenderUI.render_entity(posx=draw_pos_x, posy=draw_pos_y, glyph=desc.glyph, fg=desc.fg, bg=desc.bg, )

    @staticmethod
    def render_entity(posx, posy, glyph, fg, bg):

        str_to_print = "[color=" + fg + "][font=dungeon][bkcolor=" + bg + "]" + glyph
        terminal.printf(x=posx, y=posy, s=str_to_print)
