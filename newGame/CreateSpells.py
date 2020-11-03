from loguru import logger

from components import spells, addStatusEffects
from utilities import configUtilities, world, jsonUtilities


class AsEntities:

    @staticmethod
    def generate(gameworld):
        # cycle through ALL classes
        game_config = configUtilities.load_config()

        all_classes_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                      parameter='CLASSESFILE')

        class_file = jsonUtilities.read_json_file(all_classes_file)

        for available_class in class_file['classes']:
            _ = AsEntities.generate_spells_as_entities_for_class(gameworld=gameworld, game_config=game_config,
                                                                 spell_file=available_class['spellfile'],
                                                                 playable_class=available_class['name'])

    @staticmethod
    def generate_spells_as_entities_for_class(gameworld, game_config, spell_file, playable_class):
        spellsfile = spell_file.upper() + '_SPELLSFILE'

        spell_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                     parameter=spellsfile)
        spell_file = jsonUtilities.read_json_file(spell_file_path)

        logger.debug('Creating spells as entities for {}', playable_class)
        thisspell = - 1
        for spell in spell_file:
            thisspell = world.get_next_entity_id(gameworld=gameworld)
            myspell = spell
            logger.debug("myspell is:{}", myspell)
            gameworld.add_component(thisspell, spells.Name(myspell['name']))
            gameworld.add_component(thisspell, spells.Description(myspell['description']))
            gameworld.add_component(thisspell, spells.ShortDescription(myspell['short_description']))
            gameworld.add_component(thisspell, spells.CastTime(myspell['turns_to_cast']))
            gameworld.add_component(thisspell, spells.CoolDown(int(myspell['cool_down'])))
            gameworld.add_component(thisspell, spells.ClassName(playable_class))
            gameworld.add_component(thisspell, spells.SpellType(myspell['type_of_spell']))
            gameworld.add_component(thisspell, spells.StatusEffect(condis=[], boons=[], controls=[]))
            gameworld.add_component(thisspell, spells.MaxTargets(myspell['max_targets']))
            gameworld.add_component(thisspell, spells.AreaOfEffect(use_area_of_effect=myspell['aoe']))
            if myspell['aoe']:
                gameworld.add_component(thisspell,
                                        spells.AreaOfEffectShape(area_of_effect_shape=myspell['aoe_shape']))
            spell_range_in_file = myspell['spell_range']
            spell_range = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                      parameter=spell_range_in_file.upper())
            gameworld.add_component(thisspell, spells.MaxRange(spell_range))

            if myspell['type_of_spell'] == 'combat':
                gameworld.add_component(thisspell, spells.WeaponType(myspell['weapon_type']))
                gameworld.add_component(thisspell, spells.WeaponSlot(myspell['weapon_slot']))
                gameworld.add_component(thisspell, spells.DamageDuration(myspell['damage_duration']))
                gameworld.add_component(thisspell, spells.DamageCoefficient(myspell['damage_coef']))
                gameworld.add_component(thisspell, spells.GroundTargeted(myspell['ground_targeted']))

            if myspell['type_of_spell'] == 'heal':
                spell_heal_file = myspell['heal_duration']
                spell_heal = configUtilities.get_config_value_as_integer(configfile=game_config, section='spells',
                                                                         parameter='SPELL_HEAL_' + spell_heal_file.upper())
                gameworld.add_component(thisspell, spells.HealingDuration(spell_heal))
                gameworld.add_component(thisspell, spells.HealingCoef(float(myspell['heal_coef'])))

            if myspell['type_of_spell'] == 'utility':
                gameworld.add_component(thisspell, spells.ItemLocation(spell['location']))
                gameworld.add_component(thisspell, spells.ItemType(spell['item_type']))

            effects = myspell['effects']

            addStatusEffects.process_status_effect(gameworld=gameworld, spell_entity=thisspell, effects=effects,
                                                   game_config=game_config, ch_class=playable_class)

        return thisspell
