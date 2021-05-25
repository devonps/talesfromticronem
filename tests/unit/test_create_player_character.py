import pytest
import esper

from components import mobiles


@pytest.fixture
def world():
    return esper.World()


@pytest.fixture
def mobile_ai_level_none():
    return 0


@pytest.fixture
def mobile_ai_level_player():
    return 1


@pytest.fixture
def mobile_ai_level_wizard():
    return 2


@pytest.fixture
def mobile_ai_level_demon():
    return 3


@pytest.fixture
def mobile_ai_level_monster():
    return 4


@pytest.fixture
def mobile_ai_level_npc():
    return 5


@pytest.fixture
def mobile_ai_level_master():
    return 99


def test_add_empty_inventory_component_to_entity(world):
    mobile = world.create_entity()
    world.add_component(mobile, mobiles.Inventory())
    mobile_inventory_component = world.component_for_entity(mobile, mobiles.Inventory)

    assert mobile_inventory_component.exists is False
    assert type(mobile_inventory_component.bags) is list
    assert type(mobile_inventory_component.items) is list


def test_add_ai_level_to_entity(world):
    mobile = world.create_entity()
    world.add_component(mobile, mobiles.AILevel())
    mobile_ai_component = world.component_for_entity(mobile, mobiles.AILevel)

    assert mobile_ai_component.label == 0


def test_add_ai_player_level_to_entity(world, mobile_ai_level_player):
    mobile = world.create_entity()
    world.add_component(mobile, mobiles.AILevel())
    mobile_ai_component = world.component_for_entity(mobile, mobiles.AILevel)

    world.component_for_entity(mobile, mobiles.AILevel).label = mobile_ai_level_player

    assert mobile_ai_component.label == 1


def test_add_ai_demon_level_to_entity(world, mobile_ai_level_demon):
    mobile = world.create_entity()
    world.add_component(mobile, mobiles.AILevel())
    mobile_ai_component = world.component_for_entity(mobile, mobiles.AILevel)

    world.component_for_entity(mobile, mobiles.AILevel).label = mobile_ai_level_demon

    assert mobile_ai_component.label == 3


def test_add_ai_wizard_level_to_entity(world, mobile_ai_level_wizard):
    mobile = world.create_entity()
    world.add_component(mobile, mobiles.AILevel())
    mobile_ai_component = world.component_for_entity(mobile, mobiles.AILevel)

    world.component_for_entity(mobile, mobiles.AILevel).label = mobile_ai_level_wizard

    assert mobile_ai_component.label == 2


def test_add_ai_monster_level_to_entity(world, mobile_ai_level_monster):
    mobile = world.create_entity()
    world.add_component(mobile, mobiles.AILevel())
    mobile_ai_component = world.component_for_entity(mobile, mobiles.AILevel)

    world.component_for_entity(mobile, mobiles.AILevel).label = mobile_ai_level_monster

    assert mobile_ai_component.label == 4


def test_add_ai_npc_level_to_entity(world, mobile_ai_level_npc):
    mobile = world.create_entity()
    world.add_component(mobile, mobiles.AILevel())
    mobile_ai_component = world.component_for_entity(mobile, mobiles.AILevel)

    world.component_for_entity(mobile, mobiles.AILevel).label = mobile_ai_level_npc

    assert mobile_ai_component.label == 5


def test_add_ai_master_level_to_entity(world, mobile_ai_level_master):
    mobile = world.create_entity()
    world.add_component(mobile, mobiles.AILevel())
    mobile_ai_component = world.component_for_entity(mobile, mobiles.AILevel)

    world.component_for_entity(mobile, mobiles.AILevel).label = mobile_ai_level_master

    assert mobile_ai_component.label == 99

