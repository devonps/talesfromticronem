import esper
from components import mobiles
from utilities import gamemap, mobileHelp, replayGame
from loguru import logger

from utilities.gamemap import GameMapUtilities


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
            player_entity = mobileHelp.MobileUtilities.get_player_entity(gameworld=self.gameworld)

            message_log_just_viewed = mobileHelp.MobileUtilities.get_view_message_log_value(gameworld=self.gameworld,
                                                                                            entity=player_entity)
            if not message_log_just_viewed:
                self.attempt_to_move_entities()

    def attempt_to_move_entities(self):
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
                    gamemap.GameMapUtilities.remove_entity_from_map_position(game_map=self.game_map, px=px, py=py)

                    # add mobile entity to new game map position
                    gamemap.GameMapUtilities.set_entity_at_this_map_location(game_map=self.game_map, x=position.x,
                                                                             y=position.y,
                                                                             entity=ent)
                    spell_entities_at_map_location = GameMapUtilities.get_list_of_spells_at_this_map_location(game_map=self.game_map, x=position.x, y=position.y)
                    if len(spell_entities_at_map_location) > 0:
                        # do some checking around what do to for spells at this location
                        logger.info('Entity standing on a spell')
                        mobileHelp.MobileUtilities.set_player_scene_change(gameworld=self.gameworld,
                                                                           player_entity=ent, value=True)
                        mobileHelp.MobileUtilities.set_player_current_scene_exit(gameworld=self.gameworld, scene_exit=2,
                                                                                 player_entity=ent)

                    svx, svy = check_velocity(velocity=velocity, cvx=svx, cvy=svy)

                    mobileHelp.MobileUtilities.set_mobile_has_moved(self.gameworld, ent, True)
                    value = 'move:' + str(ent) + ':' + svx + ':' + svy
                    replayGame.ReplayGame.update_game_replay_file(value)
            else:
                logger.debug(' cannot move to x/y {}/{}', position.x + velocity.dx, position.y + velocity.dy)
            # regardless of making the move - reduce the velocity to zero
            velocity.dx = 0
            velocity.dy = 0

    # check if new position would cause a collision with a blockable tile
    def check_for_blocked_movement(self, newx, newy):
        return gamemap.GameMapUtilities.is_tile_blocked(self.game_map, newx, newy)
