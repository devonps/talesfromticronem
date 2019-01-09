
# add conditions, boons, and controls to the entity
# the entity will commonly be a spell but it could be an item
# will need to pass: (esper) World object, entity id, and effects to be added

from components import condis, spellBoons, resources
from loguru import logger
from newGame import constants


def process_status_effect(world, entity, spell_name, effects):
    logger.info('---> Working on spell {} with {}', spell_name, effects)
    for key, val in effects[0].items():
        spell_not_added = True
        if key.lower() in constants.condi_effects:
            add_condition(world, entity, key.lower(), val)
            spell_not_added = False
        if key.lower() in constants.boon_effects:
            add_boon(world, entity, key.lower(), val)
            spell_not_added = False
        if key.lower() in constants.class_resources:
            add_class_resource(world, entity, key.lower(), val)
            spell_not_added = False
        if spell_not_added:
            logger.warning("{} effect * {} * has no associated code - check constants", spell_name, key.lower())


def add_class_resource(world, entity, effect, resource_value):
    if effect == 'lifeforce':
        world.add_component(entity, resources.Lifeforce(onhit=resource_value))
    if effect == 'damage':
        world.add_component(entity, resources.Damage(coefficient=resource_value))
    if effect == 'strikes_for':
        world.add_component(entity, resources.Strikesfor())
    if effect =='boonsconverted':
        world.add_component(entity, resources.ConvertBoons())
    logger.info('Class resource {} added to spell', effect)


def add_condition(world, entity, effect, condi_value):
    if effect == 'bleeding':
        world.add_component(entity, condis.Bleeding(stacks_applied=condi_value))

    if effect == 'burning':
        world.add_component(entity, condis.Burning(stacks_applied=condi_value))

    if effect == 'confusion':
        world.add_component(entity, condis.Confusion(stacks_applied=condi_value))

    if effect == 'poison':
        world.add_component(entity, condis.Poison(stacks_applied=condi_value))

    if effect == 'torment':
        world.add_component(entity, condis.Torment(stacks_applied=condi_value))

    if effect == 'blind':
        world.add_component(entity, condis.Blind(stacks_applied=condi_value))

    if effect == 'chill':
        world.add_component(entity, condis.Chill(stacks_applied=condi_value))

    if effect == 'cripple':
        world.add_component(entity, condis.Cripple(stacks_applied=condi_value))

    if effect == 'fear':
        world.add_component(entity, condis.Fear(stacks_applied=condi_value))

    if effect == 'immobilize':
        world.add_component(entity, condis.Immobilize(stacks_applied=condi_value))

    if effect == 'vulnerability':
        world.add_component(entity, condis.Vulnerability(stacks_applied=condi_value))

    logger.info('Condition {} added to spell', effect)


def add_boon(world, entity, effect, boon_value):
    if effect == 'aegis':
        world.add_component(entity, spellBoons.Aegis())

    if effect == 'alacrity':
        world.add_component(entity, spellBoons.Alacrity())

    if effect == 'fury':
        world.add_component(entity, spellBoons.Fury())

    if effect == 'might':
        world.add_component(entity, spellBoons.Might())

    if effect == 'protection':
        world.add_component(entity, spellBoons.Protection())

    if effect == 'regeneration':
        world.add_component(entity, spellBoons.Regeneration())

    if effect == 'resistance':
        world.add_component(entity, spellBoons.Resistance())

    if effect == 'retaliation':
        world.add_component(entity, spellBoons.Retaliation())

    if effect == 'stability':
        world.add_component(entity, spellBoons.Stability())

    if effect == 'swiftness':
        world.add_component(entity, spellBoons.Swiftness())

    logger.info('Boon {} added to spell', effect)
