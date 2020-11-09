from loguru import logger

from components import items, mobiles, spells
from newGame import Items
from utilities import configUtilities, jsonUtilities, colourUtilities, itemsHelp, mobileHelp


class JewelleryUtilities:

    @staticmethod
    def create_and_equip_jewellery_for_npc(gameworld, entity_id, jewellery_set, npc_class_file):
        class_file = jsonUtilities.read_json_file(npc_class_file)
        entity_class = mobileHelp.MobileUtilities.get_character_class(gameworld=gameworld, entity=entity_id)
        left_ear_string = 'left ear'
        right_ear_string = 'right ear'

        for entityclass in class_file['classes']:
            if entityclass['name'] == entity_class:
                neck_gemstone = entityclass[jewellery_set]['neck']
                ear1_gemstone = entityclass[jewellery_set]['earring1']
                ear2_gemstone = entityclass[jewellery_set]['earring2']
                # create jewellery entity
                pendant = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='neck',
                                                              e_setting='copper', e_hook='copper',
                                                              e_activator=neck_gemstone, playable_class=entity_class)
                left_ear = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='earring1',
                                                               e_setting='copper', e_hook='copper',
                                                               e_activator=ear1_gemstone, playable_class=entity_class)

                right_ear = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='earring2',
                                                                e_setting='copper', e_hook='copper',
                                                                e_activator=ear2_gemstone, playable_class=entity_class)

                # equip jewellery entity to player character
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation='neck',
                                                   trinket=pendant)
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation=left_ear_string,
                                                   trinket=left_ear)
                JewelleryUtilities.equip_jewellery(gameworld=gameworld, mobile=entity_id, bodylocation=right_ear_string,
                                                   trinket=right_ear)

                # apply gemstone benefits
                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld,
                                                                                  jewellery_entity=pendant)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                         statbonus=jewelley_stat_bonus)

                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld,
                                                                                  jewellery_entity=left_ear)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                         statbonus=jewelley_stat_bonus)

                jewelley_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld,
                                                                                  jewellery_entity=right_ear)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                         statbonus=jewelley_stat_bonus)


    @staticmethod
    def get_gemstone_details(this_gemstone):
        game_config = configUtilities.load_config()
        playable_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                    parameter='GEMSTONESFILE')
        gemstone_file = jsonUtilities.read_json_file(playable_class_file)

        gem_details = []

        for gems in gemstone_file['gemstones']:
            if this_gemstone == gems['Stone'].lower():
                gem_details.append(gems['shop_display'])
                gem_details.append('+' + str(gems['Amulet']))
                gem_details.append('+' + str(gems['Ring']))
                gem_details.append('+' + str(gems['Earring']))

        return gem_details


    @staticmethod
    def load_jewellery_package_based_on_class(playable_class, game_config):
        playable_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                    parameter='CLASSESFILE')
        class_file = jsonUtilities.read_json_file(playable_class_file)

        balanced = []
        defensive = []
        offensive = []

        for play_class in class_file['classes']:
            if playable_class == play_class['name']:
                balanced.append(play_class['balanced'])
                defensive.append(play_class['defensive'])
                offensive.append(play_class['offensive'])

        return defensive, balanced, offensive


    @staticmethod
    def get_jewellery_activator(gameworld, jewellery_entity):
        jewellery_materials_componet = gameworld.component_for_entity(jewellery_entity, items.JewelleryComponents)
        return jewellery_materials_componet.activator

    @staticmethod
    def get_jewellery_stat_bonus(gameworld, jewellery_entity):
        jewellery_statbonus_component = gameworld.component_for_entity(jewellery_entity, items.JewelleryStatBonus)
        statbonus = [jewellery_statbonus_component.stat_name, jewellery_statbonus_component.stat_bonus]
        return statbonus

    @staticmethod
    def get_jewellery_already_equipped_status(gameworld, jewellery_entity):
        jewellery_equipped_component = gameworld.component_for_entity(jewellery_entity, items.JewelleryEquipped)
        return jewellery_equipped_component.istrue

    @staticmethod
    def set_jewellery_equipped_status_to_true(gameworld, jewellery_entity):
        gameworld.component_for_entity(jewellery_entity, items.JewelleryEquipped).istrue = True

    @staticmethod
    def set_jewellery_equipped_status_to_false(gameworld, jewellery_entity):
        gameworld.component_for_entity(jewellery_entity, items.JewelleryEquipped).istrue = False


    @staticmethod
    def get_list_of_spell_entities_for_equpped_jewellery(gameworld, player_entity):
        spell_entities = []

        for a in ['neck', 'lear', 'rear', 'lhand', 'rhand']:
            entity_id = JewelleryUtilities.get_jewellery_entity_from_body_location(gameworld=gameworld, entity=player_entity, bodylocation=a)

            if entity_id > 0:
                spell_id = JewelleryUtilities.get_spell_entity_from_jewellery(gameworld=gameworld, piece_of_jewellery=entity_id)
                if spell_id > 0:
                    spell_entities.append(spell_id)

        return spell_entities



    @staticmethod
    def get_jewellery_entity_from_body_location(gameworld, entity, bodylocation):
        jewellery_worn = 0
        if bodylocation == 'neck':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).neck
        if bodylocation == 'lear':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).left_ear
        if bodylocation == 'rear':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).right_ear
        if bodylocation == 'lhand':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).left_hand
        if bodylocation == 'rhand':
            jewellery_worn = gameworld.component_for_entity(entity, mobiles.Jewellery).right_hand

        return jewellery_worn

    @staticmethod
    def equip_jewellery(gameworld, mobile, bodylocation, trinket):
        is_jewellery_equipped = JewelleryUtilities.get_jewellery_already_equipped_status(gameworld, jewellery_entity=trinket)
        if not is_jewellery_equipped:
            if bodylocation == 'left ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).left_ear = trinket
            if bodylocation == 'right ear':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).right_ear = trinket
            if bodylocation == 'left hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).left_hand = trinket
            if bodylocation == 'right hand':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).right_hand = trinket
            if bodylocation == 'neck':
                gameworld.component_for_entity(mobile, mobiles.Jewellery).neck = trinket

            JewelleryUtilities.set_jewellery_equipped_status_to_true(gameworld, jewellery_entity=trinket)

    @staticmethod
    def add_jewellery_benefit(gameworld, entity, statbonus):

        stat = statbonus[0]
        benefit = statbonus[1]

        if stat.lower() == 'condition damage':
            mobileHelp.MobileUtilities.set_mobile_secondary_condition_damage(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'power':
            mobileHelp.MobileUtilities.set_mobile_primary_power(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'vitality':
            mobileHelp.MobileUtilities.set_mobile_primary_vitality(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'toughness':
            mobileHelp.MobileUtilities.set_mobile_primary_toughness(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'healing power':
            mobileHelp.MobileUtilities.set_mobile_secondary_healing_power(gameworld=gameworld, entity=entity, value=benefit)

        if stat.lower() == 'precision':
            mobileHelp.MobileUtilities.set_mobile_primary_precision(gameworld=gameworld, entity=entity, value=benefit)

    @staticmethod
    def add_spell_to_jewellery(gameworld, piece_of_jewellery, spell_entity):
        gameworld.add_component(piece_of_jewellery, items.JewellerySpell(entity=spell_entity))


    @staticmethod
    def get_spell_entity_from_jewellery(gameworld, piece_of_jewellery):
        jewellery_spell_component = gameworld.component_for_entity(piece_of_jewellery, items.JewellerySpell)
        return jewellery_spell_component.entity


    @staticmethod
    def create_jewellery_for_utility_spells(gameworld, game_config, jewellery_set):

        npc_class_file = configUtilities.get_config_value_as_string(configfile=game_config,
                                                                    section='files', parameter='CLASSESFILE')
        entity_id = mobileHelp.MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)

        class_file = jsonUtilities.read_json_file(npc_class_file)
        entity_class = mobileHelp.MobileUtilities.get_character_class(gameworld=gameworld, entity=entity_id)

        for entityclass in class_file['classes']:
            if entityclass['name'] == entity_class:
                neck_gemstone = entityclass[jewellery_set]['neck']
                ear1_gemstone = entityclass[jewellery_set]['earring1']
                ear2_gemstone = entityclass[jewellery_set]['earring2']
                ring1_gemstone = entityclass[jewellery_set]['ring1']
                ring2_gemstone = entityclass[jewellery_set]['ring2']
                # create jewellery entity
                pendant = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='neck',
                                                       e_setting='copper', e_hook='copper', e_activator=neck_gemstone, playable_class=entity_class)

                left_ear = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='earring1',
                                                        e_setting='copper', e_hook='copper', e_activator=ear1_gemstone, playable_class=entity_class)

                right_ear = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='earring2',
                                                         e_setting='copper', e_hook='copper', e_activator=ear2_gemstone, playable_class=entity_class)

                left_hand = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='ring1',
                                                         e_setting='copper', e_hook='copper', e_activator=ring1_gemstone, playable_class=entity_class)

                right_hand = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='ring2',
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
                jewellery_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=pendant)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewellery_stat_bonus)

                jewellery_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=left_ear)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewellery_stat_bonus)

                jewellery_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=right_ear)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id,
                                                    statbonus=jewellery_stat_bonus)

                jewellery_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=left_hand)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id, statbonus=jewellery_stat_bonus)

                jewellery_stat_bonus = JewelleryUtilities.get_jewellery_stat_bonus(gameworld=gameworld, jewellery_entity=right_hand)
                JewelleryUtilities.add_jewellery_benefit(gameworld=gameworld, entity=entity_id, statbonus=jewellery_stat_bonus)

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
                bdl = JewelleryUtilities.define_jewellery_bodylocation_string(bodylocation=bodylocation)
                piece_of_jewellery = Items.ItemManager.create_base_item(gameworld=gameworld)
                # generate common item components
                itemsHelp.ItemUtilities.set_type_of_item(gameworld=gameworld, entity_id=piece_of_jewellery, value='jewellery')
                gameworld.add_component(piece_of_jewellery, items.Material(texture=trinket_setting))
                gameworld.add_component(piece_of_jewellery, items.RenderItem(istrue=True))
                gameworld.add_component(piece_of_jewellery, items.Quality(level='common'))

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
                        JewelleryUtilities.earring_processing(bdl=bdl, trinket_activator=trinket_activator, gemstone_string=gemstone_string, gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, gemstone_attribute=gemstone['Attribute'], gemstone_bonus=gemstone['Earring'])

                        JewelleryUtilities.pendant_processing(bdl=bdl, trinket_activator=trinket_activator, gemstone_string=gemstone_string, gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, gemstone_attribute=gemstone['Attribute'], gemstone_bonus=gemstone['Amulet'])

                        JewelleryUtilities.hands_processing(bdl=bdl, trinket_activator=trinket_activator, gemstone_string=gemstone_string, gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, gemstone_attribute=gemstone['Attribute'], gemstone_bonus=gemstone['Ring'])

                        bdl = ''
                return piece_of_jewellery

    @staticmethod
    def define_jewellery_bodylocation_string(bodylocation):
        if bodylocation in ('earring1', 'earring2'):
            bdl = 'ear'
        elif bodylocation in ('ring1', 'ring2'):
            bdl = 'hands'
        else:
            bdl = 'neck'

        return bdl

    @staticmethod
    def hands_processing(bdl, trinket_activator, gemstone_string, gameworld, piece_of_jewellery, gemstone_attribute, gemstone_bonus):
        if 'hands' in bdl:
            # create a ring
            desc = ' ring, offset with a ' + trinket_activator + gemstone_string
            nm = 'ring'
            gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(fingers=True))
            gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                statname=gemstone_attribute, statbonus=gemstone_bonus))

            JewelleryUtilities.common_jewellery_create_method(gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, nm=nm, desc=desc, trinket_activator=trinket_activator)

    @staticmethod
    def pendant_processing(bdl, trinket_activator, gemstone_string, gameworld, piece_of_jewellery, gemstone_attribute, gemstone_bonus):
        if 'neck' in bdl:
            # create a pendant
            desc = ' pendant, offset with a ' + trinket_activator + gemstone_string
            nm = 'pendant'
            gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(neck=True))
            gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                statname=gemstone_attribute, statbonus=gemstone_bonus))

            JewelleryUtilities.common_jewellery_create_method(gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, nm=nm, desc=desc, trinket_activator=trinket_activator)

    @staticmethod
    def earring_processing(bdl, trinket_activator, gemstone_string, gameworld, piece_of_jewellery, gemstone_attribute, gemstone_bonus):
        if 'ear' in bdl:
            # create an earring
            desc = ' earring, offset with a ' + trinket_activator + gemstone_string
            nm = 'earring'
            gameworld.add_component(piece_of_jewellery, items.JewelleryBodyLocation(ears=True))
            gameworld.add_component(piece_of_jewellery, items.JewelleryStatBonus(
                statname=gemstone_attribute, statbonus=gemstone_bonus))

            JewelleryUtilities.common_jewellery_create_method(gameworld=gameworld, piece_of_jewellery=piece_of_jewellery, nm=nm, desc=desc, trinket_activator=trinket_activator)

    @staticmethod
    def common_jewellery_create_method(gameworld,piece_of_jewellery, nm, desc, trinket_activator):
        itemsHelp.ItemUtilities.set_item_name(gameworld=gameworld, entity_id=piece_of_jewellery, value=nm)
        itemsHelp.ItemUtilities.set_item_description(gameworld=gameworld, entity_id=piece_of_jewellery, value=desc)
        itemsHelp.ItemUtilities.set_item_glyph(gameworld=gameworld, entity_id=piece_of_jewellery, value='*')
        itemsHelp.ItemUtilities.set_item_foreground_colour(gameworld=gameworld, entity_id=piece_of_jewellery,
                                                 value=colourUtilities.get('BLUE'))
        itemsHelp.ItemUtilities.set_item_background_colour(gameworld=gameworld, entity_id=piece_of_jewellery,
                                                 value=colourUtilities.get('BLACK'))
        itemsHelp.ItemUtilities.set_item_displayname(gameworld=gameworld, entity_id=piece_of_jewellery,
                                           value=trinket_activator + ' ' + nm)
