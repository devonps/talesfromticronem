# add conditions, boons, and controls to the entity
# the entity will commonly be a spell but it could be an item
# will need to pass: (esper) World object, entity id, and effects to be added

from components import condis, spellBoons, resources
from loguru import logger
from utilities import configUtilities


def process_status_effect(gameworld, spell_entity, effects, game_config):
    condis = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                      parameter='condi_effects')
    boons = configUtilities.get_config_value_as_list(configfile=game_config, section='spells', parameter='boon_effects')
    resources = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                         parameter='class_resources')

    # remember the list is packed as a dictionary
    for effect in effects:
        logger.debug('Key is {}', effect)

        if effect['name'] in condis:
            add_condition(world=gameworld, entity=spell_entity, effect=effect['name'], condi_value=effect['value'])
        if effect['name'] in boons:
            add_boon(world=gameworld, entity=spell_entity, effect=effect['name'], boon_value=effect['value'])
        if effect['name'] in resources:
            add_class_resource(world=gameworld, entity=spell_entity, effect=effect['name'],
                               resource_value=effect['value'])


def add_class_resource(world, entity, effect, resource_value):
    if effect == 'gain_lifeforce':
        world.add_component(entity, resources.Lifeforce(onhit=resource_value))
    if effect == 'damage':
        world.add_component(entity, resources.Damage(coefficient=resource_value))
    if effect == 'strikes_for':
        world.add_component(entity, resources.Strikesfor())
    if effect == 'boonsconverted':
        world.add_component(entity, resources.ConvertBoons())
    logger.info('Class resource {} added to spell', effect)


def add_condition(world, entity, effect, condi_value):
    if effect == 'bleeding':
        world.add_component(entity, condis.Bleeding())

    elif effect == 'burning':
        world.add_component(entity, condis.Burning())

    elif effect == 'confusion':
        world.add_component(entity, condis.Confusion())

    elif effect == 'poison':
        world.add_component(entity, condis.Poison())

    elif effect == 'torment':
        world.add_component(entity, condis.Torment())

    elif effect == 'blind':
        world.add_component(entity, condis.Blind(stacks_applied=condi_value))

    elif effect == 'chill':
        world.add_component(entity, condis.Chill(stacks_applied=condi_value))

    elif effect == 'cripple':
        world.add_component(entity, condis.Cripple(stacks_applied=condi_value))

    elif effect == 'fear':
        world.add_component(entity, condis.Fear(stacks_applied=condi_value))

    elif effect == 'immobilize':
        world.add_component(entity, condis.Immobilize(stacks_applied=condi_value))

    elif effect == 'vulnerability':
        world.add_component(entity, condis.Vulnerability(stacks_applied=condi_value))
    else:
        logger.warning('Dont know about condition called {}', effect)

    logger.info('Condition {} added to spell', effect)


def add_boon(world, entity, effect, boon_value):
    if effect == 'aegis':
        world.add_component(entity, spellBoons.Aegis())

    elif effect == 'alacrity':
        world.add_component(entity, spellBoons.Alacrity())

    elif effect == 'fury':
        world.add_component(entity, spellBoons.Fury())

    elif effect == 'might':
        world.add_component(entity, spellBoons.Might())

    elif effect == 'protection':
        world.add_component(entity, spellBoons.Protection())

    elif effect == 'regeneration':
        world.add_component(entity, spellBoons.Regeneration())

    elif effect == 'resistance':
        world.add_component(entity, spellBoons.Resistance())

    elif effect == 'retaliation':
        world.add_component(entity, spellBoons.Retaliation())

    elif effect == 'stability':
        world.add_component(entity, spellBoons.Stability())

    elif effect == 'swiftness':
        world.add_component(entity, spellBoons.Swiftness())
    else:
        logger.warning('Dont know about boon called {}', effect)

    logger.info('Boon {} added to spell', effect)
