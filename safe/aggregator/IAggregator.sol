// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.12;

/**
 * Aggregated Signatures validator.
 */
interface IAggregator {

    /**
     * validate aggregated signature.
     * revert if the aggregated signature does not match the given list of operations.
     */
    function validateSignatures(bytes32 dataHash, uint256[4][] calldata publicKeys, bytes calldata signature) external view;

    function aggregateSignatures(bytes[] calldata signatures) external view returns (bytes memory aggregatedSignature);
}