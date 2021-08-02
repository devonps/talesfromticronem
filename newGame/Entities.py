import random

from components import mobiles, scorekeeper, items
from newGame.CreateSpells import AsEntities
from newGame.Items import ItemManager
from utilities import configUtilities, armourManagement, itemsHelp, jewelleryManagement, jsonUtilities, \
    spellHelp, weaponManagement, world, colourUtilities
from loguru import logger

from utilities.jewelleryManagement import JewelleryUtilities
from utilities.mobileHelp import MobileUtilities


class NewEntity:

    @staticmethod
    def build_named_npc(gameworld, cell, this_npc, game_config, posx, posy):

        logger.info('--------- CREATING NAMED MOBILE ---------')
        new_entity = NewEntity.create_base_entity(gameworld=gameworld, game_config=game_config,
                                                  npc_glyph=cell, posx=posx, posy=posy)
        NewEntity.add_enemy_components_to_entity(gameworld=gameworld, entity_id=new_entity, max_attack='long',
                                                 min_attack='medium', game_config=game_config)

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
        this_colour = colourUtilities.get(this_npc['fg'])

        MobileUtilities.set_mobile_fg_render_colour(gameworld=gameworld, entity=new_entity, value=this_colour)

        logger.info('--------- MOBILE HAS BEEN CREATED ---------')

        return new_entity

    @staticmethod
    def build_random_enemy(gameworld, cell, game_config, posx, posy, chosen_race_name):
        ai_roles_file_path = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                        section='files', parameter='NPCROLES')
        combat_kits_file_path = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                           section='files', parameter='COMBATKITS')
        # choose an enemy role
        enemy_roles = ['bomber', 'squealer', 'bully', 'sniper']
        npc_race = chosen_race_name
        npc_name = 'random'
        new_entity = 0
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
                                                          npc_glyph=cell, posx=posx, posy=posy, min_range=attack_min,
                                                          max_range=attack_max)
                NewEntity.add_enemy_components_to_entity(gameworld=gameworld, entity_id=new_entity,
                                                         min_attack=attack_min, max_attack=attack_max,
                                                         game_config=game_config)
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
                weapons_both, weapons_main, weapons_off = NewEntity.sort_out_weapons(all_weapons=a_weapons)
                res = sum(1 for i in range(len(a_weapons))
                          if a_weapons.startswith(",", i))
                if res > 0:
                    available_weapons = a_weapons.split(',')
                else:
                    available_weapons = a_weapons
                available_arm_mods = a_arm_mods.split(',')

                logger.debug('Random combat kit chosen is {}', combat_kit_chosen['title'])
                MobileUtilities.set_combat_kit_title(gameworld=gameworld, entity=new_entity,
                                                     title_string=combat_kit_chosen['title'])

                chosen_spells = NewEntity.set_spells_from_combat_role(gameworld=gameworld, available_spells=a_spells, game_config=game_config)

                # set enemy glyph
                NewEntity.set_entity_glyph(gameworld=gameworld, entity=new_entity, glyph=combat_kit_chosen['glyph'])
                MobileUtilities.set_combat_kit_glyph(gameworld=gameworld, entity=new_entity,
                                                     glyph=combat_kit_chosen['glyph'])
                # set enemy FG colour
                NewEntity.set_enemy_fg_color(gameworld=gameworld, entity=new_entity, color_string=combat_kit_chosen['glyph-colour'])

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

                MobileUtilities.set_combat_kit_armourset(gameworld=gameworld, entity=new_entity,
                                                         armourset=npc_armourset)
                MobileUtilities.set_combat_kit_armour_mod(gameworld=gameworld, entity=new_entity,
                                                          armour_mod=available_arm_mods)

                NewEntity.choose_armourset_for_mobile(armour_file_option=armourset, entity_id=new_entity,
                                                      gameworld=gameworld, game_config=game_config)

                # equip enemy with jewelery
                JewelleryUtilities.create_jewellery_from_combat_kit(gameworld=gameworld, gemstones=a_jewellery,
                                                                    entity_id=new_entity)
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
                MobileUtilities.set_combat_kit_weapons(gameworld=gameworld, entity=new_entity,
                                                       weapons=available_weapons)

                # set enemy AI
                NewEntity.set_entity_ai_level(game_config=game_config, gameworld=gameworld, entity_id=new_entity)
                # create spellbar for enemy
                NewEntity.create_empty_spell_bar(gameworld=gameworld, entity_id=new_entity)

                # --- POPULATE SPELL BAR BASED ON EQUIPMENT -

                spellHelp.SpellUtilities.populate_spell_bar_initially(gameworld=gameworld, player_entity=new_entity)

                logger.info('enemy npc created')
        return new_entity

    @staticmethod
    def create_base_entity(gameworld, game_config, npc_glyph, posx, posy, min_range='earshot', max_range='long'):
        entity_id = world.get_next_entity_id(gameworld=gameworld)
        MobileUtilities.create_base_mobile(gameworld=gameworld, game_config=game_config, entity_id=entity_id)
        MobileUtilities.set_mobile_description(gameworld=gameworld, entity=entity_id, value='nothing to say')
        MobileUtilities.set_mobile_glyph(gameworld=gameworld, entity=entity_id, value=npc_glyph)
        MobileUtilities.set_mobile_visible(gameworld=gameworld, entity=entity_id)
        MobileUtilities.set_mobile_position(gameworld=gameworld, entity=entity_id, posx=posx, posy=posy)
        NewEntity.set_min_max_preferred_ranges(entity_id=entity_id, min_range=min_range, max_range=max_range,
                                               gameworld=gameworld, game_config=game_config)
        MobileUtilities.set_mobile_derived_personality(gameworld=gameworld, entity=entity_id)

        return entity_id

    @staticmethod
    def set_entity_glyph(gameworld, entity, glyph):
        MobileUtilities.set_mobile_glyph(gameworld=gameworld, entity=entity, value=glyph)

    @staticmethod
    def set_enemy_combat_role(gameworld, entity, combat_role):
        MobileUtilities.set_enemy_combat_role(gameworld=gameworld, entity=entity, value=combat_role)

    @staticmethod
    def set_enemy_fg_color(gameworld, entity, color_string):
        this_colour = colourUtilities.get(color_string)
        MobileUtilities.set_mobile_fg_render_colour(gameworld=gameworld, entity=entity, value=this_colour)

    @staticmethod
    def set_min_max_preferred_ranges(entity_id, min_range, max_range, game_config, gameworld):

        min_text = 'SPELL_DIST_' + min_range
        max_text = 'SPELL_DIST_' + max_range
        minimum_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                    parameter=min_text)
        maximum_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                    parameter=max_text)

        MobileUtilities.set_enemy_preferred_max_distance_from_target(gameworld=gameworld, entity=entity_id,
                                                                     value=maximum_range)
        MobileUtilities.set_enemy_preferred_min_distance_from_target(gameworld=gameworld, entity=entity_id,
                                                                     value=minimum_range)

        # this is the one that sets the vision range of the mobile - default range is 20 tiles
        MobileUtilities.set_mobile_senses_vision_range(gameworld=gameworld, entity=entity_id, value=20)

    @staticmethod
    def add_enemy_components_to_entity(gameworld, entity_id, max_attack, min_attack, game_config):
        MobileUtilities.add_enemy_components(gameworld=gameworld, entity_id=entity_id, max_range=max_attack, min_range=min_attack, game_config=game_config)

    @staticmethod
    def choose_name_for_mobile(name_choice, gameworld, entity_id):
        first_name = name_choice
        MobileUtilities.set_mobile_gender(gameworld=gameworld, entity=entity_id, gender='male')
        if name_choice == 'random':
            # need to create random name generator here
            random_suffix = str(random.randint(3, 100))

            first_name = 'not-tcod-' + random_suffix

        logger.info('Their name is {}', first_name)
        MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=entity_id, name=first_name)

        if name_choice == 'Joe':
            gameworld.add_component(entity_id, mobiles.DialogFlags(welcome=True))
            MobileUtilities.set_talk_to_me_flag(gameworld=gameworld, target_entity=entity_id)

    @staticmethod
    def choose_race_for_mobile(race_choice, entity_id, game_config, gameworld):

        player_race_file = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                      section='files', parameter='RACESFILE')
        race_file = jsonUtilities.read_json_file(player_race_file)
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
            race_bg_colour.append('0,0,0')
            race_size.append(option['size'])
            race_name_desc.append(option['singular_plural_adjective'])

        if race_choice == 'random':

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

        MobileUtilities.setup_racial_attributes(gameworld=gameworld, entity=entity_id, selected_race=selected_race,
                                                race_size=selected_race_size, bg=selected_bg_colour,
                                                race_names=selected_race_names)

        return selected_race

    @staticmethod
    def choose_class_for_mobile(class_choice, entity_id, game_config, gameworld):

        enemy_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='CLASSESFILE')
        class_file = jsonUtilities.read_json_file(enemy_class_file)
        class_name = []
        class_health = []
        class_spell_file = []
        selected_class_id = - 1

        for option in class_file['classes']:
            class_name.append(option['name'])
            class_health.append(option['health'])
            class_spell_file.append(option['spellfile'])
        if class_choice != 'undefined':
            if class_choice == 'random':
                selected_class_id = random.randint(0, len(class_name) - 1)
            else:
                for n in range(len(class_name)):
                    if class_name[n] == class_choice:
                        selected_class_id = n

            selected_class_name = class_name[selected_class_id]
            selected_class_health = class_health[selected_class_id]
            selected_cass_spellfile = class_spell_file[selected_class_id]

            MobileUtilities.setup_class_attributes(gameworld=gameworld, player=entity_id,
                                                   selected_class=selected_class_name,
                                                   health=int(selected_class_health),
                                                   spellfile=selected_cass_spellfile)

            logger.info('Their class is {}', selected_class_name)
            logger.info('Their class health is {}', selected_class_health)
        else:
            logger.info('Their class is UNDEFINED')

    @staticmethod
    def set_spells_from_combat_role(gameworld, available_spells, game_config):
        chosen_spells = NewEntity.pick_random_spells_for_combat_role(available_spells=available_spells)
        spell_entities = []
        for spell_name in chosen_spells:
            spell_entity = spellHelp.SpellUtilities.get_spell_entity_from_spell_name(gameworld=gameworld, spell_name=spell_name)
            # now I want to generate a new spell entity from the existing entity
            new_spell = AsEntities.create_new_spell_entity_from_existing_spell_entity(gameworld=gameworld, existing_spell_entity=spell_entity)
            spell_range = spellHelp.SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=new_spell)
            logger.info('Spell chosen: {}, id is {} range is {}', spell_name, new_spell, spell_range)
            spell_entities.append(new_spell)
        return spell_entities


    @staticmethod
    def pick_random_spells_for_combat_role(available_spells):
        spells_list = available_spells.split(',')
        chosen_spells = []
        count_of_spells = len(spells_list)
        for _ in range(5):
            spell_id = random.randrange(0, count_of_spells)
            chosen_spells.append(spells_list[spell_id])
        return chosen_spells


    @staticmethod
    def choose_weapons(weapon_file_option_both, weapon_file_option_main, weapon_file_option_off, entity_id, gameworld,
                       game_config, spell_list=None):

        if weapon_file_option_both != '':
            equipped_weapons = NewEntity.are_weapons_equipped(both_hands=weapon_file_option_both,
                                                              main_hand=weapon_file_option_main,
                                                              off_hand=weapon_file_option_off)
            if equipped_weapons:
                created_weapon_entity = NewEntity.choose_weaponset(entity_id=entity_id, main_hand='', off_hand='',
                                                                   both_hands=weapon_file_option_both,
                                                                   gameworld=gameworld, game_config=game_config)

                if spell_list is not None:
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_one = spell_list[0]
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_two = spell_list[1]
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_three = spell_list[2]
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_four = spell_list[3]
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_five = spell_list[4]
                else:
                    NewEntity.generate_sample_spells_to_be_loaded(created_weapon_entity=created_weapon_entity,
                                                                  entity_id=entity_id, gameworld=gameworld)
        if weapon_file_option_main != '':
            equipped_weapons = NewEntity.are_weapons_equipped(both_hands=weapon_file_option_both,
                                                              main_hand=weapon_file_option_main,
                                                              off_hand=weapon_file_option_off)
            if equipped_weapons:
                created_weapon_entity = NewEntity.choose_weaponset(entity_id=entity_id,
                                                                   main_hand=weapon_file_option_main,
                                                                   off_hand='', both_hands='',
                                                                   gameworld=gameworld, game_config=game_config)

                if spell_list is not None:
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_one = spell_list[0]
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_two = spell_list[1]
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_three = spell_list[2]
                else:
                    NewEntity.generate_sample_spells_to_be_loaded(created_weapon_entity=created_weapon_entity,
                                                                  entity_id=entity_id, gameworld=gameworld)

        if weapon_file_option_off != '':
            equipped_weapons = NewEntity.are_weapons_equipped(both_hands=weapon_file_option_both,
                                                              main_hand=weapon_file_option_main,
                                                              off_hand=weapon_file_option_off)
            if equipped_weapons:
                created_weapon_entity = NewEntity.choose_weaponset(entity_id=entity_id, main_hand='',
                                                                   off_hand=weapon_file_option_off,  both_hands='',
                                                                   gameworld=gameworld, game_config=game_config)

                if spell_list is not None:
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_four = spell_list[3]
                    weapon_slot_component = gameworld.component_for_entity(created_weapon_entity, items.Spells)
                    weapon_slot_component.slot_five = spell_list[4]
                else:
                    NewEntity.generate_sample_spells_to_be_loaded(created_weapon_entity=created_weapon_entity,
                                                                  entity_id=entity_id, gameworld=gameworld)


    @staticmethod
    def are_weapons_equipped(both_hands, main_hand, off_hand):
        equipped_weapons = False
        if both_hands != '' or main_hand != '' or off_hand != '':
            equipped_weapons = True
        return equipped_weapons

    @staticmethod
    def choose_weaponset(entity_id, main_hand, off_hand, both_hands, gameworld, game_config):
        created_weapon_entity = 0

        selected_class = MobileUtilities.get_character_class(gameworld, entity=entity_id)
        # gather list of available weapons for the player class

        if main_hand != '':
            weapon_to_create, which_hand = NewEntity.select_main_hand_weapon(main_hand=main_hand,
                                                                             selected_class=selected_class,
                                                                             game_config=game_config)
            created_weapon_entity = NewEntity.create_weapon_and_equip_npc(weapon_to_be_created=weapon_to_create,
                                                                          enemy_class=selected_class,
                                                                          entity_id=entity_id,
                                                                          hand_to_wield=which_hand, gameworld=gameworld,
                                                                          game_config=game_config)

        if off_hand != '':
            weapon_to_create, which_hand = NewEntity.select_off_hand_weapon(off_hand=off_hand,
                                                                            selected_class=selected_class,
                                                                            game_config=game_config)
            created_weapon_entity = NewEntity.create_weapon_and_equip_npc(weapon_to_be_created=weapon_to_create,
                                                                          enemy_class=selected_class,
                                                                          entity_id=entity_id,
                                                                          hand_to_wield=which_hand, gameworld=gameworld,
                                                                          game_config=game_config)

        if both_hands != '':
            weapon_to_create, which_hand = NewEntity.select_both_hands_weapon(both_hands=both_hands,
                                                                              selected_class=selected_class,
                                                                              game_config=game_config)
            created_weapon_entity = NewEntity.create_weapon_and_equip_npc(weapon_to_be_created=weapon_to_create,
                                                                          enemy_class=selected_class,
                                                                          entity_id=entity_id,
                                                                          hand_to_wield=which_hand, gameworld=gameworld,
                                                                          game_config=game_config)

        return created_weapon_entity

    @staticmethod
    def generate_sample_spells_to_be_loaded(created_weapon_entity, entity_id, gameworld):

        enemy_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=entity_id)
        weapon_type = weaponManagement.WeaponUtilities.get_weapon_type(gameworld, created_weapon_entity)

        spell_list = spellHelp.SpellUtilities.get_list_of_spells_for_enemy(gameworld=gameworld, weapon_type=weapon_type,
                                                                           mobile_class=enemy_class)
        sample_spells = weaponManagement.WeaponUtilities.load_enemy_weapon_with_spells(gameworld=gameworld,
                                                                                       enemy_id=entity_id,
                                                                                       spell_list=spell_list,
                                                                                       weapon_entity_id=created_weapon_entity,
                                                                                       weapon_type=weapon_type)

        logger.debug('=================')
        for k in sample_spells:
            name = spellHelp.SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=k)
            logger.info('Sample spell {}', name)
        logger.debug('=================')

    @staticmethod
    def select_main_hand_weapon(main_hand, selected_class, game_config):
        weapon_choices = []
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='WEAPONSFILE')

        if main_hand == 'random':
            available_weapons = NewEntity.build_available_weapons(selected_class=selected_class,
                                                                  game_config=game_config)
            logger.info('weapons available {}', available_weapons)
            weapon_file = jsonUtilities.read_json_file(weapon_class_file)
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

        if off_hand == 'random':
            available_weapons = NewEntity.build_available_weapons(selected_class=selected_class,
                                                                  game_config=game_config)
            weapon_file = jsonUtilities.read_json_file(weapon_class_file)
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
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                       parameter='WEAPONSFILE')

        if both_hands == 'random':
            available_weapons = NewEntity.build_available_weapons(selected_class=selected_class,
                                                                  game_config=game_config)
            weapon_file = jsonUtilities.read_json_file(weapon_class_file)
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
        class_file = jsonUtilities.read_json_file(player_class_file)
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

    @staticmethod
    def choose_jewellery_package(jewellery_file_option, entity_id, game_config, gameworld):
        if jewellery_file_option != 'none':
            jewellery_packages = configUtilities.get_config_value_as_list(configfile=game_config, section='newgame',
                                                                          parameter='JEWELLERY_PACKAGES')

            npc_class_file = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                        section='files', parameter='CLASSESFILE')
            if jewellery_file_option == 'random':
                jewellery_set = random.choice(jewellery_packages)
            else:
                jewellery_set = jewellery_file_option.lower()

            logger.info('Their jewellery package is {}', jewellery_set)
            jewelleryManagement.JewelleryUtilities.create_and_equip_jewellery_for_npc(gameworld=gameworld,
                                                                                      entity_id=entity_id,
                                                                                      jewellery_set=jewellery_set,
                                                                                      npc_class_file=npc_class_file)
        else:
            logger.info('They are wearing no jewellery')

    @staticmethod
    def choose_armourset_for_mobile(armour_file_option, entity_id, game_config, gameworld):
        if armour_file_option != 'none':
            armourset_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                        parameter='ARMOURSETFILE')
            armour_file = jsonUtilities.read_json_file(armourset_file)
            as_display_name = ''
            as_prefix_list = []
            px_att_bonus = []

            for armourset in armour_file['armoursets']:
                if armourset['startset'] == 'true':
                    as_display_name = (armourset['displayname'])
                    prefix_list = armourset['prefixlist'].split(",")
                    prefix_count = armourset['prefixcount']
                    attribute_bonus_count = armourset['attributebonuscount']

                    as_prefix_list, px_att_bonus = NewEntity.build_armourset_prefix_list(prefix_count=prefix_count,
                                                                                         attribute_bonus_count=attribute_bonus_count,
                                                                                         as_prefix_list=as_prefix_list,
                                                                                         prefix_list=prefix_list,
                                                                                         armourset=armourset)
            armour_modifier = NewEntity.choose_armour_modifier(armour_file_option=armour_file_option,
                                                               as_prefix_list=as_prefix_list)

            logger.info('Their armour modifier is {}', armour_modifier)
            armour_mod_index = as_prefix_list.index(armour_modifier)
            px_bonus = int(px_att_bonus[armour_mod_index])
            MobileUtilities.add_armour_modifier(gameworld=gameworld, entity_id=entity_id,
                                                armour_modifier=armour_modifier, px_bonus=px_bonus)
            armourManagement.ArmourUtilities.create_and_equip_armourset_for_npc(gameworld=gameworld,
                                                                                as_display_name=as_display_name,
                                                                                armour_modifier=armour_modifier,
                                                                                entity_id=entity_id)
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
        if armour_file_option == 'random':
            # generate them procedurally
            # choose random armour modifier taken from as_prefix_list-armour_modifier = random.choice(as_prefix_list)
            armour_modifier = 'malign'
        else:
            armour_modifier = armour_file_option.lower()

        return armour_modifier

    @staticmethod
    def add_spells_to_spell_bar_based_on_equipped_jewellery(gameworld, entity_id):
        # get list of equipped jewellery
        jewellery_list = MobileUtilities.get_jewellery_already_equipped(gameworld=gameworld, mobile=entity_id)

        left_ear = jewellery_list[0]
        right_ear = jewellery_list[1]
        neck_entity = jewellery_list[4]

        # get spell entity from that piece of jewellery
        if neck_entity > 0:
            sp1 = itemsHelp.ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=neck_entity)
            spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp1, slot=6,
                                                       player_entity=entity_id)
        if left_ear > 0:
            sp2 = itemsHelp.ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=left_ear)
            spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp2, slot=7,
                                                       player_entity=entity_id)
        if right_ear > 0:
            sp3 = itemsHelp.ItemUtilities.get_spell_from_item(gameworld=gameworld, item_entity=right_ear)
            spellHelp.SpellUtilities.set_spellbar_slot(gameworld=gameworld, spell_entity=sp3, slot=8,
                                                       player_entity=entity_id)

    @staticmethod
    def set_entity_ai_level(game_config, gameworld, entity_id):
        entity_ai = configUtilities.get_config_value_as_string(configfile=game_config, section='game',
                                                               parameter='AI_LEVEL_MONSTER')
        MobileUtilities.set_mobile_ai_level(gameworld=gameworld, entity=entity_id, value=int(entity_ai))
        MobileUtilities.set_mobile_ai_description(gameworld=gameworld, entity=entity_id, value='monster')

    @staticmethod
    def is_entity_a_shopkeeper(gameworld, entity_id, this_entity):
        npc_shopkeeper = this_entity['shopkeeper']
        shopkeeper_type = this_entity['type_of_shopkeeper']
        if npc_shopkeeper == 'True':
            MobileUtilities.set_type_of_shopkeeper(gameworld=gameworld, target_entity=entity_id,
                                                   shopkeeper_type=shopkeeper_type)

    @staticmethod
    def is_entity_a_tutor(gameworld, entity_id, this_entity):
        tutor_type = ['type_of_tutor']
        npc_tutor = this_entity['tutor']
        if npc_tutor == 'True':
            MobileUtilities.set_type_of_tutor(gameworld=gameworld, target_entity=entity_id,
                                              tutor_type=tutor_type)

    @staticmethod
    def create_empty_spell_bar(gameworld, entity_id):
        spellHelp.SpellUtilities.setup_mobile_empty_spellbar(gameworld=gameworld,
                                                             player_entity=entity_id)

    @staticmethod
    def create_scorekeeper_entity(gameworld):

        scorekeeper_entity = world.get_next_entity_id(gameworld=gameworld)

        logger.debug('===----- Creating scorekeeper -----===')
        logger.debug('Scorekeeper entity id {}', scorekeeper_entity)
        gameworld.add_component(scorekeeper_entity, scorekeeper.ScoreKeeperFlag(sc_flag=True))
        gameworld.add_component(scorekeeper_entity, scorekeeper.MetaEvents())
        gameworld.add_component(scorekeeper_entity, scorekeeper.AreasVisited())
        logger.debug('===----- Scorekeeper: now created-----===')

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