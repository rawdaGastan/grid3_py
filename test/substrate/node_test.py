"""Node testing"""

import logging
import pytest
from substrate.exceptions import NodeUpdateException
from substrate.farm import Farm
from substrate.twin import Twin
from .utils import start_local_connection, ALICE_IDENTITY, TEST_NAME, ALICE_ADDRESS, GIGABYTE
from substrate.node import Location, Node, NodeCertification, OptionSerial, Resources

substrate = start_local_connection()
test_node_id = 0
test_twin_id = 0
test_farm_id = 0


def test_create_node():
    """test create node"""

    global test_farm_id
    test_farm_id = Farm.create(substrate, ALICE_IDENTITY, TEST_NAME, [])

    resources = Resources(
        hru=1024 * GIGABYTE,
        sru=100 * GIGABYTE,
        cru=8,
        mru=1024 * GIGABYTE,
    )

    location = Location(
        city="someCity",
        country="someCountry",
        latitude="51.049999",
        longitude="3.733333",
    )

    serial_number = OptionSerial(has_value=True, as_value="some_serial")

    global test_node_id
    test_node_id = Node.create(
        substrate, ALICE_IDENTITY, test_farm_id, resources, location, [], False, False, serial_number
    )

    global test_twin_id
    test_twin_id = Twin.get_twin_id_from_public_key(substrate, ALICE_ADDRESS)

    assert test_node_id != 0


def test_update_node():
    """test update node"""

    resources = Resources(
        hru=1024 * GIGABYTE,
        sru=100 * GIGABYTE,
        cru=8,
        mru=1024 * GIGABYTE,
    )

    location = Location(
        city="someCity",
        country="someCountry",
        latitude="51.049999",
        longitude="3.733333",
    )

    serial_number = OptionSerial(has_value=True, as_value="some_serial")

    try:
        Node.update(
            substrate, ALICE_IDENTITY, test_node_id, test_farm_id, resources, location, [], False, False, serial_number
        )
    except NodeUpdateException as exp:
        logging.exception(exp)


def test_set_node_certification():
    """test set node certificate"""
    certification = NodeCertification(is_diy=True, is_certified=False)

    with pytest.raises(Exception) as e:
        Node.set_node_certificate(substrate, ALICE_IDENTITY, test_node_id, certification)


'''TODO  
def test_update_node_uptime():
    """test update node uptime"""
    
    try:
        Node.update_uptime(substrate, ALICE_IDENTITY, 0)
    except NodeUpdateException as exp:
        logging.exception(exp)
'''


def test_get_node_id_by_twin_id():
    """test get node ID by twin ID"""

    node_id = Node.get_id_by_twin_id(substrate, test_twin_id)
    assert node_id == test_node_id


def test_get_nodes_by_farm_id():
    """test get nodes' IDs by farm ID"""

    nodes = Node.get_nodes_by_farm_id(substrate, test_farm_id)
    assert test_node_id in nodes


def test_last_node_id():
    """test get last node ID"""

    node_id = Node.get_last_node_id(substrate)
    assert node_id != 0


def test_get_node_by_id():
    """test get node by ID"""

    node = Node.get(substrate, test_node_id)
    assert node.id == test_node_id
    assert node.twin_id == test_twin_id
    assert node.farm_id == test_farm_id
