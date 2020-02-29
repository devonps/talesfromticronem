import esper

from components import mobiles
from utilities.mobileHelp import MobileUtilities


class UpdateEntitiesProcessor(esper.Processor):
    """
    This processor cycles through ALL entities and calculates their attributes
    """

    def __init__(self, gameworld):
        super().__init__()
        self.gameworld = gameworld

    def process(self, game_config):
        for ent, ai in self.gameworld.get_component(mobiles.AI):
            inCombat = MobileUtilities.get_combat_status(self.gameworld, entity=ent)

            # apply condition damage + effects
            current_condis = MobileUtilities.get_current_condis_applied_to_mobile(gameworld=self.gameworld, entity=ent)
            if len(current_condis) != 0:
                pass

            # apply buffs
            current_boons = MobileUtilities.get_current_boons_applied_to_mobile(gameworld=self.gameworld, entity=ent)
            if len(current_boons) != 0:
                pass

            # apply controls

            # gain resources from spells


            if not inCombat:
                MobileUtilities.calculate_derived_attributes(self.gameworld, entity=ent)

