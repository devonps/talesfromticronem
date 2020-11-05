from utilities import configUtilities, externalfileutilities


class ReplayGame:

    @staticmethod
    def get_game_replay_actions(game_config):
        action_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files',
                                                                 parameter='GAME_ACTIONS_FILE')

        # game_actions should be created as a list
        game_actions = externalfileutilities.Externalfiles.load_existing_file(action_file)

        return game_actions

    @staticmethod
    def update_game_replay_file(game_config, value):
        game_replay_file = configUtilities.get_config_value_as_string(configfile=game_config, section='files', parameter='GAME_ACTIONS_FILE')

        externalfileutilities.Externalfiles.write_to_existing_file(game_replay_file, value + '\n')
