from bearlibterminal import terminal
from loguru import logger

from utilities.input_handlers import handle_game_keys


class GameOver:

    @staticmethod
    def process_game_over(player_died):
        if player_died:
            logger.debug('Player Died - display Game Over Screen')
            terminal.clear()
            GameOver.display_game_over_screen()
            valid_event = False
            while not valid_event:
                event_to_be_processed, event_action = handle_game_keys()
                if event_action == 'quit':
                    valid_event = True
        else:
            logger.debug('Player Quit - display something else')

    @staticmethod
    def display_game_over_screen():
        x = 10
        y = 5
        terminal.printf(x=x, y=y,  s=" ██████╗  █████╗ ███╗   ███╗███████╗   █████╗ ██╗   ██╗███████╗██████╗ ")
        terminal.printf(x=x, y=y+1, s="██╔════╝ ██╔══██╗████╗ ████║██╔════╝  ██╔══██╗██║   ██║██╔════╝██╔══██╗")
        terminal.printf(x=x, y=y+2, s="██║  ██╗ ███████║██╔████╔██║█████╗    ██║  ██║╚██╗ ██╔╝█████╗  ██████╔╝")
        terminal.printf(x=x, y=y+3, s="██║  ╚██╗██╔══██║██║╚██╔╝██║██╔══╝    ██║  ██║ ╚████╔╝ ██╔══╝  ██╔══██╗")
        terminal.printf(x=x, y=y+4, s="╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗  ╚█████╔╝  ╚██╔╝  ███████╗██║  ██║")
        terminal.printf(x=x, y=y+5, s=" ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝   ╚════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝")

        terminal.refresh()