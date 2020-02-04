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

    def create_new_enemy(self, entity_id, enemy_name):
        enemy_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
                                                                      parameter='ENEMIESFILE')

        MobileUtilities.create_base_mobile(gameworld=self.gameworld, game_config=self.game_config, entity_id=entity_id)

        enemies_file = read_json_file(enemy_file)

        for option in enemies_file['enemies']:
            if enemy_name == option['name']:
                enemy_race = option['race']
                enemy_class = option['class']
                enemy_desc = option['description']
                enemy_glyph = option['glyph']
                enemy_fg = option['fg']
                enemy_bg = option['bg']
                enemy_image = int(option['image'])
                enemy_ai = option['ai']

                entity_ai = configUtilities.get_config_value_as_string(configfile=self.game_config, section='game',
                                                                          parameter='AI_LEVEL_' + enemy_ai)
                armour_file_option = option['armourset']
                jewellery_file_option = option['jeweleryset']
                weapon_file_option_main = option['weapons-main']
                weapon_file_option_off = option['weapons-off']
                weapon_file_option_both = option['weapons-both']

                # -------------------------------------
                # --- CREATE ARMOURSET ----------------
                # -------------------------------------

                armourset_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
                                                                            parameter='ARMOURSETFILE')
                armour_file = read_json_file(armourset_file)
                as_display_name = ''
                px_att_bonus = []
                pxstring = 'prefix'
                attvaluestring = 'attributebonus'

                for armourset in armour_file['armoursets']:
                    if armourset['startset'] == 'true':
                        as_display_name = (armourset['displayname'])
                        prefix_list = armourset['prefixlist'].split(",")
                        prefix_count = armourset['prefixcount']
                        attribute_bonus_count = armourset['attributebonuscount']

                        for px in range(1, prefix_count + 1):
                            prefix_string = pxstring + str(px)

                            if attribute_bonus_count > 1:
                                att_bonus_string = attvaluestring + str(px)
                            else:
                                att_bonus_string = attvaluestring + str(1)

                            px_att_bonus.append(armourset[prefix_string][att_bonus_string])

                            as_prefix_list = []
                            [as_prefix_list.append(i.lower()) if not i.islower() else as_prefix_list.append(i) for i in prefix_list]

                if armour_file_option == 'RANDOM':
                    # generate them procedurally
                    # choose random armour modifier taken from as_prefix_list
                    armour_modifier = random.choice(as_prefix_list)
                else:
                    armour_modifier = armour_file_option.lower()

                logger.info('Armour modifier is {}', armour_modifier)
                armour_mod_index = as_prefix_list.index(armour_modifier)
                px_bonus = int(px_att_bonus[armour_mod_index])
                MobileUtilities.create_armour_for_npc(gameworld=self.gameworld, entity_id=entity_id, armour_modifier=armour_modifier, px_bonus=px_bonus)
                ItemManager.create_and_equip_armourset_for_npc(gameworld=self.gameworld, as_display_name=as_display_name, armour_modifier=armour_modifier, entity_id=entity_id)

                # -------------------------------------
                # --- CREATE JEWELLERYSET -------------
                # -------------------------------------
                jewellery_packages = configUtilities.get_config_value_as_list(configfile=self.game_config,
                                                                            section='newgame', parameter='JEWELLERY_PACKAGES')

                npc_class_file = configUtilities.get_config_value_as_string(configfile=self.game_config,
                                                                            section='default', parameter='CLASSESFILE')
                if jewellery_file_option == 'RANDOM':
                    jewellery_set = random.choice(jewellery_packages.lower())
                else:
                    jewellery_set = jewellery_file_option.lower()

                logger.info('Jewellery package is {}',jewellery_set)
                ItemManager.create_and_equip_jewellery_for_npc(gameworld=self.gameworld, entity_id=entity_id, jewellery_set=jewellery_set, npc_class_file=npc_class_file)

                # -------------------------------------
                # --- CREATE WEAPONSET ----------------
                # -------------------------------------
                weapon_to_be_created = ''
                if weapon_file_option_main != '':
                    if weapon_file_option_main == 'RANDOM':
                        weapon_to_be_created = 'random shit'
                        hand_to_wield = 'main'
                    else:
                        weapon_to_be_created = weapon_file_option_main
                        hand_to_wield = 'main'
                        logger.info('Weapon in main hand will be a {}', weapon_file_option_main)

                if weapon_file_option_off != '':
                    if weapon_file_option_off == 'RANDOM':
                        weapon_to_be_created = 'random shit'
                        hand_to_wield = 'off'
                    else:
                        weapon_to_be_created = weapon_file_option_off
                        hand_to_wield = 'off'
                        logger.info('Weapon in off hand will be a {}', weapon_file_option_off)

                if weapon_file_option_both != '':
                    if weapon_file_option_both == 'RANDOM':
                        weapon_to_be_created = 'random shit'
                        hand_to_wield = 'both'
                    else:
                        weapon_to_be_created = weapon_file_option_both
                        hand_to_wield = 'both'

                logger.info('Weapon to be created is a {}', weapon_to_be_created)

                self.create_weapon_and_wield_for_npc(weapon_to_be_created=weapon_to_be_created, enemy_class=enemy_class, entity_id=entity_id, hand_to_wield=hand_to_wield)

            # now apply the values to the base mobile object

                MobileUtilities.set_entity_ai(gameworld=self.gameworld, entity=entity_id, value=entity_ai)
                MobileUtilities.setup_racial_attributes(gameworld=self.gameworld, player=entity_id, selected_race=enemy_race, race_size='normal', bg=colourUtilities.get('BLACK'))
                MobileUtilities.setup_class_attributes(gameworld=self.gameworld, player=entity_id, selected_class=enemy_class, health=100, spellfile='')
                MobileUtilities.set_mobile_description(gameworld=self.gameworld, entity=entity_id, value=enemy_desc)
                MobileUtilities.set_mobile_glyph(gameworld=self.gameworld, entity=entity_id, value=enemy_glyph)
                MobileUtilities.set_mobile_fg_render_colour(gameworld=self.gameworld, entity=entity_id, value=enemy_fg.upper())
                MobileUtilities.set_mobile_bg_render_colour(gameworld=self.gameworld, entity=entity_id, value=enemy_bg.upper())
                MobileUtilities.set_mobile_render_image(gameworld=self.gameworld, entity=entity_id, value=enemy_image)
                MobileUtilities.set_mobile_visible(gameworld=self.gameworld, entity=entity_id)
                MobileUtilities.set_mobile_first_name(gameworld=self.gameworld, entity=entity_id, name=enemy_name)

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