import random

from newGame.ClassWeapons import WeaponClass
from newGame.Items import ItemManager
from newGame.initialiseNewGame import generate_spells
from utilities import configUtilities, colourUtilities
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from loguru import logger
from utilities.jsonUtilities import read_json_file


class Entity:
    def __init__(self, gameworld):
        self.gameworld = gameworld
        self.game_config = configUtilities.load_config()

    def create_new_entity(self):
        entity_id = MobileUtilities.get_next_entity_id(self.gameworld)
        return entity_id

    def mobile_purpose(self, npcs_for_scene, posx, posy, cellid):
        entity_id = self.create_new_entity()

        for npc in npcs_for_scene:
            identifer = npc['identifier']
            if identifer == cellid:
                npc_name = npc['displayName']
                MobileUtilities.create_base_mobile(gameworld=self.gameworld, game_config=self.game_config,
                                                   entity_id=entity_id)
                npc_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
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
                        npc_image = int(npc['image'])
                        npc_ai = npc['ai']
                        armour_file_option = npc['armourset']
                        jewellery_file_option = npc['jeweleryset']
                        weapon_file_option_main = npc['weapons-main']
                        weapon_file_option_off = npc['weapons-off']
                        weapon_file_option_both = npc['weapons-both']

                        entity_ai = configUtilities.get_config_value_as_string(configfile=self.game_config,
                                                                               section='game',
                                                                               parameter='AI_LEVEL_' + npc_ai)
                        logger.warning('--- CREATING NEW MOBILE ---')
                        # -------------------------------------
                        # --- CHOOSE NAME ---------------------
                        # -------------------------------------
                        first_name = self.choose_name_for_mobile(name_choice=npc_name)
                        MobileUtilities.set_mobile_first_name(gameworld=self.gameworld, entity=entity_id,
                                                              name=first_name)
                        logger.info('Their name is {}', first_name)
                        # -------------------------------------
                        # --- CHOOSE RACE ---------------------
                        # -------------------------------------
                        self.choose_race_for_mobile(race_choice=npc_race, entity_id=entity_id)

                        # -------------------------------------
                        # --- CHOOSE CLASS --------------------
                        # -------------------------------------
                        self.choose_class_for_mobile(class_choice=npc_class, entity_id=entity_id)

                        # -------------------------------------
                        # --- CREATE ARMOURSET ----------------
                        # -------------------------------------
                        self.choose_armourset_for_mobile(armour_file_option=armour_file_option, entity_id=entity_id)

                        # -------------------------------------
                        # --- CREATE JEWELLERYSET -------------
                        # -------------------------------------
                        self.choose_jewellery_package(jewellery_file_option=jewellery_file_option,
                                                          entity_id=entity_id)

                        # -------------------------------------
                        # --- CREATE WEAPONSET ----------------
                        # -------------------------------------
                        self.choose_weaponset(entity_id=entity_id, main_hand=weapon_file_option_main, off_hand=weapon_file_option_off, both_hands=weapon_file_option_both)

                        # now apply the values to the base mobile object

                        MobileUtilities.set_entity_ai(gameworld=self.gameworld, entity=entity_id, value=entity_ai)
                        MobileUtilities.set_mobile_description(gameworld=self.gameworld, entity=entity_id,
                                                               value=npc_desc)
                        MobileUtilities.set_mobile_glyph(gameworld=self.gameworld, entity=entity_id, value=npc_glyph)
                        MobileUtilities.set_mobile_fg_render_colour(gameworld=self.gameworld, entity=entity_id,
                                                                    value=npc_fg.upper())
                        MobileUtilities.set_mobile_bg_render_colour(gameworld=self.gameworld, entity=entity_id,
                                                                    value=npc_bg.upper())
                        MobileUtilities.set_mobile_render_image(gameworld=self.gameworld, entity=entity_id,
                                                                value=npc_image)
                        MobileUtilities.set_mobile_visible(gameworld=self.gameworld, entity=entity_id)
                        MobileUtilities.set_mobile_position(gameworld=self.gameworld, entity=entity_id, posx=posx,
                                                            posy=posy)

                        logger.warning('--- NEW MOBILE CREATED ---')

    def choose_name_for_mobile(self, name_choice):
        selected_name = name_choice
        if name_choice == 'RANDOM':
            selected_name = 'something'
        return selected_name

    def choose_race_for_mobile(self, race_choice, entity_id):
        if race_choice == 'RANDOM':
            player_race_file = configUtilities.get_config_value_as_string(configfile=self.game_config,
                                                                          section='default', parameter='RACESFILE')
            race_file = read_json_file(player_race_file)

            race_name = []
            race_flavour = []
            race_prefix = []
            race_bg_colour = []
            race_size = []
            race_attributes = []

            for option in race_file['races']:
                race_name.append(option['name'])
                race_flavour.append(option['flavour'])
                race_prefix.append(option['prefix'])
                # race_bg_colour.append(option['bg_colour']) // TODO use colorutils to set the background colour
                race_bg_colour.append(colourUtilities.get('BLACK'))
                race_size.append(option['size'])
                race_attributes.append(option['attributes'])

            selected_race_id = random.randint(0, len(race_name) - 1)

            selected_race = race_name[selected_race_id]
            selected_race_size = race_size[selected_race_id]
            selected_bg_colour = race_bg_colour[selected_race_id]

        else:
            selected_race = race_choice
            selected_race_size = 'normal'
            selected_bg_colour = 'black'

        MobileUtilities.setup_racial_attributes(gameworld=self.gameworld, player=entity_id,
                                                selected_race=selected_race,
                                                race_size=selected_race_size,
                                                bg=selected_bg_colour)
        logger.info('Their race is {}', selected_race)

    def choose_class_for_mobile(self, class_choice, entity_id):

        if class_choice == 'RANDOM':
            player_class_file = configUtilities.get_config_value_as_string(configfile=self.game_config,
                                                                           section='default',
                                                                           parameter='CLASSESFILE')
            class_file = read_json_file(player_class_file)
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

        MobileUtilities.setup_class_attributes(gameworld=self.gameworld, player=entity_id,
                                               selected_class=selected_class_name, health=int(selected_class_health),
                                               spellfile=selected_cass_spellfile)

        logger.info('Their class is {}', selected_class_name)

    def choose_armourset_for_mobile(self, armour_file_option, entity_id):
        if armour_file_option != '':
            armourset_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
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

                    as_prefix_list, px_att_bonus = self.build_armourset_prefix_list(prefix_count=prefix_count,
                                                                                    attribute_bonus_count=attribute_bonus_count,
                                                                                    as_prefix_list=as_prefix_list,
                                                                                    prefix_list=prefix_list,
                                                                                    armourset=armourset)
            armour_modifier = self.choose_armour_modifier(armour_file_option=armour_file_option,
                                                          as_prefix_list=as_prefix_list)

            logger.info('Their armour modifier is {}', armour_modifier)
            armour_mod_index = as_prefix_list.index(armour_modifier)
            px_bonus = int(px_att_bonus[armour_mod_index])
            MobileUtilities.create_armour_for_npc(gameworld=self.gameworld, entity_id=entity_id,
                                                  armour_modifier=armour_modifier, px_bonus=px_bonus)
            ItemManager.create_and_equip_armourset_for_npc(gameworld=self.gameworld, as_display_name=as_display_name,
                                                           armour_modifier=armour_modifier, entity_id=entity_id)

    def build_armourset_prefix_list(self, prefix_count, attribute_bonus_count, as_prefix_list, prefix_list, armourset):
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

    def choose_armour_modifier(self, armour_file_option, as_prefix_list):
        armour_modifier = ''
        if armour_file_option == 'RANDOM':
            # generate them procedurally
            # choose random armour modifier taken from as_prefix_list
            armour_modifier = random.choice(as_prefix_list)
        else:
            armour_modifier = armour_file_option.lower()

        return armour_modifier

    def choose_jewellery_package(self, jewellery_file_option, entity_id):
        if jewellery_file_option != '':
            jewellery_packages = configUtilities.get_config_value_as_list(configfile=self.game_config, section='newgame',
                                                                          parameter='JEWELLERY_PACKAGES')

            npc_class_file = configUtilities.get_config_value_as_string(configfile=self.game_config,
                                                                        section='default', parameter='CLASSESFILE')
            if jewellery_file_option == 'RANDOM':
                jewellery_set = random.choice(jewellery_packages)
            else:
                jewellery_set = jewellery_file_option.lower()

            logger.info('Their jewellery package is {}', jewellery_set)
            ItemManager.create_and_equip_jewellery_for_npc(gameworld=self.gameworld, entity_id=entity_id,
                                                           jewellery_set=jewellery_set, npc_class_file=npc_class_file)

    def choose_weaponset(self, entity_id, main_hand, off_hand, both_hands):

        selected_class = MobileUtilities.get_character_class(self.gameworld, entity=entity_id)
        # gather list of available weapons for the player class
        available_weapons = self.build_available_weapons(selected_class=selected_class)
        if main_hand != '':
            self.select_main_hand_weapon(main_hand=main_hand, available_weapons=available_weapons, selected_class=selected_class, entity_id=entity_id)

        if off_hand != '':
            self.select_off_hand_weapon(off_hand=off_hand, available_weapons=available_weapons, selected_class=selected_class, entity_id=entity_id)

        if both_hands != '':
            self.select_both_hands_weapon(both_hands=both_hands, available_weapons=available_weapons, selected_class=selected_class, entity_id=entity_id)

    def select_main_hand_weapon(self, main_hand, available_weapons, selected_class, entity_id):
        weapon_choices = []
        weapon_to_create = ''
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
                                                                       parameter='WEAPONSFILE')

        logger.info('weapons available {}', available_weapons)
        if main_hand == 'RANDOM':
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

        self.create_weapon_and_wield_for_npc(weapon_to_be_created=weapon_to_create, enemy_class=selected_class,
                                             entity_id=entity_id, hand_to_wield='main')
        logger.info('Their main hand weapon is {}', weapon_to_create)

    def select_off_hand_weapon(self, off_hand, available_weapons, selected_class, entity_id):
        weapon_choices = []
        weapon_to_create = ''
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
                                                                       parameter='WEAPONSFILE')

        if off_hand == 'RANDOM':
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

        self.create_weapon_and_wield_for_npc(weapon_to_be_created=weapon_to_create, enemy_class=selected_class,
                                             entity_id=entity_id, hand_to_wield='main')
        logger.info('Their off hand weapon is {}', weapon_to_create)

    def select_both_hands_weapon(self, both_hands, available_weapons, selected_class, entity_id):
        weapon_choices = []
        weapon_to_create = ''
        weapon_class_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
                                                                       parameter='WEAPONSFILE')

        if both_hands == 'RANDOM':
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

        self.create_weapon_and_wield_for_npc(weapon_to_be_created=weapon_to_create, enemy_class=selected_class,
                                             entity_id=entity_id, hand_to_wield='main')
        logger.info('Their both hands weapon is {}', weapon_to_create)

    def build_available_weapons(self, selected_class):
        player_class_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
                                                                       parameter='CLASSESFILE')
        class_file = read_json_file(player_class_file)
        available_weapons = []

        for option in class_file['classes']:
            if option['spellfile'] == selected_class:
                if option["weapons"]["sword"] == 'true':
                    available_weapons.append('sword')
                elif option["weapons"]["wand"] == 'true':
                    available_weapons.append('wand')
                elif option["weapons"]["scepter"] == 'true':
                    available_weapons.append('scepter')
                elif option["weapons"]["staff"] == 'true':
                    available_weapons.append('staff')
                elif option["weapons"]["dagger"] == 'true':
                    available_weapons.append('dagger')
                elif option["weapons"]["rod"] == 'true':
                    available_weapons.append('rod')
                elif option["weapons"]["focus"] == 'true':
                    available_weapons.append('focus')
        return available_weapons

    def create_weapon_and_wield_for_npc(self, weapon_to_be_created, enemy_class, entity_id, hand_to_wield):
        created_weapon = ItemManager.create_weapon(gameworld=self.gameworld, weapon_type=weapon_to_be_created,
                                                   game_config=self.game_config)
        weapon_type = ItemUtilities.get_weapon_type(self.gameworld, created_weapon)

        if enemy_class == '':
            logger.warning('Spell file name not set')

        generate_spells(gameworld=self.gameworld, game_config=self.game_config, spell_file=enemy_class,
                        player_class=enemy_class)

        WeaponClass.load_weapon_with_spells(self.gameworld, created_weapon, weapon_type, enemy_class)

        # equip player with newly created starting weapon
        MobileUtilities.equip_weapon(gameworld=self.gameworld, entity=entity_id, weapon=created_weapon,
                                     hand=hand_to_wield)
