import esper

from bearlibterminal import terminal

from components import mobiles, items
from utilities import configUtilities
from utilities.mobileHelp import MobileUtilities
from mapRelated.gameMap import RenderLayer
from utilities.common import CommonUtils


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
        self.render_mobiles(game_config, self.gameworld)

        # GUI viewport
        terminal.composition(terminal.TK_ON)
        self.render_statusbox(game_config)
        self.render_player_status_effects(game_config=game_config)
        self.render_spell_bar(self, game_config=game_config)
        self.render_player_vitals(gameworld=self.gameworld, game_config=game_config)
        terminal.composition(terminal.TK_OFF)

    @staticmethod
    def clear_map_layer():
        # prev_layer = terminal.state(terminal.TK_LAYER)
        # terminal.layer(RenderLayer.MAP.value)
        terminal.bkcolor('black')
        terminal.clear_area(0, 0, terminal.state(terminal.TK_WIDTH), terminal.state(terminal.TK_HEIGHT))

        # terminal.layer(prev_layer)

    @staticmethod
    def render_map(gameworld, game_config, game_map):

        render_style = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='render_style')
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')
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
            vpXmin = CommonUtils.get_viewport_x_axis_min_value(gameworld=gameworld, viewport_id=viewport_id)
            vpYmin = CommonUtils.get_viewport_y_axis_min_value(gameworld=gameworld, viewport_id=viewport_id)

            x_min = max(player_pos_x - vp_width, vpXmin)
            x_max = min(player_pos_x + vp_width, game_map.width)
            y_min = max(player_pos_y - vp_height, vpYmin)
            y_max = min(player_pos_y + vp_height, game_map.height)

            # x_min = 0
            # x_max = game_map.width
            # y_min = 0
            # y_max = game_map.height

            if player_has_moved:
                RenderGameMap.clear_map_layer()

            scry = player_pos_y
            for y in range(y_min, y_max):
                scrx = player_pos_x
                for x in range(x_min, x_max):
                    tile = game_map.tiles[x][y].type_of_tile
                    char_to_display = '.'
                    if tile == tile_type_wall:
                        char_to_display = '#'
                    if tile == tile_type_door:
                        char_to_display = '+'

                    if tile > 0:
                        terminal.printf(x=x, y=y, s="[font=dungeon]" + char_to_display)
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
        ymin = CommonUtils.get_viewport_y_axis_min_value(gameworld=gameworld, viewport_id=viewport_id)
        ymax = CommonUtils.get_viewport_y_axis_max_value(gameworld=gameworld, viewport_id=viewport_id)

        right_boundary_visited = CommonUtils.get_viewport_right_boundary(gameworld=gameworld, viewport_id=viewport_id)
        left_boundary_visited = CommonUtils.get_viewport_left_boundary(gameworld=gameworld, viewport_id=viewport_id)
        viewport_player_position = CommonUtils.get_player_viewport_position_info(gameworld=gameworld,
                                                                                 viewport_id=viewport_id)
        vpx = viewport_player_position[0]
        vpy = viewport_player_position[1]

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
    def render_mobiles(game_config, gameworld):

        render_style = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                   parameter='render_style')
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        # terminal.layer(RenderLayer.ENTITIES.value)
        draw_pos_x = 0
        draw_pos_y = 0

        if render_style == 1:
            for ent, (rend, pos, desc) in gameworld.get_components(mobiles.Renderable, mobiles.Position,
                                                                   mobiles.Describable):
                if rend.isVisible:
                    draw_pos_x = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=ent)
                    draw_pos_y = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=ent)
                    fg = desc.foreground
                    bg = desc.background
                    RenderGameMap.render_entity(draw_pos_x, draw_pos_y, desc.glyph, 0, 0, render_style, fg, bg)
        else:
            image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='map_Xscale')
            image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                        parameter='map_Yscale')

            # pos.x represents the game map position and should be used to check for map obstructions only

            viewport_id = MobileUtilities.get_viewport_id(gameworld=gameworld, entity=player_entity)
            viewport_width = CommonUtils.get_viewport_width(gameworld=gameworld, viewport_id=viewport_id)
            viewport_height = CommonUtils.get_viewport_height(gameworld=gameworld, viewport_id=viewport_id)
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
            # characterbits = [glyph]

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

        # prev_layer = terminal.state(terminal.TK_LAYER)
        # terminal.layer(RenderLayer.HUD.value)

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

        prev_layer = terminal.state(terminal.TK_LAYER)
        # terminal.layer(RenderLayer.HUD.value)

        # top left
        terminal.put(x=(message_panel_start_x * image_x_scale), y=message_panel_height * image_y_scale, c=0xE700 + 0)

        # left edge
        for d in range(message_panel_depth):
            terminal.put(x=(message_panel_start_x * image_x_scale), y=(message_panel_height + d) * image_y_scale, c=0xE700 + 4)

        # bottom left
        terminal.put(x=(message_panel_start_x * image_x_scale), y=(message_panel_height + 5) * image_y_scale, c=0xE700 + 2)

        # top right
        terminal.put(x=(message_panel_start_x * image_x_scale) + message_panel_width, y=message_panel_height * image_y_scale, c=0xE700 + 1)

        # bottom right
        terminal.put(x=(message_panel_start_x * image_x_scale) + message_panel_width, y=(message_panel_height + 5) * image_y_scale, c=0xE700 + 3)

        # top edge
        for a in range(message_panel_width):
            terminal.put(x=a + (message_panel_start_x * image_x_scale), y=message_panel_height * image_y_scale, c=0xE700 + 6)

        # right edge
        for d in range(message_panel_depth):
            terminal.put(x=message_panel_start_x * image_x_scale + message_panel_width, y=(message_panel_height + d) * image_y_scale, c=0xE700 + 5)

        # bottom edge
        for a in range(message_panel_width):
            terminal.put(x=a + (message_panel_start_x * image_x_scale), y=(message_panel_height + 5) * image_y_scale, c=0xE700 + 7)

        # now show the messages

        # terminal.layer(prev_layer)

    @staticmethod
    def render_player_status_effects(game_config):
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='STATUSBOX_HEIGHT')

        prev_layer = terminal.state(terminal.TK_LAYER)
        # terminal.layer(RenderLayer.STATUSEFFECTS.value)
        RenderGameMap.render_boons(iy=image_y_scale, statusbox_y_position=statusbox_height)
        RenderGameMap.render_conditions(iy=image_y_scale, statusbox_y_position=statusbox_height)
        RenderGameMap.render_controls(iy=image_y_scale, statusbox_y_position=statusbox_height)
        # terminal.layer(prev_layer)

    @staticmethod
    def render_boons(iy, statusbox_y_position):
        ac = 1
        sc = 2
        for a in range(10):
            terminal.put(x=(ac + a) * sc, y=statusbox_y_position * iy, c=0xE600 + a)

    @staticmethod
    def render_conditions(iy, statusbox_y_position):

        ac = 11
        sc = 2
        for a in range(10):
            terminal.put(x=(ac + a) * sc, y=(statusbox_y_position * iy), c=0xE630 + a)

    @staticmethod
    def render_controls(iy, statusbox_y_position):

        ac = 21
        sc = 2
        for a in range(10):
            terminal.put(x=(ac + a) * sc, y=(statusbox_y_position * iy), c=0xE630 + a)

    @staticmethod
    def render_player_status_effects_content(self, posy, glyph, foreground, game_config):
        pass

    @staticmethod
    def render_player_vitals(gameworld, game_config):

        prev_layer = terminal.state(terminal.TK_LAYER)
        # terminal.layer(RenderLayer.HUD.value)
        RenderGameMap.render_health(gameworld=gameworld, game_config=game_config)
        RenderGameMap.render_mana(gameworld=gameworld, game_config=game_config)
        RenderGameMap.render_special_power(gameworld=gameworld, game_config=game_config)
        # terminal.layer(prev_layer)

    @staticmethod
    def render_health(gameworld, game_config):
        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')
        image_x_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Xscale')

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(gameworld, game_config)
        currentHealth = MobileUtilities.get_derived_current_health(gameworld=gameworld, entity=player_entity)
        maximum_health = MobileUtilities.get_derived_maximum_health(gameworld=gameworld, entity=player_entity)

        strToPrint = "[color=red]Health[/color]"

        RenderGameMap.render_bar(printString=strToPrint, lowNumber=currentHealth, highNumber=maximum_health,
                                 posy=statusbox_height + 3, posx=6, spriteRef=0xE770,
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
        currentMana = MobileUtilities.get_derived_current_mana(gameworld=gameworld, entity=player_entity)
        maxMana = MobileUtilities.get_derived_maximum_mana(gameworld=gameworld, entity=player_entity)
        strToPrint = "[color=blue]Mana[/color]"

        RenderGameMap.render_bar(printString=strToPrint, lowNumber=currentMana, highNumber=maxMana,
                                 posy=statusbox_height + 4, posx=6, spriteRef=0xE800,
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
        currentF1Power = MobileUtilities.get_derived_special_bar_current_value(gameworld=gameworld,
                                                                               entity=player_entity)
        maxF1Power = MobileUtilities.get_derived_special_bar_max_value(gameworld=gameworld, entity=player_entity)

        strToPrint = "[color=green]Power[/color]"

        RenderGameMap.render_bar(printString=strToPrint, lowNumber=currentF1Power, highNumber=maxF1Power,
                                 posy=statusbox_height + 5, posx=6, spriteRef=0xE880,
                                 xscale=image_x_scale, yscale=image_y_scale)

    @staticmethod
    def render_bar(printString, lowNumber, highNumber, posy, posx, spriteRef, xscale, yscale):

        displayPercentage = CommonUtils.calculate_percentage(lowNumber, highNumber)
        tens = int(displayPercentage / 10)
        units = displayPercentage % 10
        px = 0

        terminal.printf(4, posy * yscale, printString)
        for a in range(tens):
            terminal.put(x=(a + posx) * xscale, y=posy * yscale, c=spriteRef + 0)
            px += 1

        if units > 0:
            if units < 5:
                terminal.put(x=(px + posx) * xscale, y=posy * yscale, c=spriteRef + 3)

            if units == 5:
                terminal.put(x=(px + posx) * xscale, y=posy * yscale, c=spriteRef + 2)

            if units > 5:
                terminal.put(x=(px + posx) * xscale, y=posy * yscale, c=spriteRef + 1)

    @staticmethod
    def render_player_vertical_bar_content(self, x, current_value, foreground, background, game_config):
        pass

    @staticmethod
    def render_spell_bar(self, game_config):

        image_y_scale = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                    parameter='map_Yscale')

        statusbox_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='STATUSBOX_HEIGHT')

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)
        weapons_list = MobileUtilities.get_weapons_equipped(gameworld=self.gameworld, entity=player_entity)
        main_weapon = weapons_list[0]
        off_weapon = weapons_list[1]
        both_weapon = weapons_list[2]
        slot = ['NO SPEL'] * 10
        ac = 1
        sc = 5
        y = statusbox_height + 1

        # prev_layer = terminal.state(terminal.TK_LAYER)
        # terminal.layer(RenderLayer.SPELLBAR.value)

        # spell bar slots are drawn first
        for a in range(10):
            terminal.put(x=(ac + a) * sc, y=y * image_y_scale, c=0xE500 + 0)
        # then the spell images themselves
        for a in range(10):
            terminal.put(x=(ac + a) * sc, y=y * image_y_scale, c=0xE400)

        # terminal.layer(prev_layer)
