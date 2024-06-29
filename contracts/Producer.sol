// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Producer {
    address manager;
    mapping(string => uint[]) public batches;
    mapping(string => uint) public products;

    constructor(address _manager) {
        manager = _manager;
    }

    modifier restricted() {
        require(msg.sender == manager, "Can only be executed by the manager. ");
        _;
    }

    event ReturnValue(
        address indexed from,
        uint value
    );

    event ReturnHash(
        address indexed from,
        uint value
    );

    // Backend: record `productType`, `quantity`, `batchNo`
    function inbound(string memory productType, uint batchHash, uint quantity) public restricted returns (uint batchNo) {
        products[productType] += quantity;
        batches[productType].push(batchHash);
        emit ReturnValue(msg.sender, products[productType]);
        return batches[productType].length - 1;
    }

    // Backend: check `productType`, `quantity` before calling this function
    function outbound(string memory productType, uint quantity) public restricted returns (uint currentQuantity) {
        products[productType] -= quantity;
        emit ReturnValue(msg.sender, products[productType]);
        return products[productType];
    }

    // Backend: check `productType`, `batchNo` before calling this function
    function getBatchHash(string memory productType, uint batchNo) public restricted returns (uint) {
        emit ReturnHash(msg.sender, batches[productType][batchNo]);
        return batches[productType][batchNo];
    }
}
