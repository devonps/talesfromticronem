from newGame import constants
from components import items
from utilities import world
from utilities import jsonUtilities
from loguru import logger


class Items:

    def create_weapon(gameworld, weapon_type):
        """
        :type gameworld: esper.world
        :type weapon_type: the type of weapon to be created, e.g. sword
        """
        weapon_file = jsonUtilities.read_json_file(constants.JSONFILEPATH + 'weapons.json')
        for weapon in weapon_file['weapons']:
            if weapon['name'] == weapon_type:
                myweapon = world.get_next_entity_id(gameworld=gameworld)
                # generate common item components
                gameworld.add_component(myweapon, items.TypeOfItem(label=weapon_type))
                gameworld.add_component(myweapon, items.Describable(
                    description=weapon['description'],
                    name=weapon['display_name'],
                    glyph=weapon['glyph'],
                    fg=weapon['fg_colour'],
                    bg=weapon['bg_colour']))
                gameworld.add_component(myweapon, items.Location(x=0, y=0))
                gameworld.add_component(myweapon, items.Material)
                gameworld.add_component(myweapon, items.RenderItem)
                gameworld.add_component(myweapon, items.Quality(level=weapon['quality_level']))

                # generate weapon specific components
                gameworld.add_component(myweapon, items.Spells(
                    slot_one=weapon['spell_slot_one'],
                    slot_two=weapon['spell_slot_two'],
                    slot_three=weapon['spell_slot_three'],
                    slot_four=weapon['spell_slot_four'],
                    slot_five=weapon['spell_slot_five']))

                gameworld.add_component(myweapon, items.Wielded(
                    main_hand=weapon['wielded_main_hand'],
                    off_hand=weapon['wielded_off_hand'],
                    both_hands=weapon['wielded_both_hands'],
                    true_or_false=True))

                gameworld.add_component(myweapon, items.Experience(current_level=1))

                gameworld.add_component(myweapon, items.Hallmarks(
                    hallmark_slot_one=weapon['hallmark_slot_one'],
                    hallmark_slot_two=weapon['hallmark_slot_two']))

                logger.info('Entity {} has been created using the {} template', myweapon, weapon['name'])
                return myweapon  # this is the entity id for the newly created weapon

