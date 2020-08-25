import random

from components import mobiles
from newGame.CreateSpells import AsEntities
from newGame.Items import ItemManager
from utilities import configUtilities, colourUtilities
from utilities.armourManagement import ArmourUtilities
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from loguru import logger
from utilities.jsonUtilities import read_json_file
from utilities.spellHelp import SpellUtilities
from utilities.weaponManagement import WeaponUtilities


class Entity:

    @staticmethod
    def create_random_enemies(gameworld, game_map, game_config):
        mx = game_map.width
        my = game_map.height
        enemy_roles = ['bomber', 'squealer', 'bully', 'sniper']

        for enemy_role in enemy_roles:
            placed = False
            while not placed:
                x = random.randint(0, mx - 1)
                y = random.randint(0, my - 1)
                if not game_map.tiles[x][y].blocked:
                    placed = True
                Entity.create_enemy_role(posx=x, posy=y, gameworld=gameworld, game_config=game_config, enemy_role=enemy_role)

    @staticmethod
    def create_new_entity(gameworld):
        entity_id = MobileUtilities.get_next_entity_id(gameworld)
        return entity_id

    @staticmethod
    def create_named_mobile(npcs_for_scene, posx, posy, cellid, gameworld, game_config):
        entity_id = Entity.create_new_entity(gameworld=gameworld)

        equipped_weapons = False

        for npc in npcs_for_scene:
            identifer = npc['identifier']
            if identifer == cellid:
                npc_name = npc['displayName']
                MobileUtilities.create_base_mobile(gameworld=gameworld, game_config=game_config,
                                                   entity_id=entity_id)
                MobileUtilities.add_enemy_components(gameworld=gameworld, entity_id=entity_id)
                npc_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='NPCSFILE')
                npcs_file = read_json_file(npc_file)
                for npc in npcs_file['npc']:
                    if npc_name == npc['name']:
                        npc_race = npc['race']
                        npc_class = npc['class']
                        npc_desc = npc['description']
                        npc_glyph = npc['glyph']
                        npc_fg = npc['fg']
                        npc_bg = npc['bg']
                        npc_shopkeeper = npc['shopkeeper']
                        npc_tutor = npc['tutor']
                        armour_file_option = npc['armourset']
                        jewellery_file_option = npc['jeweleryset']
                        weapon_file_option_main = npc['weapons-main']
                        weapon_file_option_off = npc['weapons-off']
                        weapon_file_option_both = npc['weapons-both']

                        if weapon_file_option_both != '' or weapon_file_option_main != '' or weapon_file_option_off != '':
                            equipped_weapons = True

                        logger.warning('--- CREATING NEW MOBILE ---')
                        # -------------------------------------
                        # --- CHOOSE RACE ---------------------
                        # -------------------------------------
                        Entity.choose_race_for_mobile(race_choice=npc_race, entity_id=entity_id, gameworld=gameworld, game_config=game_config)

                        # -------------------------------------
                        # --- CHOOSE NAME ---------------------
                        # -------------------------------------
                        Entity.choose_name_for_mobile(name_choice=npc_name, entity_id=entity_id, gameworld=gameworld)
                        if npc_name == 'Joe':
                            gameworld.add_component(entity_id, mobiles.DialogFlags(welcome=True))
                            MobileUtilities.set_talk_to_me_flag(gameworld=gameworld, target_entity=entity_id)

                        # -------------------------------------
                        # --- CHOOSE CLASS --------------------
                        # -------------------------------------
                        Entity.choose_class_for_mobile(class_choice=npc_class, entity_id=entity_id, gameworld=gameworld, game_config=game_config)

                        # -------------------------------------
                        # --- CREATE ARMOURSET ----------------
                        # -------------------------------------
                        Entity.choose_armourset_for_mobile(armour_file_option=armour_file_option, entity_id=entity_id, gameworld=gameworld, game_config=game_config)

                        # --------------------------------------
                        # --- CREATE SPELL BAR WITH NO SPELLS  -
                        # --------------------------------------
                        logger.info('Loading spell bar based on equipped weapons')
                        SpellUtilities.setup_mobile_empty_spellbar(gameworld=gameworld, player_entity=entity_id)

                        # -------------------------------------
                        # --- CREATE JEWELLERYSET -------------
                        # -------------------------------------
                        Entity.choose_jewellery_package(jewellery_file_option=jewellery_file_option,
                                                      entity_id=entity_id, game_config=game_config, gameworld=gameworld)

                        # get list of equipped jewellery
                        jewellery_list = MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld,
                                                                                        mobile=entity_id)

                        left_ear = jewellery_list[0]
                        right_ear = jewellery_list[1]
                        neck_entity = jewellery_list[4]

                        # get spell entity from that piece of jewellery
                        sp1 = ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=neck_entity)
                        sp2 = ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=left_ear)
                        sp3 = ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=right_ear)

                        # add spells from jewellery into spell bar
                        SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp1, slot=7,
                                                         player_entity=entity_id)
                        SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp2, slot=8,
                                                         player_entity=entity_id)
                        SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp3, slot=9,
                                                         player_entity=entity_id)

                        if equipped_weapons:
                            # --------------------------------------
                            # --- CREATE WEAPONSET AND -------------
                            # --- CHOOSE SPELLS AND LOAD TO WEAPON -
                            # --------------------------------------
                            Entity.choose_weaponset(entity_id=entity_id, main_hand=weapon_file_option_main, off_hand=weapon_file_option_off, both_hands=weapon_file_option_both, gameworld=gameworld, game_config=game_config)

                        # --------------------------------------
                        # --- add heal spell to spellbar     ---
                        # --------------------------------------
                        heal_spell_entity = SpellUtilities.get_class_heal_spell(gameworld=gameworld,
                                                                                player_entity=entity_id)
                        SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=heal_spell_entity, slot=6,
                                                         player_entity=entity_id)

                        # --------------------------------------
                        # --- SET COMBAT ROLE -
                        # --------------------------------------
                        MobileUtilities.set_enemy_combat_role(entity=entity_id, gameworld=gameworld, value='none')

                        # --------------------------------------
                        # --- SET AI LEVEL                     -
                        # --------------------------------------
                        entity_ai = configUtilities.get_config_value_as_string(configfile=game_config, section='game',
                                                                               parameter='AI_LEVEL_NPC')
                        MobileUtilities.set_mobile_ai_level(gameworld=gameworld, entity=entity_id, value=entity_ai)
                        MobileUtilities.set_mobile_ai_description(gameworld=gameworld, entity=entity_id,
                                                                  value='NPC')
                        # -------------------------------------
                        # --- SHOPKEEPER ? --------------------
                        # -------------------------------------
                        if npc_shopkeeper == 'True':
                            MobileUtilities.set_type_of_shopkeeper(gameworld=gameworld, target_entity=entity_id, shopkeeper_type=npc['type_of_shopkeeper'])

                        # -------------------------------------
                        # --- TUTOR ? -------------------------
                        # -------------------------------------
                        if npc_tutor == 'True':
                            MobileUtilities.set_type_of_tutor(gameworld=gameworld, target_entity=entity_id, tutor_type=npc['type_of_tutor'])

                        # now apply the values to the base mobile object
                        Entity.set_min_max_preferred_ranges(entity_id=entity_id, min_range='TOUCH',
                                                            max_range='EARSHOT', gameworld=gameworld,
                                                            game_config=game_config)

                        MobileUtilities.set_mobile_description(gameworld=gameworld, entity=entity_id,
                                                               value=npc_desc)
                        MobileUtilities.set_mobile_glyph(gameworld=gameworld, entity=entity_id, value=npc_glyph)
                        MobileUtilities.set_mobile_fg_render_colour(gameworld=gameworld, entity=entity_id,
                                                                    value=npc_fg.upper())
                        MobileUtilities.set_mobile_bg_render_colour(gameworld=gameworld, entity=entity_id,
                                                                    value=npc_bg.upper())
                        MobileUtilities.set_mobile_visible(gameworld=gameworld, entity=entity_id)
                        MobileUtilities.set_mobile_position(gameworld=gameworld, entity=entity_id, posx=posx,
                                                            posy=posy)
                        MobileUtilities.set_mobile_derived_personality(gameworld=gameworld, game_config=game_config,
                                                                       entity=entity_id)

                        logger.warning('--- NEW MOBILE CREATED ---')
        return entity_id

    @staticmethod
    def create_enemy_role(gameworld, game_config, posx, posy, enemy_role):
        entity_id = Entity.create_new_entity(gameworld=gameworld)
        MobileUtilities.create_base_mobile(gameworld=gameworld, game_config=game_config, entity_id=entity_id)
        MobileUtilities.add_enemy_components(gameworld=gameworld, entity_id=entity_id)

        npc_name = 'RANDOM'
        equipped_weapons = False

        npc_fg = 'white'
        npc_bg = 'black'

        # temporary code to load in the bomber role
        role_file = read_json_file('static/data/roles.json')
        for role in role_file['roles']:
            if role['id'] == enemy_role:
                npc_race = role['race']
                npc_class = role['class']
                npc_glyph = role['glyph']
                armour_file_option = role['armourset']
                jewellery_file_option = role['jewellery']
                weapon_main_hand = role['main-hand-weapon']
                weapon_off_hand = role['off-hand-weapon']
                weapon_both_hands = role['both-hands-weapon']
                min_range = role['min-range']
                max_range = role['max-range']

                if weapon_both_hands != '' or weapon_main_hand !='' or weapon_off_hand !='':
                    equipped_weapons = True

                logger.warning('--- CREATING ENEMY ROLE {} ---', enemy_role)
                logger.info('With entity id {}', entity_id)

                # -------------------------------------
                # --- CHOOSE RACE ---------------------
                # -------------------------------------
                Entity.choose_race_for_mobile(race_choice=npc_race, entity_id=entity_id, game_config=game_config, gameworld=gameworld)

                # -------------------------------------
                # --- CHOOSE NAME ---------------------
                # -------------------------------------
                Entity.choose_name_for_mobile(name_choice=npc_name, entity_id=entity_id, gameworld=gameworld)

                # -------------------------------------
                # --- CHOOSE CLASS --------------------
                # -------------------------------------
                Entity.choose_class_for_mobile(class_choice=npc_class, entity_id=entity_id, gameworld=gameworld, game_config=game_config)

                # -------------------------------------
                # --- CREATE ARMOURSET ----------------
                # -------------------------------------
                Entity.choose_armourset_for_mobile(armour_file_option=armour_file_option, entity_id=entity_id, gameworld=gameworld, game_config=game_config)

                # -------------------------------------
                # --- CREATE JEWELLERYSET -------------
                # -------------------------------------
                Entity.choose_jewellery_package(jewellery_file_option=jewellery_file_option, entity_id=entity_id, game_config=game_config, gameworld=gameworld)

                if equipped_weapons:
                    # -------------------------------------
                    # --- CREATE WEAPONSET ----------------
                    # -------------------------------------
                    Entity.choose_weaponset(entity_id=entity_id, main_hand=weapon_main_hand,
                                                                    off_hand=weapon_off_hand,
                                                                    both_hands=weapon_both_hands, gameworld=gameworld, game_config=game_config)

                    # --------------------------------------
                    # --- CREATE SPELL BAR WITH SPELLS     -
                    # --------------------------------------
                    logger.info('Loading spell bar based on equipped weapons')
                    SpellUtilities.populate_spell_bar_initially(gameworld=gameworld, player_entity=entity_id)

                # --------------------------------------
                # --- SET COMBAT ROLE -
                # --------------------------------------
                MobileUtilities.set_enemy_combat_role(entity=entity_id, gameworld=gameworld, value=enemy_role)

                # --------------------------------------
                # --- SET AI LEVEL                     -
                # --------------------------------------
                entity_ai = configUtilities.get_config_value_as_string(configfile=game_config, section='game',
                                                                       parameter='AI_LEVEL_MONSTER')
                MobileUtilities.set_mobile_ai_level(gameworld=gameworld, entity=entity_id, value=int(entity_ai))
                MobileUtilities.set_mobile_ai_description(gameworld=gameworld, entity=entity_id, value='monster')

                # now apply the values to the base mobile object

                MobileUtilities.set_mobile_description(gameworld=gameworld, entity=entity_id, value='nothing to say')
                MobileUtilities.set_mobile_glyph(gameworld=gameworld, entity=entity_id, value=npc_glyph)
                MobileUtilities.set_mobile_fg_render_colour(gameworld=gameworld, entity=entity_id, value=npc_fg.upper())
                MobileUtilities.set_mobile_bg_render_colour(gameworld=gameworld, entity=entity_id, value=npc_bg.upper())
                MobileUtilities.set_mobile_visible(gameworld=gameworld, entity=entity_id)

                MobileUtilities.set_mobile_position(gameworld=gameworld, entity=entity_id, posx=posx, posy=posy)
                Entity.set_min_max_preferred_ranges(entity_id=entity_id, min_range=min_range, max_range=max_range, gameworld=gameworld, game_config=game_config)
                MobileUtilities.set_mobile_derived_personality(gameworld=gameworld, game_config=game_config,
                                                               entity=entity_id)

    @staticmethod
    def set_min_max_preferred_ranges(entity_id, min_range, max_range, game_config, gameworld):

        min_text = 'SPELL_DIST_' + min_range
        max_text = 'SPELL_DIST_' + max_range
        minimum_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                    parameter=min_text)
        maximum_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                    parameter=max_text)

        if minimum_range == 0:
            logger.warning('ENTITY PREFERRED MIN RANGE SET TO ZERO')
        else:
            logger.debug('ENTITY PREFERRED MIN RANGE SET TO {}', minimum_range)

        if maximum_range == 0:
            logger.warning('ENTITY PREFERRED MAX RANGE SET TO ZERO')
        else:
            logger.debug('ENTITY PREFERRED MAX RANGE SET TO {}', maximum_range)

        MobileUtilities.set_enemy_preferred_max_distance_from_target(gameworld=gameworld, entity=entity_id,
                                                                     value=maximum_range)
        MobileUtilities.set_enemy_preferred_min_distance_from_target(gameworld=gameworld, entity=entity_id,
                                                                     value=minimum_range)

    @staticmethod
    def choose_name_for_mobile(name_choice, gameworld, entity_id):
        first_name = name_choice
        MobileUtilities.set_player_gender(gameworld=gameworld, entity=entity_id, gender='male')
        if name_choice == 'RANDOM':
            # need to create random name generator here
            random_suffix = str(random.randint(3, 100))

            first_name = 'not-tcod-' + random_suffix

        logger.info('Their name is {}', first_name)
        MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=entity_id, name=first_name)

    @staticmethod
    def choose_race_for_mobile(race_choice, entity_id, game_config, gameworld):

        player_race_file = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                      section='files', parameter='RACESFILE')
        race_file = read_json_file(player_race_file)
        selected_race = ''
        selected_race_size = ''
        selected_bg_colour = ''
        selected_race_names = ''

        race_name = []
        race_bg_colour = []
        race_size = []
        race_name_desc = []

        for option in race_file['races']:
            race_name.append(option['name'])
            race_bg_colour.append(colourUtilities.get('BLACK'))
            race_size.append(option['size'])
            race_name_desc.append(option['singular_plural_adjective'])

        if race_choice == 'RANDOM':

            selected_race_id = random.randint(0, len(race_name) - 1)

            selected_race = race_name[selected_race_id]
            selected_race_size = race_size[selected_race_id]
            selected_bg_colour = race_bg_colour[selected_race_id]
            selected_race_names = race_name_desc[selected_race_id]

        else:
            rcount = 0
            for rc in race_name:
                if rc.lower() == race_choice.lower():
                    selected_race = race_choice
                    selected_race_size = race_size[rcount]
                    selected_bg_colour = race_bg_colour[rcount]
                    selected_race_names = race_name_desc[rcount]
                rcount += 1

        MobileUtilities.setup_racial_attributes(gameworld=gameworld, player=entity_id, selected_race=selected_race,
                                                race_size=selected_race_size, bg=selected_bg_colour, race_names=selected_race_names)

        return selected_race

    @staticmethod
    def choose_class_for_mobile(class_choice, entity_id, game_config, gameworld):

        if class_choice == 'RANDOM':
            enemy_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                           parameter='CLASSESFILE')
            class_file = read_json_file(enemy_class_file)
            class_name = []
            class_health = []
            class_spell_file = []

            for option in class_file['classes']:
                class_name.append(option['name'])
                class_health.append(option['health'])
                class_spell_file.append(option['spellfile'])

            selected_class_id = random.randint(0, len(class_name) - 1)
            selected_class_name = class_name[selected_class_id]
            selected_class_health = class_health[selected_class_id]
            selected_cass_spellfile = class_spell_file[selected_class_id]

        else:
            selected_class_name = class_choice
            selected_class_health = 100
            selected_cass_spellfile = class_choice

        MobileUtilities.setup_class_attributes(gameworld=gameworld, player=entity_id,
                                               selected_class=selected_class_name, health=int(selected_class_health),
                                               spellfile=selected_cass_spellfile)

        logger.info('Their class is {}', selected_class_name)

    @staticmethod
    def choose_armourset_for_mobile(armour_file_option, entity_id, game_config, gameworld):
        if armour_file_option != 'none':
            armourset_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                        parameter='ARMOURSETFILE')
            armour_file = read_json_file(armourset_file)
            as_display_name = ''
            as_prefix_list = []
            px_att_bonus = []

            for armourset in armour_file['armoursets']:
                if armourset['startset'] == 'true':
                    as_display_name = (armourset['displayname'])
                    prefix_list = armourset['prefixlist'].split(",")
                    prefix_count = armourset['prefixcount']
                    attribute_bonus_count = armourset['attributebonuscount']

                    as_prefix_list, px_att_bonus = Entity.build_armourset_prefix_list(prefix_count=prefix_count,
                                                                                      attribute_bonus_count=attribute_bonus_count,
                                                                                      as_prefix_list=as_prefix_list,
                                                                                      prefix_list=prefix_list,
                                                                                      armourset=armourset)
            armour_modifier = Entity.choose_armour_modifier(armour_file_option=armour_file_option,
                                                            as_prefix_list=as_prefix_list)

            logger.info('Their armour modifier is {}', armour_modifier)
            armour_mod_index = as_prefix_list.index(armour_modifier)
            px_bonus = int(px_att_bonus[armour_mod_index])
            MobileUtilities.add_armour_modifier(gameworld=gameworld, entity_id=entity_id,
                                                armour_modifier=armour_modifier, px_bonus=px_bonus)
            ArmourUtilities.create_and_equip_armourset_for_npc(gameworld=gameworld, as_display_name=as_display_name,
                                                           armour_modifier=armour_modifier, entity_id=entity_id)
        else:
            logger.info('They are wearing no armour')

    @staticmethod
    def build_armourset_prefix_list(prefix_count, attribute_bonus_count, as_prefix_list, prefix_list, armourset):
        attvaluestring = 'attributebonus'
        pxstring = 'prefix'
        px_att_bonus = []

        for px in range(1, prefix_count + 1):
            prefix_string = pxstring + str(px)

            if attribute_bonus_count > 1:
                att_bonus_string = attvaluestring + str(px)
            else:
                att_bonus_string = attvaluestring + str(1)

            px_att_bonus.append(armourset[prefix_string][att_bonus_string])

            [as_prefix_list.append(i.lower()) if not i.islower() else as_prefix_list.append(i) for i in
             prefix_list]

        return as_prefix_list, px_att_bonus

    @staticmethod
    def choose_armour_modifier(armour_file_option, as_prefix_list):
        armour_modifier = ''
        if armour_file_option == 'RANDOM':
            # generate them procedurally
            # choose random armour modifier taken from as_prefix_list
            armour_modifier = random.choice(as_prefix_list)
        else:
            armour_modifier = armour_file_option.lower()

        return armour_modifier

    @staticmethod
    def choose_jewellery_package(jewellery_file_option, entity_id, game_config, gameworld):
        if jewellery_file_option != 'none':
            jewellery_packages = configUtilities.get_config_value_as_list(configfile=game_config, section='newgame',
                                                                          parameter='JEWELLERY_PACKAGES')

            npc_class_file = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                        section='files', parameter='CLASSESFILE')
            if jewellery_file_option == 'RANDOM':
                jewellery_set = random.choice(jewellery_packages)
            else:
                jewellery_set = jewellery_file_option.lower()

            logger.info('Their jewellery package is {}', jewellery_set)
            ItemManager.create_and_equip_jewellery_for_npc(gameworld=gameworld, entity_id=entity_id,
                                                           jewellery_set=jewellery_set, npc_class_file=npc_class_file)
        else:
            logger.info('They are wearing no jewellery')

    @staticmethod
    def generate_sample_spells_to_be_loaded(created_weapon_entity, entity_id, gameworld, game_config):

        enemy_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=entity_id)
        weapon_type = WeaponUtilities.get_weapon_type(gameworld, created_weapon_entity)

        AsEntities.generate_spells_as_entities_for_class(gameworld=gameworld, game_config=game_config, spell_file=enemy_class, playable_class=enemy_class)

        spell_list = SpellUtilities.get_list_of_spells_for_enemy(gameworld=gameworld, weapon_type=weapon_type,
                                                                 mobile_class=enemy_class)
        sample_spells = WeaponUtilities.load_enemy_weapon_with_spells(gameworld=gameworld, enemy_id=entity_id,
                                                                    spell_list=spell_list,
                                                                    weapon_entity_id=created_weapon_entity,
                                                                    weapon_type=weapon_type)

        logger.debug('=================')
        for k in sample_spells:
            name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=k)
            logger.info('Sample spell {}', name)
        logger.debug('=================')

    @staticmethod
    def choose_weaponset(entity_id, main_hand, off_hand, both_hands, gameworld, game_config):

        weapon_to_create = ''
        which_hand = ''
        created_weapon_entity = 0

        selected_class = MobileUtilities.get_character_class(gameworld, entity=entity_id)
        # gather list of available weapons for the player class

        if main_hand != '':
            weapon_to_create, which_hand = Entity.select_main_hand_weapon(main_hand=main_hand, selected_class=selected_class, game_config=game_config)
            created_weapon_entity = Entity.create_weapon_and_equip_npc(weapon_to_be_created=weapon_to_create,
                                                                       enemy_class=selected_class, entity_id=entity_id,
                                                                       hand_to_wield=which_hand, gameworld=gameworld, game_config=game_config)

        if off_hand != '':
            weapon_to_create, which_hand = Entity.select_off_hand_weapon(off_hand=off_hand,
                                                                         selected_class=selected_class, game_config=game_config)
            created_weapon_entity = Entity.create_weapon_and_equip_npc(weapon_to_be_created=weapon_to_create,
                                                                       enemy_class=selected_class, entity_id=entity_id,
                                                                       hand_to_wield=which_hand, gameworld=gameworld,
                                                                       game_config=game_config)

        if both_hands != '':
            weapon_to_create, which_hand = Entity.select_both_hands_weapon(both_hands=both_hands,
                                                                           selected_class=selected_class, game_config=game_config)
            created_weapon_entity = Entity.create_weapon_and_equip_npc(weapon_to_be_created=weapon_to_create,
                                                                       enemy_class=selected_class, entity_id=entity_id,
                                                                       hand_to_wield=which_hand, gameworld=gameworld,
                                                                       game_config=game_config)

        return created_weapon_entity

    @staticmethod
    def select_main_hand_weapon(main_hand, selected_class, game_config):
        weapon_choices = []
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='WEAPONSFILE')

        if main_hand == 'RANDOM':
            available_weapons = Entity.build_available_weapons(selected_class=selected_class, game_config=game_config)
            logger.info('weapons available {}', available_weapons)
            weapon_file = read_json_file(weapon_class_file)
            for weapon in available_weapons:
                for wpn in weapon_file['weapons']:
                    if wpn['wielded_hands'] == 'main' and wpn['name'] == weapon:
                        weapon_choices.append(weapon)

            logger.info('weapons available for main hand are {}', weapon_choices)
            selected_weapon_id = random.randint(0, len(weapon_choices) - 1)
            weapon_to_create = weapon_choices[selected_weapon_id]
        else:
            weapon_to_create = main_hand

        return weapon_to_create, 'main'

    @staticmethod
    def select_off_hand_weapon(off_hand, selected_class, game_config):
        weapon_choices = []
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='WEAPONSFILE')

        if off_hand == 'RANDOM':
            available_weapons = Entity.build_available_weapons(selected_class=selected_class, game_config=game_config)
            weapon_file = read_json_file(weapon_class_file)
            for weapon in available_weapons:
                for wpn in weapon_file['weapons']:
                    if wpn['wielded_hands'] == 'off' and wpn['name'] == weapon:
                        weapon_choices.append(weapon)

            logger.info('weapons available for off hand are {}', weapon_choices)
            selected_weapon_id = random.randint(0, len(weapon_choices) - 1)
            weapon_to_create = weapon_choices[selected_weapon_id]
        else:
            weapon_to_create = off_hand

        return weapon_to_create, 'off'

    @staticmethod
    def select_both_hands_weapon(both_hands, selected_class, game_config):
        weapon_choices = []
        weapon_to_create = ''
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='WEAPONSFILE')

        if both_hands == 'RANDOM':
            available_weapons = Entity.build_available_weapons(selected_class=selected_class, game_config=game_config)
            weapon_file = read_json_file(weapon_class_file)
            for weapon in available_weapons:
                for wpn in weapon_file['weapons']:
                    if wpn['wielded_hands'] == 'both' and wpn['name'] == weapon:
                        weapon_choices.append(weapon)

            logger.info('weapons available for both hands are {}', weapon_choices)
            selected_weapon_id = random.randint(0, len(weapon_choices) - 1)
            weapon_to_create = weapon_choices[selected_weapon_id]
        else:
            weapon_to_create = both_hands

        return weapon_to_create, 'both'

    @staticmethod
    def build_available_weapons(selected_class, game_config):
        player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='CLASSESFILE')
        class_file = read_json_file(player_class_file)
        available_weapons = []

        for option in class_file['classes']:
            if option['spellfile'] == selected_class:
                wpns = option["weapons"]

                # If you use this approach along
                # with a small trick, then you can process the keys and values of any dictionary.
                # The trick consists of using the indexing operator[] with the dictionary and its keys to
                # get access to the values:

                for key in wpns:
                    if wpns[key] == 'true':
                        available_weapons.append(key)
                        logger.info('weapon added {}', key)
        return available_weapons

    @staticmethod
    def create_weapon_and_equip_npc(weapon_to_be_created, enemy_class, entity_id, hand_to_wield, gameworld,
                                    game_config):
        created_weapon_entity = ItemManager.create_weapon(gameworld=gameworld, weapon_type=weapon_to_be_created,
                                                          game_config=game_config)
        if enemy_class == '':
            logger.warning('Spell file name not set')
        # equip player with newly created starting weapon
        MobileUtilities.equip_weapon(gameworld=gameworld, entity=entity_id, weapon=created_weapon_entity,
                                     hand=hand_to_wield)
        return created_weapon_entity
