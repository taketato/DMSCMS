// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Delivery {
    enum DeliveryState {
        preparing,
        shipped,
        received
    }

    address manager;
    address public from;
    address public to;
    DeliveryState public state = DeliveryState.preparing;
    uint public shipTime;
    uint public receiveTime;

    // producer, productType, quantity
    mapping(address => mapping(string => uint)) public products;

    constructor(address _manager, address _from, address _to) {
        manager = _manager;
        from = _from;
        to = _to;
    }

    modifier restricted() {
        require(msg.sender == manager, "Can only be executed by the manager. ");
        _;
    }

    function addProduct(address producer, string memory productType, uint quantity) public restricted {
        require(state == DeliveryState.preparing, "Can only be executed during preparation. ");
        products[producer][productType] += quantity;
    }

    function productLost(address producer, string memory productType, uint quantity) public restricted {
        require(state != DeliveryState.received, "Cannot be executed after received. ");
        products[producer][productType] -= quantity;
    }

    function shipping(uint time) public restricted {
        require(state == DeliveryState.preparing, "Can only be executed during preparation. ");
        shipTime = time;
        state = DeliveryState.shipped;
    }

    function receiving(uint time) public restricted {
        require(state == DeliveryState.shipped, "Can only be executed during shipping. ");
        receiveTime = time;
        state = DeliveryState.received;
    }
}
