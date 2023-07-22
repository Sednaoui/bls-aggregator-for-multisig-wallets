//SPDX-License-Identifier: GPL
pragma solidity >=0.8.12 <0.9.0;

import "./interfaces/IAggregator.sol";
import "@gnosis.pm/safe-contracts/contracts/Safe.sol";

/// @title Aggregation Authenticator
contract AggregationAuthenticator {
    string public constant NAME = "Aggregation Authentication Module";
    string public constant VERSION = "0.0.1";

    struct SafeBLSOwners {
        uint8 length;
        uint8 threshold;
        uint256[4][] owners;
    }

    mapping (Safe => SafeBLSOwners) internal safeOwners;
    mapping (Safe => uint256) internal nonces;
    
    IAggregator public immutable aggregator;

    /**
     * @notice Throws if the sender is not the module itself or the owner of the target wallet.
     */
    modifier authorized(Safe safe) {
        require(msg.sender == address(safe), "SM: unauthorized");
        _;
    }

    constructor(IAggregator _aggregator) {
        aggregator = _aggregator;
    }

    ////////////////


    /// @dev Returns the chain id used by this contract.
    function getChainId() public view returns (uint256) {
        uint256 id;
        // solhint-disable-next-line no-inline-assembly
        assembly {
            id := chainid()
        }
        return id;
    }

    function getTransactionHash(
        address to,
        uint256 value,
        bytes calldata data,
        uint256 _nonce
    ) public view returns (bytes32) {
        bytes32 txHash = keccak256(
            abi.encode(
                to,
                value,
                keccak256(data),
                _nonce
            )
        );
        return keccak256(abi.encodePacked(getChainId(), address(this), txHash));
    }

    function execTransaction(
        Safe safe,
        address to,
        uint256 value,
        bytes calldata data,
        uint8 bitmask,
        bytes calldata aggregatedSignature
    ) public payable returns (bool) {
        uint256 nonce = nonces[safe];
        bytes32 txHash = getTransactionHash(to, value, data, nonce);
        nonces[safe]++;
        validateTxSignature(safe, txHash, bitmask, aggregatedSignature);
        bool success = safe.execTransactionFromModule({
            to: to,
            value: value,
            data: data,
            operation: Enum.Operation.Call
        });
        return success;
    }

    function validateTxSignature(
        Safe safe, 
        bytes32 dataHash,
        uint8 bitmask,
        bytes calldata aggregatedSignature
    ) public view {
        uint256[4][] memory publicKeys = getSignersFromBitmask(safe, bitmask);
        require(publicKeys.length >= safeOwners[safe].threshold, "AM: not enough signers");
        aggregator.validateSignatures(dataHash, publicKeys, aggregatedSignature);
    }

    function isBitSet(uint8 number, uint8 index) public pure returns (bool) {
        require(index < 8, "AM: Invalid index. Must be between 0 and 7.");
        uint8 bitmask = uint8(1) << index;
        return (number & bitmask) != 0;
    }

    function getSignersFromBitmask(Safe safe, uint8 bitmask) public view returns (uint256[4][] memory signers){
        SafeBLSOwners memory blsOwners = safeOwners[safe];

        uint8 pubKeysLen = blsOwners.length;
        uint256[4][] memory _signers = new uint256[4][](pubKeysLen);
        uint8 bitsSet = 0;
        for (uint8 i = 0; i < pubKeysLen; i++) {
            if (isBitSet(bitmask, i)){
                _signers[i] = blsOwners.owners[i];
                bitsSet++;
            }
        }

        uint256[4][] memory _onlySigners = new uint256[4][](bitsSet);
        for(uint8 i = 0; i < bitsSet; i++){
            _onlySigners[i] = _signers[i];
        }

        return _onlySigners;
    }

    function addOwnerWithThreshold(Safe safe, uint256[4] calldata owner, uint8 threshold) external authorized(safe) {
        SafeBLSOwners storage blsOwners = safeOwners[safe];
        require(blsOwners.length < 8, "AM: cannot have more than 8 owners"); // this is because we're using uint8 as a bitmask, can be modified to enable more owners
        require(!isOwner(safe, owner), "AM: owner already exists");
        blsOwners.owners.push(owner);
        blsOwners.length++;
        _changeThreshold(safe, threshold);
    }

    function removeOwnerWithThreshold(Safe safe, uint256[4] calldata owner, uint256 threshold) external authorized(safe) {
        // TODO THIS CONTRACT IS JUST FOR PROOF OF CONCEPT
    }

    function changeThreshold(Safe safe, uint8 threshold) external authorized(safe) {
        _changeThreshold(safe, threshold);
    }

    function _changeThreshold(Safe safe, uint8 threshold) internal {
        SafeBLSOwners storage blsOwners = safeOwners[safe];
        require(blsOwners.length >= threshold, "AM: threshold cannot be larger than owners count");
        require(threshold > 0, "AM: threshold cannot be 0");
        blsOwners.threshold = threshold;
    }


    function isOwner(Safe safe, uint256[4] calldata owner) public view returns (bool _isOwner) {
        SafeBLSOwners memory blsOwners = safeOwners[safe];
        uint pubKeysLen = blsOwners.length;
        bytes32 ownerHash = keccak256(abi.encode(owner));
        for (uint256 i = 0; i < pubKeysLen; i++) {
            bytes32 currentOwnerHash = keccak256(abi.encode(blsOwners.owners[i]));
            if (currentOwnerHash == ownerHash) return true;
        }
        return false;
    }

    function getThreshold(Safe safe) public view returns (uint8 _threshold) {
        return safeOwners[safe].threshold;
    }

    function getOwners(Safe safe) public view returns (uint256[4][] memory _owners) {
        return safeOwners[safe].owners;
    }

    function getNonce(Safe safe) public view returns (uint256 _nonce) {
        return nonces[safe];
    }

}