from loguru import logger

from components import mobiles
from utilities import configUtilities, formulas, common, gamemap, mobileHelp, scorekeeper, spellHelp


class StatelessAI:
    """
    The AI I'm looking to build out here in pseudo code is:
        Intrnsic pointers (things the enemy knows about itself)
            damage taken --> do I need to refine this further?
            morale --> hardcoded so they won't naturally retreat
        Questions it needs to answer:
            can-run-away-from-player --> am I under the effects of immobilize or cripple
            can-attack-player --> am I able to cast a spell
            too-far-from-player --> Am I further away from the player than my max spell range
            can-move-toward-player --> am I under the effects of immobilize or cripple or fear
            too-close-to-character --> am I too close to the player
            can-move-away-from-player --> am I under the effects of immobilize or cripple
            can-i-cast-a-spell --> is there one available to me
        Actions to consider:
            stand-still --> what should I do here?
            cast-spell-against-target --> pick a random one


    """

    @staticmethod
    def do_something(gameworld, game_config, player_entity, game_map):

        mobile_ai_level = configUtilities.get_config_value_as_integer(configfile=game_config, section='game',
                                                                      parameter='AI_LEVEL_MONSTER')

        current_turn = scorekeeper.ScorekeeperUtilities.get_meta_event_value(gameworld=gameworld, event_name='game_turn')

        for ent, ai in gameworld.get_component(mobiles.AI):
            entity_ai = mobileHelp.MobileUtilities.get_mobile_ai_level(gameworld=gameworld, entity_id=ent)
            if entity_ai == mobile_ai_level:
                entity_names = mobileHelp.MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=ent)
                current_health = mobileHelp.MobileUtilities.get_mobile_derived_current_health(gameworld=gameworld, entity=ent)
                current_morale = 25
                i_can_see_the_player = mobileHelp.MobileUtilities.can_i_see_the_other_entity(gameworld=gameworld, from_entity=ent, to_entity=player_entity, game_map=game_map)
                i_can_cast_a_spell, remaining_spells, weapon_type = spellHelp.SpellUtilities.can_mobile_cast_a_spell(gameworld=gameworld, entity_id=ent, target_entity=player_entity)
                am_i_too_far_from_the_target = StatelessAI.am_i_too_far_away_from_the_enemy(gameworld=gameworld, from_entity=ent, to_entity=player_entity)
                am_i_too_close_to_the_target = StatelessAI.am_i_too_close_to_the_target(gameworld=gameworld, from_entity=ent, to_entity=player_entity)
                i_can_retreat = StatelessAI.can_i_move_away_from_target(gameworld=gameworld, source_entity=ent, target_entity=player_entity, game_map=game_map, config_file=game_config)
                i_can_advance = StatelessAI.can_i_move_towards_target(gameworld=gameworld, source_entity=ent, target_entity= player_entity, game_map=game_map)

                logger.info('----------------------------------------')
                logger.info('Entity name:{}', entity_names[0])
                logger.info('Entity current health:{}', current_health)
                logger.info('Can entity see the player:{}', i_can_see_the_player)
                logger.info('Can entity cast a spell:{}', i_can_cast_a_spell)
                logger.info('Is it too far from the target:{}', am_i_too_far_from_the_target)
                logger.info('Is it too close to the target:{}', am_i_too_close_to_the_target)
                logger.info('Can the entity retreat:{}', i_can_retreat)
                logger.info('Can the entity advance:{}', i_can_advance)
                logger.info('----------------------------------------')

                if current_health < current_morale:
                    if i_can_retreat:
                        # run away from target (stupid for now)
                        logger.info('on turn {}: {} decided to move away', current_turn, entity_names[0])
                        mobileHelp.MobileUtilities.set_direction_velocity_away_from_player(gameworld=gameworld,
                                                                                game_config=game_config, enemy_entity=ent)
                    elif i_can_cast_a_spell:
                        if i_can_see_the_player:
                            spell_to_cast, spell_bar_slot_id = spellHelp.SpellUtilities.enemy_choose_random_spell_to_cast(spells_to_choose_from=remaining_spells, weapon_type=weapon_type)
                            logger.info('on turn {}: {} couldnt retreat so attempted to cast spell entity {}', current_turn,
                                        entity_names[0], spell_to_cast)

                            StatelessAI.the_spell_i_want_to_cast(gameworld=gameworld, player_entity=player_entity, spell_to_cast=spell_to_cast, spell_bar_slot_id=spell_bar_slot_id, ent=ent)
                        else:
                            # stand still #TODO
                            logger.info('on turn {}: {} felt threatened but didnt really know why', current_turn,
                                        entity_names[0])
                    else:
                        # stand still #TODO
                        logger.info('on turn {}: {} was too scared to run away or cast a spell', current_turn, entity_names[0])

                elif am_i_too_far_from_the_target:
                    if i_can_advance:
                        logger.info('on turn {}: {} decided to move towards the player', current_turn, entity_names[0])
                        mobileHelp.MobileUtilities.set_direction_velocity_towards_player(gameworld=gameworld, game_config=game_config,
                                                                              enemy_entity=ent)
                    elif i_can_cast_a_spell:
                        if i_can_see_the_player:
                            spell_to_cast, spell_bar_slot_id = spellHelp.SpellUtilities.enemy_choose_random_spell_to_cast(spells_to_choose_from=remaining_spells, weapon_type=weapon_type)
                            logger.info('on turn {}: {} stood firm and cast spell entity {}', current_turn, entity_names[0], spell_to_cast)
                            StatelessAI.the_spell_i_want_to_cast(gameworld=gameworld, player_entity=player_entity, spell_to_cast=spell_to_cast, spell_bar_slot_id=spell_bar_slot_id, ent=ent)
                        else:
                            # stand still #TODO
                            logger.info('on turn {}: {} was out of luck, they couldnt see the player', current_turn,
                                        entity_names[0])
                    else:
                        # stand still #TODO
                        logger.info('on turn {}: {} has no other option but to stand still', current_turn, entity_names[0])

                elif am_i_too_close_to_the_target:
                    if i_can_retreat:
                        # retreat from the player
                        logger.info('on turn {}: {} decided to retreat from the player', current_turn, entity_names[0])
                        mobileHelp.MobileUtilities.set_direction_velocity_away_from_player(gameworld=gameworld, game_config=game_config,
                                                                                enemy_entity=ent)
                    elif i_can_cast_a_spell:
                        if i_can_see_the_player:
                            spell_to_cast, spell_bar_slot_id = spellHelp.SpellUtilities.enemy_choose_random_spell_to_cast(spells_to_choose_from=remaining_spells, weapon_type=weapon_type)
                            logger.info('on turn {}: {} is casting spell entity {}', current_turn, entity_names[0], spell_to_cast)
                            StatelessAI.the_spell_i_want_to_cast(gameworld=gameworld, player_entity=player_entity, spell_to_cast=spell_to_cast, spell_bar_slot_id=spell_bar_slot_id, ent=ent)
                        else:
                            logger.info('on turn {}: {} was really perplexed', current_turn,
                                        entity_names[0])
                    else:
                        # stand still #TODO
                        logger.info('on turn {}: {} stood still and took the punishment', current_turn, entity_names[0])
                elif i_can_cast_a_spell and i_can_see_the_player:
                    spell_to_cast, spell_bar_slot_id = spellHelp.SpellUtilities.enemy_choose_random_spell_to_cast(spells_to_choose_from=remaining_spells, weapon_type=weapon_type)
                    logger.info('on turn {}: {} decided to cast spell entity {}', current_turn, entity_names[0], spell_to_cast)
                    StatelessAI.the_spell_i_want_to_cast(gameworld=gameworld, player_entity=player_entity, spell_to_cast=spell_to_cast, spell_bar_slot_id=spell_bar_slot_id, ent=ent)
                else:
                    # stand still #TODO
                    logger.info('on turn {}: {} really didnt know what to do', current_turn, entity_names[0])
            else:
                # not the right entity #TODO
                pass

    @staticmethod
    def the_spell_i_want_to_cast(gameworld, player_entity, spell_to_cast,spell_bar_slot_id, ent):

        # check if there is actually a spell to cast: if Zero then previous checks stopped a spell from being cast
        if spell_to_cast > 0:
            # add component covering spell has been cast
            gameworld.add_component(ent,
                                    mobiles.SpellCast(has_cast_a_spell=True, spell_entity=spell_to_cast,
                                                      spell_target=player_entity, spell_bar_slot=spell_bar_slot_id,
                                                      spell_caster=ent))
        else:
            # spit out a game message
            common.CommonUtils.fire_event("spell-fizzle", gameworld=gameworld, fg="yellow")


    @staticmethod
    def am_i_too_far_away_from_the_enemy(gameworld, from_entity, to_entity):

        the_truth = False

        distance = formulas.calculate_distance_to_target(gameworld=gameworld, from_entity=from_entity, to_entity=to_entity)
        max_pref_distance = mobileHelp.MobileUtilities.get_enemy_preferred_max_range(gameworld=gameworld, entity=from_entity)

        if distance > max_pref_distance:
            the_truth = True
        return the_truth

    @staticmethod
    def am_i_too_close_to_the_target(gameworld, from_entity, to_entity):
        the_truth = False

        distance = int(formulas.calculate_distance_to_target(gameworld=gameworld, from_entity=from_entity, to_entity=to_entity))
        min_pref_distance = int(mobileHelp.MobileUtilities.get_enemy_preferred_min_range(gameworld=gameworld, entity=from_entity))

        if distance < min_pref_distance:
            the_truth = True
        return the_truth

    @staticmethod
    def can_i_move_away_from_target(gameworld, source_entity, target_entity, game_map, config_file):
        i_can_move = StatelessAI.can_i_move(gameworld=gameworld, source_entity=source_entity)
        movement = False

        if i_can_move:
            movement = True
            # retreat
            entity_current_xpos = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=source_entity)
            entity_current_ypos = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=source_entity)

            target_current_xpos = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=target_entity)
            target_current_ypos = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=target_entity)
            tile_is_blocked = True

            # check: are source and target entities on the same row (x coordinate)
            if entity_current_ypos == target_current_ypos:
                # if on same row: check we're not at the left edge of the world
                if entity_current_xpos - 1 > 1:
                    tile_is_blocked = StatelessAI.can_i_move_backwards_horizontally(game_map=game_map, entity_current_xpos=entity_current_xpos, entity_current_ypos=entity_current_ypos)

                # if can't move back (regardless of the reason):
                if tile_is_blocked:
                    movement = False
                    logger.info('movement status via horizontal set to {}', movement)
            # check: are source and target entities on the same column (y coordinate)
            elif entity_current_xpos == target_current_xpos:
                # if on same column: can the source entity move back 1 tile
                if entity_current_ypos - 1 < 100:
                    tile_is_blocked = StatelessAI.can_i_move_backwards_vertically(game_map=game_map, entity_current_xpos=entity_current_xpos, entity_current_ypos=entity_current_ypos)
                # if can't move back (regardless of the reason):
                if tile_is_blocked:
                    movement = False
                    logger.info('movement status via vertical set to {}', movement)
        return movement

    @staticmethod
    def can_i_move_backwards_horizontally(game_map, entity_current_xpos, entity_current_ypos):
        tile_is_blocked = False
        # if on same row: can the source entity move back 1 tile
        tile_is_blocked = gamemap.GameMapUtilities.is_tile_blocked(game_map=game_map, x=entity_current_xpos - 1,
                                                           y=entity_current_ypos)
        return tile_is_blocked

    @staticmethod
    def can_i_move_backwards_vertically(game_map, entity_current_xpos, entity_current_ypos):
        tile_is_blocked = False
        # if on same row: can the source entity move back 1 tile
        tile_is_blocked = gamemap.GameMapUtilities.is_tile_blocked(game_map=game_map, x=entity_current_xpos,
                                                           y=entity_current_ypos - 1)
        return tile_is_blocked

    @staticmethod
    def can_i_move_towards_target(gameworld, source_entity, target_entity, game_map):
        movement = False
        i_can_move = StatelessAI.can_i_move(gameworld=gameworld, source_entity=source_entity)

        if i_can_move:
            movement = True
            # advance
            target_current_xpos = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=target_entity)
            target_current_ypos = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=target_entity)

            entity_current_xpos = mobileHelp.MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=source_entity)
            entity_current_ypos = mobileHelp.MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=source_entity)
            tile_is_blocked = True

            # check: are source and target entities on the same row (x coordinate)
            if entity_current_ypos == target_current_ypos:
                # if on same row: check we're not at the left edge of the world
                if entity_current_xpos - 1 > 1:
                    tile_is_blocked = StatelessAI.can_i_move_forwards_horizontally(game_map=game_map, entity_current_xpos=entity_current_xpos, entity_current_ypos=entity_current_ypos)

                # if can't move back (regardless of the reason):
                if tile_is_blocked:
                    movement = False
                    logger.info('movement status via horizontal set to {}', movement)
            # check: are source and target entities on the same column (y coordinate)
            elif entity_current_xpos == target_current_xpos:
                # if on same column: can the source entity move back 1 tile
                if entity_current_ypos - 1 < 100:
                    tile_is_blocked = StatelessAI.can_i_move_forwards_vertically(game_map=game_map, entity_current_xpos=entity_current_xpos, entity_current_ypos=entity_current_ypos)
                # if can't move back (regardless of the reason):
                if tile_is_blocked:
                    movement = False
                    logger.info('movement status via vertical set to {}', movement)

        return movement

    @staticmethod
    def can_i_move_forwards_horizontally(game_map, entity_current_xpos, entity_current_ypos):
        tile_is_blocked = False
        # if on same row: can the source entity move back 1 tile
        tile_is_blocked = gamemap.GameMapUtilities.is_tile_blocked(game_map=game_map, x=entity_current_xpos + 1,
                                                           y=entity_current_ypos)

        return tile_is_blocked

    @staticmethod
    def can_i_move_forwards_vertically(game_map, entity_current_xpos, entity_current_ypos):
        tile_is_blocked = False
        # if on same row: can the source entity move back 1 tile
        tile_is_blocked = gamemap.GameMapUtilities.is_tile_blocked(game_map=game_map, x=entity_current_xpos,
                                                           y=entity_current_ypos + 1)

        return tile_is_blocked

    @staticmethod
    def can_i_move(gameworld, source_entity):

        movement = True
        list_of_conditions = mobileHelp.MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld, entity=source_entity)
        if ['crippled', 'immobilize'] in list_of_conditions:
            movement = False

        return movement

