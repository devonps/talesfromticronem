from bearlibterminal import terminal
from loguru import logger

from utilities import configUtilities
from utilities.input_handlers import handle_game_keys
from utilities.mobileHelp import MobileUtilities


class GameOver:

    @staticmethod
    def process_game_over(player_died, gameworld):
        game_config = configUtilities.load_config()
        player_entity = MobileUtilities.get_player_entity(gameworld=gameworld, game_config=game_config)
        player_names = MobileUtilities.get_mobile_name_details(gameworld=gameworld, entity=player_entity)

        terminal.clear()
        GameOver.display_game_over_screen(game_config=game_config)

        if player_died:
            logger.debug('Player Died - display Game Over Screen')
            GameOver.display_killed_by_information(game_config=game_config, gameworld=gameworld, player_entity=player_entity)
        else:
            logger.debug('Player Quit - display something else')

        terminal.refresh()
        valid_event = False
        while not valid_event:
            event_to_be_processed, event_action = handle_game_keys()
            if event_action == 'quit':
                valid_event = True

    @staticmethod
    def display_game_over_screen(game_config):
        banner_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                               parameter='GO_BANNER_POS_X')
        banner_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                               parameter='GO_BANNER_POS_Y')

        terminal.printf(x=banner_x, y=banner_y,
                        s=" ██████╗  █████╗ ███╗   ███╗███████╗   █████╗ ██╗   ██╗███████╗██████╗ ")
        terminal.printf(x=banner_x, y=banner_y + 1,
                        s="██╔════╝ ██╔══██╗████╗ ████║██╔════╝  ██╔══██╗██║   ██║██╔════╝██╔══██╗")
        terminal.printf(x=banner_x, y=banner_y + 2,
                        s="██║  ██╗ ███████║██╔████╔██║█████╗    ██║  ██║╚██╗ ██╔╝█████╗  ██████╔╝")
        terminal.printf(x=banner_x, y=banner_y + 3,
                        s="██║  ╚██╗██╔══██║██║╚██╔╝██║██╔══╝    ██║  ██║ ╚████╔╝ ██╔══╝  ██╔══██╗")
        terminal.printf(x=banner_x, y=banner_y + 4,
                        s="╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗  ╚█████╔╝  ╚██╔╝  ███████╗██║  ██║")
        terminal.printf(x=banner_x, y=banner_y + 5,
                        s=" ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝   ╚════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝")

    @staticmethod
    def display_killed_by_information(game_config, gameworld, player_entity):
        killed_by_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_KILLED_BY_X')
        killed_by_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_KILLED_BY_Y')
        died_when_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_WHEN_DIED_X')
        died_when_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_WHEN_DIED_Y')
        condi_print_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_CONDI_X')
        condi_print_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_CONDI_Y')
        boon_print_x = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_BOON_X')
        boon_print_y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gameOver',
                                                                  parameter='GO_BOON_Y')

        # the thing that killed the player
        terminal.printf(x=killed_by_x, y=killed_by_y, s='You died of poisoning!')

        # at the time of your death
        terminal.printf(x=died_when_x, y=died_when_y, s='At the time of your death...')

        # condis attached
        current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld, entity=player_entity)
        condi_string = 'You were suffering from '
        if len(current_condis) > 0:
            condi_count = 0
            max_condi = len(current_condis)
            for condi in current_condis:
                condi_string += condi['name']
                if condi_count + 1 < max_condi:
                    condi_string += ', '
                else:
                    condi_string += ', and '
        else:
            condi_string += 'no conditions, lucky you!'

        terminal.printf(x=condi_print_x, y=condi_print_y, s=condi_string)

        # boons attached
        current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=gameworld, entity=player_entity)
        boon_string = 'You benefited from '
        max_boon = len(current_boons)
        if max_boon > 0:
            boon_count = 0
            for boon in current_boons:
                boon_string += boon['name']
                if boon_count + 1 < max_boon:
                    boon_string += ', '
                else:
                    boon_string += ', and '
        else:
            boon_string += 'absolutely nothing.'

        terminal.printf(x=boon_print_x, y=boon_print_y, s=boon_string)


    # when you died

    # Armour / Jewellery / Weapons panel
