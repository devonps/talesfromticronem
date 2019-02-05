from processors.render import RenderConsole, RenderPlayerCharacterScreen, RenderInventory
from processors.move_entities import MoveEntities


def remove_all_processors(gameworld):
    gameworld.remove_processor(processor_type=RenderConsole)
    gameworld.remove_processor(processor_type=RenderInventory)
    gameworld.remove_processor(processor_type=RenderPlayerCharacterScreen)
    gameworld.remove_processor(processor_type=MoveEntities)


def clear_world_database(gameworld):
    gameworld.clear_database()


def reset_gameworld(gameworld):
    clear_world_database(gameworld)
    remove_all_processors(gameworld)
