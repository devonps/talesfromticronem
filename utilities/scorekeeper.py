from components import scorekeeper


class ScorekeeperUtilities:

    # Get scorekeeper entity id
    @staticmethod
    def get_scorekeeper_entity(gameworld):
        scorekeeper_entity = 0
        for ent, scf in gameworld.get_component(scorekeeper.ScoreKeeperFlag):
            if scf.sc_flag:
                scorekeeper_entity = ent

        return scorekeeper_entity

    # NUMBER OF TURNS

    @staticmethod
    def get_current_turn_id(gameworld):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)

        game_turn_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.NumberOfTurns)
        return game_turn_component.count

    @staticmethod
    def increase_game_turn_count(gameworld):
        scorekeeper_entity = ScorekeeperUtilities.get_scorekeeper_entity(gameworld=gameworld)

        current_game_turn_id = ScorekeeperUtilities.get_current_turn_id(gameworld=gameworld)

        game_turn_component = gameworld.component_for_entity(scorekeeper_entity, scorekeeper.NumberOfTurns)
        game_turn_component.count = current_game_turn_id + 1
