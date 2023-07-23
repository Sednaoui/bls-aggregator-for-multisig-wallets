//SPDX-License-Identifier: Unlicense
pragma solidity >=0.8.4 <0.9.0;
pragma abicoder v2;

import "../interfaces/IAggregator.sol";
import {BLSOpen} from  "./bls-lib/BLSOpen.sol";
import "./BLSHelper.sol";

/**
 * A BLS-based signature aggregator, to validate aggregated signature of multisig wallets
 */
contract SafeBLSSignatureAggregator is IAggregator {

    bytes32 public constant BLS_DOMAIN = keccak256("safe.bls.domain");

     //copied from BLS.sol
    uint256 public  constant N = 21888242871839275222246405745257275088696311157297823662689037894645226208583;

    /// @inheritdoc IAggregator
    function validateSignatures(bytes32 dataHash, uint256[4][] calldata publicKeys, bytes calldata signature)
    external view override {
        require(signature.length == 64, "BLS: invalid signature");
        (uint256[2] memory blsSignature) = abi.decode(signature, (uint256[2]));

        uint pubKeysLen = publicKeys.length;
        uint256[2][] memory messages = new uint256[2][](pubKeysLen);
        for (uint256 i = 0; i < pubKeysLen; i++) {
            messages[i] = dataHashToMessage(dataHash, getPublicKeyHash(publicKeys[i]));
        }
        require(BLSOpen.verifyMultiple(blsSignature, publicKeys, messages), "BLS: validateSignatures failed");
    }

    function dataHashToMessage(bytes32 dataHash, bytes32 publicKeyHash) public view returns (uint256[2] memory) {
        bytes32 messageHash = getDataHash(dataHash, publicKeyHash);
        return BLSOpen.hashToPoint(BLS_DOMAIN, abi.encodePacked(messageHash));
    }

    function getDataHash(bytes32 message, bytes32 publicKeyHash) public view returns (bytes32) {
        return keccak256(abi.encode(message, publicKeyHash, address(this), block.chainid));
    }

    function getPublicKeyHash(uint256[4] memory publicKey) public pure returns(bytes32) {
        return keccak256(abi.encode(publicKey));
    }

    function aggregateSignatures(bytes[] calldata signatures) external pure returns (bytes memory aggregatedSignature) {
        BLSHelper.XY[] memory points = new BLSHelper.XY[](signatures.length);
        for (uint i = 0; i < points.length; i++) {
            (uint256 x, uint256 y) = abi.decode(signatures[i], (uint256, uint256));
            points[i] = BLSHelper.XY(x, y);
        }
        BLSHelper.XY memory sum = BLSHelper.sum(points, N);
        return abi.encode(sum.x, sum.y);
    }
}