from loguru import logger

from components import spells
from utilities import configUtilities, world
from utilities.jsonUtilities import read_json_file
from utilities.spellHelp import SpellUtilities


class AsEntities:

    @staticmethod
    def generate(gameworld):
        # cycle through ALL classes
        game_config = configUtilities.load_config()

        all_classes_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='CLASSESFILE')

        class_file = read_json_file(all_classes_file)

        start_spell_entity = 0
        end_spell_entity = 0

        for available_class in class_file['classes']:
            this_spell = AsEntities.generate_spells_as_entities_for_class(gameworld=gameworld, game_config=game_config,
                                                                    spell_file=available_class['spellfile'],
                                                                    playable_class=available_class['name'])

            if start_spell_entity == 0:
                start_spell_entity = this_spell
            else:
                end_spell_entity = this_spell

        logger.debug('1st Spell entity was {}', start_spell_entity)
        logger.debug('last Spell entity was {}', end_spell_entity)

    @staticmethod
    def generate_spells_as_entities_for_class(gameworld, game_config, spell_file, playable_class):
        spellsfile = spell_file.upper() + '_SPELLSFILE'

        spell_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                     parameter=spellsfile)
        spell_file = read_json_file(spell_file_path)

        condis = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                          parameter='condi_effects')
        boons = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                         parameter='boon_effects')
        resources = configUtilities.get_config_value_as_list(configfile=game_config, section='spells',
                                                             parameter='class_resources')

        logger.debug('Creating spells as entities for {}', playable_class)
        thisspell = - 1
        for spell in spell_file['spells']:
            thisspell = world.get_next_entity_id(gameworld=gameworld)
            gameworld.add_component(thisspell, spells.Name(spell['name']))
            gameworld.add_component(thisspell, spells.Description(spell['description']))
            gameworld.add_component(thisspell, spells.ShortDescription(spell['short_description']))
            gameworld.add_component(thisspell, spells.CastTime(spell['turns_to_cast']))
            gameworld.add_component(thisspell, spells.CoolDown(spell['cool_down']))
            gameworld.add_component(thisspell, spells.ClassName(playable_class))
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
                    gameworld.add_component(thisspell, spells.AreaOfEffect(use_area_of_effect=spell['aoe']))
                    gameworld.add_component(thisspell,
                                                 spells.AreaOfEffectSize(area_of_effect_size=spell['aoe_size']))
                else:
                    gameworld.add_component(thisspell, spells.AreaOfEffect(use_area_of_effect=spell['aoe']))

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
                    if effect['name'] in condis:
                        SpellUtilities.add_status_effect_condi(gameworld=gameworld, spell_entity=thisspell,
                                                               status_effect=str(effect['name']))
                    if effect['name'] in boons:
                        SpellUtilities.add_status_effect_boon(gameworld=gameworld, spell_entity=thisspell,
                                                              status_effect=str(effect['name']))
                    if effect['name'] in resources:
                        SpellUtilities.add_resources_to_spell(gameworld=gameworld, spell_entity=thisspell,
                                                              resource=str(effect['name']))

        return thisspell
