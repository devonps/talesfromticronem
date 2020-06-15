# add conditions, boons, and controls to the entity
# the entity will commonly be a spell but it could be an item
# will need to pass: (esper) World object, entity id, and effects to be added

from components import condis, boons, resources
from loguru import logger
from utilities import configUtilities
from utilities.externalfileutilities import Externalfiles
from utilities.world import check_if_entity_has_component


def process_status_effect(gameworld, spell_entity, effects, game_config, ch_class):
    condis = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                      parameter='condi_effects')
    boons = configUtilities.get_config_value_as_list(configfile=game_config, section='spells', parameter='boon_effects')
    resources = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                         parameter='class_resources')

    # remember the list is packed as a dictionary
    for effect in effects:
        logger.debug('Key is {}', effect)
        valid_effect = False
        effect_name = effect['name'].lower()
        if effect_name != '':
            if effect_name in condis:
                valid_effect = True
                add_condition(gameworld=gameworld, entity=spell_entity, effect=effect_name, condi_value=effect['value'])
            if effect_name in boons:
                valid_effect = True
                add_boon(gameworld=gameworld, entity=spell_entity, effect=effect_name, boon_value=effect['value'])
            if effect_name in resources:
                valid_effect = True
                add_class_resource(gameworld=gameworld, entity=spell_entity, effect=effect_name,
                                   resource_value=effect['value'])

            if not valid_effect:
                logger.warning('Effect named {} is not in lists', effect_name)
                Externalfiles.write_to_existing_file('missing_effects.txt', value=ch_class + ':' + effect_name)


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

    if effect == 'burning':
        gameworld.add_component(entity, condis.Burning())

    if effect == 'confusion':
        gameworld.add_component(entity, condis.Confusion())

    if effect == 'poison':
        gameworld.add_component(entity, condis.Poison())

    if effect == 'torment':
        gameworld.add_component(entity, condis.Torment())

    if effect == 'blind':
        gameworld.add_component(entity, condis.Blind())

    if effect == 'chill':
        gameworld.add_component(entity, condis.Chill())

    if effect == 'cripple':
        gameworld.add_component(entity, condis.Cripple())

    if effect == 'fear':
        gameworld.add_component(entity, condis.Fear())

    if effect == 'immobilize':
        gameworld.add_component(entity, condis.Immobilize())

    if effect == 'vulnerability':
        gameworld.add_component(entity, condis.Vulnerability())

    # logger.info('Condition {} added to spell', effect)


def add_boon(gameworld, entity, effect, boon_value):
    if effect == 'aegis':
        gameworld.add_component(entity, boons.Aegis())

    elif effect == 'alacrity':
        gameworld.add_component(entity, boons.Alacrity())

    elif effect == 'fury':
        gameworld.add_component(entity, boons.Fury())

    elif effect == 'might':
        gameworld.add_component(entity, boons.Might())

    elif effect == 'protection':
        gameworld.add_component(entity, boons.Protection())

    elif effect == 'regeneration':
        gameworld.add_component(entity, boons.Regeneration())

    elif effect == 'resistance':
        gameworld.add_component(entity, boons.Resistance())

    elif effect == 'retaliation':
        gameworld.add_component(entity, boons.Retaliation())

    elif effect == 'stability':
        gameworld.add_component(entity, boons.Stability())

    elif effect == 'swiftness':
        gameworld.add_component(entity, boons.Swiftness())
    else:
        logger.warning('Dont know about boon called {}', effect)

    logger.info('Boon {} added to spell', effect)
