from loguru import logger

from newGame.ClassWeapons import WeaponClass
from newGame.Items import ItemManager
from newGame.initialiseNewGame import generate_spells
from utilities import configUtilities, colourUtilities, world
from utilities.buildLibrary import BuildLibrary
from utilities.externalfileutilities import Externalfiles
from utilities.input_handlers import handle_game_keys
from utilities.display import display_coloured_box, draw_colourful_frame, draw_clear_text_box
from utilities.itemsHelp import ItemUtilities
from utilities.jsonUtilities import read_json_file
from newGame.CharacterCreation import CharacterCreation
from utilities.mobileHelp import MobileUtilities
import tcod
import tcod.console
import tcod.event

from utilities.spellHelp import SpellUtilities


class Build:
    BUILDRACE = 0
    BUILDCLASS = 1
    BUILDJEWELLERY = 2
    BUILDMAINHAND = 3
    BUILDOFFHAND = 4
    BUILDARMOUR = 5
    BUILDGENDER = 6


def display_build_library(root_console):

    game_config = configUtilities.load_config()

    build_library_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_WIDTH')
    build_library_height = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_HEIGHT')
    build_library_frame_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_FRAME_X')
    build_library_frame_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_FRAME_Y')
    build_library_frame_width = configUtilities.get_config_value_as_integer(game_config, 'newgame','BUILD_LIBRARY_FRAME_WIDTH')
    build_library_frame_height = configUtilities.get_config_value_as_integer(game_config, 'newgame','BUILD_LIBRARY_FRAME_HEIGHT')
    saved_build_template_width = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_WIDTH')
    saved_build_template_height = configUtilities.get_config_value_as_integer(game_config, 'newgame','BUILD_LIBRARY_TEMPLATE_HEIGHT')
    saved_build_template_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_Y')
    saved_build_template_original_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_X')
    saved_build_pagination_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PAGINATION_X')
    saved_build_pagination_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PAGINATION_Y')
    saved_build_class_filter_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_CLASS_FILTER_X')
    saved_build_class_filter_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_CLASS_FILTER_Y')
    saved_build_page_min_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PAGE_MIN_X')
    saved_build_page_max_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PAGE_MAX_X')
    saved_build_template_info_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_INFO_X')
    saved_build_template_info_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_TEMPLATE_INFO_Y')
    saved_build_avatar_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_AVATAR_X')
    saved_build_avatar_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_AVATAR_Y')
    saved_build_code_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_CODE_X')
    saved_build_code_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_CODE_Y')
    saved_build_play_x = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PLAY_X')
    saved_build_play_y = configUtilities.get_config_value_as_integer(game_config, 'newgame', 'BUILD_LIBRARY_PLAY_Y')
    fileName = configUtilities.get_config_value_as_string(game_config, 'default', 'BUILDLIBRARYFILE')
    player_class_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default',parameter='CLASSESFILE')
    armourset_file = configUtilities.get_config_value_as_string(configfile=game_config, section='default', parameter='ARMOURSETFILE')

    playable_classes = []
    class_spell_file = []
    build_library_is_displayed = True
    selected_build = 0
    build_grid_selected = 1
    draw_template_ui = True
    build_codes = []
    build_names = []
    build_dates = []
    build_times = []
    decoded_build = []
    buildCount = 0
    template_view_current_min = 1
    buildZoneLeft = 0
    buildZoneRight = 1
    buildZoneTop = 2
    buildZoneBottom = 3
    buildZoneXOffset = 5
    buildZoneYOffset = 5

    # load saved builds
    buildContent = Externalfiles.load_existing_file(filename=fileName)
    for row in buildContent:
        elements = row.split(':')
        build_codes.append(elements[0])
        build_names.append(elements[1])
        build_dates.append(elements[2])
        build_times.append(elements[3])
        decoded_build.append(BuildLibrary.decode_saved_build(build_codes[buildCount]))
        buildCount += 1

    if buildCount < 10:
        template_view_current_max = buildCount
    else:
        template_view_current_max = 10
    template_view_template_max = buildCount

    # load playable classes
    class_file = read_json_file(player_class_file)
    class_health = []
    playable_classes.append('List Only...')
    playable_classes.append('all')
    for option in class_file['classes']:
        playable_classes.append(option['name'])
        class_health.append(option['health'])
        class_spell_file.append(option['spellfile'])

    # build library console
    build_library_console = tcod.console.Console(width=build_library_width, height=build_library_height, order='F')

    # build library frame around console
    draw_colourful_frame(console=build_library_console, game_config=game_config,
                         startx=build_library_frame_x, starty=build_library_frame_y,
                         width=build_library_frame_width,
                         height=build_library_frame_height,
                         title='[ Character Build Library ]', title_loc='centre',
                         title_decorator=False,
                         corner_decorator='', corner_studs='square',
                         msg='ESC/ to go back, mouse to select.')

    while build_library_is_displayed:
        if draw_template_ui:
            draw_template_ui = False
            build_zones = []
            saved_cur_avatar_x = saved_build_avatar_x
            template_box_posx = saved_build_template_original_x
            template_position_x = saved_build_template_original_x
            saved_build_template_x = saved_build_template_original_x

            personal_info = 'You are known as '

            personal_info += build_names[selected_build] + ' a ' + decoded_build[selected_build][
                Build.BUILDGENDER] + ' ' + decoded_build[selected_build][Build.BUILDCLASS]
            personal_info += ' from the ' + decoded_build[selected_build][Build.BUILDRACE] + '.'
            personal_info += ' You are wearing ' + decoded_build[selected_build][Build.BUILDARMOUR] + ' armour and a '
            personal_info += decoded_build[selected_build][Build.BUILDJEWELLERY] + ' set of jewellery.'
            if decoded_build[selected_build][Build.BUILDMAINHAND] == decoded_build[selected_build][Build.BUILDOFFHAND]:
                personal_info += ' You are wielding a ' + decoded_build[selected_build][Build.BUILDMAINHAND] + ' in both hands.'
            else:
                personal_info += ' You are wielding a ' + decoded_build[selected_build][ Build.BUILDMAINHAND] + ' in your main hand'
                personal_info += ' and a ' + decoded_build[selected_build][Build.BUILDOFFHAND] + ' in your off hand.'

            # display build library grid
            for template_id in range(template_view_current_min, template_view_current_max + 1):
                if template_id == build_grid_selected:
                    fg = colourUtilities.YELLOW
                else:
                    fg = colourUtilities.GREEN

                display_coloured_box(console=build_library_console, title='',
                                     posx=template_box_posx, posy=saved_build_template_y,
                                     width=saved_build_template_width, height=saved_build_template_height,
                                     fg=fg, bg=tcod.black)
                build_zones.append((buildZoneXOffset + template_box_posx, buildZoneXOffset + template_box_posx + 8,
                                    buildZoneYOffset + saved_build_template_y, buildZoneYOffset + saved_build_template_y + 8))
                # draw build template info/avatar here
                if template_id < buildCount + 1:
                    build_library_console.print(x=saved_cur_avatar_x, y=saved_build_avatar_y, string=build_names[template_id - 1],
                                                fg=fg)

                template_position_x += saved_build_template_width
                saved_cur_avatar_x += saved_build_template_width
                if template_id == 5:
                    saved_build_template_y += saved_build_template_height
                    template_position_x = saved_build_template_x
                    saved_cur_avatar_x = saved_build_avatar_x
                    saved_build_avatar_y += saved_build_template_height

                template_box_posx = template_position_x

            # display pagination
            page_string = 'Showing ' + \
                          str(template_view_current_min) + '-' + \
                          str(template_view_current_max) + ' of ' + \
                          str(template_view_template_max)
            build_library_console.print(x=saved_build_pagination_x, y=saved_build_pagination_y, string=page_string,
                                        fg=colourUtilities.YELLOW1)

            if template_view_current_min > 1:
                build_library_console.print(x=saved_build_page_min_x, y=saved_build_pagination_y, string='PREV PAGE',
                                            fg=colourUtilities.BLUE)

            if template_view_template_max > template_view_current_max:
                build_library_console.print(x=saved_build_page_max_x, y=saved_build_pagination_y, string='NEXT PAGE',
                                            fg=colourUtilities.YELLOW)

            # display class filter options
            for clfilter in range(len(playable_classes)):
                build_library_console.print(x=saved_build_class_filter_x, y=saved_build_class_filter_y + clfilter, string=playable_classes[clfilter],
                                            fg=colourUtilities.BLUE)

            # display selected build template info

            draw_clear_text_box(console=build_library_console,
                                posx=saved_build_template_info_x, posy=saved_build_template_info_y,
                                width=70, height=3,
                                text=personal_info,
                                fg=colourUtilities.BLUE, bg=colourUtilities.BLACK)

            # display build code
            build_library_console.print(x=saved_build_code_x, y=saved_build_code_y, string='BUILD CODE: ' + build_codes[selected_build],
                                        fg=colourUtilities.YELLOW)

            # display PLAY button
            bz = len(build_zones) + 1
            build_zones.append((buildZoneXOffset + saved_build_play_x, buildZoneXOffset + saved_build_play_x + len('START GAME') - 1, saved_build_play_y + 4, (saved_build_play_y + 4) + 1))
            build_library_console.print(x=saved_build_play_x, y=saved_build_play_y, string='START GAME',
                                        fg=colourUtilities.RED)

            # blit to the root console
            build_library_console.blit(dest=root_console, dest_x=5, dest_y=5)
            tcod.console_flush()

        # handle player events
        event_to_be_processed, event_action = handle_game_keys()
        if event_to_be_processed != '':
            if event_to_be_processed == 'keypress':
                if event_action == 'quit':
                    build_library_is_displayed = False

            if event_to_be_processed == 'mousebutton':
                if event_action[0] == 'left':
                    mx = event_action[1]
                    my = event_action[2]
                    for zone in range(len(build_zones)):
                        if build_zones[zone][buildZoneLeft] <= mx <= build_zones[zone][buildZoneRight]:
                            if build_zones[zone][buildZoneTop] <= my <= build_zones[zone][buildZoneBottom]:
                                if zone < len(build_zones) - 1:
                                    logger.info('Zone {} clicked', zone)
                                    if zone == 0:
                                        build_grid_selected = 1
                                        selected_build = 0
                                    else:
                                        build_grid_selected = zone + 1
                                        selected_build = zone
                                    logger.info('build_grid_selected {}', build_grid_selected)
                                    logger.info('Number of zones {}', len(build_zones))
                                    draw_template_ui = True
                                if zone == len(build_zones) - 1:
                                    gameworld = world.create_game_world()
                                    player_entity = MobileUtilities.generate_base_mobile(gameworld=gameworld, game_config=game_config)

                                    # creating build entity to keep character creation process happy
                                    build_entity = BuildLibrary.create_build_entity(gameworld=gameworld)

                                    # name
                                    MobileUtilities.set_mobile_first_name(gameworld=gameworld, entity=player_entity, name=build_names[selected_build])

                                    # gender
                                    MobileUtilities.set_player_gender(gameworld=gameworld, entity=player_entity, gender=decoded_build[selected_build][Build.BUILDGENDER])
                                    # race
                                    race_size = 'normal'
                                    MobileUtilities.setup_racial_attributes( gameworld=gameworld, player=player_entity,
                                    selected_race=decoded_build[selected_build][Build.BUILDRACE], race_size=race_size, bg=colourUtilities.BLACK)

                                    # class
                                    health = 0
                                    spell_file = ''
                                    for option in range(len(playable_classes)):
                                        if playable_classes[option] == decoded_build[selected_build][Build.BUILDCLASS]:
                                            health = int(class_health[option - 2])
                                            spell_file = class_spell_file[option - 2]

                                    MobileUtilities.setup_class_attributes(gameworld=gameworld, player=player_entity,
                                                                           selected_class=decoded_build[selected_build][Build.BUILDCLASS],
                                                                           health=health, spellfile=spell_file)

                                    # personality
                                    MobileUtilities.calculate_mobile_personality(gameworld, game_config)

                                    # armour
                                    armour_file = read_json_file(armourset_file)
                                    as_internal_name = []
                                    px_flavour = []
                                    px_att_name = []
                                    px_att_bonus = []
                                    pxstring = 'prefix'
                                    attnamestring = 'attributename'
                                    attvaluestring = 'attributebonus'

                                    for armourset in armour_file['armoursets']:
                                        if armourset['startset'] == 'true':
                                            as_internal_name.append(armourset['internalsetname'])
                                            prefix_count = armourset['prefixcount']
                                            attribute_bonus_count = armourset['attributebonuscount']

                                            for px in range(1, prefix_count + 1):
                                                prefix_string = pxstring + str(px)
                                                px_flavour.append(armourset[prefix_string]['flavour'])

                                                if attribute_bonus_count > 1:
                                                    att_bonus_string = attvaluestring + str(px)
                                                    att_name_string = attnamestring + str(px)
                                                else:
                                                    att_bonus_string = attvaluestring + str(1)
                                                    att_name_string = attnamestring + str(1)

                                                px_att_bonus.append(armourset[prefix_string][att_bonus_string])
                                                px_att_name.append(armourset[prefix_string][att_name_string])

                                    # assign armour prefix benefit
                                    if decoded_build[selected_build][Build.BUILDARMOUR] == 'healer':
                                        current_healingpower = MobileUtilities.get_mobile_healing_power( gameworld=gameworld, entity=player_entity)
                                        px_bonus = int(px_att_bonus[1])
                                        new_bonus = current_healingpower + px_bonus
                                        MobileUtilities.set_mobile_healing_power(gameworld=gameworld, entity=player_entity, value=new_bonus)

                                    if decoded_build[selected_build][Build.BUILDARMOUR] == 'malign':
                                        current_condidamage = MobileUtilities.get_mobile_condition_damage( gameworld=gameworld, entity=player_entity)
                                        px_bonus = int(px_att_bonus[2])
                                        new_bonus = current_condidamage + px_bonus
                                        MobileUtilities.set_mobile_condition_damage(gameworld=gameworld, entity=player_entity,  value=new_bonus)

                                    if decoded_build[selected_build][Build.BUILDARMOUR] == 'mighty':
                                        current_power = MobileUtilities.get_mobile_power(gameworld=gameworld, entity=player_entity)
                                        px_bonus = int(px_att_bonus[3])
                                        new_bonus = current_power + px_bonus
                                        MobileUtilities.set_mobile_power(gameworld=gameworld, entity=player_entity, value=new_bonus)

                                    if decoded_build[selected_build][Build.BUILDARMOUR] == 'precise':
                                        current_precision = MobileUtilities.get_mobile_precision(gameworld=gameworld, entity=player_entity)
                                        px_bonus = int(px_att_bonus[4])
                                        new_bonus = current_precision + px_bonus
                                        MobileUtilities.set_mobile_precision(gameworld=gameworld, entity=player_entity, value=new_bonus)

                                    if decoded_build[selected_build][Build.BUILDARMOUR] == 'resilient':
                                        current_toughness = MobileUtilities.get_mobile_toughness(gameworld=gameworld, entity=player_entity)
                                        px_bonus = int(px_att_bonus[0])
                                        new_bonus = current_toughness + px_bonus
                                        MobileUtilities.set_mobile_toughness(gameworld=gameworld, entity=player_entity, value=new_bonus)

                                    if decoded_build[selected_build][Build.BUILDARMOUR] == 'vital':
                                        current_vitality = MobileUtilities.get_mobile_vitality(gameworld=gameworld, entity=player_entity)
                                        px_bonus = int(px_att_bonus[5])
                                        new_bonus = current_vitality + px_bonus
                                        MobileUtilities.set_mobile_vitality(gameworld=gameworld, entity=player_entity, value=new_bonus)

                                    # create starting armour from armourset and prefix
                                    this_armourset = ItemManager.create_full_armour_set(gameworld=gameworld, armourset='Embroided', prefix=decoded_build[selected_build][Build.BUILDARMOUR].lower(),
                                                                                        game_config=game_config)

                                    ItemUtilities.equip_full_set_of_armour(gameworld=gameworld, entity=player_entity, armourset=this_armourset)

                                    # spells for the player character
                                    spellfile = MobileUtilities.get_character_class_spellfilename(gameworld, player_entity)

                                    class_component = MobileUtilities.get_character_class(gameworld, player_entity)
                                    generate_spells(gameworld=gameworld, game_config=game_config, spell_file=spellfile,
                                                    player_class=class_component)

                                    # weapons
                                    if decoded_build[selected_build][Build.BUILDMAINHAND] == decoded_build[selected_build][Build.BUILDOFFHAND]:
                                        created_weapon = ItemManager.create_weapon(gameworld=gameworld,weapon_type=decoded_build[selected_build][Build.BUILDMAINHAND],
                                                                                   game_config=game_config)
                                        weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)
                                        WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type, class_component)

                                        # equip player with newly created starting weapon
                                        MobileUtilities.equip_weapon(gameworld=gameworld, entity=player_entity, weapon=created_weapon, hand='both')
                                    else:
                                        main_hand = decoded_build[selected_build][Build.BUILDMAINHAND]
                                        off_hand = decoded_build[selected_build][Build.BUILDOFFHAND]

                                        if main_hand != '' and main_hand != off_hand:
                                            logger.info('creating a 1-handed weapon (main hand) for the player')

                                            # created_weapon, hands_to_hold = NewCharacter.create_starting_weapon(gameworld, player, game_config)
                                            created_weapon = ItemManager.create_weapon(gameworld=gameworld,
                                                                                       weapon_type=main_hand,
                                                                                       game_config=game_config)
                                            weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)

                                            # parameters are: gameworld, weapon object, weapon type as a string, mobile class
                                            logger.info('Loading that weapon with the necessary spells')
                                            WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type,
                                                                                class_component)

                                            # equip player with newly created starting weapon
                                            MobileUtilities.equip_weapon(gameworld=gameworld, entity=player_entity,
                                                                         weapon=created_weapon, hand='main')

                                        if off_hand != '' and off_hand != main_hand:

                                            created_weapon = ItemManager.create_weapon(gameworld=gameworld,
                                                                                       weapon_type=off_hand,
                                                                                       game_config=game_config)
                                            weapon_type = ItemUtilities.get_weapon_type(gameworld, created_weapon)

                                            # parameters are: gameworld, weapon object, weapon type as a string, mobile class
                                            logger.info('Loading that weapon with the necessary spells')
                                            WeaponClass.load_weapon_with_spells(gameworld, created_weapon, weapon_type,
                                                                                class_component)

                                            # equip player with newly created starting weapon
                                            MobileUtilities.equip_weapon(gameworld=gameworld, entity=player_entity,
                                                                         weapon=created_weapon, hand='off')

                                    # load spell bar with spells from weapon
                                    spell_bar_entity = MobileUtilities.create_spell_bar_as_entity(gameworld=gameworld)
                                    MobileUtilities.set_spellbar_for_entity(gameworld=gameworld, entity=player_entity,
                                                                            spellbarEntity=spell_bar_entity)
                                    logger.info('Loading spell bar based on equipped weapons')
                                    weapons_equipped = MobileUtilities.get_weapons_equipped(gameworld=gameworld,
                                                                                            entity=player_entity)
                                    SpellUtilities.populate_spell_bar_from_weapon(gameworld, player_entity=player_entity,
                                                                                  spellbar=spell_bar_entity,
                                                                                  wpns_equipped=weapons_equipped)

                                    # jewellery
                                    player_class = MobileUtilities.get_character_class(gameworld=gameworld, entity=player_entity)
                                    class_file = read_json_file(player_class_file)
                                    jewellery_set = decoded_build[selected_build][Build.BUILDJEWELLERY]

                                    for playerClass in class_file['classes']:
                                        if playerClass['name'] == player_class:
                                            neck_gemstone = playerClass[jewellery_set]['neck']
                                            ring1_gemstone = playerClass[jewellery_set]['ring1']
                                            ring2_gemstone = playerClass[jewellery_set]['ring2']
                                            ear1_gemstone = playerClass[jewellery_set]['earring1']
                                            ear2_gemstone = playerClass[jewellery_set]['earring2']

                                    # create jewellery entity
                                    pendant = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='neck',
                                                                           e_setting='copper', e_hook='copper',
                                                                           e_activator=neck_gemstone)
                                    left_ring = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ring',
                                                                             e_setting='copper', e_hook='copper',
                                                                             e_activator=ring1_gemstone)
                                    right_ring = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ring',
                                                                              e_setting='copper', e_hook='copper',
                                                                              e_activator=ring2_gemstone)
                                    left_ear = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ear',
                                                                            e_setting='copper', e_hook='copper',
                                                                            e_activator=ear1_gemstone)
                                    right_ear = ItemManager.create_jewellery(gameworld=gameworld, bodylocation='ear',
                                                                             e_setting='copper', e_hook='copper',
                                                                             e_activator=ear2_gemstone)

                                    # equip jewellery entity to player character
                                    ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player_entity, bodylocation='neck', trinket=pendant)
                                    ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player_entity, bodylocation='left hand', trinket=left_ring)
                                    ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player_entity, bodylocation='right hand', trinket=right_ring)
                                    ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player_entity, bodylocation='left ear', trinket=left_ear)
                                    ItemUtilities.equip_jewellery(gameworld=gameworld, mobile=player_entity, bodylocation='right ear', trinket=right_ear)

                                    # apply gemstone benefits
                                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=pendant)
                                    ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player_entity, statbonus=jewelleyStatBonus)

                                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=left_ring)
                                    ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player_entity, statbonus=jewelleyStatBonus)

                                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=right_ring)
                                    ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player_entity, statbonus=jewelleyStatBonus)

                                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=left_ear)
                                    ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player_entity, statbonus=jewelleyStatBonus)

                                    jewelleyStatBonus = ItemUtilities.get_jewellery_stat_bonus(gameworld=gameworld, entity=right_ear)
                                    ItemUtilities.add_jewellery_benefit(gameworld=gameworld, entity=player_entity, statbonus=jewelleyStatBonus)

                                    #
                                    # calculate derived stats
                                    #
                                    MobileUtilities.calculate_derived_attributes(gameworld=gameworld, gameconfig=game_config)
                                    CharacterCreation.display_starting_character(root_console=root_console, gameworld=gameworld)


