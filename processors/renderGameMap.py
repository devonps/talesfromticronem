import esper

from bearlibterminal import terminal

from components import mobiles, items
from utilities import configUtilities
from utilities.display import create_display_area
from utilities.mobileHelp import MobileUtilities
from utilities.common import CommonUtils
from utilities.spellHelp import SpellUtilities


class RenderGameMap(esper.Processor):
    def __init__(self, game_map, gameworld):
        self.game_map = game_map
        self.gameworld = gameworld

    def process(self, game_config):
        """
        Rendering during actual gameplay

        Render Order:
        1. game map                 dungeon floors, walls, furniture, spell effects??
        2. Entities                 player, enemies, items, etc
        3. HUD                      hp, mana, f1 bars, hotkeys, etc
        4. Spellbar                 spell bar
        5. Player status effects    effects player is suffering from

        """
        terminal.clear()
        # render the game map
        self.render_map(self.gameworld, game_config, self.game_map)
        # draw the entities
        # self.render_items(game_config, self.gameworld)
        visible_entities = self.render_mobiles(game_config, self.gameworld, self.game_map)
        if len(visible_entities) > 0:
            self.render_entity_display_panel(gameworld=self.gameworld, game_config=game_config,
                                             visible_entities=visible_entities)

        # GUI viewport
        terminal.composition(terminal.TK_ON)
        self.render_statusbox(game_config)

        self.render_player_status_effects(gameworld=self.gameworld, game_config=game_config)
        self.render_spell_bar(self, game_config=game_config)
        self.render_player_vitals(gameworld=self.gameworld, game_config=game_config)
        terminal.composition(terminal.TK_OFF)

    @staticmethod
    def clear_map_layer():
        terminal.bkcolor('black')
        terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH), terminal.state(terminal.TK_HEIGHT))


    @staticmethod
    def render_entity_display_panel(gameworld, game_config, visible_entities):
        render_style = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='render_style')

        # right hand side divider
        for dy in range(47):
            terminal.printf(x=62, y=dy, s="[color=red][font=dungeon]▒")

        image_start_x_pos = 64
        entity_y_draw_pos = 4
        str_colour_msg = "[color="

        if render_style == 1:

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
                current_health = MobileUtilities.get_derived_current_health(gameworld=gameworld, entity=entity)
                maximum_health = MobileUtilities.get_derived_maximum_health(gameworld=gameworld, entity=entity)

                display_percentage = CommonUtils.calculate_percentage(low_number=current_health, max_number=maximum_health)

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

        render_style = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='render_style')
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_DOOR')
        player_has_moved = MobileUtilities.has_player_moved(gameworld, game_config)
        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        viewport_id = MobileUtilities.get_viewport_id(gameworld=gameworld, entity=player_entity)
        player_pos_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player_entity)
        player_pos_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player_entity)

        if render_style == 1:
            # display ascii

            vp_width = CommonUtils.get_viewport_width(gameworld=gameworld, viewport_id=viewport_id)
            vp_height = CommonUtils.get_viewport_height(gameworld=gameworld, viewport_id=viewport_id)
            vp_x_mmin = CommonUtils.get_viewport_x_axis_min_value(gameworld=gameworld, viewport_id=viewport_id)
            vp_y_min = CommonUtils.get_viewport_y_axis_min_value(gameworld=gameworld, viewport_id=viewport_id)

            x_min = max(player_pos_x - vp_width, vp_x_mmin)
            x_max = min(player_pos_x + vp_width, game_map.width)
            y_min = max(player_pos_y - vp_height, vp_y_min)
            y_max = min(player_pos_y + vp_height, game_map.height)
            config_prefix = 'ASCII_'
            config_prefix_wall = config_prefix + 'WALL_'
            config_prefix_floor = config_prefix + 'FLOOR_'
            config_prefix_door = config_prefix + 'DOOR_'
            blank_tile = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_floor, tile_assignment=0)
            unicode_string_to_print = '[font=dungeon]['
            if player_has_moved:
                RenderGameMap.clear_map_layer()

            scry = player_pos_y
            for y in range(y_min, y_max):
                scrx = player_pos_x
                for x in range(x_min, x_max):
                    tile = game_map.tiles[x][y].type_of_tile
                    tile_assignment = game_map.tiles[x][y].assignment
                    char_to_display = blank_tile
                    if tile == tile_type_wall:
                        char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_wall, tile_assignment=tile_assignment)
                    if tile == tile_type_door:
                        char_to_display = CommonUtils.get_unicode_ascii_char(game_config=game_config, config_prefix=config_prefix_door, tile_assignment=0)

                    if tile > 0:
                        str = unicode_string_to_print + char_to_display + ']'
                        terminal.printf(x=x, y=y, s=str)
                    scrx += 1
                scry += 1
        else:
            image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='map_Xscale')
            image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='map_Yscale')
            y_offset = 0
            x_offset = 0

            x_min, x_max, y_min, y_max = RenderGameMap.get_viewport_boundary(gameworld=gameworld,
                                                                             player_entity=player_entity)
            if player_has_moved:
                RenderGameMap.clear_map_layer()

            scry = 0

            for y in range(y_min, y_max):
                scrx = 0
                for x in range(x_min, x_max):
                    image = game_map.tiles[x][y].image
                    tile = game_map.tiles[x][y].type_of_tile
                    if tile > 0:
                        terminal.put(x=(scrx + x_offset) * image_x_scale, y=(scry + y_offset) * image_y_scale,
                                     c=0xE300 + image)
                    scrx += 1
                scry += 1

    @staticmethod
    def get_viewport_boundary(gameworld, player_entity):

        viewport_id = MobileUtilities.get_viewport_id(gameworld=gameworld, entity=player_entity)

        xmin = CommonUtils.get_viewport_x_axis_min_value(gameworld=gameworld, viewport_id=viewport_id)
        xmax = CommonUtils.get_viewport_x_axis_max_value(gameworld=gameworld, viewport_id=viewport_id)

        right_boundary_visited = CommonUtils.get_viewport_right_boundary(gameworld=gameworld, viewport_id=viewport_id)
        left_boundary_visited = CommonUtils.get_viewport_left_boundary(gameworld=gameworld, viewport_id=viewport_id)
        viewport_player_position = CommonUtils.get_player_viewport_position_info(gameworld=gameworld,
                                                                                 viewport_id=viewport_id)
        vpx = viewport_player_position[0]

        # current 'scrolling' method is to simply add +5 to both the min and max values of the viewport

        scroll_amount = 5

        if right_boundary_visited:
            if xmax + scroll_amount < 42:
                CommonUtils.set_viewport_x_axis_min_value(gameworld=gameworld, viewport_id=viewport_id,
                                                          value=xmin + scroll_amount)
                CommonUtils.set_viewport_x_axis_max_value(gameworld=gameworld, viewport_id=viewport_id,
                                                          value=xmax + scroll_amount)
                CommonUtils.set_viewport_right_boundary_visited_false(gameworld=gameworld, viewport_id=viewport_id)

                CommonUtils.set_player_viewport_position_x(gameworld=gameworld, viewport_id=viewport_id,
                                                           posx=vpx - scroll_amount)

        if left_boundary_visited:
            if xmin - scroll_amount == 0:
                CommonUtils.set_viewport_x_axis_min_value(gameworld=gameworld, viewport_id=viewport_id,
                                                          value=xmin - scroll_amount)
                CommonUtils.set_viewport_x_axis_max_value(gameworld=gameworld, viewport_id=viewport_id,
                                                          value=xmax - scroll_amount)
                CommonUtils.set_viewport_left_boundary_visited_false(gameworld=gameworld, viewport_id=viewport_id)

                CommonUtils.set_player_viewport_position_x(gameworld=gameworld, viewport_id=viewport_id,
                                                           posx=vpx + scroll_amount)

        viewport_x_min = CommonUtils.get_viewport_x_axis_min_value(gameworld=gameworld, viewport_id=viewport_id)
        viewport_x_max = CommonUtils.get_viewport_x_axis_max_value(gameworld=gameworld, viewport_id=viewport_id)

        viewport_y_min = CommonUtils.get_viewport_y_axis_min_value(gameworld=gameworld, viewport_id=viewport_id)
        viewport_y_max = CommonUtils.get_viewport_y_axis_max_value(gameworld=gameworld, viewport_id=viewport_id)

        return viewport_x_min, viewport_x_max, viewport_y_min, viewport_y_max

    @staticmethod
    def render_mobiles(game_config, gameworld, game_map):

        render_style = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='render_style')
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        # terminal.layer(RenderLayer.ENTITIES.value)
        draw_pos_x = 0
        draw_pos_y = 0
        visible_entities = []

        if render_style == 1:
            x_min, x_max, y_min, y_max = create_display_area(gameworld=gameworld,
                                                                         player_entity=player_entity, game_map=game_map)

            for ent, (rend, pos, desc) in gameworld.get_components(mobiles.Renderable, mobiles.Position,
                                                                   mobiles.Describable):
                if rend.isVisible:
                    draw_pos_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=ent)
                    draw_pos_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=ent)
                    fg = desc.foreground
                    bg = desc.background
                    if x_min <= draw_pos_x <= x_max:
                        if y_min <= draw_pos_y <= y_max:
                            RenderGameMap.render_entity(draw_pos_x, draw_pos_y, desc.glyph, 0, 0, render_style, fg, bg)
                            if ent != player_entity:
                                visible_entities.append(ent)
        else:
            image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='map_Xscale')
            image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='map_Yscale')

            # pos.x represents the game map position and should be used to check for map obstructions only

            viewport_id = MobileUtilities.get_viewport_id(gameworld=gameworld, entity=player_entity)
            viewport_width = CommonUtils.get_viewport_width(gameworld=gameworld, viewport_id=viewport_id)
            viewport_player_position = CommonUtils.get_player_viewport_position_info(gameworld=gameworld,
                                                                                     viewport_id=viewport_id)

            vpx = viewport_player_position[0]
            vpy = viewport_player_position[1]

            for ent, (rend, pos, desc) in gameworld.get_components(mobiles.Renderable, mobiles.Position,
                                                                   mobiles.Describable):
                if rend.isVisible:
                    if ent == player_entity:
                        if vpx > viewport_width:
                            vpx = viewport_width
                        draw_pos_x = vpx
                        draw_pos_y = vpy
                    RenderGameMap.render_entity(draw_pos_x, draw_pos_y, desc.image, image_x_scale, image_y_scale,
                                                render_style)

        return visible_entities

    @staticmethod
    def render_items(game_config, gameworld):
        map_view_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='MAP_VIEW_DRAW_X')
        map_view_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='MAP_VIEW_DRAW_Y')
        render_style = 1
        for ent, (rend, loc, desc) in gameworld.get_components(items.RenderItem, items.Location, items.Describable):
            if rend.isTrue:
                draw_pos_x = map_view_across + loc.x
                draw_pos_y = map_view_down + loc.y
                RenderGameMap.render_entity(draw_pos_x, draw_pos_y, desc.glyph, desc.fg, desc.bg, render_style)

    @staticmethod
    def render_entity(posx, posy, glyph, image_x_scale, image_y_scale, render_style, fg, bg):

        if render_style == 1:
            str_to_print = "[color=" + fg + "][font=dungeon][bkcolor=" + bg + "]" + glyph
            terminal.printf(x=posx, y=posy, s=str_to_print)
        else:
            cloak = 21
            robe = 22
            shoes = 23
            weapon = 24
            characterbits = [cloak, glyph, robe, shoes, weapon]

            for cell in characterbits:
                terminal.put(x=posx * image_x_scale, y=posy * image_y_scale, c=0xE300 + cell)

    @staticmethod
    def render_statusbox(game_config):

        statusbox_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='STATUSBOX_WIDTH')
        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')



        left_x = 1

        # top left
        terminal.put(x=left_x, y=statusbox_height * image_y_scale, c=0xE700 + 0)

        # left edge
        for d in range(left_x, 5):
            terminal.put(x=left_x, y=(statusbox_height + d) * image_y_scale, c=0xE700 + 4)

        # bottom left
        terminal.put(x=left_x, y=(statusbox_height + 5) * image_y_scale, c=0xE700 + 2)

        # top right
        terminal.put(x=(statusbox_width) * image_x_scale, y=statusbox_height * image_y_scale, c=0xE700 + 1)

        # bottom right
        terminal.put(x=(statusbox_width) * image_x_scale, y=(statusbox_height + 5) * image_y_scale, c=0xE700 + 3)

        # top edge
        for a in range(left_x, statusbox_width):
            terminal.put(x=a * image_x_scale, y=statusbox_height * image_y_scale, c=0xE700 + 6)

        # right edge
        for d in range(1, 5):
            terminal.put(x=statusbox_width * image_x_scale, y=(statusbox_height + d) * image_y_scale, c=0xE700 + 5)

        # bottom edge
        for a in range(left_x, statusbox_width):
            terminal.put(x=a * image_x_scale, y=(statusbox_height + 5) * image_y_scale, c=0xE700 + 7)

        # terminal.layer(prev_layer)

    @staticmethod
    def render_message_panel(game_config):
        message_panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                          parameter='MSG_PANEL_WIDTH')
        message_panel_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                           parameter='MSG_PANEL_START_Y')

        message_panel_start_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                            parameter='MSG_PANEL_START_X')
        message_panel_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                          parameter='MSG_PANEL_DEPTH')

        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')

        # top left
        terminal.put(x=(message_panel_start_x * image_x_scale), y=message_panel_height * image_y_scale, c=0xE700 + 0)

        # left edge
        for d in range(message_panel_depth):
            terminal.put(x=(message_panel_start_x * image_x_scale), y=(message_panel_height + d) * image_y_scale,
                         c=0xE700 + 4)

        # bottom left
        terminal.put(x=(message_panel_start_x * image_x_scale), y=(message_panel_height + 5) * image_y_scale,
                     c=0xE700 + 2)

        # top right
        terminal.put(x=(message_panel_start_x * image_x_scale) + message_panel_width,
                     y=message_panel_height * image_y_scale, c=0xE700 + 1)

        # bottom right
        terminal.put(x=(message_panel_start_x * image_x_scale) + message_panel_width,
                     y=(message_panel_height + 5) * image_y_scale, c=0xE700 + 3)

        # top edge
        for a in range(message_panel_width):
            terminal.put(x=a + (message_panel_start_x * image_x_scale), y=message_panel_height * image_y_scale,
                         c=0xE700 + 6)

        # right edge
        for d in range(message_panel_depth):
            terminal.put(x=message_panel_start_x * image_x_scale + message_panel_width,
                         y=(message_panel_height + d) * image_y_scale, c=0xE700 + 5)

        # bottom edge
        for a in range(message_panel_width):
            terminal.put(x=a + (message_panel_start_x * image_x_scale), y=(message_panel_height + 5) * image_y_scale,
                         c=0xE700 + 7)

        # now show the messages

        # terminal.layer(prev_layer)

    @staticmethod
    def render_player_status_effects(gameworld, game_config):
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        player_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld, entity=player_entity)
        player_conditions = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld,
                                                                                 entity=player_entity)

        RenderGameMap.render_boons(posx=1, posy=statusbox_height * image_y_scale, list_of_boons=player_boons)
        RenderGameMap.render_conditions(posx=11, posy=statusbox_height * image_y_scale,
                                        list_of_conditions=player_conditions)

    @staticmethod
    def render_boons(posx, posy, list_of_boons):
        image_count = 0
        image_scale_factor = 2

        for boon in list_of_boons:
            boon_image_id = int(boon['image'])
            terminal.put(x=(posx + image_count) * image_scale_factor, y=posy, c=0xE600 + boon_image_id)
            image_count += 1

    @staticmethod
    def render_conditions(posx, posy, list_of_conditions):

        image_count = 0
        image_scale_factor = 2

        for condition in list_of_conditions:
            condition_image_id = int(condition['image'])
            terminal.put(x=(posx + image_count) * image_scale_factor, y=posy, c=0xE630 + condition_image_id)
            image_count += 1

    @staticmethod
    def render_player_vitals(gameworld, game_config):

        RenderGameMap.render_health(gameworld=gameworld, game_config=game_config)
        RenderGameMap.render_mana(gameworld=gameworld, game_config=game_config)
        RenderGameMap.render_special_power(gameworld=gameworld, game_config=game_config)

    @staticmethod
    def render_health(gameworld, game_config):
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        current_health = MobileUtilities.get_derived_current_health(gameworld=gameworld, entity=player_entity)
        maximum_health = MobileUtilities.get_derived_maximum_health(gameworld=gameworld, entity=player_entity)

        str_to_print = "[color=red]Health[/color]"

        RenderGameMap.render_bar(print_string=str_to_print, low_number=current_health, high_number=maximum_health,
                                 posy=statusbox_height + 3, posx=6, sprite_ref=0xE770,
                                 xscale=image_x_scale, yscale=image_y_scale)

    @staticmethod
    def render_mana(gameworld, game_config):

        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        current_mana = MobileUtilities.get_derived_current_mana(gameworld=gameworld, entity=player_entity)
        max_mana = MobileUtilities.get_derived_maximum_mana(gameworld=gameworld, entity=player_entity)
        str_to_print = "[color=blue]Mana[/color]"

        RenderGameMap.render_bar(print_string=str_to_print, low_number=current_mana, high_number=max_mana,
                                 posy=statusbox_height + 4, posx=6, sprite_ref=0xE800,
                                 xscale=image_x_scale, yscale=image_y_scale)

    @staticmethod
    def render_special_power(gameworld, game_config):
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                       parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        current_f1_power = MobileUtilities.get_derived_special_bar_current_value(gameworld=gameworld,
                                                                               entity=player_entity)
        max_f1_power = MobileUtilities.get_derived_special_bar_max_value(gameworld=gameworld, entity=player_entity)

        str_to_print = "[color=green]Power[/color]"

        RenderGameMap.render_bar(print_string=str_to_print, low_number=current_f1_power, high_number=max_f1_power,
                                 posy=statusbox_height + 5, posx=6, sprite_ref=0xE880,
                                 xscale=image_x_scale, yscale=image_y_scale)

    @staticmethod
    def render_bar(print_string, low_number, high_number, posy, posx, sprite_ref, xscale, yscale):

        display_percentage = CommonUtils.calculate_percentage(low_number, high_number)
        tens = int(display_percentage / 10)
        units = display_percentage % 10
        px = 0

        if print_string != "":
            terminal.printf(4, posy * yscale, print_string)

        for a in range(tens):
            terminal.put(x=(a + posx) * xscale, y=posy * yscale, c=sprite_ref + 0)
            px += 1

        if units > 0:
            if units < 5:
                terminal.put(x=(px + posx) * xscale, y=posy * yscale, c=sprite_ref + 3)

            if units == 5:
                terminal.put(x=(px + posx) * xscale, y=posy * yscale, c=sprite_ref + 2)

            if units > 5:
                terminal.put(x=(px + posx) * xscale, y=posy * yscale, c=sprite_ref + 1)

    @staticmethod
    def render_spell_bar(self, game_config):

        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='map_Yscale')
        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='STATUSBOX_HEIGHT')
        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)

        ac = 1
        sc = 5
        y = statusbox_height + 1

        # spell bar slots are drawn first
        for a in range(10):
            terminal.put(x=(ac + a) * sc, y=y * image_y_scale, c=0xE500 + 0)


        # now the spells based on the spell bar entities -- currently loads slots 1 - 6
        slotid = 1
        for spell_slot in range(6):

            spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=self.gameworld, slot=slotid, player_entity=player_entity)
            spell_image = SpellUtilities.get_spell_image(gameworld=self.gameworld, spell_entity=spell_entity)

            terminal.put(x=(ac + spell_slot) * sc, y=y * image_y_scale, c=0xE400 + spell_image)
            slotid += 1

        # and finally the utility spells

