# add conditions, boons, and controls to the entity
# the entity will commonly be a spell but it could be an item
# will need to pass: (esper) World object, entity id, and effects to be added

from components import condis, spellBoons, resources
from loguru import logger
from utilities import configUtilities
from utilities.world import check_if_entity_has_component


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
            add_condition(gameworld=gameworld, entity=spell_entity, effect=effect['name'], condi_value=effect['value'])
        if effect['name'] in boons:
            add_boon(gameworld=gameworld, entity=spell_entity, effect=effect['name'], boon_value=effect['value'])
        if effect['name'] in resources:
            add_class_resource(gameworld=gameworld, entity=spell_entity, effect=effect['name'],
                               resource_value=effect['value'])


def add_class_resource(gameworld, entity, effect, resource_value):
    if effect == 'gain_lifeforce':
        gameworld.add_component(entity, resources.Lifeforce(onhit=resource_value))
    if effect == 'damage':
        gameworld.add_component(entity, resources.Damage(coefficient=resource_value))
    if effect == 'strikes_for':
        gameworld.add_component(entity, resources.Strikesfor())
    if effect == 'boonsconverted':
        gameworld.add_component(entity, resources.ConvertBoons())
    logger.info('Class resource {} added to spell', effect)


def add_condition(gameworld, entity, effect, condi_value):
    if effect == 'bleeding':
        gameworld.add_component(entity, condis.Bleeding())
        
        has_spell_got_bleeding = check_if_entity_has_component(gameworld=gameworld, entity=entity, component=condis.Bleeding)
        logger.warning('Has spell got bleeding component {}', has_spell_got_bleeding)
        bleed_component = gameworld.component_for_entity(entity=entity, component_type=condis.Bleeding)
        logger.debug('Component label is {}', bleed_component.condition_status_effect)

    elif effect == 'burning':
        gameworld.add_component(entity, condis.Burning())

    elif effect == 'confusion':
        gameworld.add_component(entity, condis.Confusion())

    elif effect == 'poison':
        gameworld.add_component(entity, condis.Poison())

    elif effect == 'torment':
        gameworld.add_component(entity, condis.Torment())

    elif effect == 'blind':
        gameworld.add_component(entity, condis.Blind(stacks_applied=condi_value))

    elif effect == 'chill':
        gameworld.add_component(entity, condis.Chill(stacks_applied=condi_value))

    elif effect == 'cripple':
        gameworld.add_component(entity, condis.Cripple(stacks_applied=condi_value))

    elif effect == 'fear':
        gameworld.add_component(entity, condis.Fear(stacks_applied=condi_value))

    elif effect == 'immobilize':
        gameworld.add_component(entity, condis.Immobilize(stacks_applied=condi_value))

    elif effect == 'vulnerability':
        gameworld.add_component(entity, condis.Vulnerability(stacks_applied=condi_value))
    else:
        logger.warning('Dont know about condition called {}', effect)

    logger.info('Condition {} added to spell', effect)


def add_boon(gameworld, entity, effect, boon_value):
    if effect == 'aegis':
        gameworld.add_component(entity, spellBoons.Aegis())

    elif effect == 'alacrity':
        gameworld.add_component(entity, spellBoons.Alacrity())

    elif effect == 'fury':
        gameworld.add_component(entity, spellBoons.Fury())

    elif effect == 'might':
        gameworld.add_component(entity, spellBoons.Might())

    elif effect == 'protection':
        gameworld.add_component(entity, spellBoons.Protection())

    elif effect == 'regeneration':
        gameworld.add_component(entity, spellBoons.Regeneration())

    elif effect == 'resistance':
        gameworld.add_component(entity, spellBoons.Resistance())

    elif effect == 'retaliation':
        gameworld.add_component(entity, spellBoons.Retaliation())

    elif effect == 'stability':
        gameworld.add_component(entity, spellBoons.Stability())

    elif effect == 'swiftness':
        gameworld.add_component(entity, spellBoons.Swiftness())
    else:
        logger.warning('Dont know about boon called {}', effect)

    logger.info('Boon {} added to spell', effect)
