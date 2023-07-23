# BLS aggregator for multi-signature wallets

## Summary
A set of smart contracts to bring lower gas costs for **multi-sig wallets** on EVM rollups via aggregated BLS signatures.

## Description

If you have used a multisig wallet, you might have probably noticed the higher gas fees that you paid in comparison to a regular EOA. There exists signature aggregation contracts for single owner account, but none for multisig accounts.We have created a set of smart contracts that implements a BLS-based signature aggregator, to validate aggregated signatures of multisig wallets.

We designed two contract implementation: 

1. An Aggregation Auth Module for Safe (completed)
2. ERC-4337 BLS multi-sig aggregator (work in progress)

### Aggregation Auth Module for Safe
![safe-module-signature-aggregation-for-multi-owner-accounts](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/89019d58-1b46-49cc-aeb4-ec03b3198163)


Wallet:
1. Aggregate all owner signatures
2. Generate bitmask
3. Call Aggregation Auth Module

Module: 

- Instead of taking a signature field, it takes an aggregated signature. The module then calls the validateTxSignature on the aggregator contract with the following arguments: list of public address, aggregated signature, message hash

## ERC-4337 BLS multi-sig aggregator

### Background

ERC-4337 Account Abstraction introduces a singleton contract called the entrypoint to execute bundles of UserOperations. Bundlers/Clients whitelist the supported entrypoint.

#### Single Owner account flow without signature aggregation
![normal- erc-4337-flow](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/df3623c6-8b1d-40e9-86ab-cf80187a01d2)

#### Single Owner account flow with signature aggregation
![signature-aggregation-for-single-owner-accounts](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/61973dcc-e175-4573-ad7c-79eb1d855f94)

**Account**: 
1. The account setup its aggregator
2. The owner of the account is BLS
3. The rest of the account implentation is exactly the same, and the flow remains for sending userOps

**Bundler**:
1. Received multiple user operations from different accounts
2. Take the signature filed of each user operation
3. Aggregate all signatures
4. Output: aggregated signature offchain
5. handleAggregatedOps

## Signature Aggregation for multi-owner accounts
![signature-aggregation-for-multi-owner-accounts](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/427f9559-229a-4e08-be81-a957ddcb663a)


Multisig Account: 
1. The account setup its aggregator
2. The owners of the account are BLS owners
3. The rest of the account implentation is exactly the same
4. The wallet aggregate the signatures of different owners into a single aggregated signature

Bundler:

1. Received multiple aggregated signatures from different multisig accounts
2. Take the aggregated signature of each user operaton
3. Aggregate the aggregated signature offchain
4. Output: Aggregated signature 
5.handleAggregatedOps


##### Aggregated signature Transaction onchain
https://goerli-optimism.etherscan.io/tx/0x1b347061606c1aa6d2d2f55cbd5c88914c109e4c8405c4d3579a7855af51fbd6

#### Contract Deployments

##### Optimisic Goerli
https://goerli-optimism.etherscan.io/address/0xAa0599ccEF72f0624FaF004F398ceD5813128056
https://goerli-optimism.etherscan.io/address/0xe92dE7160b9Ab1c0239FA9c6A880624ABfCF0279
https://goerli-optimism.etherscan.io/address/0x55758A3316D9fbe59153013FB8109Bc32cFb1E63
