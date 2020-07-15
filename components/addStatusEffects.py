# add conditions, boons, and controls to the entity
# the entity will commonly be a spell but it could be an item
# will need to pass: (esper) World object, entity id, and effects to be added

from components import condis, boons, resources
from loguru import logger
from utilities import configUtilities
from utilities.spellHelp import SpellUtilities


def process_status_effect(gameworld, spell_entity, effects, game_config, ch_class):
    condis = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                      parameter='condi_effects')
    boons = configUtilities.get_config_value_as_list(configfile=game_config, section='spells', parameter='boon_effects')
    resources = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                         parameter='class_resources')

    #
    # I use .statusEffects() to hold a list of different effects attached to the spells
    # condis=[], boons=[], controls=[]
    #
    #
    # remember the list is packed as a dictionary
    for effect in effects:
        # logger.debug('Key is {}', effect)
        valid_effect = False
        effect_name = effect['name'].lower()
        if effect_name != '':
            if effect_name in condis:
                valid_effect = True
                add_condition(gameworld=gameworld, entity=spell_entity, effect=effect_name)
            if effect_name in boons:
                valid_effect = True
                add_boon(gameworld=gameworld, entity=spell_entity, effect=effect_name, boon_value=effect['value'])
            if effect_name in resources:
                valid_effect = True
                add_class_resource(gameworld=gameworld, entity=spell_entity, effect=effect_name,
                                   resource_value=effect['value'])

            if not valid_effect:
                logger.warning('Effect named {} is not in lists', effect_name)


def add_class_resource(gameworld, entity, effect, resource_value):
    if effect == 'gain_lifeforce':
        gameworld.add_component(entity, resources.Lifeforce(onhit=resource_value))
        SpellUtilities.add_resources_to_spell(gameworld=gameworld, spell_entity=entity, resource='gainlifeforce')
    if effect == 'damage':
        gameworld.add_component(entity, resources.Damage(coefficient=resource_value))
        SpellUtilities.add_resources_to_spell(gameworld=gameworld, spell_entity=entity, resource='damage')
    if effect == 'strikes_for':
        gameworld.add_component(entity, resources.Strikesfor())
        SpellUtilities.add_resources_to_spell(gameworld=gameworld, spell_entity=entity, resource='strikes_for')
    if effect == 'boonsconverted':
        gameworld.add_component(entity, resources.ConvertBoons())
        SpellUtilities.add_resources_to_spell(gameworld=gameworld, spell_entity=entity, resource='boonsconverted')
    if effect == 'selfbleed':
        gameworld.add_component(entity, resources.Selfbleeding())
        SpellUtilities.add_resources_to_spell(gameworld=gameworld, spell_entity=entity, resource='selfbleed')
    # logger.info('Class resource {} added to spell', effect)


def add_condition(gameworld, entity, effect):
    if effect == 'bleeding':
        gameworld.add_component(entity, condis.Bleeding())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='bleeding')

    if effect == 'burning':
        gameworld.add_component(entity, condis.Burning())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='burning')
    if effect == 'confusion':
        gameworld.add_component(entity, condis.Confusion())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='confusion')
    if effect == 'poison':
        gameworld.add_component(entity, condis.Poison())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='poison')
    if effect == 'torment':
        gameworld.add_component(entity, condis.Torment())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='torment')

    if effect == 'blind':
        gameworld.add_component(entity, condis.Blind())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='blind')

    if effect == 'chill':
        gameworld.add_component(entity, condis.Chill())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='chill')

    if effect == 'cripple':
        gameworld.add_component(entity, condis.Cripple())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='cripple')

    if effect == 'fear':
        gameworld.add_component(entity, condis.Fear())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='fear')

    if effect == 'immobilize':
        gameworld.add_component(entity, condis.Immobilize())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='immobilize')

    if effect == 'vulnerability':
        gameworld.add_component(entity, condis.Vulnerability())
        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=entity, status_effect='vulnerability')

    # logger.info('Condition {} added to spell', effect)


def add_boon(gameworld, entity, effect, boon_value):
    if effect == 'aegis':
        gameworld.add_component(entity, boons.Aegis())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='aegis')

    elif effect == 'alacrity':
        gameworld.add_component(entity, boons.Alacrity())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='alacrity')

    elif effect == 'fury':
        gameworld.add_component(entity, boons.Fury())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='fury')

    elif effect == 'might':
        gameworld.add_component(entity, boons.Might())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='might')

    elif effect == 'protection':
        gameworld.add_component(entity, boons.Protection())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='protection')

    elif effect == 'regeneration':
        gameworld.add_component(entity, boons.Regeneration())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='regeneration')

    elif effect == 'resistance':
        gameworld.add_component(entity, boons.Resistance())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='resistance')

    elif effect == 'retaliation':
        gameworld.add_component(entity, boons.Retaliation())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='retaliation')

    elif effect == 'stability':
        gameworld.add_component(entity, boons.Stability())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='stability')

    elif effect == 'swiftness':
        gameworld.add_component(entity, boons.Swiftness())
        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=entity, status_effect='swiftness')
    else:
        logger.warning('Dont know about boon called {}', effect)

    # logger.info('Boon {} added to spell', effect)
