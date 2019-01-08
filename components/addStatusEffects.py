
# add conditions, boons, and controls to the entity
# the entity will commonly be a spell but it could be an item
# will need to pass: (esper) World object, entity id, and effects to be added

from components import condis, spellBoons, resources
from loguru import logger
from newGame import constants


def process_status_effect(world, entity, spell_name, effects):
    logger.info('---> Working on spell {}', spell_name)
    for e in effects:
        spell_not_added = True
        if e.lower() in constants.condi_effects:
            add_condition(world, entity, e.lower())
            spell_not_added = False
        if e.lower() in constants.boon_effects:
            add_boon(world, entity, e.lower())
            spell_not_added = False
        if e.lower() in constants.class_resources:
            add_class_resource(world, entity, e.lower())
            spell_not_added = False
        if spell_not_added:
            logger.warning("{} effect * {} * has no associated code - check constants", spell_name, e.lower())


def add_class_resource(world, entity, effect):
    if effect == 'lifeforce':
        world.add_component(entity, resources.Lifeforce())
    if effect == 'damage':
        world.add_component(entity, resources.Damage())
    logger.info('Class resource {} added to spell', effect)


def add_condition(world, entity, effect):
    if effect == 'bleeding':
        world.add_component(entity, condis.Bleeding())

    if effect == 'burning':
        world.add_component(entity, condis.Burning())

    if effect == 'confusion':
        world.add_component(entity, condis.Confusion())

    if effect == 'poison':
        world.add_component(entity, condis.Poison())

    if effect == 'torment':
        world.add_component(entity, condis.Torment())

    if effect == 'blind':
        world.add_component(entity, condis.Blind())

    if effect == 'chill':
        world.add_component(entity, condis.Chill())

    if effect == 'cripple':
        world.add_component(entity, condis.Cripple())

    if effect == 'fear':
        world.add_component(entity, condis.Fear())

    if effect == 'immobilize':
        world.add_component(entity, condis.Immobilize())

    if effect == 'vulnerability':
        world.add_component(entity, condis.Vulnerability())

    logger.info('Condition {} added to spell', effect)


def add_boon(world, entity, effect):
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
