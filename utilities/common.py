from utilities import configUtilities
from components import viewport, mobiles


class CommonUtils:

    @staticmethod
    def calculate_percentage(lowNumber, maxNumber):
        return int((lowNumber / maxNumber) * 100)

    @staticmethod
    def create_viewport_as_entity(gameworld, vwp):
        game_config = configUtilities.load_config()

        viewport_width = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                     parameter='VIEWPORT_WIDTH')
        viewport_height = configUtilities.get_config_value_as_integer(configfile=game_config, section='gui',
                                                                      parameter='VIEWPORT_HEIGHT')

        gameworld.add_component(vwp, viewport.Dimensions(width=viewport_width, height=viewport_height))
        gameworld.add_component(vwp,
                                viewport.DisplayRange(min_x=0, max_x=viewport_width, min_y=0, max_y=viewport_height))
        gameworld.add_component(vwp, viewport.PlayerViewportPosition(viewport_x=0, viewport_y=0))

    @staticmethod
    def get_viewport_width(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Dimensions)

        return viewport_component.width

    @staticmethod
    def get_viewport_height(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.Dimensions)

        return viewport_component.height

    @staticmethod
    def get_x_axis_info(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)

        return [viewport_component.min_x, viewport_component.max_x]

    @staticmethod
    def get_y_axis_info(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.DisplayRange)

        return [viewport_component.min_y, viewport_component.max_y]

    @staticmethod
    def get_player_position_info(gameworld, viewport_id):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.PlayerViewportPosition)

        return [viewport_component.viewport_x, viewport_component.viewport_y]

    @staticmethod
    def set_player_position_x(gameworld, viewport_id, posx):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.PlayerViewportPosition)

        viewport_component.viewport_x = posx

    @staticmethod
    def set_player_position_y(gameworld, viewport_id, posy):
        viewport_component = gameworld.component_for_entity(viewport_id, viewport.PlayerViewportPosition)

        viewport_component.viewport_y = posy

