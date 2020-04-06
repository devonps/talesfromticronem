from utilities import configUtilities


def text_entry(game_config):
    TXT_PANEL_FPS = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_FPS')
    TXT_PANEL_WIDTH = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WIDTH')
    TXT_PANEL_HEIGHT = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_HEIGHT')
    TXT_PANEL_WRITE_X = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WRITE_X')
    TXT_PANEL_WRITE_Y = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui', parameter='TXT_PANEL_WRITE_Y')

    timer = 0
    letter_count = 0
    my_word = ""
    key_pressed = False
    max_letters = 15
    bg = 0
