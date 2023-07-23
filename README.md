# BLS aggregator for multi-signature wallets

## Summary
A set of smart contracts to bring lower gas costs for **multi-sig wallets** on EVM rollups via aggregated BLS signatures.

## Description

If you have used a multisig wallet, you might have probably noticed the higher gas fees that you paid in comparison to a regular EOA. There exists signature aggregation contracts for single owner account, but none for multisig accounts.We have created a set of smart contracts that implements a BLS-based signature aggregator, to validate aggregated signatures of multisig wallets.

We designed two contract implementation: 

1. ERC-4337 BLS multi-sig aggregator
2. An Aggregation Auth Module for Safe

## ERC-4337 BLS multi-sig aggregator

### Background

ERC-4337 Account Abstraction introduces a singleton contract called the entrypoint to execute bundles of UserOperations. Bundlers/Clients whitelist the supported entrypoint.

#### Single Owner account flow without signature aggregation
![normal- erc-4337-flow](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/59046107-531c-4a1a-a87d-6f4d48cca354)

#### Single Owner account flow with BLS signature aggregation
![signature-aggregation-for-single-owner-accounts](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/83bcec0c-19a1-4817-bcb6-30354359bb47)

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

![signature-aggregation-for-multi-owner-accounts](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/04dc4963-72d6-4996-a4fa-f2912783a724)

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


### Aggregation Auth Module for Safe
![safe-module-signature-aggregation-for-multi-owner-accounts](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/62be627d-7d58-41db-9bb0-3959901b0a08)

#### Contract Deployments

##### Polyon
https://polygonscan.com/address/0xAa0599ccEF72f0624FaF004F398ceD5813128056
https://polygonscan.com/address/0xe92dE7160b9Ab1c0239FA9c6A880624ABfCF0279
https://polygonscan.com/address/0x55758A3316D9fbe59153013FB8109Bc32cFb1E63

##### Celo
https://celoscan.io/address/0xAa0599ccEF72f0624FaF004F398ceD5813128056
https://celoscan.io/address/0xe92dE7160b9Ab1c0239FA9c6A880624ABfCF0279
https://celoscan.io/address/0x55758A3316D9fbe59153013FB8109Bc32cFb1E63

##### Mantel
https://explorer.testnet.mantle.xyz/address/0x464589093B7D17b197FCB5aa88fd4727C697Eb90
https://explorer.testnet.mantle.xyz/address/0x96320a2dc2Dd1D00F7f4A9D6cFEA65750944605A
https://explorer.testnet.mantle.xyz/address/0xba7A7Ec4c89C4a205AdCC35c48292dd1316Cfe2d

##### Gnosis
https://gnosisscan.io/address/0x63d2b9d8dd9a1643ae7ce2adfcd86e2bd0be250e
https://gnosisscan.io/address/0x75dF851E42b146659419a4A1fE2D4418B713C0b4
https://gnosisscan.io/address/0x5f0898D011AfEfeD2C10fDFCe5Cea07B97F85C9c

##### Linea
https://goerli.lineascan.build/address/0x63d2b9d8dd9a1643ae7ce2adfcd86e2bd0be250e
https://goerli.lineascan.build/address/0x75dF851E42b146659419a4A1fE2D4418B713C0b4
https://goerli.lineascan.build/address/0x5f0898D011AfEfeD2C10fDFCe5Cea07B97F85C9c

##### Optimisic Goerli
https://goerli-optimism.etherscan.io/address/0xAa0599ccEF72f0624FaF004F398ceD5813128056
https://goerli-optimism.etherscan.io/address/0xe92dE7160b9Ab1c0239FA9c6A880624ABfCF0279
https://goerli-optimism.etherscan.io/address/0x55758A3316D9fbe59153013FB8109Bc32cFb1E63

