import esper

from components import mobiles
from mapRelated.gameMap import GameMap
from utilities.common import CommonUtils
from utilities.gamemap import GameMapUtilities
from utilities.mobileHelp import MobileUtilities
from utilities.replayGame import ReplayGame
from loguru import logger


class MoveEntities(esper.Processor):
    def __init__(self, gameworld, game_map):
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, game_config):

        player_entity = MobileUtilities.get_player_entity(gameworld=self.gameworld, game_config=game_config)

        message_log_just_viewed = MobileUtilities.get_view_message_log_value(gameworld=self.gameworld, entity=player_entity)
        if not message_log_just_viewed:

            viewport_id = MobileUtilities.get_viewport_id(gameworld=self.gameworld, entity=player_entity)

            viewport_width = CommonUtils.get_viewport_width(gameworld=self.gameworld, viewport_id=viewport_id)

            viewport_player_position = CommonUtils.get_player_viewport_position_info(gameworld=self.gameworld,
                                                                                     viewport_id=viewport_id)

            vpx = viewport_player_position[0]
            vpy = viewport_player_position[1]

            for ent, (vel, pos) in self.gameworld.get_components(mobiles.Velocity, mobiles.Position):
                am_i_blocked = self.check_for_blocked_movement(pos.x + vel.dx, pos.y + vel.dy)
                if not am_i_blocked:
                    pos.x += vel.dx
                    pos.y += vel.dy
                    vpx += vel.dx
                    vpy += vel.dy
                    CommonUtils.set_player_viewport_position_x(gameworld=self.gameworld, viewport_id=viewport_id, posx=vpx)
                    CommonUtils.set_player_viewport_position_y(gameworld=self.gameworld, viewport_id=viewport_id, posy=vpy)

                    if vpx >= (viewport_width - 8):
                        # logger.info('Hit imaginary right-edge boundary on the X axis')
                        CommonUtils.set_viewport_right_boundary_visited_true(gameworld=self.gameworld, viewport_id=viewport_id)

                    if vpx - 8 <= 0:
                        # logger.info('Hit imaginary left-edge boundary on the X axis')
                        CommonUtils.set_viewport_left_boundary_visited_true(gameworld=self.gameworld, viewport_id=viewport_id)

                    if vel.dx != 0 or vel.dy != 0:
                        svx = '0'
                        svy = '0'

                        if vel.dx != 0:
                            svx = str(vel.dx)
                        if vel.dy != 0:
                            svy = str(vel.dy)

                        MobileUtilities.set_mobile_has_moved(self.gameworld, ent, True)
                        value = 'move:' + str(ent) + ':' + svx + ':' + svy
                        ReplayGame.update_game_replay_file(game_config, value)
                else:
                    logger.debug(' cannot move to x/y {}/{}', pos.x + vel.dx, pos.y + vel.dy)
                # regardless of making the move - reduce the velocity to zero
                vel.dx = 0
                vel.dy = 0

    # check if new position would cause a collision with a blockable tile
    def check_for_blocked_movement(self, newx, newy):
        return GameMapUtilities.is_tile_blocked(self.game_map, newx, newy)
