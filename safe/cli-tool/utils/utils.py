import os

from constants import blsSigners


def to_kebab_case(input_string):
    kebab_string = input_string.replace(" ", "-").replace("_", "-")
    kebab_string = kebab_string.lower()
    return kebab_string


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_bls_pubkey(index):
    pub = blsSigners[index]
    print(f"[{pub['x1']},{pub['x2']},{pub['y1']},{pub['y2']}]")


def print_bls_pubkeys():
    pub0 = blsSigners[0]
    pub1 = blsSigners[1]
    pub2 = blsSigners[2]
    print(f"[[{pub0['x1']},{pub0['x2']},{pub0['y1']},{pub0['y2']}],[{pub1['x1']},{pub1['x2']},{pub1['y1']},{pub1['y2']}],[{pub2['x1']},{pub2['x2']},{pub2['y1']},{pub2['y2']}]]")