// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Producer.sol";
import "./Warehouse.sol";
import "./Delivery.sol";

contract Deployer {
    address manager;

    constructor() {
        manager = msg.sender;
    }

    modifier restricted() {
        require(msg.sender == manager, "Can only be executed by the manager. ");
        _;
    }

    function newProducer() public restricted returns (address) {
        address producerAddress = address(new Producer(manager));
        return producerAddress;
    }

    function newWarehouse() public restricted returns (address) {
        address wholesalerAddress = address(new Warehouse(manager));
        return wholesalerAddress;
    }
    
    event ReturnValue(
        address indexed from,
        address indexed toReturn,
        uint value
    );

    function newDelivery(address from, address to) public restricted returns (address) {
        address deliveryAddress = address(new Delivery(manager, from, to));
        emit ReturnValue(msg.sender, deliveryAddress, msg.value);
        return deliveryAddress;
    }
}
