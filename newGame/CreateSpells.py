from loguru import logger

from components import spells, addStatusEffects
from utilities import configUtilities, world, jsonUtilities
from utilities.spellHelp import SpellUtilities


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

    @staticmethod
    def create_new_spell_entity_from_existing_spell_entity(gameworld, existing_spell_entity):
        thisspell = world.get_next_entity_id(gameworld=gameworld)
        spell_name = SpellUtilities.get_spell_name(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.Name(spell_name.lower()))
        spell_description = SpellUtilities.get_spell_description(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.Description(spell_description))
        short_desc = SpellUtilities.get_spell_short_description(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.ShortDescription(short_desc))
        turns_to_cast = SpellUtilities.get_spell_cast_time(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.CastTime(turns_to_cast))
        cool_down_turns = SpellUtilities.get_spell_cooldown_time(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.CoolDown(cool_down_turns))

        play_class = gameworld.component_for_entity(existing_spell_entity, spells.ClassName)
        gameworld.add_component(thisspell, spells.ClassName(play_class.label))
        spell_type = SpellUtilities.get_spell_type(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.SpellType(spell_type))
        condi_effects = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld, spell_entity=existing_spell_entity)
        boon_effects = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld, spell_entity=existing_spell_entity)
        control_effects = SpellUtilities.get_all_controls_for_spell(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.StatusEffect(condi_effects, boon_effects, control_effects))
        max_targets = SpellUtilities.get_spell_max_targets(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.MaxTargets(max_targets))
        spell_aoe = SpellUtilities.get_spell_aoe_status(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.AreaOfEffect(spell_aoe))
        if spell_aoe:
            aoe_shape = SpellUtilities.get_spell_aoe_shape(gameworld=gameworld, spell_entity=existing_spell_entity)
            gameworld.add_component(thisspell,
                                    spells.AreaOfEffectShape(aoe_shape))
        spell_range = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=existing_spell_entity)
        gameworld.add_component(thisspell, spells.MaxRange(spell_range))

        if spell_type == 'combat':
            wpn_type = gameworld.component_for_entity(existing_spell_entity, spells.WeaponType)
            gameworld.add_component(thisspell, spells.WeaponType(wpn_type.label))
            wpn_slot = gameworld.component_for_entity(existing_spell_entity, spells.WeaponSlot)
            gameworld.add_component(thisspell, spells.WeaponSlot(wpn_slot.slot))
            dmg_dur = gameworld.component_for_entity(existing_spell_entity, spells.DamageDuration)
            gameworld.add_component(thisspell, spells.DamageDuration(dmg_dur))
            dmg_coe = SpellUtilities.get_spell_damage_coeff(gameworld=gameworld, spell_entity=existing_spell_entity)
            gameworld.add_component(thisspell, spells.DamageCoefficient(dmg_coe))
            grnd = SpellUtilities.get_spell_ground_targeted_status(gameworld=gameworld, spell_entity=existing_spell_entity)
            gameworld.add_component(thisspell, spells.GroundTargeted(grnd))

            if spell_type == 'heal':
                heal_dur = gameworld.component_for_entity(existing_spell_entity, spells.HealingDuration)
                gameworld.add_component(thisspell, spells.HealingDuration(heal_dur))
                heal_coe = SpellUtilities.get_spell_healing_coeff(gameworld=gameworld, spell_entity=existing_spell_entity)
                gameworld.add_component(thisspell, spells.HealingCoef(heal_coe))

            if spell_type == 'utility':
                spell_loc = gameworld.component_for_entity(existing_spell_entity, spells.ItemLocation)
                gameworld.add_component(thisspell, spells.ItemLocation(spell_loc))
                item_type = gameworld.component_for_entity(existing_spell_entity, spells.ItemType)
                gameworld.add_component(thisspell, spells.ItemType(item_type))

        return thisspell
