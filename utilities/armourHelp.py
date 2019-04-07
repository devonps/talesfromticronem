from components import armour


class ArmourUtilities:

    @staticmethod
    def get_armour_defense_value(gameworld, body_location):
        return gameworld.component_for_entity(body_location, armour.Defense).value

    @staticmethod
    def get_armour_set_name(gameworld, entity):
        return gameworld.component_for_entity(entity, armour.Set).label

    @staticmethod
    def get_armour_quality_level(gameworld, entity):
        return gameworld.component_for_entity(entity, armour.Quality).label

    @staticmethod
    def get_armour_piece_weight(gameworld, entity):
        return gameworld.component_for_entity(entity, armour.Weight).label

    @staticmethod
    def get_armour_prefix(gameworld, entity):
        return gameworld.component_for_entity(entity, armour.Describable).prefix

    @staticmethod
    def get_armour_suffix(gameworld, entity):
        return gameworld.component_for_entity(entity, armour.Describable).suffix

    @staticmethod
    def get_armour_piece_level(gameworld, entity):
        return gameworld.component_for_entity(entity, armour.Describable).level

    @staticmethod
    def get_armour_major_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, armour.AttributeBonus)
        major = [armour_attributes_component.majorName, armour_attributes_component.majorBonus]

        return major

    @staticmethod
    def get_armour_minor_attributes(gameworld, entity):
        armour_attributes_component = gameworld.component_for_entity(entity, armour.AttributeBonus)
        minor = [armour_attributes_component.minorOneName, armour_attributes_component.minorOneBonus]
        return minor
