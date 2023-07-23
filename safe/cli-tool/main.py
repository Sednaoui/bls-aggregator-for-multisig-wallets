import random

import eth_abi
from py_ecc.optimized_bn128 import curve_order

from constants import blsSigners
from execution_handler import execution_handler, bls_sign
from prompts import wallet_prompt, transaction_prompt, signers_prompt
from utils.bls_utils import aggregate_signatures, xyz_to_affine_G1, get_public_key, xyz_to_affine_G2
from utils.utils import clear_terminal
from utils.wallet_utils import create_binary_bitmap


def program_loop():
    one_time_loop = False
    while True:
        clear_terminal()
        wallet = wallet_prompt()
        if wallet == "exit":
            exit()
        transaction = transaction_prompt(wallet)
        execution_handler(wallet, transaction)
        if one_time_loop:
            break


def main():
    program_loop()
    # secret_key1 = random.randrange(curve_order)
    # public_key1 = get_public_key(secret_key1)
    # pubkey11_affine = xyz_to_affine_G2(public_key1)
    # print(secret_key1)
    # print("-------------")
    # print(pubkey11_affine[0])
    # print(pubkey11_affine[1])
    # print(pubkey11_affine[2])
    # print(pubkey11_affine[3])

if __name__ == '__main__':
    main()
