import esper

from components import mobiles
from map_objects.gameMap import GameMap


class MoveEntities(esper.Processor):
    def __init__(self, gameworld, game_map):
        super().__init__()
        self.gameworld = gameworld
        self.game_map = game_map

    def process(self, *args, **kwargs):
        for ent, (vel, pos) in self.gameworld.get_components(mobiles.Velocity, mobiles.Position):
            am_i_blocked = self.check_for_blocked_movement(pos.x + vel.dx, pos.y + vel.dy)

            if not am_i_blocked:
                pos.x += vel.dx
                pos.y += vel.dy

            # regardless of making the move - reduce the velocity to zero
            vel.dx = 0
            vel.dy = 0

    # check if new position would cause a collision with a blockable tile
    def check_for_blocked_movement(self, newx, newy):
        return GameMap.is_blocked(self.game_map, newx, newy)
