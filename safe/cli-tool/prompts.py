from PyInquirer import prompt

from constants import blsSigners
from utils.utils import to_kebab_case, clear_terminal
from utils.wallet_utils import is_module_enabled, are_bls_owners_added, get_bls_threshold


def transaction_prompt(wallet):
    choices = ['Self-transfer']
    if is_module_enabled(wallet):
        if not are_bls_owners_added(wallet):
            choices.insert(0, 'Add BLS Owners')
    else:
        choices.insert(0, 'Enable BLS Authentication Module')
    questions = [
        {
            'type': 'list',
            'name': 'transaction',
            'message': 'What type of transaction do you want to execute',
            'choices': choices
        }
    ]
    answers = prompt(questions)
    return to_kebab_case(answers["transaction"])


def wallet_prompt():
    questions = [
        {
            'type': 'list',
            'name': 'wallet',
            'message': 'Choose the wallet',
            'choices': ['Wallet 1', 'Wallet 2', 'Wallet 3', 'Wallet 4', "Exit"]
        }
    ]
    answers = prompt(questions)
    return to_kebab_case(answers["wallet"])


def signers_prompt(wallet):
    threshold = get_bls_threshold(wallet)
    choices = []
    for index in range(len(blsSigners)):
        choices.append({'name': f'Signer {index+1}'})
    questions = [
        {
            'type': 'checkbox',
            'name': 'signers',
            'message': 'Choose the signers who will sign the tx',
            'choices': choices
        },
    ]
    answers = prompt(questions)
    if len(answers["signers"]) < threshold:
        clear_terminal()
        print(f"Select signers more than your threshold of {threshold}")
        return signers_prompt(wallet)
    signers = []
    for signer in answers["signers"]:
        signers.append(int(signer.replace("Signer ", ""))-1)
    return signers
