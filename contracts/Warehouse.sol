// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Warehouse {
    address manager;

    // producer, productType, quantity
    mapping(address => mapping(string => uint)) public products;

    constructor(address _manager) {
        manager = _manager;
    }

    modifier restricted() {
        require(msg.sender == manager, "Can only be executed by the manager. ");
        _;
    }

    event ReturnValue(
        address indexed from,
        uint to
    );

    // Backend: record `producer`, `productType`, `currentQuantity`
    function inbound(address producer, string memory productType, uint quantity) public restricted returns (uint currentQuantity) {
        products[producer][productType] += quantity;
        // emit ReturnValue(msg.sender, products[producer][productType]);
        return products[producer][productType];
    }

    // Backend: check `producer`, `productType`, `quantity` before calling this function
    function outbound(address producer, string memory productType, uint quantity) public restricted returns (uint currentQuantity) {
        products[producer][productType] -= quantity;
        // emit ReturnValue(msg.sender, products[producer][productType]);
        return products[producer][productType];
    }
}
