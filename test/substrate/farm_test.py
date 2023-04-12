"""Farm testing"""

from .utils import start_local_connection, ALICE_IDENTITY, TEST_NAME
from substrate.farm import Farm, PublicIP

substrate = start_local_connection()
test_farm_id = 0


def test_create_farm():
    """test create farm"""

    global test_farm_id
    test_farm_id = Farm.create(
        substrate, ALICE_IDENTITY, TEST_NAME, [PublicIP(ip="1.1.1.1", gw="1.1.1.1", contract_id=0)]
    )
    assert test_farm_id != 0


def test_get_farm_by_id():
    """test get farm by ID"""

    farm = Farm.get(substrate, test_farm_id)
    assert farm.id == test_farm_id


def test_get_farm_id_by_name():
    """test get farm ID by name"""

    farm_id = Farm.get_farm_id_by_name(substrate, TEST_NAME)
    assert farm_id == test_farm_id
