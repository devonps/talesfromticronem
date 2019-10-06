import tcod

from loguru import logger
from utilities import configUtilities
from utilities.jsonUtilities import read_json_file


def validate_spells(game_config):

    classes = ['necromancer', 'witchdoctor', 'illusionist']

    for playerclass in classes:
        spellsfile = playerclass.upper() + '_SPELLSFILE'
        spell_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                      parameter=spellsfile)
        status_effects_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                      parameter='STATUSEFFECTSFILE')
        spell_file = read_json_file(spell_class_file)
        statuseffect_file = read_json_file(status_effects_file)

        for spell in spell_file['spells']:
            # spelleffects = spell['effects']
            # for effect in spelleffects:
            #     effectname = effect['name']
            #     effectIsValid = False
            #     for statuseffect in statuseffect_file['status-effects']:
            #         if statuseffect['name'] == effectname:
            #             effectIsValid = True
            #     if not effectIsValid:
            #         logger.warning('Status effect {} is not present - spell {} - class {}', effectname, spell['name'], playerclass)
            if spell['type_of_spell'] == 'utility':
                logger.info('spell name {}: {}', spell['name'], spell.keys())

