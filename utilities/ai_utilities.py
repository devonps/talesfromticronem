from utilities import mobileHelp


class AIUtilities:

    @staticmethod
    def can_i_move(gameworld, source_entity):
        list_of_conditions = mobileHelp.MobileUtilities.get_current_condis_applied_to_mobile(gameworld=gameworld,
                                                                                             entity=source_entity)
        if ['crippled', 'immobilize', 'stunned', 'dazed'] in list_of_conditions:
            return False
        else:
            return True

    @staticmethod
    def what_can_i_see_around_me(gameworld, source_entity):
        # pending
        pass

    @staticmethod
    def have_i_taken_damage(gameworld, source_entity):
        # pending
        pass

    @staticmethod
    def can_i_cast_a_spell(gameworld, source_entity):
        # pending
        pass

    @staticmethod
    def can_i_see_my_target(gameworld, from_entity, to_entity, game_map):
        # pending
        pass
