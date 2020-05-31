import esper

from components import mobiles
from utilities import configUtilities
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

            viewport_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_WIDTH')

            vpx = MobileUtilities.get_player_viewport_x(gameworld=self.gameworld, entity=player_entity)
            vpy = MobileUtilities.get_player_viewport_y(gameworld=self.gameworld, entity=player_entity)

            for ent, (vel, pos) in self.gameworld.get_components(mobiles.Velocity, mobiles.Position):
                am_i_blocked = self.check_for_blocked_movement(pos.x + vel.dx, pos.y + vel.dy)
                if not am_i_blocked:
                    pos.x += vel.dx
                    pos.y += vel.dy
                    vpx += vel.dx
                    vpy += vel.dy

                    if ent == player_entity:
                        MobileUtilities.set_player_viewport_x(gameworld=self.gameworld, entity=player_entity, value=vpx)
                        MobileUtilities.set_player_viewport_y(gameworld=self.gameworld, entity=player_entity, value=vpy)

                    if vpx >= (viewport_width - 8):
                        configUtilities.set_config_value(configfile=game_config, section='gui',
                                                         parameter='VIEWPORT_RIGHT_VISITED', value='True')

                    if vpx - 8 <= 0:
                        configUtilities.set_config_value(configfile=game_config, section='gui',
                                                         parameter='VIEWPORT_LEFT_VISITED', value='True')

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
