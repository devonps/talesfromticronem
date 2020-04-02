import esper
import pytest


@pytest.fixture
def world():
    return esper.World()


def test_create_world(world):
    assert type(world) == esper.World


def test_create_entity(world):
    e1 = world.create_entity()
    e2 = world.create_entity()
    assert type(e1) == int
    assert type(e2) == int
    assert e1 < e2


def test_entity_has_one_component(world):
    e1 = world.create_entity()
    e2 = world.create_entity()
    world.add_component(e1, ComponentA())
    world.add_component(e2, ComponentB())
    assert world.has_component(e1, ComponentA) is True
    assert world.has_component(e1, ComponentB) is False
    assert world.has_component(e2, ComponentA) is False
    assert world.has_component(e2, ComponentB) is True


def test_clear_database(world):
    world.clear_database()
    assert len(world._entities) == 0
    assert len(world._components) == 0
    assert len(world._processors) == 0
    assert len(world._dead_entities) == 0
    assert world._next_entity_id == 0

# helpers

class ComponentA:
    def __init__(self):
        self.posx = 1
        self.posy = 1

class ComponentB:
    def __init__(self):
        self.health = 100
