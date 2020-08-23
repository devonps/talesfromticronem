from components import items, spells
from utilities import world, jsonUtilities
from utilities.armourManagement import ArmourUtilities
from utilities.jewelleryManagement import JewelleryUtilities
from utilities.mobileHelp import MobileUtilities
from utilities import configUtilities, colourUtilities
from loguru import logger


class ItemManager:
    """
    The purpose of the ItemManager class is to:
    Create ALL items in the game
    Delete ALL items from the game
    Place items in the dungeon

    """
    @staticmethod
    def create_weapon(gameworld, weapon_type, game_config):
        """
        Currently this creates a new weapon using the information in an external file
        :type gameworld: esper.world
        :type weapon_type: the type of weapon to be created, e.g. sword
        """
        weapon_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='WEAPONSFILE')
        weapon_action_list = configUtilities.get_config_value_as_list(configfile=game_config, section='game',
                                                                      parameter='ITEM_WEAPON_ACTIONS')

        weapon_file = jsonUtilities.read_json_file(weapon_file_path)
        for weapon in weapon_file['weapons']:
            if weapon['name'] == weapon_type:
                myweapon = world.get_next_entity_id(gameworld=gameworld)
                # generate common item components
                gameworld.add_component(myweapon, items.TypeOfItem(label='weapon'))
                gameworld.add_component(myweapon, items.Material(texture='wooden'))
                gameworld.add_component(myweapon, items.Actionlist(action_list=weapon_action_list))
                gameworld.add_component(myweapon, items.Describable(
                    description=weapon['description'],
                    name=weapon['name'],
                    glyph=weapon['glyph'],
                    fg=colourUtilities.get('WHITE'),
                    bg=colourUtilities.get('BLACK'),
                    displayname=weapon['display_name']
                ))
                gameworld.add_component(myweapon, items.RenderItem(istrue=True))
                gameworld.add_component(myweapon, items.Quality(level=weapon['quality_level']))

                # generate weapon specific components
                gameworld.add_component(myweapon, items.WeaponType(label=weapon_type))
                gameworld.add_component(myweapon, items.Spells(
                    slot_one='00',
                    slot_two='00',
                    slot_three='00',
                    slot_four='00',
                    slot_five='00'))

                gameworld.add_component(myweapon, items.Wielded(
                    hands=weapon['wielded_hands'],
                    true_or_false=True))

                gameworld.add_component(myweapon, items.Experience(current_level=1))

                gameworld.add_component(myweapon, items.Hallmarks(
                    hallmark_slot_one='00',
                    hallmark_slot_two='00'))

                gameworld.add_component(myweapon, items.DamageRange(ranges=weapon['damage_ranges']))

                return myweapon  # this is the entity id for the newly created weapon

    @staticmethod
    def create_jewellery_for_utility_spells(gameworld, game_config):

        npc_class_file = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                    section='files', parameter='CLASSESFILE')
        entity_id = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

        jewellery_set = 'balanced'
        class_file = jsonUtilities.read_json_file(npc_class_file)
        entity_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=entity_id)

        for entityclass in class_file['classes']:
            if entityclass['name'] == entity_class:
                neck_gemstone = entityclass[jewellery_set]['neck']
                ear1_gemstone = entityclass[jewellery_set]['earring1']
                ear2_gemstone = entityclass[jewellery_set]['earring2']
                ring1_gemstone = entityclass[jewellery_set]['ring1']
                ring2_gemstone = entityclass[jewellery_set]['ring2']
                # create jewellery entity
                pendant = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='neck',
                                                       e_setting='copper', e_hook='copper', e_activator=neck_gemstone, playable_class=entity_class)

                left_ear = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='earring1',
                                                        e_setting='copper', e_hook='copper', e_activator=ear1_gemstone, playable_class=entity_class)

                right_ear = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='earring2',
                                                         e_setting='copper', e_hook='copper', e_activator=ear2_gemstone, playable_class=entity_class)

                left_hand = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ring1',
                                                         e_setting='copper', e_hook='copper', e_activator=ring1_gemstone, playable_class=entity_class)

                right_hand = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ring2',
                                                         e_setting='copper', e_hook='copper', e_activator=ring2_gemstone, playable_class=entity_class)

                # equip jewellery entity to player character
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='neck',
                                              trinket=pendant)
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='left ear',
                                              trinket=left_ear)
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='right ear',
                                              trinket=right_ear)

                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='left hand',
                                              trinket=left_hand)

                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='right hand',
                                              trinket=right_hand)


                # apply gemstone benefits
                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=pendant)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewelley_stat_bonus)

                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=left_ear)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewelley_stat_bonus)

                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=right_ear)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewelley_stat_bonus)

                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=left_hand)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id, statbonus=jewelley_stat_bonus)

                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=right_hand)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id, statbonus=jewelley_stat_bonus)


    @staticmethod
    def create_and_equip_jewellery_for_npc(gameworld, entity_id, jewellery_set, npc_class_file):
        class_file = jsonUtilities.read_json_file(npc_class_file)
        entity_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=entity_id)

        for entityclass in class_file['classes']:
            if entityclass['name'] == entity_class:
                neck_gemstone = entityclass[jewellery_set]['neck']
                ear1_gemstone = entityclass[jewellery_set]['earring1']
                ear2_gemstone = entityclass[jewellery_set]['earring2']
                # create jewellery entity
                pendant = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='neck',
                                                       e_setting='copper', e_hook='copper', e_activator=neck_gemstone, playable_class=entity_class)
                left_ear = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='earring1',
                                                        e_setting='copper', e_hook='copper', e_activator=ear1_gemstone, playable_class=entity_class)

                right_ear = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='earring2',
                                                         e_setting='copper', e_hook='copper', e_activator=ear2_gemstone, playable_class=entity_class)

                # equip jewellery entity to player character
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='neck',
                                              trinket=pendant)
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='left ear',
                                              trinket=left_ear)
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='right ear',
                                              trinket=right_ear)

                # apply gemstone benefits
                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=pendant)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewelley_stat_bonus)

                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=left_ear)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewelley_stat_bonus)

                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=right_ear)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewelley_stat_bonus)




    @staticmethod
    def create_jewellery(gameworld, bodylocation, e_setting, e_hook, e_activator, playable_class):
        """
        Will create a piece of jewellery the e_setting informs the tier, e.g. copper is only used in Tier 1 jewellery
        The e_activator is the gemstone - this drives the attribute bonuses

        :param bodylocation:
        :param e_setting: the quality level of the jewellery and the base metal used, e.g. copper
        :param e_hook: a 3rd component used in crafting
        :param e_activator: the gemstone used in the jewellery, drives the attribute bonus
        :return:
        """
        game_config = configUtilities.load_config()
        trinket_setting = e_setting.lower()
        trinket_hook = e_hook.lower()
        trinket_activator = e_activator.lower()

        gemstones_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                         parameter='GEMSTONESFILE')
        jewellery_action_list = configUtilities.get_config_value_as_list(configfile=game_config, section='game',
                                                                         parameter='ITEM_JEWELLERY_ACTIONS')
        if trinket_setting == '' or trinket_activator == '' or trinket_hook == '':
            logger.debug('At least one base component is missing')
            return 0
        if trinket_setting != trinket_hook:
            logger.debug("Jewellery setting and hook base metals don't match")
            return 0

        gemstone_file = jsonUtilities.read_json_file(gemstones_file_path)
        gemstone_string = ' gemstone.'

        for gemstone in gemstone_file['gemstones']:
            file_gemstone = gemstone['Stone'].lower()
            if file_gemstone == trinket_activator:
                bdl = ItemManager.define_jewellery_bodylocation_string(bodylocation=bodylocation)
                piece_of_jewellery = world.get_next_entity_id(gameworld=gameworld)
                # generate common item components
                gameworld.add_component(piece_of_jewellery, items.TypeOfItem(label='jewellery'))
                gameworld.add_component(piece_of_jewellery, items.Material(texture=trinket_setting))
                gameworld.add_component(piece_of_jewellery, items.RenderItem(istrue=True))
                gameworld.add_component(piece_of_jewellery, items.Quality(level='common'))
                gameworld.add_component(piece_of_jewellery, items.Actionlist(action_list=jewellery_action_list))

                # create jewellery specific components
                gameworld.add_component(piece_of_jewellery, items.JewelleryEquipped(istrue=False))
                gameworld.add_component(piece_of_jewellery,
                                        items.JewelleryComponents(setting=trinket_setting, hook=trinket_hook,
                                                                  activator=trinket_activator))
                gameworld.add_component(piece_of_jewellery, items.JewellerySpell)

                for spell_entity, (name, location, spell_type, item_type, spclass) in gameworld.get_components(spells.Name,
                                                                                                      spells.ItemLocation,
                                                                                                      spells.SpellType,
                                                                                                      spells.ItemType, spells.ClassName):
                    if spclass.label == playable_class and spell_type.label == 'utility' and item_type.label == 'jewellery' and location.label == bodylocation:
                        JewelleryUtilities.add_spell_to_jewellery(gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, spell_entity=spell_entity)
                        ItemManager.earring_processing(bdl=bdl, trinket_activator=trinket_activator, gemstone_string=gemstone_string, gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, gemstone_attribute=gemstone['Attribute'], gemstone_bonus=gemstone['Earring'])

                        ItemManager.pendant_processing(bdl=bdl, trinket_activator=trinket_activator, gemstone_string=gemstone_string, gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, gemstone_attribute=gemstone['Attribute'], gemstone_bonus=gemstone['Amulet'])

                        ItemManager.hands_processing(bdl=bdl, trinket_activator=trinket_activator, gemstone_string=gemstone_string, gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, gemstone_attribute=gemstone['Attribute'], gemstone_bonus=gemstone['Ring'])

                        bdl = ''
                return piece_of_jewellery

    @staticmethod
    def hands_processing(bdl, trinket_activator, gemstone_string, gameworld, piece_of_jewellery, gemstone_attribute, gemstone_bonus):
        if 'hands' in bdl:
            # create a ring
            desc = ' ring, offset with a ' + trinket_activator + gemstone_string
            nm = 'ring'
            gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(fingers=True))
            gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                statname=gemstone_attribute, statbonus=gemstone_bonus))
            gameworld.add_component(piece_of_jewellery, items.Describable(
                description=desc, name=nm, glyph='*',
                fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'),
                displayname=trinket_activator + ' ' + nm))



    @staticmethod
    def pendant_processing(bdl, trinket_activator, gemstone_string, gameworld, piece_of_jewellery, gemstone_attribute, gemstone_bonus):
        if 'neck' in bdl:
            # create a pendant
            desc = ' pendant, offset with a ' + trinket_activator + gemstone_string
            nm = 'pendant'
            gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(neck=True))
            gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                statname=gemstone_attribute, statbonus=gemstone_bonus))
            gameworld.add_component(piece_of_jewellery, items.Describable(
                description=desc, name=nm, glyph='*',
                fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'),
                displayname=trinket_activator + ' ' + nm))

    @staticmethod
    def earring_processing(bdl, trinket_activator, gemstone_string, gameworld, piece_of_jewellery, gemstone_attribute, gemstone_bonus):
        if 'ear' in bdl:
            # create an earring
            desc = ' earring, offset with a ' + trinket_activator + gemstone_string
            nm = 'earring'
            gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(ears=True))
            gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                statname=gemstone_attribute, statbonus=gemstone_bonus))
            gameworld.add_component(piece_of_jewellery, items.Describable(
                description=desc, name=nm, glyph='*',
                fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'),
                displayname=trinket_activator + ' ' + nm))

    @staticmethod
    def define_jewellery_bodylocation_string(bodylocation):
        if bodylocation in ('earring1', 'earring2'):
            bdl = 'ear'
        elif bodylocation in ('ring1', 'ring2'):
            bdl = 'hands'
        else:
            bdl = 'neck'

        return bdl

