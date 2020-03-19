from loguru import logger
from components import spells, spellBar, items, mobiles, condis
from components.messages import Message
from utilities import colourUtilities, formulas, configUtilities
from utilities.common import CommonUtils
from utilities.display import draw_colourful_frame, draw_simple_frame
from utilities.input_handlers import handle_game_keys
from utilities.itemsHelp import ItemUtilities
from utilities.jsonUtilities import read_json_file
from utilities.mobileHelp import MobileUtilities
from bearlibterminal import terminal
from mapRelated.gameMap import RenderLayer


class SpellUtilities:

    @staticmethod
    def get_spell_type(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.SpellType).label

    @staticmethod
    def cast_spell(slot, gameworld, message_log_id, player):

        spell_entity = SpellUtilities.get_spell_entity_from_spellbar_slot(gameworld=gameworld, slot=slot,
                                                                          playerEntity=player)

        logger.info('Casting spell with entity id {} from slot {}', spell_entity, slot)

        weapon_used = 0
        if slot <= 2:
            weapon_used = 1
        else:
            weapon_used = 2

        # check if spell is on cool-down
        isSpellOnCooldown = SpellUtilities.get_spell_cooldown_status(gameworld=gameworld, spell_entity=spell_entity)

        if not isSpellOnCooldown:
            # spell isn't on cooldown
            validTargets = SpellUtilities.get_valid_targets_for_spell(gameworld=gameworld,
                                                                      player=player, spell_entity=spell_entity)

            # display list of valid targets and wait for the player
            # to select one of them
            lft = 10
            tp = 15
            height = 5 + len(validTargets) + 1
            width = 26

            terminal.clear_area(lft, tp, width, height)
            prev_layer = terminal.state(terminal.TK_LAYER)
            terminal.layer(RenderLayer.VALIDTARGETS.value)

            draw_simple_frame(startx=lft, starty=tp, width=width, height=height, title='| Valid Targets |',
                              fg=colourUtilities.get('BLUE'), bg=colourUtilities.get('BLACK'))

            entity_tag = tp + 3
            xx = 0
            targetLetters = []
            if len(validTargets) == 0:
                str_to_print = "[color=white][font=dungeon]" + 'No valid targets'
                terminal.printf(x=lft + 3, y=entity_tag, s=str_to_print)
            else:
                for x in validTargets:
                    str_to_print = "[color=white]" + chr(97 + xx) + ") [color=" + x[3] + "][font=dungeon][bkcolor=" + x[
                        4] + "]" + x[2] + ' ' + x[1]
                    terminal.printf(x=lft + 2, y=entity_tag, s=str_to_print)
                    entity_tag += 1
                    targetLetters.append(chr(97 + xx))
                    xx += 1
            str_to_print = "[color=white][font=dungeon]" + 'Press ESC to cancel'
            terminal.printf(x=lft + 3, y=tp + height, s=str_to_print)

            terminal.layer(prev_layer)

            # blit the terminal
            terminal.refresh()

            # wait for user key press
            # validTargets[ent, name.first, desc.glyph, desc.foreground, desc.background]
            player_not_pressed_a_key = True
            while player_not_pressed_a_key:
                event_to_be_processed, event_action = handle_game_keys()
                if event_to_be_processed != '':
                    if event_to_be_processed == 'keypress':

                        if event_action == 'quit':
                            player_not_pressed_a_key = False
                        if len(targetLetters) != 0:
                            key_pressed = chr(97 + event_action)
                            if key_pressed in targetLetters:
                                target = targetLetters.index(key_pressed)
                                player_not_pressed_a_key = False

                                # add component covering spell has been cast
                                gameworld.add_component(player,
                                                        mobiles.SpellCast(truefalse=True, spell_entity=spell_entity,
                                                                          spell_target=validTargets[target][0],
                                                                          spell_bar_slot=1))

        else:
            msg = Message(text="Spell is on cooldown ", msgclass="all", fg="white", bg="black", fnt="")
            CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id)

    @staticmethod
    def get_valid_targets_for_spell(gameworld, player, spell_entity):

        # get x/y position of player character
        sx = MobileUtilities.get_mobile_x_position(gameworld=gameworld, entity=player)
        sy = MobileUtilities.get_mobile_y_position(gameworld=gameworld, entity=player)

        spellRange = SpellUtilities.get_spell_max_range(gameworld=gameworld, spell_entity=spell_entity)

        fx = sx - spellRange
        tx = (sx + spellRange) + 1
        fy = sy - spellRange
        ty = (sy + spellRange) + 1
        # get list of targets within the range of the spell - I scan a square around the player character
        validTargets = []
        for xx in range(fx, tx):
            for yy in range(fy, ty):
                if xx != sx and yy != sy:
                    str_to_print = "[font=dungeon][color=blue].[/color]"
                    terminal.printf(x=xx, y=yy, s=str_to_print)
                for ent, (pos, name, desc) in gameworld.get_components(mobiles.Position, mobiles.Name,
                                                                       mobiles.Describable):
                    if pos.x == xx and pos.y == yy:
                        # is this a valid target for the spell?
                        if ent != player:
                            validTargets.append((ent, name.first, desc.glyph, desc.foreground, desc.background))
        return validTargets

    @staticmethod
    def get_spell_cooldown_status(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.CoolDown).isTrue

    @staticmethod
    def get_spell_name_in_weapon_slot(gameworld, weapon_equipped, slotid):
        """
        Returns the spell name from weapon slot
        :param weapon_equipped:
        :param slotid:
        :return:
        """
        spell_name = 'no spell'
        spell = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld, weapon_equipped, slotid)
        if int(spell) > 0:
            spell_name = gameworld.component_for_entity(spell, spells.Name).label

        return spell_name

    @staticmethod
    def get_spell_entity_at_weapon_slot(gameworld, weapon_equipped, slotid):

        spell_entity = 0

        if slotid == 1:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_one
        if slotid == 2:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_two
        if slotid == 3:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_three
        if slotid == 4:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_four
        if slotid == 5:
            spell_entity = gameworld.component_for_entity(weapon_equipped, items.Spells).slot_five

        return spell_entity

    @staticmethod
    def populate_spell_bar_initially(gameworld, playerEntity):

        spellbar = MobileUtilities.get_next_entity_id(gameworld=gameworld)

        MobileUtilities.set_spellbar_for_entity(gameworld=gameworld, entity=playerEntity, spellbarEntity=spellbar)
        weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=playerEntity)

        if len(weapons_equipped) != 0:
            main_hand_weapon = weapons_equipped[0]
            off_hand_weapon = weapons_equipped[1]
            both_hands_weapon = weapons_equipped[2]
            if both_hands_weapon > 0:
                slotid = 1
                for a in range(5):
                    this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                                       weapon_equipped=both_hands_weapon,
                                                                                       slotid=slotid)
                    SpellUtilities.set_spellbar_slot(gameworld=gameworld, playerEntity=playerEntity, spellEntityId=this_spell_entity, slot=slotid)
                    slotid += 1

            if main_hand_weapon > 0:
                slotid = 1
                for a in range(3):
                    this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                                       weapon_equipped=main_hand_weapon,
                                                                                       slotid=slotid)
                    SpellUtilities.set_spellbar_slot(gameworld=gameworld, playerEntity=playerEntity, spellEntityId=this_spell_entity, slot=slotid)
                    slotid += 1

            if off_hand_weapon > 0:
                slotid = 4
                for a in range(2):
                    this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                                       weapon_equipped=main_hand_weapon,
                                                                                       slotid=slotid)
                    SpellUtilities.set_spellbar_slot(gameworld=gameworld, playerEntity=playerEntity, spellEntityId=this_spell_entity, slot=slotid)
                    slotid += 1

        # now get the heal skill
        playerClass = MobileUtilities.get_character_class(gameworld=gameworld, entity=playerEntity)
        for ent, (cl, typ) in gameworld.get_components(spells.ClassName, spells.SpellType):
            if typ.label == 'heal' and cl.label == playerClass:
                SpellUtilities.set_spellbar_slot(gameworld=gameworld, playerEntity=playerEntity,
                                                 spellEntityId=ent, slot=6)

    @staticmethod
    def populate_spell_bar_from_weapon(gameworld, player_entity, spellbar, wpns_equipped):

        # this method takes each of the spells 'loaded into the weapon' and 'loads them into the spellbar entity'

        # weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld, entity=player_entity)
        weapons_equipped = wpns_equipped

        # are there any weapons equippped
        if len(weapons_equipped) == 0:
            logger.debug('no weapons equipped for player')

        main_hand_weapon = weapons_equipped[0]
        off_hand_weapon = weapons_equipped[1]
        both_hands_weapon = weapons_equipped[2]

        if both_hands_weapon > 0:
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=both_hands_weapon,
                                                                               slotid=1)
            gameworld.component_for_entity(spellbar, spellBar.SlotOne).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=both_hands_weapon,
                                                                               slotid=2)
            gameworld.component_for_entity(spellbar, spellBar.SlotTwo).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=both_hands_weapon,
                                                                               slotid=3)
            gameworld.component_for_entity(spellbar, spellBar.SlotThree).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=both_hands_weapon,
                                                                               slotid=4)
            gameworld.component_for_entity(spellbar, spellBar.SlotFour).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=both_hands_weapon,
                                                                               slotid=5)
            gameworld.component_for_entity(spellbar, spellBar.SlotFive).id = this_spell_entity

        if main_hand_weapon > 0:
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=main_hand_weapon,
                                                                               slotid=1)
            gameworld.component_for_entity(spellbar, spellBar.SlotOne).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=main_hand_weapon,
                                                                               slotid=2)
            gameworld.component_for_entity(spellbar, spellBar.SlotTwo).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=main_hand_weapon,
                                                                               slotid=3)
            gameworld.component_for_entity(spellbar, spellBar.SlotThree).id = this_spell_entity

        if off_hand_weapon > 0:
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=off_hand_weapon,
                                                                               slotid=4)
            gameworld.component_for_entity(spellbar, spellBar.SlotFour).id = this_spell_entity
            this_spell_entity = SpellUtilities.get_spell_entity_at_weapon_slot(gameworld,
                                                                               weapon_equipped=off_hand_weapon,
                                                                               slotid=5)
            gameworld.component_for_entity(spellbar, spellBar.SlotFive).id = this_spell_entity

    # @staticmethod
    # def get_spell_bar_slot_componet(gameworld, spell_bar, slotid):
    #     if slotid == 1:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotOne)
    #     if slotid == 2:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotTwo)
    #     if slotid == 3:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotThree)
    #     if slotid == 4:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotFour)
    #     if slotid == 5:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotFive)
    #     if slotid == 6:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotSix)
    #     if slotid == 7:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotSeven)
    #     if slotid == 8:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotEight)
    #     if slotid == 9:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotNine)
    #     if slotid == 10:
    #         return gameworld.component_for_entity(spell_bar, spellBar.SlotTen)
    #     return -1

    @staticmethod
    def get_spell_name(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.Name).label

    @staticmethod
    def get_spell_cast_time(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.CastTime).number_of_turns

    @staticmethod
    def get_spell_cooldown_time(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.CoolDown).number_of_turns

    @staticmethod
    def get_spell_description(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.Description).label

    @staticmethod
    def get_spell_max_targets(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.MaxTargets).number_of_targets

    @staticmethod
    def get_spell_max_range(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.MaxRange).max_range

    @staticmethod
    def get_spell_DamageCoeff(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.DamageCoefficient).is_set_to

    @staticmethod
    def get_spell_HealingCoeff(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.HealingCoef).value

    @staticmethod
    def add_status_effect_condi(gameworld, spell_entity, status_effect):

        current_condis = SpellUtilities.get_all_condis_for_spell(gameworld=gameworld, spell_entity=spell_entity)
        current_condis.append(status_effect)
        status_effect_component = gameworld.component_for_entity(spell_entity, spells.StatusEffect)
        status_effect_component.condis = current_condis

    @staticmethod
    def get_all_condis_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).condis

    @staticmethod
    def add_status_effect_boon(gameworld, spell_entity, status_effect):
        current_boons = SpellUtilities.get_all_boons_for_spell(gameworld=gameworld, spell_entity=spell_entity)
        current_boons.append(status_effect)
        status_effect_component = gameworld.component_for_entity(spell_entity, spells.StatusEffect)
        status_effect_component.boons = current_boons

    @staticmethod
    def get_all_boons_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).boons

    @staticmethod
    def add_status_effect_control(gameworld, spell_entity, status_effect):
        current_controls = SpellUtilities.get_all_controls_for_spell(gameworld=gameworld, spell_entity=spell_entity)
        current_controls.append(status_effect)
        status_effect_component = gameworld.component_for_entity(spell_entity, spells.StatusEffect)
        status_effect_component.controls = current_controls

    @staticmethod
    def get_all_controls_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).controls

    @staticmethod
    def add_resources_to_spell(gameworld, spell_entity, resource):
        current_resources = SpellUtilities.get_all_resources_for_spell(gameworld=gameworld, spell_entity=spell_entity)
        current_resources.append(resource)
        status_effect_component = gameworld.component_for_entity(spell_entity, spells.StatusEffect)
        status_effect_component.resources = current_resources

    @staticmethod
    def get_all_resources_for_spell(gameworld, spell_entity):
        return gameworld.component_for_entity(spell_entity, spells.StatusEffect).resources

    @staticmethod
    def apply_condis_to_target(gameworld, target_entity, list_of_condis):

        game_config = configUtilities.load_config()

        current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld, entity=target_entity)
        target_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=target_entity)
        target_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=target_entity)
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player_entity)

        # read the conditions.json file
        conditions_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                          parameter='CONDITIONSFILE')
        conditions_file = read_json_file(conditions_file_path)

        for condi in list_of_condis:

            for condition in conditions_file['conditions']:
                if condi == condition['condition_status_effect']:
                    z = {'name': condi, 'duration': int(condition['default_exists_for_turns']),
                         'baseDamage': int(condition['base_damage_per_stack']),
                         'condDamageMod': float(condition['condition_damage_modifier']),
                         'weaponLevelMod': float(condition['weapon_level_modifier']), 'image': int(condition['image']),
                         'dialogue': condition['dialogue_options'][0][target_class],
                         'displayChar': condition['char']}

                    # add dialog for condition damage to message log
                    msg = Message(text=target_names[0] + " screams: " + condition['dialogue_options'][0][target_class],
                                  msgclass="all", fg="white", bg="black", fnt="")
                    CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id)

                    current_condis.append(z)

            status_effects_component = gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
            status_effects_component.conditions = current_condis

        logger.debug('Condis applied to {} is {}', target_names[0], current_condis)

    @staticmethod
    def apply_boons_to_target(gameworld, target_entity, list_of_boons, spell_caster):

        game_config = configUtilities.load_config()

        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld, entity=target_entity)
        target_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=target_entity)
        target_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=target_entity)
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        message_log_id = MobileUtilities.get_MessageLog_id(gameworld=gameworld, entity=player_entity)

        # read the boons.json file
        boons_file_path = configUtilities.get_config_value_as_string(configfile=game_config, section='default',
                                                                     parameter='BOONSFILE')
        boons_file = read_json_file(boons_file_path)

        for boon in list_of_boons:

            for fileBoon in boons_file['boons']:
                if boon == fileBoon['boon_status_effect']:
                    b = {'name': boon, 'duration': int(fileBoon['default_exists_for_turns']),
                         'dialogue': fileBoon['dialogue_options'][0][target_class], 'image': fileBoon['image'],
                         'displayChar': fileBoon['char']}
                    if boon == 'fury':
                        b['improvement'] = 'crit_chance_increased'
                        b['increased_by'] = fileBoon['crit_chance_improved']
                        target_entity = spell_caster
                        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld,
                                                                                            entity=target_entity)
                        # target_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld,
                        #                                                        entity=target_entity)
                        # logger.warning('-----> target entity for fury is {}', target_names[0])

                    # add dialog for boon effect to message log
                    msg = Message(text=target_names[0] + " " + fileBoon['dialogue_options'][0][target_class],
                                  msgclass="all", fg="white", bg="black", fnt="")
                    CommonUtils.add_message(gameworld=gameworld, message=msg, logid=message_log_id)

                    # current_boons is a map
                    current_boons.append(b)
        if len(current_boons) != 0:
            status_effects_component = gameworld.component_for_entity(target_entity, mobiles.StatusEffects)
            status_effects_component.boons = current_boons
            logger.debug('Boons applied to {} is {}', target_names[0], current_boons)

    @staticmethod
    def get_spell_image(gameworld, spellEntity):
        return gameworld.component_for_entity(spellEntity, spells.Image).id

    @staticmethod
    def get_spell_entity_from_spellbar_slot(gameworld, slot, playerEntity):
        currentSpells = SpellUtilities.get_current_spellbar_spells(gameworld=gameworld, playerEntity=playerEntity)
        return currentSpells[slot - 1]

    @staticmethod
    def set_spellbar_slot(gameworld, playerEntity, slot, spellEntityId):
        currentSpells = SpellUtilities.get_current_spellbar_spells(gameworld=gameworld, playerEntity=playerEntity)
        logger.warning('current spells in spell bar are {}', currentSpells)
        if len(currentSpells) > 0:
            currentSpells[slot - 1] = spellEntityId
        else:
            currentSpells[0] = spellEntityId

        spellbar_slots_component = gameworld.component_for_entity(playerEntity, mobiles.SpellBar)
        spellbar_slots_component.slots = currentSpells

    @staticmethod
    def get_current_spellbar_spells(gameworld, playerEntity):
        return gameworld.component_for_entity(playerEntity, mobiles.SpellBar).slots
