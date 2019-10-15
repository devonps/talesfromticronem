import esper
from loguru import logger
# from processors import move_entities, updateEntities, renderGameMap


def create_game_world():
    return esper.World()


def remove_all_processors(gameworld):
    # gameworld.remove_processor(renderGameMap.RenderGameMap)
    # gameworld.remove_processor(move_entities.MoveEntities)
    # gameworld.remove_processor(updateEntities.UpdateEntitiesProcessor)
    pass


def clear_world_database(gameworld):
    gameworld.clear_database()
    if gameworld._next_entity_id > 0:
        logger.warning('Gameworld not cleared down correctly - next entity')
    if len(gameworld._processors) > 0:
        logger.warning('Gameworld not cleared down correctly - processors')
    if len(gameworld._components) > 0:
        logger.warning('Gameworld not cleared down correctly - components')


def reset_gameworld(gameworld):
    remove_all_processors(gameworld)
    clear_world_database(gameworld)


def get_next_entity_id(gameworld):
    return gameworld.create_entity()


def remove_component_from_entity(gameworld, entity, component):
    gameworld.remove_component(entity, component)


def does_entity_have_component(gameworld, entity, component):
    return gameworld.has_component(entity, component)
