import random

from newGame.Items import ItemManager
from utilities import configUtilities, colourUtilities
from utilities.itemsHelp import ItemUtilities
from utilities.mobileHelp import MobileUtilities
from loguru import logger
from utilities.jsonUtilities import read_json_file

# actions
# create new entity with no trappings --> done
# create and equip armour --> done
# create and equip  weapons
# create and equip  jewellery
# position entity in the game map


class Entity:
    def __init__(self, gameworld):
        self.gameworld = gameworld
        self.game_config = configUtilities.load_config()

    def create_new_entity(self):
        entity_id = MobileUtilities.get_next_entity_id(self.gameworld)
        return entity_id

    def create_new_enemy(self, entity_id):
        enemy_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
                                                                      parameter='ENEMIESFILE')

        MobileUtilities.create_base_mobile(gameworld=self.gameworld, game_config=self.game_config, entity_id=entity_id)

        enemies_file = read_json_file(enemy_file)

        for option in enemies_file['enemies']:
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
            class_file = read_json_file(npc_class_file)
            entity_class = MobileUtilities.get_character_class(gameworld=self.gameworld, entity=entity_id)

            for entityClass in class_file['classes']:
                if entityClass['name'] == entity_class:
                    neck_gemstone = entityClass[jewellery_set]['neck']
                    ring1_gemstone = entityClass[jewellery_set]['ring1']
                    ring2_gemstone = entityClass[jewellery_set]['ring2']
                    ear1_gemstone = entityClass[jewellery_set]['earring1']
                    ear2_gemstone = entityClass[jewellery_set]['earring2']
                    # create jewellery entity
                    pendant = ItemManager.create_jewellery(gameworld=self.gameworld, bodylocation='neck',
                                                           e_setting='copper', e_hook='copper', e_activator=neck_gemstone)
                    left_ring = ItemManager.create_jewellery(gameworld=self.gameworld, bodylocation='ring',
                                                             e_setting='copper', e_hook='copper', e_activator=ring1_gemstone)
                    right_ring = ItemManager.create_jewellery(gameworld=self.gameworld, bodylocation='ring',
                                                              e_setting='copper', e_hook='copper', e_activator=ring2_gemstone)
                    left_ear = ItemManager.create_jewellery(gameworld=self.gameworld, bodylocation='ear',
                                                            e_setting='copper', e_hook='copper', e_activator=ear1_gemstone)
                    right_ear = ItemManager.create_jewellery(gameworld=self.gameworld, bodylocation='ear',
                                                             e_setting='copper', e_hook='copper', e_activator=ear2_gemstone)
                    # equip jewellery entity to player character
                    ItemUtilities.equip_jewellery(gameworld=self.gameworld, mobile=entity_id, bodylocation='neck', trinket=pendant)
                    ItemUtilities.equip_jewellery(gameworld=self.gameworld, mobile=entity_id, bodylocation='left hand', trinket=left_ring)
                    ItemUtilities.equip_jewellery(gameworld=self.gameworld, mobile=entity_id, bodylocation='right hand', trinket=right_ring)
                    ItemUtilities.equip_jewellery(gameworld=self.gameworld, mobile=entity_id, bodylocation='left ear', trinket=left_ear)
                    ItemUtilities.equip_jewellery(gameworld=self.gameworld, mobile=entity_id, bodylocation='right ear', trinket=right_ear)

                    # apply gemstone benefits
                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=self.gameworld, entity=pendant)
                    ItemUtilities.add_jewellery_benefit(gameworld=self.gameworld, entity=entity_id, statbonus=jewelleyStatBonus)

                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=self.gameworld, entity=left_ring)
                    ItemUtilities.add_jewellery_benefit(gameworld=self.gameworld, entity=entity_id, statbonus=jewelleyStatBonus)

                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=self.gameworld,entity=right_ring)
                    ItemUtilities.add_jewellery_benefit(gameworld=self.gameworld, entity=entity_id, statbonus=jewelleyStatBonus)

                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=self.gameworld, entity=left_ear)
                    ItemUtilities.add_jewellery_benefit(gameworld=self.gameworld, entity=entity_id, statbonus=jewelleyStatBonus)

                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=self.gameworld, entity=right_ear)
                    ItemUtilities.add_jewellery_benefit(gameworld=self.gameworld, entity=entity_id, statbonus=jewelleyStatBonus)

            # -------------------------------------
            # --- CREATE WEAPONS ------------------
            # -------------------------------------


            # if option['weapons-present'] == 'no':
            #     if option['weapons-generate'] == 'yes':
            #         pass
            #         # generate them procedurally
            # else:
            #     main_hand = option['weapons-main']
            #     off_hand = option['weapons-off']
            #     both_hands = option['weapons-both']
            #
            # if option['jewellery-present'] == 'no':
            #     if option['jewellery-generate'] == 'yes':
            #         pass
            #         # generate them procedurally
            # else:
            #     jewell_neck = option['jewellery-neck']
            #     jewell_ring1 = option['jewellery-ring1']
            #     jewell_ring2 = option['jewellery-ring2']
            #     jewell_earring1 = option['jewellery-earring1']
            #     jewell_earring2 = option['jewellery-earring2']

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
