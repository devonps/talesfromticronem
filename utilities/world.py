from loguru import logger
from processors import move_entities, render, updateEntities


def remove_all_processors(gameworld):
    gameworld.remove_processor(render.RenderConsole)
    gameworld.remove_processor(render.RenderInventory)
    gameworld.remove_processor(render.RenderPlayerCharacterScreen)
    gameworld.remove_processor(move_entities.MoveEntities)
    gameworld.remove_processor(updateEntities.UpdateEntitiesProcessor)


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
