import esper
import pytest


@pytest.fixture
def world():
    return esper.World()


class Position:
    def __init__(self):
        self.posx = 1
        self.posy = 1


class Health:
    def __init__(self):
        self.current = 100


def test_create_world(world):
    assert type(world) == esper.World


def test_create_entity(world):
    player = world.create_entity()
    assert type(player) == int


def test_two_entities_cannot_share_the_same_id(world):
    player = world.create_entity()
    enemy = world.create_entity()
    assert player < enemy


def test_entity_can_be_assigned_a_component(world):
    player = world.create_entity()
    world.add_component(player, Position())
    assert world.has_component(player, Position) is True


def test_entity_does_not_have_the_position_component(world):
    enemy = world.create_entity()
    world.add_component(enemy, Health())
    assert world.has_component(enemy, Position) is False


def test_clear_database(world):
    world.clear_database()
    assert len(world._entities) == 0
    assert len(world._components) == 0
    assert len(world._processors) == 0
    assert len(world._dead_entities) == 0
    assert world._next_entity_id == 0
