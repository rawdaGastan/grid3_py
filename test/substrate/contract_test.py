"""contract testing"""

## 4 tests

import logging
from substrate.contract import Contract
from substrate.farm import Farm
from substrate.node import Location, Node, OptionSerial, Resources
from test.substrate.utils import start_local_connection, ALICE_IDENTITY, TEST_NAME, GIGABYTE

substrate = start_local_connection()


def test_name_contract():
    """test name contracts"""

    # create a name contract
    contract_id = Contract.create_name_contract(substrate, ALICE_IDENTITY, TEST_NAME)
    name_contract_id = Contract.get_contract_id_by_name_registration(substrate, TEST_NAME)

    # get rent contract
    created_contract: Contract = Contract.get(substrate, contract_id)

    # cancel created rent contract
    Contract.cancel(substrate, ALICE_IDENTITY, contract_id)

    assert name_contract_id == contract_id
    assert created_contract.contract_type.is_name_contract


def test_node_contract():
    """test create node contract"""

    # create a farm
    test_farm_id = Farm.create(substrate, ALICE_IDENTITY, TEST_NAME, [])

    # create a node
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

    test_node_id = Node.create(
        substrate, ALICE_IDENTITY, test_farm_id, resources, location, [], False, False, serial_number
    )

    # create a node contract
    contract_id = Contract.create_node_contract(substrate, ALICE_IDENTITY, test_node_id, "", "", 0)

    # get node contract
    created_contract: Contract = Contract.get(substrate, contract_id)

    node_contract_id = Contract.get_contract_id_with_hash_and_node_id(
        substrate, test_node_id, created_contract.contract_type.node_contract.deployment_hash
    )

    # update node contract
    Contract.update_node_contract(substrate, ALICE_IDENTITY, contract_id, "", "")

    # get node contracts
    node_contracts_ids = Contract.get_node_contracts(substrate, test_node_id)

    # cancel created node contract
    Contract.cancel(substrate, ALICE_IDENTITY, contract_id)

    assert node_contract_id == contract_id
    assert len(node_contracts_ids) == 1
    assert node_contract_id in node_contracts_ids
    assert created_contract.contract_type.is_node_contract
    assert created_contract.state.is_created


def test_rent_contract():
    """test rent contract"""

    # create a farm
    test_farm_id = Farm.create(substrate, ALICE_IDENTITY, TEST_NAME, [])

    # create a node
    resources = Resources(
        hru=1024 * GIGABYTE,
        sru=100 * GIGABYTE,
        cru=8,
        mru=1024 * GIGABYTE,
    )

    location = Location(
        city="someCity",
        country="someCountry",
        latitude="1.049999",
        longitude="3.733333",
    )

    serial_number = OptionSerial(has_value=True, as_value="some_serial_value")

    test_node_id = Node.create(
        substrate, ALICE_IDENTITY, test_farm_id, resources, location, [], False, False, serial_number
    )

    # create a rent contract
    contract_id = Contract.create_rent_contract(substrate, ALICE_IDENTITY, test_node_id)
    rent_contract_id = Contract.get_node_rent_contract_id(substrate, test_node_id)

    # get rent contract
    created_contract: Contract = Contract.get(substrate, contract_id)

    # cancel created rent contract
    Contract.cancel(substrate, ALICE_IDENTITY, contract_id)

    assert rent_contract_id == contract_id
    assert created_contract.contract_type.is_rent_contract
