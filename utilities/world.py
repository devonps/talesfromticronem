import esper


def create_game_world():
    return esper.World()


def get_next_entity_id(gameworld):
    return gameworld.create_entity()


def delete_entity(gameworld, entity):
    gameworld.delete_entity(entity=entity, immediate=True)


def remove_component_from_entity(gameworld, entity, component):
    gameworld.remove_component(entity, component)


def does_entity_have_component(gameworld, entity, component):
    return gameworld.has_component(entity, component)


def get_all_components_for_entity(gameworld, entity):
    return gameworld.components_for_entity(entity)


def check_if_entity_has_component(gameworld, entity, component):
    if gameworld.has_component(entity, component):
        return True
    else:
        return False
