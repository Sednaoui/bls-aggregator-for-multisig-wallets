import eth_abi
from eth_account import Account
from hexbytes import HexBytes
from web3.auto import w3
from eth_abi.packed import encode_packed

from constants import wallets, safe_abi, normalSigners, aggregation_auth_module_address, aggregation_auth_abi, \
    blsSigners, bls_open_address, bls_open_abi, aggregator_address
from prompts import signers_prompt
from utils.bls_utils import affine_to_xyz_G1, sign, aggregate_signatures, xyz_to_affine_G1
from utils.wallet_utils import web3_client, create_binary_bitmap


def execution_handler(wallet, transaction):
    if transaction == "enable-bls-authentication-module":
        calldata = get_enable_module_calldata()
        exec_transaction(wallet, wallets[wallet]["address"], 0, calldata)
    elif transaction == "add-bls-owners":
        for index in range(len(blsSigners)):
            calldata = get_add_bls_owner_calldata(wallet, index)
            exec_transaction(wallet, aggregation_auth_module_address, 0, calldata)
    elif transaction == "self-transfer":
        tx_hash = get_self_transfer_txhash(wallet)
        signers = signers_prompt(wallet)
        signatures = []
        for index in signers:
            signatures.append(bls_sign(tx_hash, index))
        agg_sig = aggregate_signatures(signatures)
        agg_sig_affine = xyz_to_affine_G1(agg_sig)
        aggregated_sig = eth_abi.encode(["uint256[2]"], [[agg_sig_affine[0], agg_sig_affine[1]]]).hex()
        bitmask = create_binary_bitmap(signers, len(blsSigners))
        module_exec_transaction(wallet, wallets[wallet]["address"], 1, b'', bitmask, aggregated_sig)


def module_exec_transaction(
    wallet,
    to,
    value,
    data,
    bitmask,
    aggregated_sig
):
    module = web3_client.eth.contract(address=aggregation_auth_module_address, abi=aggregation_auth_abi["abi"])
    signer_pk = normalSigners[0]["publicKey"]
    signer_sk = normalSigners[0]["privateKey"]
    caller_nonce = web3_client.eth.get_transaction_count(signer_pk)
    execute_function = module.functions.execTransaction(
        wallets[wallet]["address"],
        to,
        value,
        data,
        bitmask,
        HexBytes(aggregated_sig)
    ).build_transaction({"from": signer_pk, "nonce": caller_nonce})
    signed_tx = web3_client.eth.account.sign_transaction(execute_function, private_key=signer_sk)
    send_tx = web3_client.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = str(send_tx.hex())
    print(f"Transaction sent: #{tx_hash}")
    tx_receipt = web3_client.eth.wait_for_transaction_receipt(send_tx, timeout=15)
    print(f"Transaction executed, status: {str(tx_receipt['status'])}")


def exec_transaction(
    wallet,
    to,
    value,
    data,
):
    safe = web3_client.eth.contract(address=wallets[wallet]["address"], abi=safe_abi["abi"])
    _nonce = safe.functions.nonce().call()
    tx_hash = safe.functions.getTransactionHash(
        to,
        value,
        data,
        0,
        0,
        0,
        0,
        "0x0000000000000000000000000000000000000000",
        "0x0000000000000000000000000000000000000000",
        _nonce,
    ).call()

    contract_transaction_hash = HexBytes(tx_hash)
    signer_pk = normalSigners[0]["publicKey"]
    signer_sk = normalSigners[0]["privateKey"]
    signer = Account.from_key(signer_sk)
    signature = signer.signHash(contract_transaction_hash)
    #
    caller_nonce = web3_client.eth.get_transaction_count(signer_pk)
    execute_function = safe.functions.execTransaction(
        to,
        value,
        data,
        0,
        0,
        0,
        0,
        "0x0000000000000000000000000000000000000000",
        "0x0000000000000000000000000000000000000000",
        signature.signature.hex(),
    ).build_transaction({"from": signer_pk, "nonce": caller_nonce})
    signed_tx = web3_client.eth.account.sign_transaction(execute_function, private_key=signer_sk)
    send_tx = web3_client.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = str(send_tx.hex())
    print(f"Transaction sent: #{tx_hash}")
    tx_receipt = web3_client.eth.wait_for_transaction_receipt(send_tx, timeout=15)
    print(f"Transaction executed, status: {str(tx_receipt['status'])}")


def get_enable_module_calldata():
    safe = web3_client.eth.contract(address="0x0000000000000000000000000000000000000000", abi=safe_abi["abi"])
    call_data = safe.encodeABI("enableModule", [aggregation_auth_module_address])
    return call_data


def get_add_bls_owner_calldata(wallet, bls_owner_index):
    module = web3_client.eth.contract(address="0x0000000000000000000000000000000000000000",
                                      abi=aggregation_auth_abi["abi"])
    blsSigner = blsSigners[bls_owner_index]
    call_data = module.encodeABI("addOwnerWithThreshold", [
        wallets[wallet]["address"],
        [blsSigner["x1"], blsSigner["x2"], blsSigner["y1"], blsSigner["y2"]],
        1 if bls_owner_index == 0 else 2
    ])
    return call_data


def get_self_transfer_txhash(wallet):
    module = web3_client.eth.contract(address=aggregation_auth_module_address, abi=aggregation_auth_abi["abi"])
    nonce = module.functions.getNonce(wallets[wallet]["address"]).call()
    transaction_hash = module.functions.getTransactionHash(
        wallets[wallet]["address"],
        1,
        b'',
        nonce
    ).call()
    return transaction_hash


def bls_sign(data_hash, bls_index):
    bls_domain = bytes.fromhex(
        w3.solidity_keccak(
            ["string"], ["safe.bls.domain"]
        ).hex()[2:]
    )
    bls_open = web3_client.eth.contract(address=bls_open_address, abi=bls_open_abi["abi"])
    public_key_hash = w3.keccak(
        hexstr=eth_abi.encode(
            ["uint256[4]"],
            [[blsSigners[bls_index]["x1"], blsSigners[bls_index]["x2"], blsSigners[bls_index]["y1"],
              blsSigners[bls_index]["y2"]]]
        ).hex()
    )
    message_hash = w3.keccak(
        hexstr=eth_abi.encode(
            ["bytes32", "bytes32", "address", "uint256"],
            [HexBytes(data_hash), public_key_hash, aggregator_address, 420]
        ).hex()
    )
    message_affine = tuple(
        bls_open.functions.hashToPoint(bls_domain, encode_packed(["bytes32"], [message_hash])).call())
    message_xyz = affine_to_xyz_G1(message_affine)
    sig = sign(message_xyz, blsSigners[bls_index]["secret"])
    return sig
