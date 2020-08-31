import esper

from components import mobiles
from utilities.gamemap import GameMapUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.replayGame import ReplayGame
from loguru import logger


def check_velocity(velocity, cvx, cvy):
    if velocity.dx != 0:
        svx = str(velocity.dx)
    else:
        svx = cvx
    if velocity.dy != 0:
        svy = str(velocity.dy)
    else:
        svy = cvy
    return svx, svy


class MoveEntities(esper.Processor):
    def __init__(self, gameworld, game_map):
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, game_config, advance_game_turn):
        if advance_game_turn:
            player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)

            message_log_just_viewed = MobileUtilities.get_view_message_log_value(gameworld=self.gameworld, entity=player_entity)
            if not message_log_just_viewed:
                self.attempt_to_move_entities(game_config=game_config)

    def attempt_to_move_entities(self, game_config):
        #
        # this works off the game map positioning AND NOT THE SCREEN POSITION
        #
        for ent, (velocity, position) in self.gameworld.get_components(mobiles.Velocity, mobiles.Position):
            px = position.x
            py = position.y

            am_i_blocked = self.check_for_blocked_movement(px + velocity.dx, py + velocity.dy)
            if not am_i_blocked:
                position.x += velocity.dx
                position.y += velocity.dy

                if velocity.dx != 0 or velocity.dy != 0:
                    svx = '0'
                    svy = '0'

                    # remove mobile from current game map position
                    GameMapUtilities.remove_mobile_from_map_position(game_map=self.game_map, px=px, py=py)

                    # add mobile entity to new game map position
                    GameMapUtilities.add_mobile_to_map_position(game_map=self.game_map, px=position.x, py=position.y,
                                                                entity=ent)

                    svx, svy = check_velocity(velocity=velocity, cvx=svx, cvy=svy)

                    MobileUtilities.set_mobile_has_moved(self.gameworld, ent, True)
                    value = 'move:' + str(ent) + ':' + svx + ':' + svy
                    ReplayGame.update_game_replay_file(game_config, value)
            else:
                logger.debug(' cannot move to x/y {}/{}', position.x + velocity.dx, position.y + velocity.dy)
            # regardless of making the move - reduce the velocity to zero
            velocity.dx = 0
            velocity.dy = 0

    # check if new position would cause a collision with a blockable tile
    def check_for_blocked_movement(self, newx, newy):
        return GameMapUtilities.is_tile_blocked(self.game_map, newx, newy)
