from loguru import logger
from components import spells, items


class WeaponClass:

    @staticmethod
    def load_weapon_with_spells(gameworld, weapon_obj, weapon_type, mobile_class):
        # get list of spells for that weapon and mobile class
        logger.warning('loading weapon {} / {} with spells for {}', weapon_obj, weapon_type, mobile_class)
        for ent, (cl, wpn, weapon_slot) in gameworld.get_components(spells.ClassName, spells.WeaponType, spells.WeaponSlot):
            logger.debug('class/weapon label {}/{}', cl.label, wpn.label)
            if (wpn.label == weapon_type) and (cl.label == mobile_class):
                if weapon_slot.slot == '1':
                    logger.info('Spell {} added to weapon slot 1', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, items.Spells)
                    weapon_slot_component.slot_one = ent
                if weapon_slot.slot == '2':
                    logger.info('Spell {} added to weapon slot 2', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, items.Spells)
                    weapon_slot_component.slot_two = ent
                if weapon_slot.slot == '3':
                    logger.info('Spell {} added to weapon slot 3', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, items.Spells)
                    weapon_slot_component.slot_three = ent
                if weapon_slot.slot == '4':
                    logger.info('Spell {} added to weapon slot 4', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, items.Spells)
                    weapon_slot_component.slot_four = ent
                if weapon_slot.slot == '5':
                    logger.info('Spell {} added to weapon slot 5', ent)
                    weapon_slot_component = gameworld.component_for_entity(weapon_obj, items.Spells)
                    weapon_slot_component.slot_five = ent
