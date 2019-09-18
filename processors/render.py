import esper
import tcod
import tcod.event

from loguru import logger
from components import mobiles, items
from utilities.display import menu
from utilities.mobileHelp import MobileUtilities
from utilities.spellHelp import SpellUtilities
from utilities import configUtilities
from utilities import colourUtilities
from utilities.itemsHelp import ItemUtilities
from utilities.display import draw_colourful_frame
from utilities.input_handlers import handle_game_keys


class RenderConsole(esper.Processor):
    def __init__(self, con, game_map, gameworld, fov_compute, fov_object, spell_bar, message_log):
        super().__init__()
        self.con = con
        self.game_map = game_map
        self.gameworld = gameworld
        self.fov_compute = fov_compute
        self.fov_object = fov_object
        self.spell_bar = spell_bar
        self.message_log = message_log

    def process(self, game_config):
        game_state = configUtilities.get_config_value_as_integer(configfile=game_config, section='game', parameter='DISPLAY_GAME_STATE')
        # logger.info('display game state set to {}', game_state)
        if game_state == 1:
            self.render_game_map(game_config)
        elif game_state == 2:
            self.render_inventory_screen(game_config)
        elif game_state == 3:
            self.render_personal_screen(game_config)
        elif game_state == 4:
            self.render_equipment_screen(game_config)
        elif game_state == 5:
            self.render_build_screen(game_config)
        else:
            self.render_weapons_screen(game_config)

        # blit the console
        self.blit_the_console(game_config)
        # clear the entity
        # self.clear_entity()

    def render_game_map(self, game_config):
        # GUI viewport and message box borders
        self.render_viewport(game_config)
        self.render_message_box(game_config)
        # self.render_spell_bar(game_config)
        self.render_player_status_effects(game_config)
        self.render_player_vitals(game_config)

        # render the game map
        self.render_map(game_config)

        # draw the entities
        self.render_items(game_config)
        self.render_entities(game_config)

    def render_inventory_screen(self, game_config):

        frame_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_frame_down')
        inv_key_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_key_pos')
        inv_glyph_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_glyph_pos')
        inv_desc_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_desc_pos')
        inv_section_pos = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_section_pos')
        inv_nothing_posx = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_nothing_msg_x')
        inv_nothing_posy = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_nothing_msg_y')
        inv_section_char = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='inv_section_line')
        panel_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv',parameter='INV_PANEL_MAX_WIDTH')
        panel_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='INV_PANEL_MAX_HEIGHT')
        panel_left_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv', parameter='INV_PANEL_LEFT_X')
        panel_left_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv',parameter='INV_PANEL_LEFT_Y')
        other_game_state = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',parameter='DISPLAY_GAME_MAP')
        act_menu_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv',parameter='act_menu_width')
        act_menu_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='inv',parameter='act_menu_height')

        inv_panel = tcod.console_new(panel_width, panel_height)

        player = MobileUtilities.get_player_entity(self.gameworld, game_config)
        mobile_inventory_component = self.gameworld.component_for_entity(player, mobiles.Inventory)
        def_fg = colourUtilities.GRAY19
        def_wd = colourUtilities.GOLDENROD1
        inv_def_fg = colourUtilities.WHITE
        inv_def_bg = colourUtilities.BLACK

        inv_panel_displayed = True
        display_action_menu = False

        while inv_panel_displayed:

            letter_index = 97
            iy = frame_down + 1

            inventory_items = mobile_inventory_component.items
            disp_inv = []
            if len(inventory_items) != 0:
                max_lines = 2

                items_armour, cnt = self.populate_inv_lists(inventory_items, self.gameworld, 'armour')
                max_lines += cnt
                items_weapons, cnt = self.populate_inv_lists(inventory_items, self.gameworld, 'weapon')
                max_lines += cnt
                items_jewellery, cnt = self.populate_inv_lists(inventory_items, self.gameworld, 'jewellery')
                max_lines += cnt
                items_bags, cnt = self.populate_inv_lists(inventory_items, self.gameworld, 'bag')
                max_lines += cnt
                items_gemstones, cnt = self.populate_inv_lists(inventory_items, self.gameworld, 'gemstone')
                max_lines += cnt

                if len(items_armour) != 0:
                    inv_panel.print_box(x=inv_section_pos, y=iy, width=6, height=1, string='Armour')
                    sectlen = len('Armour')
                    sx = inv_section_pos + sectlen
                    sectseplen = panel_width - sx
                    inv_panel.draw_rect(x=inv_section_pos + sectlen + 1, y=iy, width=sectseplen, height=1, ch=inv_section_char, fg=def_fg, bg=None)
                    iy += 1

                    for armour in items_armour:
                        item_glyph = ItemUtilities.get_item_glyph(gameworld=self.gameworld, entity=armour)
                        item_name = ItemUtilities.get_item_displayname(gameworld=self.gameworld, entity=armour)
                        item_fg = ItemUtilities.get_item_fg_colour(gameworld=self.gameworld, entity=armour)
                        item_bg = ItemUtilities.get_item_bg_colour(gameworld=self.gameworld, entity=armour)

                        # KEY
                        inv_panel.print(x=inv_key_pos, y=iy, string=chr(letter_index), fg=def_wd, bg=None)
                        # GLYPH
                        inv_panel.print(x=inv_glyph_pos , y=iy, string=item_glyph, fg=item_fg, bg=item_bg)
                        # DESCRIPTION
                        inv_panel.print(x=inv_desc_pos, y=iy, string=item_name, fg=def_wd, bg=None)
                        disp_inv.append(armour)
                        letter_index += 1
                        iy += 1

                if len(items_weapons) != 0:
                    inv_panel.print_box(x=inv_section_pos, y=iy, width=15, height=1, string='Weapons')
                    sectlen = len('Weapons')
                    sx = inv_section_pos + sectlen
                    sectseplen = panel_width - sx
                    inv_panel.draw_rect(x=inv_section_pos + sectlen + 1, y=iy, width=sectseplen, height=1, ch=inv_section_char, fg=def_fg, bg=None)
                    iy += 1

                    for weapon in items_weapons:
                        item_glyph = ItemUtilities.get_item_glyph(gameworld=self.gameworld, entity=weapon)
                        item_name = ItemUtilities.get_item_displayname(gameworld=self.gameworld, entity=weapon)
                        item_fg = ItemUtilities.get_item_fg_colour(gameworld=self.gameworld, entity=weapon)
                        item_bg = ItemUtilities.get_item_bg_colour(gameworld=self.gameworld, entity=weapon)

                        # KEY
                        inv_panel.print(x=inv_key_pos, y=iy, string=chr(letter_index), fg=def_wd, bg=None)
                        # GLYPH
                        inv_panel.print(x=inv_glyph_pos, y=iy, string=item_glyph, fg=item_fg, bg=item_bg)
                        # DESCRIPTION
                        inv_panel.print(x=inv_desc_pos, y=iy, string=item_name, fg=def_wd, bg=None)
                        disp_inv.append(weapon)
                        letter_index += 1
                        iy += 1

                if len(items_jewellery) != 0:
                    inv_panel.print_box(x=inv_section_pos, y=iy, width=15, height=1, string='Jewellery')
                    sectlen = len('Jewellery')
                    sx = inv_section_pos + sectlen
                    sectseplen = panel_width - sx
                    inv_panel.draw_rect(x=inv_section_pos + sectlen + 1, y=iy, width=sectseplen, height=1, ch=inv_section_char, fg=def_fg, bg=None)
                    iy += 1

                    for jewellery in items_jewellery:
                        item_glyph = ItemUtilities.get_item_glyph(gameworld=self.gameworld, entity=jewellery)
                        item_name = ItemUtilities.get_item_displayname(gameworld=self.gameworld, entity=jewellery)
                        item_fg = ItemUtilities.get_item_fg_colour(gameworld=self.gameworld, entity=jewellery)
                        item_bg = ItemUtilities.get_item_bg_colour(gameworld=self.gameworld, entity=jewellery)

                        # KEY
                        inv_panel.print(x=inv_key_pos, y=iy, string=chr(letter_index), fg=def_wd, bg=None)
                        # GLYPH
                        inv_panel.print(x=inv_glyph_pos, y=iy, string=item_glyph, fg=item_fg, bg=item_bg)
                        # DESCRIPTION
                        inv_panel.print(x=inv_desc_pos, y=iy, string=item_name, fg=def_wd, bg=None)
                        disp_inv.append(jewellery)
                        letter_index += 1
                        iy += 1
            else:
                inv_panel.print_box(x=inv_nothing_posx, y=inv_nothing_posy, width=panel_width, height=1, string='Nothing in Inventory')

            draw_colourful_frame(console=inv_panel, game_config=game_config, startx=0, starty=0,
                                 width=panel_width, height=panel_height,
                                 title='Inventory', title_loc='centre', corner_decorator='', corner_studs='square', msg='a-z, ESC to quit')

            tcod.console_blit(inv_panel, 0, 0,
                              panel_width,
                              panel_height,
                              0,
                              panel_left_x,
                              panel_left_y)

            tcod.console_flush()
            event_to_be_processed, event_action = handle_game_keys()
            if display_action_menu is False and event_to_be_processed != '':
                if event_to_be_processed == 'keypress':
                    if event_action == 'quit':
                        inv_panel_displayed = False
                        configUtilities.write_config_value(configfile=game_config, section='game',
                                                           parameter='DISPLAY_GAME_STATE', value=str(other_game_state))
                    else:
                        # interact with item in inventory
                        # display 'action menu' for item
                        id = ord(event_action) - 97
                        if id < len(disp_inv):
                            inv_id = disp_inv[id]
                            item_actions = ItemUtilities.get_item_actions(gameworld=self.gameworld, entity=inv_id)
                            display_action_menu = True

                elif event_to_be_processed == 'mousebutton':
                    if event_action == 'left':
                        logger.info('Left mouse button pressed')
                    else:
                        logger.info('Right mouse button pressed')

            else:
                # display action menu --> works like a mini inventory panel

                action_panel = tcod.console_new(act_menu_width, act_menu_height)
                while display_action_menu:

                    draw_colourful_frame(console=action_panel, game_config=game_config, startx=0, starty=0,
                                         width=act_menu_width, height=act_menu_height,
                                         title='Actions', title_loc='right', corner_decorator='',
                                         corner_studs='round', msg='ESC to quit')

                    cnt = 1
                    for action in item_actions:
                        action_panel.print(x=3, y=cnt, string=str(cnt) + ':' + action, fg=def_wd, bg=None)
                        cnt += 1
                    tcod.console_blit(action_panel, 0, 0, act_menu_width,  act_menu_height, 0, inv_key_pos + 10, 10)

                    action_panel.clear(ch=ord(' '), fg=colourUtilities.BLACK, bg=colourUtilities.BLACK)
                    tcod.console_flush()
                    event_to_be_processed, event_action = handle_game_keys()
                    if event_action != '':
                        if event_action == 'quit':
                            display_action_menu = False
                            configUtilities.write_config_value(configfile=game_config, section='game',
                                                               parameter='DISPLAY_GAME_STATE', value=str(other_game_state))
                        else:
                            ia = ord(event_action) - 49
                            if ia < len(item_actions):
                                display_action_menu = False
                                inv_panel_displayed = False
                                if item_actions[ia] == 'drop':
                                    MobileUtilities.drop_item_from_inventory(gameworld=self.gameworld, mobile=player, entity=inv_id)
                                if item_actions[ia] == 'inspect':
                                    MobileUtilities.inspect_item(gameworld=self.gameworld, item_entity=inv_id, game_config=game_config)
                                if item_actions[ia] == 'wield':
                                    MobileUtilities.wield_weapon_from_inventory(gameworld=self.gameworld, mobile=player, entity=inv_id)
                                if item_actions[ia] == 'wear':
                                    MobileUtilities.wear_jewellery_from_inventory(gameworld=self.gameworld, mobile=player, jewellery_entity=inv_id)
                                if item_actions[ia] == 'destroy':
                                    MobileUtilities.destroy_item_from_inventory(gameworld=self.gameworld, mobile=player, entity=inv_id)
                                if item_actions[ia] == 'equip':
                                    MobileUtilities.equip_armour_from_inventory(gameworld=self.gameworld, mobile=player, armour_piece=inv_id)

            inv_panel.clear(ch=ord(' '), fg=inv_def_fg, bg=inv_def_bg)

    @staticmethod
    def populate_inv_lists(inventory_items, gameworld, item_type_in_inv):

        inv_items = []
        cnt = 0

        for item in inventory_items:
            if item > 0:
                item_type = ItemUtilities.get_item_type(gameworld=gameworld, entity=item)

                if item_type == item_type_in_inv:
                    inv_items.append(item)
                    if cnt == 0:
                        cnt = 2
                    else:
                        cnt += 1

        return inv_items, cnt

    def render_equipment_screen(self, game_config):
        pass

    def render_build_screen(self, game_config):
        pass

    def render_personal_screen(self, game_config):
        pass

    def render_weapons_screen(self, game_config):
        pass

    def blit_the_console(self, game_config):
        # update console with latest changes
        scr_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='tcod', parameter='SCREEN_WIDTH')
        scr_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='tcod', parameter='SCREEN_HEIGHT')

        # blit changes to root console
        tcod.console_blit(self.con, 0, 0, scr_width, scr_height, 0, 0, 0)
        # todo stop drawing on the root console and create a game map console!

    def render_player_status_effects(self, game_config):
        # draw the boon, condition, and control bar borders (horizontal)
        self.render_boons(game_config)
        self.render_conditions(game_config)
        self.render_controls(game_config)

    def render_player_vitals(self, game_config):
        player_entity = MobileUtilities.get_player_entity(self.gameworld, game_config)
        player_derived_attributes_component = self.gameworld.component_for_entity(player_entity,
                                                                                  mobiles.DerivedAttributes)

        self.render_health_bar(player_derived_attributes_component, game_config)
        self.render_mana_bar(player_entity, game_config)

        self.render_f1_bar(player_entity, game_config)

    def render_spell_bar(self, game_config):
        spell_box_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BOX_WIDTH')
        spell_bar_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BAR_X')
        spell_bar_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BAR_Y')
        spell_bar_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BAR_WIDTH')
        spell_bar_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_BOX_DEPTH')
        spell_slots = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='SPELL_SLOTS')

        tcod.console_set_default_foreground(self.con, tcod.yellow)
        for spellSlot in range(1, spell_slots):
            spell_slot_posx = spell_bar_across + (spellSlot * spell_box_width)
            tcod.console_print_frame(self.con,
                                     x=spell_slot_posx,
                                     y=spell_bar_down,
                                     w=spell_bar_width,
                                     h=spell_bar_depth,
                                     clear=False,
                                     flag=tcod.BKGND_DEFAULT,
                                     fmt='')
            slot_component = SpellUtilities.get_spell_bar_slot_componet(self.gameworld, spell_bar=self.spell_bar, slotid=spellSlot)
            if slot_component == -1:
                logger.warning('Could not get slot component from spell bar')
            else:
                tcod.console_put_char_ex(self.con, spell_slot_posx + 1, spell_bar_down, str(slot_component.sid), tcod.white, tcod.black)
                tcod.console_put_char_ex(self.con, spell_slot_posx + 2, spell_bar_down + 1, '&', tcod.yellow, tcod.black)
                tcod.console_put_char_ex(self.con, spell_slot_posx + 3, spell_bar_down, '*', tcod.white, tcod.black)

    def render_map(self, game_config):

        map_view_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        map_view_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_FLOOR')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_DOOR')
        tile_type_corridor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='TILE_TYPE_CORRIDOR')
        dng_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_WALL')
        dng_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_FLOOR')
        dng_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon', parameter='DNG_DOOR')
        dwl = configUtilities.get_config_value_as_string(configfile=game_config, section='colours', parameter='DUNGEON_WALL_LIGHT')
        dwd = configUtilities.get_config_value_as_string(configfile=game_config, section='colours', parameter='DUNGEON_WALL_DARK')
        dfl = configUtilities.get_config_value_as_string(configfile=game_config, section='colours', parameter='DUNGEON_FLOOR_LIGHT')
        dfd = configUtilities.get_config_value_as_string(configfile=game_config, section='colours', parameter='DUNGEON_FLOOR_DARK')

        # thisplayer = MobileUtilities.get_player_entity(self.gameworld)
        # player_position_component = self.gameworld.component_for_entity(thisplayer, mobiles.Position)
        # fov_map = self.fov_object.create_fov_map_via_raycasting(player_position_component.x, player_position_component.y)

        player_has_moved = MobileUtilities.has_player_moved(self.gameworld, game_config)
        # player_has_moved = True

        if player_has_moved:
            # calculate FOV
            # fov_map = self.fov_object.create_fov_map_via_raycasting(player_position_component.x, player_position_component.y)
            # GameMap.calculate_fov(self.fov_map, player_position_component.x, player_position_component.y, constants.FOV_RADIUS, constants.FOV_LIGHT_WALLS,constants.FOV_ALGORITHM)
            # light_wall = colourUtilities.BEIGE
            # light_ground = colourUtilities.GRAY25
            bgnd = colourUtilities.BLACK

            dng_wall_light = colourUtilities.colors[dwl]
            dng_light_ground = colourUtilities.colors[dfl]
            dng_dark_ground = colourUtilities.colors[dfd]
            dng_dark_wall = colourUtilities.colors[dwd]

            for y in range(self.game_map.height):
                for x in range(self.game_map.width):
                    isVisible = True
                    draw_pos_x = map_view_across + x
                    draw_pos_y = map_view_down + y
                    tile = self.game_map.tiles[x][y].type_of_tile
                    if isVisible:
                        if tile == tile_type_wall:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, dng_wall, dng_wall_light, bgnd)
                        elif tile == tile_type_floor:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, dng_floor, dng_light_ground, bgnd)
                        elif tile == tile_type_door:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, dng_door, dng_light_ground, bgnd)
                        elif tile == tile_type_corridor:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, dng_floor, dng_light_ground, bgnd)

                    else:
                        if tile == tile_type_wall:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, dng_wall, dng_dark_wall, bgnd)
                        elif tile == tile_type_floor:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, dng_floor, dng_dark_ground, bgnd)
                        elif tile == tile_type_door:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, dng_door, dng_dark_ground, bgnd)
                        elif tile == tile_type_corridor:
                            tcod.console_put_char_ex(self.con, draw_pos_x, draw_pos_y, dng_floor, dng_dark_ground, bgnd)

    def render_entities(self, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')

        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                draw_pos_x = px + pos.x
                draw_pos_y = py + pos.y
                self.render_entity(draw_pos_x, draw_pos_y, desc.glyph, desc.foreground, desc.background)

    def render_items(self, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MAP_VIEW_DRAW_Y')

        for ent, (rend, loc, desc) in self.world.get_components(items.RenderItem, items.Location, items.Describable):
            if rend.isTrue:
                draw_pos_x = px + loc.posx
                draw_pos_y = py + loc.posy
                self.render_entity(draw_pos_x, draw_pos_y, desc.glyph, desc.fg, desc.bg)

    def render_boons(self, game_config):
        self.render_h_bar(posy=0, border_colour=tcod.darker_gray, game_config=game_config)
        self.render_player_status_effects_content(0, tcod.CHAR_SUBP_DIAG, tcod.green, game_config)

    def render_conditions(self, game_config):
        self.render_h_bar(posy=3, border_colour=tcod.darker_gray, game_config=game_config)
        self.render_player_status_effects_content(3, chr(9), tcod.red, game_config)

    def render_controls(self, game_config):
        self.render_h_bar(posy=6, border_colour=tcod.darker_gray, game_config=game_config)
        self.render_player_status_effects_content(6, chr(10), tcod.white, game_config)

    def render_health_bar(self, player_derived_attributes_component, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bd2 = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_D')
        current_health = player_derived_attributes_component.currentHealth
        maximum_health = player_derived_attributes_component.maximumHealth
        current_health_percentage = MobileUtilities.get_number_as_a_percentage(current_health, maximum_health)

        self.render_v_bar(posx=px, posy=py, depth=bd2, border_colour=tcod.darker_gray)
        self.render_player_vertical_bar_content(0, current_health_percentage, tcod.red, tcod.black, game_config)

    def render_mana_bar(self, player_entity, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bd2 = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_D')
        player_current_mana = MobileUtilities.calculate_current_mana(self.gameworld, player_entity)
        player_maximum_mana = MobileUtilities.get_derived_maximum_mana(self.gameworld, player_entity)

        current_mana_percentage = MobileUtilities.get_number_as_a_percentage(player_current_mana, player_maximum_mana)

        self.render_v_bar(posx=px + 3, posy=py, depth=bd2, border_colour=tcod.darker_gray)
        self.render_player_vertical_bar_content(3, current_mana_percentage, tcod.blue, tcod.black, game_config)

    def render_f1_bar(self, player_entity, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bd2 = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_D')
        psc = MobileUtilities.get_derived_special_bar_current_value(self.gameworld, player_entity)
        psm = MobileUtilities.get_derived_special_bar_max_value(self.gameworld, player_entity)

        current_special_percentage = MobileUtilities.get_number_as_a_percentage(psc, psm)

        self.render_player_vertical_bar_content(6, current_special_percentage, tcod.white, tcod.black, game_config)
        self.render_v_bar(posx=px + 6, posy=py, depth=bd2, border_colour=tcod.darker_gray)

    def render_viewport(self, game_config):
        # draw the outer bounds of the map viewport

        viewport_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='VIEWPORT_START_X')
        viewport_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='VIEWPORT_START_Y')
        viewport_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='VIEWPORT_WIDTH')
        viewport_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='VIEWPORT_HEIGHT')

        self.con.draw_frame(
            x=viewport_across,
            y=viewport_down,
            width=viewport_width,
            height=viewport_height,
            title='',
            clear=False,
            fg=tcod.yellow,
            bg_blend=tcod.BKGND_DEFAULT
        )

    def render_message_box(self, game_config):
        msg_start_across = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_X')
        msg_start_down = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_START_Y')
        msg_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_WIDTH')
        msg_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='MSG_PANEL_DEPTH')

        # draw the message box area
        self.con.draw_frame(
            x=msg_start_across,
            y=msg_start_down,
            width=msg_width,
            height=msg_depth,
            title='',
            clear=False,
            fg=tcod.yellow,
            bg_blend=tcod.BKGND_DEFAULT
        )


        # render messages in message log
        y = 1
        for message in self.message_log.messages:
            self.con.print(
                x=1,
                y=msg_start_down + y,
                string=message.text,
                fg=message.color,
                bg_blend=tcod.BKGND_NONE,
                alignment=tcod.LEFT
            )

            y += 1

    def render_v_bar(self, posx, posy, depth, border_colour):
        self.con.draw_frame(
            x=posx,
            y=posy,
            width=3,
            height=depth,
            title='',
            fg=border_colour,
            bg_blend=tcod.BKGND_DEFAULT
        )
        # self.con.default_fg = border_colour
        # tcod.console_print_frame(self.con, x=posx, y=posy, w=3, h=depth, clear=False, flag=tcod.BKGND_DEFAULT,
        #                          fmt='')

    def render_h_bar(self, posy, border_colour, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_Y')
        rs = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='BCC_BAR_RIGHT_SIDE')

        self.con.draw_frame(
            x=px,
            y=py,
            width=rs,
            height=3,
            title='',
            fg=border_colour,
            bg_blend=tcod.BKGND_DEFAULT
        )


    def render_entity(self, posx, posy, glyph, fg, bg):
        tcod.console_put_char_ex(self.con, posx, posy, glyph, fg, bg)

    # clear the entity from the screen - this is used in conjunction with the Renderable component
    def clear_entity(self):
        for ent, (rend, pos, desc) in self.world.get_components(mobiles.Renderable, mobiles.Position, mobiles.Describable):
            if rend.isVisible:
                self.render_entity(pos.x, pos.y, ' ', desc.foreground, desc.background)

    def render_player_status_effects_content(self, posy, glyph, foreground, game_config):
        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_X')
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='H_BAR_Y') + posy

        x = 0
        for a in range(10):
            self.render_entity(1 + px + x, py + 1, glyph, foreground, tcod.black)
            if a < 9:
                x += 1
                self.render_entity(1 + px + x, py + 1, chr(179), tcod.darker_gray, tcod.black)
            x += 1

    def render_player_vertical_bar_content(self, x, current_value, foreground, background, game_config):

        px = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_X')
        posx = 1 + px + x
        py = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_Y')
        bar_depth = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='V_BAR_DEPTH')
        posy = py + bar_depth

        bar_count = int(MobileUtilities.get_bar_count(current_value, bar_depth))

        for y in range(bar_count):
            tcod.console_put_char_ex(self.con, posx, posy - y, chr(176), foreground, background)


class RenderGameStartScreen(esper.Processor):
    def __init__(self, con, image, key, mouse, gameworld):
        self.con = con
        self.image = image
        self.key = key
        self.mouse = mouse
        self.gameworld = gameworld
        super().__init__()

    def process(self, game_config):
        # get opening image & blit it
        tcod.image_blit_2x(self.image, self.con, 0, 0)

        self.render_game_info(game_config)
        con_width = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_WIDTH')
        con_height = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_HEIGHT')
        # display game options
        menu(self.con, header='Game Start',
            options=['New Game', 'Continue', 'Save', 'Set Seed', 'Replay', 'Quit'],
            width=24, screen_width=con_width, screen_height=con_height, posx=10, posy=26,
            foreground=tcod.yellow,
            key=self.key,
            mouse=self.mouse,
            gameworld=self.gameworld,
             game_config=game_config)

    def render_game_info(self, game_config):
        # display Game information
        game_title = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='GAME_WINDOW_TITLE')
        author = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='AUTHOR')
        con_width = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_WIDTH')
        con_height = configUtilities.get_config_value_as_integer(game_config, 'tcod', 'SCREEN_HEIGHT')

        self.con.print(x=10, y=10, string=game_title, bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)
        self.con.print(x=10, y=42, string=author, bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)

        tcod.console_blit(self.con, 0, 0, con_width, con_height, 0, 0, 0)
