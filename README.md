# BLS aggregator for multi-signature wallets

## Summary
A set of smart contracts to bring lower gas costs for **multi-sig wallets** to EVM rollups via aggregated BLS signatures.

## Description

If you have used a multisig wallet, you might have probably noticed the higher gas fees that you paid in comparison to a regular EOA. We have created a set of smart contracts that implements a BLS-based signature aggregator, to validate aggregated signatures of multisig wallets.

### ERC-4337 Manager
![normal- erc-4337-flow](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/59046107-531c-4a1a-a87d-6f4d48cca354)
![signature-aggregation-for-single-owner-accounts](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/83bcec0c-19a1-4817-bcb6-30354359bb47)
![signature-aggregation-for-multi-owner-accounts](https://github.com/Sednaoui/bls-aggregator-for-multisig-wallets/assets/7014833/04dc4963-72d6-4996-a4fa-f2912783a724)


### Aggregation Auth Module for Safe
