import random

from loguru import logger
from components import spells

from utilities.jsonUtilities import read_json_file
from utilities.randomNumberGenerator import PCG32Generator
from utilities.externalfileutilities import Externalfiles
from utilities import world
from utilities import configUtilities
from utilities.spellHelp import SpellUtilities


def setup_gameworld(game_config):
    # world seed generation
    world_seed = generate_world_seed(game_config)
    store_world_seed(game_config, world_seed)


def generate_world_seed(game_config):
    player_seed = configUtilities.get_config_value_as_string(configfile=game_config, section='pcg',
                                                             parameter='PLAYER_SEED')

    if player_seed != '':
        world_seed = PCG32Generator.convert_string_to_integer(player_seed)
        logger.info('Using player provided seed for world seed {}', player_seed)
    else:
        world_seed = random.getrandbits(30)
        logger.info('No player seed, using large random number for world seed {}', world_seed)

    return world_seed


def store_world_seed(game_config, world_seed):
    action_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                             parameter='GAME_ACTIONS_FILE')
    fileobject = Externalfiles.start_new_game_replay_file(action_file)

    value = 'world_seed:' + str(world_seed)
    Externalfiles.write_to_existing_file(action_file, value)
    Externalfiles.close_existing_file(fileobject)


def generate_spells(gameworld, game_config, spell_file, player_class):
    spellsfile = spell_file.upper() + '_SPELLSFILE'

    spell_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                 parameter=spellsfile)
    spell_file = read_json_file(spell_file_path)

    condis = configUtilities.get_config_value_as_list(configfile=game_config, section='spells', parameter='condi_effects')
    boons = configUtilities.get_config_value_as_list(configfile=game_config, section='spells', parameter='boon_effects')
    resources = configUtilities.get_config_value_as_list(configfile=game_config, section='spells', parameter='class_resources')

    logger.debug('Creating spells as entities')
    for spell in spell_file['spells']:
        thisspell = world.get_next_entity_id(gameworld=gameworld)
        gameworld.add_component(thisspell, spells.Name(spell['name']))
        logger.info('Spell name {}', spell['name'])
        gameworld.add_component(thisspell, spells.Description(spell['description']))
        gameworld.add_component(thisspell, spells.ShortDescription(spell['short_description']))
        gameworld.add_component(thisspell, spells.CastTime(spell['turns_to_cast']))
        gameworld.add_component(thisspell, spells.CoolDown(spell['cool_down']))
        gameworld.add_component(thisspell, spells.ClassName(player_class))
        gameworld.add_component(thisspell, spells.SpellType(spell['type_of_spell']))
        gameworld.add_component(thisspell, spells.StatusEffect(condis=[], boons=[], controls=[]))
        if spell['type_of_spell'] == 'combat':
            gameworld.add_component(thisspell, spells.WeaponType(spell['weapon_type']))
            gameworld.add_component(thisspell, spells.WeaponSlot(spell['weapon_slot']))
            gameworld.add_component(thisspell, spells.MaxTargets(spell['max_targets']))
            spell_range_in_file = spell['spell_range']
            spell_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                      parameter=spell_range_in_file.upper())
            gameworld.add_component(thisspell, spells.MaxRange(spell_range))
            gameworld.add_component(thisspell, spells.DamageDuration(spell['damage_duration']))
            gameworld.add_component(thisspell, spells.DamageCoefficient(spell['damage_coef']))
            gameworld.add_component(thisspell, spells.GroundTargeted(spell['ground_targeted']))
            if spell['aoe'] == 'True':
                gameworld.add_component(thisspell, spells.AreaOfEffect(spell['aoe']))
                gameworld.add_component(thisspell, spells.AreaOfEffectSize(spell['aoe_size']))

        if spell['type_of_spell'] == 'heal':
            spell_heal_file = spell['heal_duration']
            spell_heal = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                     parameter='SPELL_HEAL_' + spell_heal_file.upper())
            gameworld.add_component(thisspell, spells.HealingDuration(spell_heal))
            gameworld.add_component(thisspell, spells.HealingCoef(float(spell['heal_coef'])))

        if spell['type_of_spell'] == 'utility':
            gameworld.add_component(thisspell, spells.ItemLocation(spell['location']))
            gameworld.add_component(thisspell, spells.ItemType(spell['item_type']))

        effects = spell['effects']

        if len(effects) > 0:
            for effect in spell['effects']:
                spell_not_added = True
                if effect['name'] in condis:
                    SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=thisspell, status_effect=str(effect['name']))
                    spell_not_added = False
                if effect['name'] in boons:
                    spell_not_added = False
                    SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=thisspell, status_effect=str(effect['name']))
                if effect['name'] in resources:
                    spell_not_added = False
                    SpellUtilities.add_resources_to_spell(gameworld=gameworld, spell_entity=thisspell, resource=str(effect['name']))

            # condi_list = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld, spell_entity=thisspell)
            # boon_list = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld, spell_entity=thisspell)
            # controls_list = SpellUtilities.get_all_controls_for_spell(gameworld=gameworld, spell_entity=thisspell)
            # resource_list = SpellUtilities.get_all_resources_for_spell(gameworld=gameworld, spell_entity=thisspell)
            #
            # for condi in condi_list:
            #     logger.info('List of condis attached to the spell:{}', condi)
            #
            # for boon in boon_list:
            #     logger.info('List of boons attached to the spell:{}', boon)
            #
            # for ctrl in controls_list:
            #     logger.info('List of controls for this spell:{}', ctrl)
            #
            # for rsc in resource_list:
            #     logger.info('List of resources for this spell:{}', rsc)

