import esper

from utilities.jsonUtilities import read_json_file
from loguru import logger
from newGame import constants
from components import weapons


class WeaponClass:

    def create_staff(gameworld):
        weapon_file = read_json_file(constants.JSONFILEPATH + 'weapons.json')
        for weapon in weapon_file['weapons']:
            if weapon['name'] == 'staff':
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
                return myweapon  # this is the entity id for the newly created staff

    def create_dagger(gameworld):
        pass

    def create_scepter(self):
        pass

    def create_focus(gameworld):
        weapon_file = read_json_file(constants.JSONFILEPATH + 'weapons.json')
        for weapon in weapon_file['weapons']:
            if weapon['name'] == 'focus':
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
                return myweapon  # this is the entity id for the newly created staff

    def create_rod(gameworld):
        weapon_file = read_json_file(constants.JSONFILEPATH + 'weapons.json')
        for weapon in weapon_file['weapons']:
            if weapon['name'] == 'rod':
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
                return myweapon  # this is the entity id for the newly created staff

    def create_sword(gameworld):
        weapon_file = read_json_file(constants.JSONFILEPATH + 'weapons.json')
        for weapon in weapon_file['weapons']:
            if weapon['name'] == 'sword':
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
                return myweapon  # this is the entity id for the newly created staff

    def create_wand(gameworld):
        weapon_file = read_json_file(constants.JSONFILEPATH + 'weapons.json')
        for weapon in weapon_file['weapons']:
            if weapon['name'] == 'wand':
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
                return myweapon  # this is the entity id for the newly created staff
