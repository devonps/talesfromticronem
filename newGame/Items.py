from components import items
from utilities import jsonUtilities, itemsHelp, configUtilities, world


class ItemManager:
    """
    The purpose of the ItemManager class is to:
    Create ALL items in the game
    Delete ALL items from the game
    Place items in the dungeon

    """

    @staticmethod
    def create_base_item(gameworld):
        this_item_id = world.get_next_entity_id(gameworld=gameworld)
        gameworld.add_component(this_item_id, items.TypeOfItem())
        gameworld.add_component(this_item_id, items.Material())
        gameworld.add_component(this_item_id, items.Name())
        gameworld.add_component(this_item_id, items.Description())
        gameworld.add_component(this_item_id, items.ItemGlyph())
        gameworld.add_component(this_item_id, items.ItemForeColour())
        gameworld.add_component(this_item_id, items.ItemBackColour())
        gameworld.add_component(this_item_id, items.ItemDisplayName())

        return this_item_id


    @staticmethod
    def create_weapon(gameworld, weapon_type, game_config):
        """
        Currently this creates a new weapon using the information in an external file
        :type gameworld: esper.world
        :type weapon_type: the type of weapon to be created, e.g. sword
        """
        weapon_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='WEAPONSFILE')

        weapon_file = jsonUtilities.read_json_file(weapon_file_path)

        item_fg = "[color=ITEM_GENERIC_FG]"
        item_bg = "[color=ITEM_GENERIC_BG]"

        for weapon in weapon_file['weapons']:
            if weapon['name'] == weapon_type:
                myweapon = ItemManager.create_base_item(gameworld=gameworld)
                # generate common item components
                itemsHelp.ItemUtilities.set_type_of_item(gameworld=gameworld, entity_id=myweapon, value='weapon')
                gameworld.add_component(myweapon, items.Material(texture='wooden'))
                itemsHelp.ItemUtilities.set_item_name(gameworld=gameworld, entity_id=myweapon, value=weapon['name'])
                itemsHelp.ItemUtilities.set_item_description(gameworld=gameworld, entity_id=myweapon, value=weapon['description'])
                itemsHelp.ItemUtilities.set_item_glyph(gameworld=gameworld, entity_id=myweapon, value=weapon['glyph'])
                itemsHelp.ItemUtilities.set_item_foreground_colour(gameworld=gameworld, entity_id=myweapon, value=item_fg)
                itemsHelp.ItemUtilities.set_item_background_colour(gameworld=gameworld, entity_id=myweapon, value=item_bg)
                itemsHelp.ItemUtilities.set_item_displayname(gameworld=gameworld, entity_id=myweapon, value=weapon['display_name'])

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

                gameworld.add_component(myweapon, items.Experience(current_level=11))

                gameworld.add_component(myweapon, items.Hallmarks(
                    hallmark_slot_one='00',
                    hallmark_slot_two='00'))

                gameworld.add_component(myweapon, items.DamageRange(ranges=weapon['damage_ranges']))

                return myweapon  # this is the entity id for the newly created weapon
