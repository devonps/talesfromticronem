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
    def create_and_equip_jewellery_for_npc(gameworld, entity_id, jewellery_set, npc_class_file):
        class_file = jsonUtilities.read_json_file(npc_class_file)
        entity_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=entity_id)

        for entityclass in class_file['classes']:
            if entityclass['name'] == entity_class:
                neck_gemstone = entityclass[jewellery_set]['neck']
                ear1_gemstone = entityclass[jewellery_set]['earring1']
                ear2_gemstone = entityclass[jewellery_set]['earring2']
                # create jewellery entity
                pendant = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='neck',
                                                       e_setting='copper', e_hook='copper', e_activator=neck_gemstone, playable_class=entity_class)
                left_ear = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='earring1',
                                                        e_setting='copper', e_hook='copper', e_activator=ear1_gemstone, playable_class=entity_class)

                right_ear = JewelleryUtilities.create_jewellery(gameworld=gameworld, bodylocation='earring2',
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

