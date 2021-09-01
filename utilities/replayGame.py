from utilities import configUtilities, externalfileutilities
from static.data import constants


class ReplayGame:

    @staticmethod
    def get_game_replay_actions():
        action_file = constants.FILE_GAME_ACTIONS_FILE

        # game_actions should be created as a list
        game_actions = externalfileutilities.Externalfiles.load_existing_file(action_file)

        return game_actions

    @staticmethod
    def update_game_replay_file(value):
        game_replay_file = constants.FILE_GAME_ACTIONS_FILE

        externalfileutilities.Externalfiles.write_to_existing_file(game_replay_file, value + '\n')
