import random

from mapRelated.gameMap import GameMap
from newGame.Entities import NewEntity
from processors import castSpells, move_entities, renderUI, updateEntities, renderMessageLog, renderSpellInfoPanel
from utilities import configUtilities, externalfileutilities, jsonUtilities, mobileHelp, scorekeeper, spellHelp
from loguru import logger

from utilities.jewelleryManagement import JewelleryUtilities
from utilities.mobileHelp import MobileUtilities


class SceneManager:

    @staticmethod
    def get_current_scene(currentscene):
        this_scene = ''
        scene_found = False
        game_config = configUtilities.load_config()
        scene_list = configUtilities.get_config_value_as_list(game_config, 'game', 'SCENES')

        for scene_id, scene_name in enumerate(scene_list, 1):
            if scene_id == currentscene:
                logger.debug('Current scene set to {}', scene_name)
                scene_found = True
                this_scene = scene_name
        return scene_found, this_scene

    @staticmethod
    def new_scene(currentscene, gameworld):

        gm, mx, my = SceneManager.load_scene_card(currentscene=currentscene, gameworld=gameworld)

        return gm

    @staticmethod
    def load_scene_card(currentscene, gameworld):
        # load scene list into memory
        map_area_max_x = 0
        map_area_max_y = 0
        game_map = []
        scene_found, this_scene = SceneManager.get_current_scene(currentscene=currentscene)
        current_area_tag = ''
        if scene_found:
            map_area_file = ''
            scene_file = 'new_scenes.json'
            scene_file = jsonUtilities.read_json_file('static/scenes/' + scene_file)
            for scene_key in scene_file['scenes']:
                if scene_key['name'] == this_scene:
                    scene_name = scene_key['name']
                    scene_exits = scene_key['sceneExits']
                    current_area_tag = scene_key['area_tag']
                    logger.debug('The {} scene exits to the {}', scene_name, scene_exits)
                    if 'loadMap' in scene_key:
                        # load game_map from external file - setup variables
                        map_area_file = scene_key['loadMap']
                        map_area_max_x = int(scene_key['mapx'])
                        map_area_max_y = int(scene_key['mapy'])
                        game_map = GameMap(mapwidth=map_area_max_x, mapheight=map_area_max_y)

                    if map_area_file != '':
                        SceneManager.build_static_scene(gameworld=gameworld, game_map=game_map,
                                                        map_area_file=map_area_file, this_scene=scene_key)
                        GameMap.assign_tiles(game_map=game_map)
                    else:
                        # generate random map
                        SceneManager.generate_game_map(game_map=game_map)
            scorekeeper.ScorekeeperUtilities.set_current_area(gameworld=gameworld, current_area_tag=current_area_tag)
        SceneManager.create_ecs_systems_yes_no(gameworld=gameworld, currentscene=currentscene, game_map=game_map)

        return game_map, map_area_max_x - 1, map_area_max_y - 1

    @staticmethod
    def create_ecs_systems_yes_no(gameworld, currentscene, game_map):
        if currentscene == 1:
            update_entities_processor = updateEntities.UpdateEntitiesProcessor(gameworld=gameworld, game_map=game_map)
            move_entities_processor = move_entities.MoveEntities(gameworld=gameworld, game_map=game_map)
            cast_spells_processor = castSpells.CastSpells(gameworld=gameworld, game_map=game_map)
            render_ui_processor = renderUI.RenderUI(game_map=game_map, gameworld=gameworld)
            render_message_log_processor = renderMessageLog.RenderMessageLog(gameworld=gameworld)
            spell_info_processor = renderSpellInfoPanel.RenderSpellInfoPanel(gameworld=gameworld, game_map=game_map)
            gameworld.add_processor(move_entities_processor, priority=80)
            gameworld.add_processor(cast_spells_processor, priority=100)
            gameworld.add_processor(update_entities_processor, priority=90)
            gameworld.add_processor(render_ui_processor, priority=70)
            gameworld.add_processor(render_message_log_processor, priority=60)
            gameworld.add_processor(spell_info_processor, priority=50)

    @staticmethod
    # haven't created the proc-gen routines for this
    def generate_game_map(game_map):
        pass

    @staticmethod
    def build_static_scene(gameworld, game_map, map_area_file, this_scene):
        # get config items
        significant_npcs = this_scene['npcs']
        all_races = this_scene['races']
        game_config = configUtilities.load_config()
        prefab_folder = configUtilities.get_config_value_as_string(game_config, 'files', 'PREFABFOLDER')
        tile_type_wall = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_WALL')
        tile_type_floor = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_FLOOR')
        tile_type_door = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                     parameter='TILE_TYPE_DOOR')
        tile_type_empty = configUtilities.get_config_value_as_integer(configfile=game_config, section='dungeon',
                                                                      parameter='TILE_TYPE_EMPTY')

        # now load the game_map from the external file/csv
        filepath = prefab_folder + map_area_file + '.txt'

        file_content = externalfileutilities.Externalfiles.load_existing_file(filename=filepath)
        posy = 0
        for row in file_content:
            posx = 0
            for cell in row:
                SceneManager.place_floor_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                     tile_type=tile_type_floor)
                SceneManager.place_door_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                    tile_type=tile_type_door)
                SceneManager.place_wall_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                    tile_type=tile_type_wall)
                SceneManager.place_empty_tile_yes_no(cell=cell, game_map=game_map, posx=posx, posy=posy,
                                                     tile_type=tile_type_empty)
                player_placed = SceneManager.place_player_tile_yes_no(cell=cell, game_map=game_map, posx=posx,
                                                                      posy=posy,
                                                                      tile_type=tile_type_floor)

                if player_placed:
                    SceneManager.setup_viewport(gameworld=gameworld, posx=posx, posy=posy)
                    game_map.tiles[posx][posy].entity = mobileHelp.MobileUtilities.get_player_entity(
                        gameworld=gameworld, game_config=game_config)

                # add named NPCs to scene
                npc_list_ids = "ABCEDFG"
                if cell.upper() in npc_list_ids:
                    cc = cell.upper()
                    idx = npc_list_ids.index(cc)
                    this_npc = significant_npcs[idx]
                    logger.info('--------- CREATING NEW MOBILE ---------')
                    new_entity = NewEntity.create_base_entity(gameworld=gameworld, game_config=game_config,
                                                              npc_glyph=cell, posx=posx, posy=posy)
                    NewEntity.add_enemy_components_to_entity(gameworld=gameworld, entity_id=new_entity, max_attack='long', min_attack='medium', game_config=game_config)

                    NewEntity.choose_race_for_mobile(race_choice=this_npc['race'], entity_id=new_entity, gameworld=gameworld,
                                                     game_config=game_config)

                    NewEntity.choose_class_for_mobile(class_choice=this_npc['class'], entity_id=new_entity, gameworld=gameworld,
                                                      game_config=game_config)

                    NewEntity.choose_name_for_mobile(name_choice=this_npc['name'], entity_id=new_entity, gameworld=gameworld)

                    NewEntity.choose_armourset_for_mobile(armour_file_option=this_npc['armourset'], entity_id=new_entity,
                                                          gameworld=gameworld, game_config=game_config)
                    NewEntity.choose_jewellery_package(jewellery_file_option=this_npc['jeweleryset'], entity_id=new_entity,
                                                       game_config=game_config, gameworld=gameworld)

                    NewEntity.choose_weapons(weapon_file_option_both=this_npc['weapons-both'],
                                             weapon_file_option_main=this_npc['weapons-main'],
                                             weapon_file_option_off=this_npc['weapons-off'], entity_id=new_entity,
                                             gameworld=gameworld, game_config=game_config)

                    NewEntity.set_entity_ai_level(game_config=game_config, gameworld=gameworld, entity_id=new_entity)
                    NewEntity.is_entity_a_shopkeeper(gameworld=gameworld, entity_id=new_entity, this_entity=this_npc)
                    NewEntity.is_entity_a_tutor(gameworld=gameworld, entity_id=new_entity, this_entity=this_npc)
                    NewEntity.create_empty_spell_bar(gameworld=gameworld, entity_id=new_entity)

                    # --- POPULATE SPELL BAR BASED ON EQUIPMENT -
                    spellHelp.SpellUtilities.populate_spell_bar_initially(gameworld=gameworld, player_entity=new_entity)

                    # --- ADD JEWELLERY SPELLS TO SPELLBAR -
                    NewEntity.add_spells_to_spell_bar_based_on_equipped_jewellery(gameworld=gameworld,
                                                                                  entity_id=new_entity)

                    # --- PLACE NEW ENTITY ON TO GAME MAP -
                    game_map.tiles[posx][posy].entity = new_entity
                    SceneManager.place_floor_tile_yes_no(cell=cell, posx=posx, posy=posy, tile_type=tile_type_floor,
                                                         game_map=game_map)

                    logger.info('--------- MOBILE HAS BEEN CREATED ---------')

                    # create random enemy
                if cell.upper() == 'X':
                    ai_roles_file_path = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                                 section='files', parameter='NPCROLES')
                    combat_kits_file_path = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                                 section='files', parameter='COMBATKITS')
                    this_npc = {}
                    # set enemy race
                    allowed_races = []

                    for rc in all_races:
                        if rc['available'] == 'true':
                            allowed_races.append(rc['name'])
                    if len(allowed_races) > 0:
                        chosen_race_id = random.randrange(len(allowed_races))
                        chosen_race_name = allowed_races[chosen_race_id]
                    else:
                        logger.warning('NO AVAILABLE RACES FOR THIS SCENE')

                    # choose an enemy role
                    enemy_roles = ['bomber', 'squealer', 'bully', 'sniper']
                    npc_race = chosen_race_name
                    npc_name = 'random'
                    # commented out whilst building/testing stateless AI
                    # role_id = random.randrange(len(enemy_roles))
                    role_id = 0
                    role_file = jsonUtilities.read_json_file(ai_roles_file_path)
                    for role in role_file['roles']:
                        if role['id'] == enemy_roles[role_id]:
                            combat_role = enemy_roles[role_id]
                            npc_class = 'undefined'
                            armourset = 'random'
                            combat_kits = role['kits']
                            attack_min = role['min-range']
                            attack_max = role['max-range']
                            a_spells = role['spells']
                            logger.warning('--- CREATING ENEMY ROLE {} ---', combat_role)
                            new_entity = NewEntity.create_base_entity(gameworld=gameworld, game_config=game_config,
                                                                      npc_glyph=cell, posx=posx, posy=posy, min_range=attack_min, max_range=attack_max)
                            NewEntity.add_enemy_components_to_entity(gameworld=gameworld, entity_id=new_entity, min_attack=attack_min, max_attack=attack_max, game_config=game_config)
                            # set enemy role id
                            NewEntity.set_enemy_combat_role(gameworld=gameworld, entity=new_entity,
                                                            combat_role=combat_role)
                            # load combat kits
                            available_kits = []
                            combat_kit_count = 0
                            combat_kit_file = jsonUtilities.read_json_file(combat_kits_file_path)
                            for kit in combat_kit_file['kits']:
                                if kit['title'] in combat_kits:
                                    available_kits.append(kit)
                                    combat_kit_count += 1

                            kit_index = 0

                            if len(available_kits) > 1:
                                kit_index = random.randrange(0, combat_kit_count)
                            combat_kit_chosen = available_kits[kit_index]
                            a_armour = combat_kit_chosen['armour']
                            a_arm_mods = combat_kit_chosen['armour_modifiers']
                            a_weapons = combat_kit_chosen['weapons']
                            a_jewellery = combat_kit_chosen['jewellery']
                            available_armour = a_armour.split(',')
                            weapons_both, weapons_main, weapons_off = SceneManager.sort_out_weapons(all_weapons=a_weapons)
                            res = sum(1 for i in range(len(a_weapons))
                                      if a_weapons.startswith(",", i))
                            if res > 0:
                                available_weapons = a_weapons.split(',')
                            else:
                                available_weapons = a_weapons
                            available_arm_mods = a_arm_mods.split(',')

                            logger.debug('Random combat kit chosen is {}', combat_kit_chosen['title'])
                            MobileUtilities.set_combat_kit_title(gameworld=gameworld, entity=new_entity, title_string=combat_kit_chosen['title'])

                            chosen_spells = NewEntity.set_spells_from_combat_role(gameworld=gameworld, available_spells=a_spells)

                            # set enemy glyph
                            NewEntity.set_entity_glyph(gameworld=gameworld, entity=new_entity, glyph=combat_kit_chosen['glyph'])
                            MobileUtilities.set_combat_kit_glyph(gameworld=gameworld, entity=new_entity, glyph=combat_kit_chosen['glyph'])
                            # set race for enemy
                            NewEntity.choose_race_for_mobile(race_choice=npc_race, entity_id=new_entity, gameworld=gameworld,
                                                             game_config=game_config)
                            # set class for enemy
                            NewEntity.choose_class_for_mobile(class_choice=npc_class, entity_id=new_entity, gameworld=gameworld,
                                                              game_config=game_config)
                            # choose a name for the enemy
                            NewEntity.choose_name_for_mobile(name_choice=npc_name, entity_id=new_entity, gameworld=gameworld)

                            # equip enemy with armourset

                            armour_index = random.randrange(0, len(available_armour))
                            npc_armourset = available_armour[armour_index]
                            logger.debug('Random armourset chosen is {}', npc_armourset)

                            MobileUtilities.set_combat_kit_armourset(gameworld=gameworld, entity=new_entity, armourset=npc_armourset)
                            MobileUtilities.set_combat_kit_armour_mod(gameworld=gameworld, entity=new_entity, armour_mod=available_arm_mods)

                            NewEntity.choose_armourset_for_mobile(armour_file_option=armourset, entity_id=new_entity,
                                                                  gameworld=gameworld, game_config=game_config)

                            # equip enemy with jewelery
                            JewelleryUtilities.create_jewellery_from_combat_kit(gameworld=gameworld, gemstones=a_jewellery, entity_id=new_entity)
                            jewellery_list = MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld,
                                                                                            mobile=new_entity)

                            left_ear = jewellery_list[0]
                            right_ear = jewellery_list[1]
                            ring1 = jewellery_list[2]
                            ring2 = jewellery_list[3]
                            neck_entity = jewellery_list[4]

                            MobileUtilities.set_combat_kit_ring1(gameworld=gameworld, entity=new_entity, ring1=ring1)
                            MobileUtilities.set_combat_kit_ring2(gameworld=gameworld, entity=new_entity, ring2=ring2)
                            MobileUtilities.set_combat_kit_ear1(gameworld=gameworld, entity=new_entity, ear1=left_ear)
                            MobileUtilities.set_combat_kit_ear2(gameworld=gameworld, entity=new_entity, ear2=right_ear)
                            MobileUtilities.set_combat_kit_pendant(gameworld=gameworld, entity=new_entity,
                                                                   pendent=neck_entity)

                            # equip enemy with weapons
                            NewEntity.choose_weapons(weapon_file_option_both=weapons_both,
                                                     weapon_file_option_main=weapons_main,
                                                     weapon_file_option_off=weapons_off, entity_id=new_entity,
                                                     gameworld=gameworld, game_config=game_config, spell_list=chosen_spells)
                            MobileUtilities.set_combat_kit_weapons(gameworld=gameworld, entity=new_entity, weapons=available_weapons)

                            # set enemy AI
                            NewEntity.set_entity_ai_level(game_config=game_config, gameworld=gameworld, entity_id=new_entity)
                            # create spellbar for enemy
                            NewEntity.create_empty_spell_bar(gameworld=gameworld, entity_id=new_entity)

                            # --- POPULATE SPELL BAR BASED ON EQUIPMENT -

                            spellHelp.SpellUtilities.populate_spell_bar_initially(gameworld=gameworld, player_entity=new_entity)

                            logger.info('enemy npc created')

                            # --- PLACE NEW ENTITY ON TO GAME MAP -
                            game_map.tiles[posx][posy].entity = new_entity
                            SceneManager.place_floor_tile_yes_no(cell=cell, posx=posx, posy=posy, tile_type=tile_type_floor,
                                                                 game_map=game_map)

                posx += 1
            posy += 1

    @staticmethod
    def sort_out_weapons(all_weapons):
        both_hands = ''
        main_hand = ''
        off_hand = ''
        weapons_list = all_weapons.split(',')
        if len(weapons_list) == 1:
            if weapons_list[0] in ['sword', 'staff']:
                both_hands = weapons_list[0]
            else:
                logger.warning('Illegal weapon found: {}', weapons_list)
        else:
            main_hand = weapons_list[0]
            off_hand = weapons_list[1]
        return both_hands, main_hand, off_hand



    @staticmethod
    def place_empty_tile_yes_no(cell, game_map, posx, posy, tile_type):
        if cell == ' ':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 4
            game_map.tiles[posx][posy].blocked = False
            game_map.tiles[posx][posy].block_sight = False

    @staticmethod
    def place_floor_tile_yes_no(cell, game_map, posx, posy, tile_type):
        if cell == '.':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 4
            game_map.tiles[posx][posy].blocked = False
            game_map.tiles[posx][posy].block_sight = False

    @staticmethod
    def place_door_tile_yes_no(cell, game_map, posx, posy, tile_type):
        if cell == '+':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 10
            game_map.tiles[posx][posy].blocked = True
            game_map.tiles[posx][posy].block_sight = True

    @staticmethod
    def place_wall_tile_yes_no(cell, game_map, posx, posy, tile_type):
        if cell == '#':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].image = 9
            game_map.tiles[posx][posy].blocked = True
            game_map.tiles[posx][posy].block_sight = True

    @staticmethod
    def place_player_tile_yes_no(cell, game_map, posx, posy, tile_type):
        player_placed = False
        if cell == '@':
            game_map.tiles[posx][posy].type_of_tile = tile_type
            game_map.tiles[posx][posy].blocked = False
            game_map.tiles[posx][posy].image = 11
            game_map.tiles[posx][posy].block_sight = False
            player_placed = True
        return player_placed

    @staticmethod
    def setup_viewport(gameworld, posx, posy):
        game_config = configUtilities.load_config()
        player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        mobileHelp.MobileUtilities.set_mobile_position(gameworld=gameworld, entity=player_entity, posx=posx, posy=posy)
