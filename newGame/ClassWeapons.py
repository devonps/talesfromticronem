
from utilities.jsonUtilities import read_json_file
from loguru import logger
from newGame import constants
from components import weapons, spells


class WeaponClass:

    def create_weapon(gameworld, weapon_type):
        weapon_file = read_json_file(constants.JSONFILEPATH + 'weapons.json')
        for weapon in weapon_file['weapons']:
            if weapon['name'] == weapon_type:
                myweapon = gameworld.create_entity()
                gameworld.add_component(myweapon, weapons.Name(weapon['name']))

                gameworld.add_component(myweapon, weapons.Describable(
                    description=weapon['description'],
                    display_name=weapon['display_name'],
                    glyph=weapon['glyph'],
                    foreground=weapon['fg_colour'],
                    background=weapon['bg_colour']))

                gameworld.add_component(myweapon, weapons.Spells(
                    slot_one=weapon['spell_slot_one'],
                    slot_two=weapon['spell_slot_two'],
                    slot_three=weapon['spell_slot_three'],
                    slot_four=weapon['spell_slot_four'],
                    slot_five=weapon['spell_slot_five']))

                gameworld.add_component(myweapon, weapons.Wielded(
                    main_hand=weapon['wielded_main_hand'],
                    off_hand=weapon['wielded_off_hand'],
                    both_hands=weapon['wielded_both_hands'],
                    true_or_false=True))

                gameworld.add_component(myweapon, weapons.Experience(current_level=weapon['current_xp_level']))

                gameworld.add_component(myweapon, weapons.Hallmarks(
                    hallmark_slot_one=weapon['hallmark_slot_one'],
                    hallmark_slot_two=weapon['hallmark_slot_two']))

                gameworld.add_component(myweapon, weapons.Renderable(weapon['can_be_rendered']))
                gameworld.add_component(myweapon, weapons.Quality(weapon['quality_level']))

                logger.info('Entity {} has been created using the {} template', myweapon, weapon['name'])
                return myweapon  # this is the entity id for the newly created weapon

    def load_weapon_with_spells(gameworld, weapon_obj, weapon_type, mobile_class):
        # get list of spells for that weapon and mobile class
        for ent, (cl, wpn, weapon_slot) in gameworld.get_components(spells.ClassName, spells.WeaponType, spells.WeaponSlot):
            if (wpn.label == weapon_type) and (cl.label == mobile_class):
                if weapon_slot.slot == '1':
                    logger.info('Spell {} added to weapon slot 1', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                    weapon_slot_component.slot_one = ent
                if weapon_slot.slot == '2':
                    logger.info('Spell {} added to weapon slot 2', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                    weapon_slot_component.slot_two = ent
                if weapon_slot.slot == '3':
                    logger.info('Spell {} added to weapon slot 3', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                    weapon_slot_component.slot_three = ent
                if weapon_slot.slot == '4':
                    logger.info('Spell {} added to weapon slot 4', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                    weapon_slot_component.slot_four = ent
                if weapon_slot.slot == '5':
                    logger.info('Spell {} added to weapon slot 5', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, weapons.Spells)
                    weapon_slot_component.slot_five = ent
