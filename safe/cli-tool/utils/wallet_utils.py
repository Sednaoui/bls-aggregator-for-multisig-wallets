from web3 import Web3
from web3.middleware import geth_poa_middleware

from constants import safe_abi, aggregation_auth_module_address, wallets, aggregation_auth_abi

web3_client = Web3(
    Web3.HTTPProvider("https://optimism-goerli.blockpi.network/v1/rpc/8021a864ba8eee7a67f26645d4aa876f8dbac7d4"))
web3_client.middleware_onion.inject(geth_poa_middleware, layer=0)


def is_module_enabled(wallet):
    safe = web3_client.eth.contract(address=wallets[wallet]["address"], abi=safe_abi["abi"])
    module_enabled = safe.functions.isModuleEnabled(aggregation_auth_module_address).call()
    return module_enabled


def are_bls_owners_added(wallet):
    module = web3_client.eth.contract(address=aggregation_auth_module_address, abi=aggregation_auth_abi["abi"])
    threshold = module.functions.getThreshold(wallets[wallet]["address"]).call()
    return threshold > 0


def get_bls_threshold(wallet):
    module = web3_client.eth.contract(address=aggregation_auth_module_address, abi=aggregation_auth_abi["abi"])
    threshold = module.functions.getThreshold(wallets[wallet]["address"]).call()
    return threshold


def create_binary_bitmap(arr, upper_limit):
    bitmap = [0] * (upper_limit + 1)
    for num in arr:
        if num >= 0 and num <= upper_limit:
            bitmap[num] = 1
    binary_string = ''.join(map(str, bitmap))
    return int(binary_string[::-1], 2)
