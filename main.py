import hashlib
from substrateinterface import SubstrateInterface, Keypair

substrate = SubstrateInterface(url="wss://tfchain.dev.grid.tf")


result = substrate.query("TfgridModule", "ZosVersion")

print(result)

result = substrate.query(
    "TfgridModule",
    "TwinIdByAccountID",
    ["5DLnD4kp8KBAgTbz2p7wc5GnJSW4jAtUEtxkSdnkNtLwjk48"],
)

print(result)

account_id = substrate.ss58_decode("5DLnD4kp8KBAgTbz2p7wc5GnJSW4jAtUEtxkSdnkNtLwjk48")

print(account_id)

result = substrate.query(
    "System",
    "Account",
    ["5DLnD4kp8KBAgTbz2p7wc5GnJSW4jAtUEtxkSdnkNtLwjk48"],
)

print(result)

####################################################################################################
mnemonic = "member imitate cry social luggage hybrid leopard retreat giggle unique segment order"
keypair = Keypair.create_from_mnemonic(mnemonic)


res_hash = hashlib.md5("somedocument".encode()).hexdigest()
print("The hexadecimal equivalent of hash is : ", end="")
print(res_hash)

call = substrate.compose_call(
    "TfgridModule",
    "user_accept_tc",
    {"document_link": "somedocument", "document_hash": res_hash},
)

extrinsic = substrate.create_signed_extrinsic(call, keypair)

result = substrate.submit_extrinsic(extrinsic, True, True)

print(result.is_success)
print(result.error_message)

call = substrate.compose_call(
    "TfgridModule",
    "create_twin",
    {"ip": "::1"},
)

extrinsic = substrate.create_signed_extrinsic(call, keypair)

result = substrate.submit_extrinsic(extrinsic, True, True)

print(result.is_success)
print(result.error_message)

result = substrate.query(
    "TfgridModule",
    "TwinIdByAccountID",
    [keypair.public_key],
)

print(result)

# print(result.value['nonce']) #  7695
# print(result.value['data']['free']) # 635278638077956496
